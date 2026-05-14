---
tags:
  - projekt/packcheck
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# PackCheck — Deployment

Ziel-Host: VPS (Hostinger), TLS via Let's Encrypt, Reverse-Proxy ist der
**globale `edge-caddy`** in `/root/dev/edge/` — nicht in diesem Repo.

## Domains

| Domain | Container | Pfad |
|---|---|---|
| `lucidexpress.de`, `www.lucidexpress.de` | `packcheck-web:3001` | `/` |
| `api.lucidexpress.de` | `packcheck-api:4000` | `/` |

DNS zeigt auf den VPS, Caddy macht ACME-TLS automatisch
(`{$LE_EMAIL}` global gesetzt).

## edge-net Pattern

`edge-net` ist ein **external** Docker-Network, das genau einmal vom
edge-caddy-Compose angelegt wird. Jede App, die öffentlich erreichbar
sein soll, joined es zusätzlich zu ihrem privaten Netz:

```yaml
# packcheck_backend/docker-compose.yml (Auszug)
api:
  networks:
    - packcheck-net      # privat: nur api ↔ db
    - edge-net           # extern: caddy ↔ api
db:
  networks:
    - packcheck-net      # NICHT in edge-net — DB nicht extern erreichbar

networks:
  packcheck-net:
    driver: bridge
  edge-net:
    external: true
    name: edge-net
```

Caddy adressiert die Container per Container-Name als DNS:
`reverse_proxy packcheck-web:3001` / `reverse_proxy packcheck-api:4000`.
Siehe `/root/dev/edge/Caddyfile`.

> **Geteilt mit conformis.** edge-caddy ist **derselbe** Container für
> conformis und packcheck. Das `Caddyfile` hat einen Site-Block pro
> Projekt — siehe Pattern-Dashboard für die Cross-Projekt-Abhängigkeit.

## Container-Healthchecks

| Container | Test |
|---|---|
| `db` | `pg_isready -U $POSTGRES_USER` (10s Intervall, 10 Retries) |
| `api` | `wget --spider http://127.0.0.1:4000/health` (30s Intervall, 15s start period) |
| `web` | `wget --spider http://127.0.0.1:3001/` (30s Intervall, 20s start period) |

`api` deklariert `depends_on: db: condition: service_healthy` —
Express startet erst, wenn Postgres `pg_isready` antwortet.

## Backend-Build (`packcheck_backend/Dockerfile`)

Multi-Stage:
1. `npm ci`
2. `tsc` baut nach `dist/`
3. Slim-Image kopiert `node_modules` (prod-only) + `dist/` + `migrations/`
4. `CMD ["node", "dist/server.js"]`

`migrations/` werden im **DB-Container** über
`./migrations:/docker-entrypoint-initdb.d:ro` gemounted, nicht im API-
Container. API führt selbst keine Migration aus.

## Frontend-Build (`packcheck_frontend/Dockerfile`)

Multi-Stage mit `next build` → `output: 'standalone'`:
1. Builder: `npm ci`, `next build`
2. Runner: kopiert `.next/standalone/`, `.next/static/`, `public/`
3. `CMD ["node", "server.js"]` (das ist der von Next generierte Standalone-Server)

Build-Args (`docker compose build` oder `--build-arg`):
- `NEXT_PUBLIC_APP_URL` (Default: `https://lucidexpress.de`)
- `API_URL` (Default: `https://api.lucidexpress.de`)

Diese sind zur **Build-Zeit** ins Bundle gebrannt — Änderung erfordert
Rebuild.

## Environment-Variablen

### Backend (`packcheck_backend/.env`)

```
DATABASE_URL=postgres://packcheck:<pw>@db:5432/packcheck
POSTGRES_DB=packcheck
POSTGRES_USER=packcheck
POSTGRES_PASSWORD=<strong>
JWT_SECRET=<≥32 chars, identisch zum Frontend>
JWT_EXPIRES_IN=7d
COOKIE_DOMAIN=.lucidexpress.de
COOKIE_SECURE=true
CORS_ORIGINS=https://lucidexpress.de,https://www.lucidexpress.de
SEED_ADMIN_EMAIL=<initial admin>
SEED_ADMIN_PASSWORD=<≥8 chars>
INVOICE_RATE_EUR_PER_KG=0.10
NODE_ENV=production
PORT=4000
LOG_LEVEL=info
```

Validation läuft per zod beim Start in `src/env.ts` — fehlt eine
Variable, **stirbt der Container sofort** (bewusst: kein silent
default für Secrets).

### Frontend (`packcheck_frontend/.env.local`)

```
NEXT_PUBLIC_API_URL=https://api.lucidexpress.de
NEXT_PUBLIC_APP_URL=https://lucidexpress.de
JWT_SECRET=<muss EXAKT mit Backend übereinstimmen, falls SSR verifiziert>
```

> Beide `JWT_SECRET` **müssen** identisch sein. Symptom bei Drift:
> Frontend setzt Cookie nach Login, Middleware sieht Cookie als gültig,
> Backend lehnt aber jeden API-Call mit 401 ab.

## Deploy-Workflow

```bash
# Backend (auf VPS)
cd /root/dev/packcheck/packcheck_backend
git pull
docker compose up -d --build

# Frontend
cd /root/dev/packcheck/packcheck_frontend
git pull
docker compose up -d --build
```

`packcheck_frontend/deploy.sh` kapselt das. Caddy muss bei neuen Domains
einmalig neu geladen werden (`docker exec edge-caddy caddy reload`).

## Volumes

`packcheck_pgdata` → `/var/lib/postgresql/data`. Beim `docker compose
down -v` werden **alle** Daten gelöscht. Backup-Strategie ist offen,
siehe [[offene_fragen]].

## Logging

`json-file` Driver mit Rotation `max-size: 10m`, `max-file: 3` für
beide App-Container. Live-Logs:

```bash
docker compose logs -f api
docker exec edge-caddy caddy reload  # nach Caddyfile-Änderung
```
