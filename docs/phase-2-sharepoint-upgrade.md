# Phase 2: SharePoint Integration Upgrade

## Executive Summary

Phase 1 (current) uses a curated sample content library (~30 markdown files) to demonstrate the Marketing Brain's capabilities. Phase 2 upgrades the backend to read content directly from a SharePoint document library, enabling the team to maintain and expand content through familiar SharePoint workflows.

**What changes:** One environment variable (`BACKEND=sharepoint`) and Azure AD app registration.
**What stays the same:** All 5 MCP tools, the Claude.ai connector, and user experience are identical.

## What Changes in Phase 2

| Component | Phase 1 (Current) | Phase 2 (SharePoint) |
|-----------|-------------------|---------------------|
| Content source | `sample_content/` directory on Railway | SharePoint document library |
| Content format | Markdown files | Word docs, PDFs, markdown, PowerPoint |
| Content updates | Git commit + deploy | Upload to SharePoint (instant) |
| Authentication | Azure AD (OAuth for users) | Same + SharePoint delegated access |
| Deployment | Railway auto-deploy | Same Railway instance |
| Server code | `server.py` (unchanged) | `server.py` (unchanged) |

### Railway Configuration Change

```
# Phase 1 (current)
BACKEND=mock

# Phase 2
BACKEND=sharepoint
SHAREPOINT_SITE_NAME=FourthMarketingBrain
```

That's it. The server automatically switches backends based on this variable.

## IT Request: Azure AD App Registration Update

### Copy-Paste Template for IT

---

**Subject:** Azure AD App Registration Update - Fourth Marketing Brain (SharePoint Access)

**To:** IT / Azure AD Admin

**Priority:** Medium

**Request:**

We need to update an existing Azure AD app registration to add SharePoint read access for our Marketing Brain AI tool. The app registration already exists for OAuth authentication.

**Existing App Registration:**
- Name: Fourth Marketing Brain (or the name used during Phase 1 setup)
- Application (client) ID: [find in Railway env vars: AZURE_CLIENT_ID]

**Changes Needed:**

1. **Add Delegated API Permissions:**
   - `Microsoft Graph > Sites.Read.All` (Delegated) - Read SharePoint sites
   - `Microsoft Graph > Files.Read.All` (Delegated) - Read files in SharePoint

2. **Grant Admin Consent** for `Sites.Read.All` (requires admin consent)

3. **Verify existing permissions are still present:**
   - `openid` (Delegated)
   - `profile` (Delegated)

4. **No changes needed to:**
   - Redirect URIs (already configured)
   - Application ID URI (already configured as `api://{client_id}`)
   - Token configuration (already set to `accessTokenAcceptedVersion: 2`)

**Why:** This enables the Marketing Brain to read marketing content documents from a SharePoint site on behalf of authenticated users. Users will only see content they have SharePoint access to (delegated permissions respect SharePoint access controls).

**Security Notes:**
- These are **delegated** permissions (act on behalf of user), not application permissions
- Read-only access - the app cannot modify or delete SharePoint content
- Users can only access SharePoint sites they already have permission to access
- No new redirect URIs or secrets needed

---

### Detailed Technical Requirements

#### API Permissions (Delegated)

| Permission | Type | Admin Consent | Purpose |
|-----------|------|---------------|---------|
| `openid` | Delegated | No | Already configured - user authentication |
| `profile` | Delegated | No | Already configured - user profile |
| `Sites.Read.All` | Delegated | **Yes** | Read SharePoint site content |
| `Files.Read.All` | Delegated | **Yes** | Read files in SharePoint document libraries |

#### App Manifest Verification

Ensure these settings are in the app manifest (should already be set from Phase 1):

```json
{
  "accessTokenAcceptedVersion": 2,
  "signInAudience": "AzureADMyOrg",
  "identifierUris": ["api://{client_id}"]
}
```

#### Redirect URI (Already Configured)

Should already have:
```
https://your-railway-url.up.railway.app/oauth/callback
```

No changes needed.

## SharePoint Site Structure

### Recommended Document Library Structure

Create a SharePoint site called **FourthMarketingBrain** (or similar) with this folder structure:

