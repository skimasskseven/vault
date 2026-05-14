---
tags:
  - projekt/packcheck
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# PackCheck — Offene Fragen / TODOs

Stand 2026-05-14 — Bestandsaufnahme nach Backend-Cleanup. Punkte
geordnet nach Risiko: Security/Datenintegrität zuerst, dann
Feature-Gaps, dann Operations.

## Security & Datenintegrität

### 1. `requireAdmin` nicht auf `/admin`-Router gemounted

`server.ts` ruft `app.use('/admin', adminRoutes)`, aber im aktuellen
Stand schützt nur `requireAuth` (im Router) — `requireAdmin` muss
zusätzlich davor. **Symptom:** Jeder eingeloggte Customer könnte
`GET /admin/customers` aufrufen und alle Kundendaten ziehen.

→ Fix: `router.use(requireAuth, requireAdmin)` in `routes/admin.ts`
   oder `app.use('/admin', requireAdmin, adminRoutes)` in `server.ts`.

### 2. Email-Verifikation komplett offen

`POST /auth/register` legt User direkt mit `accepted_terms_at = NOW()`
an — keine Verify-Mail, kein `email_confirmed_at`-Flag. Email-Templates
für `registration_confirmation` existieren in `lib/` (DE/EN/ZH), werden
aber nirgends versendet. **Brevo o.ä. ist nicht im Stack.**

Entscheidung nötig:
- (a) Brevo / SMTP integrieren + Verify-Token-Tabelle + Endpoint `/auth/verify?token=…`
- (b) Manuelle Aktivierung durch Admin (Feld `is_active` in `users`)
- (c) "Trust on first login" weiterführen (Status quo, akzeptiert Spam-Registrierungen)

### 3. Password-Reset ohne Backend

`/forgot-password`-Page existiert im Frontend. Im Backend gibt es **keine**
Route `/auth/forgot-password` oder `/auth/reset-password`. User die ihr
Passwort vergessen → Sackgasse.

→ Mindestens: `password_reset_tokens`-Tabelle (token, user_id, expires_at,
   used_at), `POST /auth/forgot-password` (sendet Mail), `POST /auth/reset-password`
   (verbraucht Token, hashed neues Passwort).

### 4. JWT-Revocation nicht möglich

Stateless JWTs mit 7d-TTL. Wenn ein Token leakt (XSS, Geräte-Verlust),
gibt es keinen Weg ihn ungültig zu machen außer `JWT_SECRET`-Rotation
(invalidiert *alle* Sessions).

Optionen:
- Refresh-Token-Pattern (kurze Access-TTL ~15min + langlebiger Refresh
  in DB-Tabelle, der revoked werden kann)
- Token-Blocklist in Redis
- TTL auf 1d senken + Re-Login akzeptieren

### 5. Kein Audit-Log

Admin-Aktionen (Customer editieren, Invoice generieren, Note hinzufügen)
werden nicht persistent geloggt. Nur `pino-http` Operations-Log
(verschwindet mit Container-Restart wenn json-file rotiert).

→ Tabelle `audit_log (id, actor_user_id, action, target_table, target_id, payload jsonb, created_at)`.

## Daten-Modell

### 6. Keine Unique-Constraint auf `packaging_data`

User kann mehrere Einträge für dieselbe `(user_id, packaging_type_id, year, quarter)`-
Kombi anlegen. Invoice-Generator addiert über alle — beabsichtigt
(mehrere Lieferungen pro Quartal) oder Bug?

→ Klären, ggf. `UNIQUE`-Index ergänzen oder Frontend-UX so bauen, dass
   nur 1 Eintrag pro Kombi möglich ist (UPSERT).

### 7. `packaging_types` hardcoded auf 9 Typen

Sowohl im Frontend (`app/dashboard/packaging/new/page.tsx`) als auch
im DB-Seed (`migrations/001_init.sql`) und in der zod-Schema
(`packaging_type_id: 1..9`). Hinzufügen eines 10. Typs erfordert
3 Stellen synchron zu ändern.

→ Mittelfristig: Frontend lädt Liste via `GET /packaging-types`,
   zod nutzt dynamisches enum.

### 8. `INVOICE_RATE_EUR_PER_KG` global statt pro Typ

Aktuell **ein** Preis pro Kilo, unabhängig vom Material. Realistisch ist
eine Tabelle `pricing (packaging_type_id, valid_from, eur_per_kg)`.

### 9. Invoice-Numbering / PDF / Versand

`invoices`-Tabelle hat nur `id` (Serial). Echte Rechnungsnummern
(rechtssicher, lückenlos, Format `LE-2026-Q1-0001`) fehlen. PDF-
Rendering existiert nicht. Email-Versand existiert nicht (Templates
für `invoice` & `reminder_invoice` liegen in `lib/`, ungenutzt).

## Migrations / DB-Operations

### 10. Kein Migrations-Tool

Schema-Evolution geht aktuell über manuell nummerierte SQL-Files in
`docker-entrypoint-initdb.d/` — die laufen aber **nur beim ersten
Container-Start**. Eine Schema-Änderung im Live-Betrieb erfordert
manuelles `psql` + `ALTER TABLE`.

Optionen:
- `node-pg-migrate` (idiomatisch für pg-Stack)
- Sqitch (DB-agnostisch)
- Eigenes Migration-Runner im API-Bootstrap

### 11. Keine Backups

Postgres-Volume `packcheck_pgdata` ohne automatisches Backup.
Container-Lifecycle-Risiko: `docker compose down -v` löscht alles.

→ Mindestens täglicher `pg_dump` auf S3-kompatibles Storage,
   ideal: Streaming-Backup via `pgBackRest` oder `wal-g`.

### 12. Keine Daten-Export für Customer (DSGVO Art. 20)

`GET /customer/export/csv` exportiert nur Packaging-Daten, nicht das
volle User-Profil. DSGVO-Auskunftsrecht / Datenportabilität braucht ein
JSON mit allem.

## Operations

### 13. Keine Integration-Tests, keine CI

Backend hat `npm run build` (tsc) und `dev` (tsx watch), aber keine
`npm test`. Kein GitHub-Actions-File. Frontend genauso.

### 14. Logging-Aggregation

`pino`-JSON-Logs gehen via `json-file` Driver auf Disk und rotieren bei
10 MB. Kein Forwarder in ein zentrales Log-Backend (Loki, ELK).

### 15. Monitoring / Alerting

Healthchecks reden mit Docker, aber niemand redet mit *uns* wenn
Container 12h down ist. Uptime-Monitor (Uptime Kuma oder ähnlich) auf
externer Maschine fehlt.

### 16. Caddy-Reload-Trigger

Bei neuen Domains/Subdomains muss `docker exec edge-caddy caddy reload`
manuell laufen. Ist im Deploy-Workflow nicht automatisiert.

## Cross-Project / Doku

### 17. Geteilter `JWT_SECRET` zwischen FE und BE

Frontend hat `JWT_SECRET` in `.env.local`, Backend in `.env`. Drift
(Operator setzt nur einen) führt zu schwer zu debuggenden 401s.

→ Mindestens: gemeinsames `make secrets`-Skript, das beide `.env`-
   Files synchron updated.

### 18. `BACKEND_NOTES.md` ist historisch — wann archivieren?

Dokumentiert den **alten** Stand vor dem Cleanup am 2026-05-14. Nach
Stabilisierung der neuen Specs in `docs/` kann es nach `docs/archiv/`
oder ganz weg.
