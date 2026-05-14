---
tags:
  - projekt/packcheck
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# PackCheck — Security & Auth

Ziel: Customer-Bereich mit JWT-Auth, Admin-Bereich mit zusätzlichem
Rollen-Bit. Keine externen Identity-Provider, kein OAuth — Email +
Password, Self-Registration ist offen.

## Password-Hashing

`bcrypt`, **12 Rounds** (`auth.ts → BCRYPT_ROUNDS = 12`). Aktueller
Trade-off: ~250 ms pro Hash auf Server-CPU — bewusst hoch genug, dass
Brute-Force unrentabel ist, niedrig genug, dass Login unter 1s bleibt.

`hashPassword(plain)` und `verifyPassword(plain, hash)` sind die einzigen
Entry-Points. **Niemals** Plaintext loggen oder zurückgeben.

## JWT

| Parameter | Wert |
|---|---|
| Algorithmus | `HS256` (symmetrisch) |
| Secret | `JWT_SECRET` env (zod: `min(32)`) |
| TTL | `JWT_EXPIRES_IN` env (Default `7d`) |
| Payload | `{ sub: <user.id>, isAdmin: <boolean> }` |

Sign in `auth.ts → signToken()`, Verify in `verifyToken()`.
`verifyToken` checkt zusätzlich, dass `sub` ein Number und `isAdmin`
ein Boolean ist — alles andere → `null` → 401.

> **Symmetrisch (HS256), nicht asymmetrisch.** Bedeutet: derselbe Secret
> in Backend **und** Frontend (für SSR-Verify, falls aktiviert).
> Bei Secret-Rotation müssen beide gleichzeitig neugestartet werden.

## Token-Transport

Drei Stellen hat das Token:

| Wo | Wer setzt | Wer liest | Zweck |
|---|---|---|---|
| `Authorization: Bearer <jwt>` Header | `lib/api.ts` Request-Interceptor (axios) aus `localStorage.token` | Backend `requireAuth` (Priorität 1) | Standard-API-Calls |
| Cookie `token` (Domain `.lucidexpress.de`, `sameSite=lax`, `secure=true`) | Backend `setAuthCookies()` nach Login | Backend `requireAuth` (Fallback), Frontend `middleware.ts` | Server-Side-Routing-Guards |
| `localStorage.token` (Browser) | Frontend nach `POST /auth/login` | `lib/api.ts` Request-Interceptor | XSS-anfällig, aber nötig für API-Header |

Cookie ist `httpOnly: false` — bewusst, damit `middleware.ts` ihn
lesen kann. Trade-off: XSS könnte den Cookie ebenfalls auslesen → striktes
CSP wäre eine zukünftige Härtung.

## Authorisierungs-Middlewares

`packcheck_backend/src/middleware/requireAuth.ts`:

- `requireAuth(req, res, next)` — extrahiert Token (Header > Cookie),
  verifiziert HS256, setzt `req.user = JwtPayload | undefined`. Bei
  Fehler `401 { message: '…' }`.
- `requireAdmin(req, res, next)` — folgt nach `requireAuth`, prüft
  `req.user.isAdmin`. Bei `false` → `403 { message: 'Forbidden: admin only' }`.

> **Audit-Punkt:** Im aktuellen `server.ts` wird `requireAdmin` auf den
> `/admin`-Router noch **nicht** explizit gemounted. Der Admin-Router
> selbst muss es im Routen-File anwenden, sonst sind alle `/admin/*`
> nur via JWT (egal ob admin) erreichbar. → siehe [[offene_fragen]].

## Helmet

`helmet({ contentSecurityPolicy: false })` — alle Default-Header außer
CSP. CSP ist auf einer reinen JSON-API ohnehin wirkungslos und blockiert
nur Healthcheck-Tools.

Aktive Header: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`,
`Strict-Transport-Security` (gesetzt von Caddy mit `max-age=31536000;
includeSubDomains; preload`), `X-DNS-Prefetch-Control: off`, etc.

## CORS

```js
cors({
  origin: (origin, cb) => {
    if (!origin) return cb(null, true);              // server-to-server / curl
    if (env.CORS_ORIGINS.includes(origin)) return cb(null, true);
    return cb(new Error(`CORS: origin not allowed: ${origin}`));
  },
  credentials: true,
  methods: ['GET','POST','PUT','DELETE','OPTIONS'],
  allowedHeaders: ['Content-Type','Authorization'],
})
```

Allowlist via `CORS_ORIGINS` env (Default: `https://lucidexpress.de,
https://www.lucidexpress.de`). `credentials: true` ist Pflicht, damit
das Cookie cross-origin mitgesendet wird.

## Rate-Limiting

Zwei Schichten:

| Limiter | Anwendung | Limit |
|---|---|---|
| Global | alle Routes | 120 req / 60s / IP |
| `authLimiter` | `/auth/register`, `/auth/login` | 10 req / 60s / IP |

`standardHeaders: true` setzt `RateLimit-*` Header — Frontend kann
"too many" graceful anzeigen.

> **Tracking-Voraussetzung:** `app.set('trust proxy', 1)` muss gesetzt
> sein (ist es), sonst zählt express-rate-limit alle Requests als
> kommend von der Caddy-Container-IP → globaler Lockout.

## CSRF

Aktuell **nicht** explizit geschützt. Trade-off:
- Auth-Header-Pfad (Bearer aus localStorage) ist CSRF-immun.
- Cookie-Pfad ist `sameSite=lax` — schützt gegen klassisches CSRF auf
  POST-Forms, aber nicht gegen Subdomain-Hijacking unterhalb
  `lucidexpress.de`.

Falls cross-site POST-Endpoints später dazu kommen → `csurf` oder
double-submit-cookie nachrüsten.

## Secrets-Management

Alle Secrets in `.env` (gitignored). Kein Vault, kein KMS. JWT_SECRET
und POSTGRES_PASSWORD müssen beim ersten Deployment manuell gesetzt
werden — `env.ts` (zod-validiert) und `docker-compose.yml`
(`POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?…}`) failen hart bei
fehlenden Werten.

## Audit-Log

Aktuell **keiner**. `pino-http` loggt jeden Request mit `req-id`,
Status, Dauer — das ist ein Operations-Log, kein Security-Audit.
Login-Versuche, Admin-Aktionen, Customer-Daten-Änderungen sind nicht
separat persistiert. → siehe [[offene_fragen]].
