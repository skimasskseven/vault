---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# 🐳 Docker Setup

up:: [[../00-Index/🛡️ Conformis – RechteRadar]]
tags: #setup #docker #infrastructure

---

## Container

| Container | Image | Port |
|-----------|-------|------|
| `compliance-guard` | `ghcr.io/openclaw/openclaw:2026.3.31` | `18789` |
| `compliance-guard-db` | `postgres:16-alpine` | `5432` |

---

## Dockerfile – Highlights

```dockerfile
FROM ghcr.io/openclaw/openclaw:2026.3.31
USER root

# Dependencies
RUN apt-get install -y git chromium chromium-sandbox \
    libnss3 libatk-bridge2.0-0 libxcomposite1 \
    libxrandr2 libgbm1 libasound2 curl postgresql-client

# Chromium-Fix (Sandbox im Container)
RUN chmod 4755 /usr/bin/chromium || true

RUN chown -R node:node /home/node/.openclaw
```

---

## docker-compose.yml

```yaml
services:
  openclaw-conformis:
    build: .
    container_name: compliance-guard
    shm_size: '2gb'
    user: "0:0"
    restart: unless-stopped
    ports:
      - "18789:18789"

    environment:
      - HOME=/root
      - OPENCLAW_CONFIG_PATH=/root/.openclaw/openclaw.json
      - OPENCLAW_BROWSER_BINARY=/usr/bin/chromium
      - OPENCLAW_BROWSER_ARGS=--no-sandbox,--disable-setuid-sandbox,--disable-dev-shm-usage
      - PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
      - OPENCLAW_GATEWAY_MODE=local
      - OPENCLAW_GATEWAY_NON_INTERACTIVE=true

    volumes:
      - ./config:/root/.openclaw
      - ./workspaces:/root/.openclaw/workspaces
      - ./data:/root/.openclaw/data
      - ./db:/root/.openclaw/db
      - ./canvas:/root/.openclaw/canvas

  postgres:
    image: postgres:16-alpine
    container_name: compliance-guard-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=openclaw
      - POSTGRES_PASSWORD=openclaw_secure_2024
      - POSTGRES_DB=openclaw
    volumes:
      - ./db/data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U openclaw"]
      interval: 10s
      timeout: 5s
      retries: 5
```

---

## Volume-Mapping

| Host-Pfad | Container-Pfad | Inhalt |
|-----------|---------------|--------|
| `./config` | `/root/.openclaw` | `openclaw.json` |
| `./workspaces` | `/root/.openclaw/workspaces` | Agent-Workspaces |
| `./data` | `/root/.openclaw/data` | Laufzeitdaten |
| `./db` | `/root/.openclaw/db` | SQLite / Init |
| `./canvas` | `/root/.openclaw/canvas` | Canvas-Daten |

---

## Befehle

```bash
# Starten
docker-compose up -d

# Logs
docker logs compliance-guard -f

# In Container
docker exec -it compliance-guard bash

# Stoppen
docker-compose down
```

---

## DB-Verbindung

```
postgresql://openclaw:openclaw_secure_2024@postgres:5432/openclaw
```

- **Intern** (Docker-Netz): `postgres:5432`
- **Extern**: `localhost:5432`
