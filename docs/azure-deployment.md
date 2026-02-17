# Azure Deployment Guide

Deploy Fourth Marketing Brain as an Azure Container App in `rg-agent-architecture`.

## Prerequisites

- Azure CLI (`az`) authenticated with subscription access
- Existing infrastructure in `rg-agent-architecture`:
  - Container Apps environment (West Europe)
  - ACR: `agentarchacr`
  - Cosmos DB: `agent-architecture-cosmos`
  - AI Search: `agent-demo-search`
  - Key Vault: `agent-arch-kv-prod`

## Phase 1: Infrastructure Setup

### 1.1 Cosmos DB — Add `mcp-content` database

```bash
# New database in existing Cosmos account
az cosmosdb sql database create \
  --account-name agent-architecture-cosmos \
  --resource-group rg-agent-architecture \
  --name mcp-content

# Documents container (partitioned by content_area)
az cosmosdb sql container create \
  --account-name agent-architecture-cosmos \
  --resource-group rg-agent-architecture \
  --database-name mcp-content \
  --name documents \
  --partition-key-path "/content_area" \
  --throughput 400

# Content areas container (partitioned by slug)
az cosmosdb sql container create \
  --account-name agent-architecture-cosmos \
  --resource-group rg-agent-architecture \
  --database-name mcp-content \
  --name content-areas \
  --partition-key-path "/slug" \
  --throughput 400
```

### 1.2 AI Search — Index created by seed script

The `scripts/seed_content.py` script creates the index schema automatically.
No manual index creation needed.

### 1.3 Entra ID App Registration

```bash
# Create app registration
az ad app create \
  --display-name "MCP: Marketing Brain" \
  --sign-in-audience AzureADMyOrg

APP_ID=$(az ad app list --display-name "MCP: Marketing Brain" --query "[0].appId" -o tsv)

# User-consentable permissions only (openid, profile, User.Read)
az ad app permission add --id $APP_ID \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions \
    e1fe6dd8-ba31-4d61-89e7-88639da4683d=Scope \
    37f7f235-527c-4136-accd-4a02d197296e=Scope \
    14dad69e-099b-42c9-810b-d002981feec1=Scope

# Create client secret
az ad app credential reset --id $APP_ID --append

# Create service principal
az ad sp create --id $APP_ID

# Enable "User Assignment Required" for per-server access control
SP_ID=$(az ad sp list --display-name "MCP: Marketing Brain" --query "[0].id" -o tsv)
az ad sp update --id $SP_ID --set appRoleAssignmentRequired=true

# Assign users (repeat per user)
# az ad app assignment create --id $SP_ID --user-id <user-object-id> --role-id 00000000-0000-0000-0000-000000000000
```

## Phase 2: Seed Content

```bash
# Get Cosmos DB connection string
COSMOS_ENDPOINT=$(az cosmosdb show --name agent-architecture-cosmos -g rg-agent-architecture --query documentEndpoint -o tsv)
COSMOS_KEY=$(az cosmosdb keys list --name agent-architecture-cosmos -g rg-agent-architecture --query primaryMasterKey -o tsv)

# Get AI Search admin key
SEARCH_ENDPOINT="https://agent-demo-search.search.windows.net"
SEARCH_KEY=$(az search admin-key show --service-name agent-demo-search -g rg-agent-architecture --query primaryKey -o tsv)

# Dry run first
python scripts/seed_content.py --source sample_content/ --dry-run

# Seed both Cosmos DB and AI Search
COSMOS_ENDPOINT=$COSMOS_ENDPOINT COSMOS_KEY=$COSMOS_KEY \
SEARCH_ENDPOINT=$SEARCH_ENDPOINT SEARCH_KEY=$SEARCH_KEY \
python scripts/seed_content.py --source sample_content/ \
  --cosmos-db mcp-content --search-index mcp-marketing
```

## Phase 3: Build and Deploy Container App

### 3.1 Build and push Docker image

```bash
az acr build \
  --registry agentarchacr \
  --image mcp-marketing:latest \
  --file Dockerfile \
  .
```

### 3.2 Create Container App

```bash
ENV_NAME=$(az containerapp env list -g rg-agent-architecture --query "[0].name" -o tsv)

az containerapp create \
  --name mcp-marketing-prod \
  --resource-group rg-agent-architecture \
  --environment $ENV_NAME \
  --image agentarchacr.azurecr.io/mcp-marketing:latest \
  --target-port 8000 \
  --ingress external \
  --min-replicas 0 \
  --max-replicas 3 \
  --cpu 0.5 \
  --memory 1.0Gi \
  --registry-server agentarchacr.azurecr.io
```

