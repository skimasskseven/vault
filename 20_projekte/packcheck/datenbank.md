---
tags:
  - projekt/packcheck
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# PackCheck — Datenbank-Schema

Postgres 17 (alpine), Single-DB `packcheck`. Initial-Schema wird beim
ersten Container-Start aus `packcheck_backend/migrations/001_init.sql`
über `docker-entrypoint-initdb.d` geladen. Alles `IF NOT EXISTS` /
`ON CONFLICT DO NOTHING` — Re-Runs sind idempotent.

> **Migrations-Tool:** Aktuell **keines**. Schema-Evolution geht über
> manuell nummerierte SQL-Dateien (`002_…sql`, `003_…sql`). Migration auf
> `node-pg-migrate` ist offen — siehe [[offene_fragen]].

## Tabellen

### `users`

Kunden **und** Admins in einer Tabelle, unterschieden durch `is_admin`.

| Spalte | Typ | Constraint |
|---|---|---|
| `id` | `SERIAL` | PK |
| `email` | `VARCHAR(255)` | `UNIQUE NOT NULL`, Index auf `LOWER(email)` |
| `password_hash` | `VARCHAR(255)` | `NOT NULL` (bcrypt, 12 Rounds) |
| `is_admin` | `BOOLEAN` | `NOT NULL DEFAULT FALSE` |
| `first_name`, `last_name` | `VARCHAR(100)` | nullable |
| `company`, `street`, `zip_code`, `city`, `country`, `phone`, `tax_id` | div. | nullable, `country` default `'Deutschland'` |
| `accepted_terms_at` | `TIMESTAMPTZ` | bei `/auth/register` auf `NOW()` gesetzt |
| `created_at`, `updated_at` | `TIMESTAMPTZ` | default `NOW()`, `updated_at` per Trigger |

### `packaging_types`

Stammdaten — **9 fixe Typen**, hardcoded im Frontend (`app/dashboard/packaging/new/page.tsx`).

```
1  cardboard_custom         Kartons (eigene Maße)
2  cardboard_standard       Kartons (Standard)
3  plastic_bag_s            Plastiktüten - Größe S
4  plastic_bag_m            Plastiktüten - Größe M
5  plastic_bag_l            Plastiktüten - Größe L
6  shrink_paper             Schrumpfpapier
7  shipping_envelope        Versandtaschen
8  shipping_envelope_clear  Versandtaschen (klar)
9  shipping_envelope_red    Versandtaschen (rot)
```

`packaging_type_id` in `packaging_data` ist `1..9`-CHECK über die
zod-Validation im API-Handler — DB-seitig nur FK-Constraint.

### `packaging_data`

Quartals-Einträge: pro User × Jahr × Quartal × Verpackungstyp eine Zeile
mit Kilogramm-Menge.

| Spalte | Typ | Constraint |
|---|---|---|
| `id` | `SERIAL` | PK |
| `user_id` | `INTEGER` | FK → `users(id)` `ON DELETE CASCADE` |
| `packaging_type_id` | `INTEGER` | FK → `packaging_types(id)` |
| `year` | `INTEGER` | `CHECK 2020..2099` |
| `quarter` | `INTEGER` | `CHECK 1..4` |
| `quantity_kg` | `NUMERIC(10,2)` | `CHECK >= 0` (im API "quantity" gemappt) |
| `custom_dimensions` | `VARCHAR(50)` | nur für `cardboard_custom` relevant |
| `notes` | `TEXT` | nullable |
| `created_at`, `updated_at` | `TIMESTAMPTZ` | Trigger |

Indices: `(user_id, year)` für Customer-Liste, `(year, quarter)` für
Cross-User-Aggregate.

> ⚠️ Es gibt **keinen** `UNIQUE (user_id, packaging_type_id, year, quarter)` —
> ein User kann mehrere Einträge desselben Typs pro Quartal haben.
> Das Invoice-Aggregat addiert über alle. Beabsichtigt? → [[offene_fragen]].

### `customer_notes`

Admin-only Anmerkungen zu Kunden.

| Spalte | Typ | Constraint |
|---|---|---|
| `id` | `SERIAL` | PK |
| `customer_id` | `INTEGER` | FK → `users(id)` CASCADE |
| `admin_id` | `INTEGER` | FK → `users(id)` `ON DELETE SET NULL` |
| `note` | `TEXT` | `NOT NULL`, max 5000 chars (API-zod) |
| `created_at` | `TIMESTAMPTZ` | default `NOW()` |

Index: `(customer_id, created_at DESC)`.

### `invoices`

Generierte Quartals-Rechnungen.

| Spalte | Typ | Constraint |
|---|---|---|
| `id` | `SERIAL` | PK |
| `customer_id` | `INTEGER` | FK → `users(id)` CASCADE |
| `year`, `quarter` | `INTEGER` | quarter `CHECK 1..4` |
| `amount_eur` | `NUMERIC(10,2)` | `CHECK >= 0` (= `SUM(quantity_kg) × INVOICE_RATE_EUR_PER_KG`) |
| `status` | `VARCHAR(20)` | `CHECK IN ('pending','paid','overdue','cancelled')`, default `'pending'` |
| `generated_at` | `TIMESTAMPTZ` | default `NOW()` |
| `paid_at` | `TIMESTAMPTZ` | nullable |
| | | `UNIQUE (customer_id, year, quarter)` |

`POST /admin/invoices` macht `INSERT … ON CONFLICT DO UPDATE` — eine
Re-Generierung überschreibt `amount_eur` und resettet `status='pending'`.
Index: `(customer_id, year DESC, quarter DESC)`.

## Trigger

`trg_set_updated_at()` setzt `NEW.updated_at = NOW()` auf jeder Update-
Operation. Aktiv für `users` und `packaging_data`.

## Seed beim Boot

`server.ts → seedAdmin()` legt einen Admin-User an, falls
`SEED_ADMIN_EMAIL` + `SEED_ADMIN_PASSWORD` gesetzt sind und noch kein
Admin existiert. `ON CONFLICT (email) DO NOTHING`.

## Backups

Postgres-Volume: `packcheck_pgdata`. **Kein** automatisches Backup
konfiguriert. Siehe [[deployment]] und [[offene_fragen]].
