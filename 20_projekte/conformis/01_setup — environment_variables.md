---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# 🔑 Environment Variables

up:: [[../00-Index/🛡️ Conformis – RechteRadar]]
tags: #setup #config #secrets

> ⚠️ **Achtung:** Echte Keys nur in `.env` auf dem VPS – niemals in Git committen!

---

## OpenClaw / Gateway

| Variable | Beschreibung |
|----------|-------------|
| `OPENCLAW_GATEWAY_TOKEN` | Auth-Token für Gateway-Zugriff |
| `OPENCLAW_GATEWAY_CONTROLUI_ALLOWEDORIGINS` | Erlaubte Origins für Control UI |
| `OPENCLAW_AGENT_MODEL` | Standard-Modell (`openrouter/minimax/minimax-m2.5:free`) |
| `OPENCLAW_AGENT_TIMEOUT` | Timeout in Sekunden (`300`) |
| `OPENCLAW_RUNTIME` | `acp` |
| `OPENCLAW_SANDBOX_MODE` | `off` |
| `OPENCLAW_ACP_BACKEND` | `acpx` |
| `OPENCLAW_GLOBAL_TOOL_POLICY` | `execute` |

---

## Browser (Chromium)

| Variable | Wert |
|----------|------|
| `OPENCLAW_BROWSER_TYPE` | `local` |
| `OPENCLAW_BROWSER_BINARY` | `/usr/bin/chromium` |
| `CHROME_PATH` | `/usr/bin/chromium` |
| `BROWSER_EXECUTABLE_PATH` | `/usr/bin/chromium` |
| `OPENCLAW_BROWSER_ARGS` | `--no-sandbox,--disable-setuid-sandbox,--disable-dev-shm-usage` |

---

## API Keys

| Variable | Dienst | Verwendung |
|----------|--------|-----------|
| `OPENROUTER_API_KEY` | OpenRouter | Modell-Zugriff |
| `GOOGLE_API_KEY` | Google | Places / Suche |
| `GOOGLE_PLACES_API_KEY` | Google Places | Lead-Finder |
| `HANDELSREGISTER_API_KEY` | Handelsregister.de | DE Leads |
| `COMPANIES_HOUSE_API_KEY` | Companies House UK | UK Leads |
| `ZEFIX_BASE_URL` | Zefix CH | CH Leads (kein Key, öffentlich) |

---

## Brevo (E-Mail)

| Variable | Beschreibung |
|----------|-------------|
| `BREVO_API_KEY` | API-Key für REST-Versand |
| `BREVO_SMTP_HOST` | `smtp-relay.brevo.com` |
| `BREVO_SMTP_PORT` | `587` |
| `BREVO_SMTP_LOGIN` | SMTP-Login |
| `BREVO_SMTP_PASSWORD` | SMTP-Passwort |

---

## Datenbank (PostgreSQL)

| Variable | Wert |
|----------|------|
| `DATABASE_URL` | `postgresql://openclaw:openclaw_secure_2024@postgres:5432/openclaw` |
| `DB_HOST` | `postgres` |
| `DB_PORT` | `5432` |
| `DB_NAME` | `openclaw` |
| `DB_USER` | `openclaw` |
| `DB_PASSWORD` | `openclaw_secure_2024` |

---

## .env Template

```env
# OpenClaw
OPENCLAW_GATEWAY_TOKEN=
OPENCLAW_AGENT_MODEL=openrouter/minimax/minimax-m2.5:free
OPENCLAW_AGENT_TIMEOUT=300
OPENCLAW_RUNTIME="acp"
OPENCLAW_SANDBOX_MODE="off"
OPENCLAW_ACP_BACKEND="acpx"
OPENCLAW_GLOBAL_TOOL_POLICY="execute"

# APIs
OPENROUTER_API_KEY=
GOOGLE_API_KEY=
GOOGLE_PLACES_API_KEY=
HANDELSREGISTER_API_KEY=
COMPANIES_HOUSE_API_KEY=
ZEFIX_BASE_URL=https://www.zefix.admin.ch/ZefixPublicREST/api/v1

# Brevo
BREVO_API_KEY=
BREVO_SMTP_HOST=smtp-relay.brevo.com
BREVO_SMTP_PORT=587
BREVO_SMTP_LOGIN=
BREVO_SMTP_PASSWORD=

# Browser
OPENCLAW_BROWSER_TYPE=local
OPENCLAW_BROWSER_BINARY=/usr/bin/chromium
OPENCLAW_BROWSER_ARGS=--no-sandbox,--disable-setuid-sandbox,--disable-dev-shm-usage

# DB
DATABASE_URL=postgresql://openclaw:openclaw_secure_2024@postgres:5432/openclaw
DB_HOST=postgres
DB_PORT=5432
DB_NAME=openclaw
DB_USER=openclaw
DB_PASSWORD=openclaw_secure_2024
```
