FROM python:3.12-slim

WORKDIR /app

# Install uv from official image (guaranteed latest, correct platform)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency spec first for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies only (skip installing the project itself)
RUN uv sync --no-dev --frozen --no-install-project

# Copy application code
COPY config.py document_parser.py server.py Procfile ./
COPY backends/ backends/

EXPOSE 8000

CMD [".venv/bin/python", "server.py"]