```
FourthMarketingBrain/
  Documents/
    platform/
      restaurant-operations-suite.docx
      fourth-iq-ai-platform.docx
      hotschedules-product.docx
      fourth-hr-payroll-hcm.docx
      macromatix-inventory.docx
      peoplematter-talent.docx
      fuego-earned-wage-access.docx
      analytics-and-reporting.docx
    integrations/
      integration-guide.docx
      pos-integrations.docx
      payroll-hr-integrations.docx
      developer-api-platform.docx
    solutions/
      qsr-fast-casual.docx
      casual-dining-full-service.docx
      hotels-leisure.docx
      multi-location-operations.docx
    competitive/
      market-positioning.docx
      vs-restaurant365.docx
      vs-generic-hcm.docx
      vs-point-solutions.docx
      objection-handling.docx
    messaging/
      value-propositions-by-role.docx
      enterprise-platform-playbook.docx
      packaging-comparison.docx
      customer-proof-points.docx
      elevator-pitches.docx
    compliance/
      security-compliance.docx
      labor-law-compliance.docx
      tip-management-compliance.docx
    rfp-responses/
      workforce-scheduling.docx
      inventory-procurement.docx
      hr-payroll-benefits.docx
      ai-analytics-reporting.docx
      implementation-onboarding.docx
```

**Supported formats:** .docx, .pdf, .pptx, .md, .txt

### Content Migration

To migrate from Phase 1 sample content to SharePoint:
1. Convert markdown files to Word format (or upload as-is - both work)
2. Upload to the SharePoint document library matching the folder structure above
3. Verify file permissions - all Marketing Brain users need at least Read access to the site

## Testing Checklist

After IT completes the app registration update and SharePoint site is created:

- [ ] **1. Verify app permissions**: Go to Azure Portal > App registrations > Fourth Marketing Brain > API permissions. Confirm `Sites.Read.All` and `Files.Read.All` are listed with "Granted" status.

- [ ] **2. Update Railway environment**:
  ```
  BACKEND=sharepoint
  SHAREPOINT_SITE_NAME=FourthMarketingBrain
  ```

- [ ] **3. Test authentication**: Open Claude.ai, connect to Fourth Marketing Brain. Verify OAuth flow completes without errors.

- [ ] **4. Test list_content_areas()**: Should return all 7 content areas with correct document counts.

- [ ] **5. Test browse_library("/")**: Should show all top-level folders matching the SharePoint structure.

- [ ] **6. Test search_knowledge("Fourth iQ AI")**: Should find the AI platform document.

- [ ] **7. Test get_document("enterprise-platform-playbook")**: Should return the full document content.

- [ ] **8. Test ask_question("How does Fourth compare to Restaurant365?")**: Should return GROUNDED confidence with competitive content.

- [ ] **9. Test with Word doc**: Upload a .docx file to SharePoint, verify it's parsed and searchable.

- [ ] **10. Test with PDF**: Upload a .pdf file, verify content extraction works.

## Rollback Plan

If Phase 2 has issues, reverting to Phase 1 takes 30 seconds:

1. In Railway dashboard, change environment variable:
   ```
   BACKEND=mock
   ```
2. Railway auto-redeploys with the sample content library
3. All tools continue working with the original markdown files
4. No code changes needed - the server handles both backends

### Common Phase 2 Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| "Access denied" on SharePoint | Admin consent not granted | Have IT click "Grant admin consent" in Azure Portal |
| Empty search results | Wrong SharePoint site name | Verify `SHAREPOINT_SITE_NAME` matches exactly |
| Document parsing errors | Unsupported file format | Ensure files are .docx, .pdf, .pptx, .md, or .txt |
| Slow search results | Large document library | Consider organizing into fewer, well-structured folders |
| OAuth flow fails | Permissions not updated | Verify all 4 delegated permissions are present and consented |

## Timeline

| Step | Owner | Duration |
|------|-------|----------|
| Submit IT request | Marketing | 5 minutes |
| IT processes app registration update | IT | 1-3 business days |
| Create SharePoint site and upload content | Marketing | 2-4 hours |
| Update Railway environment variable | Developer | 5 minutes |
| Run testing checklist | Marketing + Developer | 30 minutes |
| **Total** | | **1-4 business days** |
