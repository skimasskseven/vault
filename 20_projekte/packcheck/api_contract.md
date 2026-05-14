---
tags:
  - projekt/packcheck
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# PackCheck — API Contract

Express + TypeScript, alle Routen unter `https://api.lucidexpress.de/`.
Body- und Query-Validation durchgehend mit `zod`. Auth via JWT
(HS256, 7d Default-TTL) — siehe [[security_auth]].

## Globale Pipeline

```
helmet (CSP off)
  → cors (allowlist, credentials: true)
  → cookieParser
  → express.json (1 MB limit)
  → pino-http
  → rateLimit (global: 120 req/min/IP)
  → routes
  → 404
  → errorHandler
```

`app.set('trust proxy', 1)` — Caddy terminiert TLS, `req.ip` wird aus
`X-Forwarded-For` gelesen (Pflicht für korrektes Rate-Limit-Tracking).

## `/health`

`GET /health` → `{ ok: true, ts: <ISO> }`. Wird vom docker-compose
Healthcheck gepingt (`wget --spider http://127.0.0.1:4000/health`).

## `/auth/*` — Public, mit `authLimiter` (10 req/min/IP)

| Route | Body | Response |
|---|---|---|
| `POST /auth/register` | `email, password (≥8), first_name, last_name, company?, street?, zip_code?, city?, country?, phone?, tax_id?, acceptTerms: true` | `201 { id, email }` · `409` falls Email schon existiert |
| `POST /auth/login` | `email, password` | `200 { token, isAdmin }` + setzt Cookies (`token`, `isAdmin`) auf `.lucidexpress.de` · `401` bei Fehlcredentials |
| `POST /auth/logout` | — | `200 { ok: true }` + clear Cookies |
| `GET /auth/me` | — (requireAuth) | Volles User-Objekt ohne `password_hash` |

`acceptTerms` muss exakt `true` sein, sonst `400`. Email wird
case-insensitive gespeichert (`LOWER(email)` Index).

## `/customer/*` — Auth required (JWT)

Alle Routen erfordern gültiges JWT. User-ID kommt aus `req.user.sub`,
**niemals** aus Body/Path.

### Profile

| Route | Body | Response |
|---|---|---|
| `GET /customer/profile` | — | User-Objekt |
| `PUT /customer/profile` | partial: `first_name?, last_name?, company?, street?, zip_code?, city?, country?, phone?, tax_id?` | Updated User |

Dynamische SET-Liste — nur Felder im Body werden upgedated.

### Packaging-Data

| Route | Body / Query | Response |
|---|---|---|
| `GET /customer/packaging?year=YYYY` | optional `year` | Array `{ id, user_id, packaging_type_id, packaging_type_key, year, quarter, quantity_kg, custom_dimensions, notes, created_at, updated_at }` |
| `POST /customer/packaging` | `packaging_type_id (1..9), year, quarter (1..4), quantity (mapped zu quantity_kg), custom_dimensions?, notes?` | `201` Eintrag |
| `PUT /customer/packaging/:id` | partial update, gleiche Felder | Updated |
| `DELETE /customer/packaging/:id` | — | `204` |

Ownership-Check in `PUT`/`DELETE`: Query enthält `WHERE user_id = $1`,
ein anderer User kann fremde Einträge nicht ändern (silent 404 statt 403).

### Reporting

| Route | Response |
|---|---|
| `GET /customer/comparison` | Aggregate über Jahre/Quartale für Charts im Dashboard |
| `GET /customer/export/csv?year=YYYY` | `text/csv` Attachment |

## `/admin/*` — Auth + `is_admin = true`

`requireAdmin` läuft nach `requireAuth` — siehe `middleware/requireAuth.ts`.
**Achtung:** im aktuellen `server.ts` ist `requireAdmin` auf den `/admin`-
Router noch **nicht** explizit gemounted (TODO im Code prüfen).

### Customer-Verwaltung

| Route | Body | Response |
|---|---|---|
| `GET /admin/customers` | — | Alle non-Admin-User mit Aggregat-Counts |
| `GET /admin/customers/:id` | — | User-Detail + Packaging-Summary |
| `PUT /admin/customers/:id` | gleiche Felder wie Profile | Updated (nur falls `is_admin = FALSE`) |

### Customer-Notes

| Route | Body | Response |
|---|---|---|
| `GET /admin/customers/:id/notes` | — | Liste, neueste zuerst, mit `admin_email` |
| `POST /admin/customers/:id/notes` | `{ note: string (1..5000) }` | `201` |

### Invoices

| Route | Body | Response |
|---|---|---|
| `GET /admin/invoices` | — | Alle Invoices mit Customer-Stammdaten |
| `POST /admin/invoices` | `{ customerId, year, quarter }` | Errechnet `amount_eur = SUM(quantity_kg) × INVOICE_RATE_EUR_PER_KG`, INSERT/UPSERT, returns `{ ...row, total_kg, rate }` |

### Export

| Route | Response |
|---|---|
| `GET /admin/export/csv` | Volldatenexport aller Customer × Packaging-Einträge als CSV |

## Error-Format

Konsistent: `{ message: string, issues?: <zod flatten> }`. HTTP-Codes:
`400` Validation, `401` Auth-Token fehlt/ungültig, `403` Admin-Routes
ohne Admin-Rechte, `404` Resource fehlt, `409` Email-Konflikt,
`500` über zentralen Errorhandler (loggt Stack via pino, sendet
`{ message: 'Internal server error' }`).