### 3.3 Configure environment variables

```bash
az containerapp update \
  --name mcp-marketing-prod \
  --resource-group rg-agent-architecture \
  --set-env-vars \
    BACKEND=cosmos \
    AUTH_MODE=easyauth \
    MCP_TRANSPORT=http \
    MCP_PORT=8000 \
    COSMOS_ENDPOINT=secretref:cosmos-endpoint \
    COSMOS_KEY=secretref:cosmos-key \
    COSMOS_DATABASE=mcp-content \
    SEARCH_ENDPOINT=secretref:search-endpoint \
    SEARCH_KEY=secretref:search-key \
    SEARCH_INDEX=mcp-marketing
```

### 3.4 Enable Easy Auth

```bash
# Configure Microsoft auth provider
az containerapp auth microsoft update \
  --name mcp-marketing-prod \
  --resource-group rg-agent-architecture \
  --client-id $APP_ID \
  --client-secret <secret-from-step-1.3> \
  --issuer "https://login.microsoftonline.com/$TENANT_ID/v2.0" \
  --yes

# Enable auth (AllowAnonymous so MCP clients can connect without browser flow)
az containerapp auth update \
  --name mcp-marketing-prod \
  --resource-group rg-agent-architecture \
  --enabled true \
  --unauthenticated-client-action AllowAnonymous

# Restart to apply secret changes
az containerapp revision restart \
  --name mcp-marketing-prod \
  --resource-group rg-agent-architecture \
  --revision $(az containerapp show --name mcp-marketing-prod -g rg-agent-architecture --query "properties.latestRevisionName" -o tsv)
```

### 3.5 Store secrets in Key Vault

```bash
az keyvault secret set --vault-name agent-arch-kv-prod \
  --name mcp-marketing-cosmos-endpoint --value "$COSMOS_ENDPOINT"
az keyvault secret set --vault-name agent-arch-kv-prod \
  --name mcp-marketing-cosmos-key --value "$COSMOS_KEY"
az keyvault secret set --vault-name agent-arch-kv-prod \
  --name mcp-marketing-search-endpoint --value "$SEARCH_ENDPOINT"
az keyvault secret set --vault-name agent-arch-kv-prod \
  --name mcp-marketing-search-key --value "$SEARCH_KEY"
```

## Verification

### Test MCP tools

```bash
APP_URL=$(az containerapp show --name mcp-marketing-prod -g rg-agent-architecture --query properties.configuration.ingress.fqdn -o tsv)
echo "MCP endpoint: https://$APP_URL/mcp"

# Health check
curl https://$APP_URL/health
```

### Connect clients

**Live URL:** `https://mcp-marketing-prod.happyhill-92303561.swedencentral.azurecontainerapps.io`

- **Claude.ai**: Add connector URL `https://mcp-marketing-prod.happyhill-92303561.swedencentral.azurecontainerapps.io/mcp`
- **VS Code Copilot**: Add to `.vscode/mcp.json` with `streamable-http` transport
- **Claude Code**: Add to `.mcp.json`
- **ChatGPT**: Use streamable-http URL

## User Access Management

```bash
# Grant access
az ad app assignment create --id $SP_ID --user-id <user-oid> --role-id 00000000-0000-0000-0000-000000000000

# Revoke access
az ad app assignment delete --id $SP_ID --user-id <user-oid>

# List who has access
az ad app assignment list --id $SP_ID --query "[].{user:principalDisplayName}" -o table
```

## CI/CD (GitHub Actions)

```yaml
# .github/workflows/mcp-marketing-deploy.yml
name: Deploy MCP Marketing Brain
on:
  push:
    branches: [master]
    paths:
      - 'server.py'
      - 'config.py'
      - 'backends/**'
      - 'Dockerfile'
      - 'pyproject.toml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Build and push to ACR
        run: |
          az acr build \
            --registry agentarchacr \
            --image mcp-marketing:${{ github.sha }} \
            --image mcp-marketing:latest \
            --file Dockerfile .

      - name: Deploy to Container App
        run: |
          az containerapp update \
            --name mcp-marketing-prod \
            --resource-group rg-agent-architecture \
            --image agentarchacr.azurecr.io/mcp-marketing:${{ github.sha }}
```
