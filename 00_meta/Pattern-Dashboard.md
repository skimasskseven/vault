---
tags:
  - type/dashboard
  - meta/pattern-analyse
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# Pattern-Dashboard

Cross-Projekt-Analyse: welche Tech-Bausteine wiederholen sich, welche sind
unique. Wird bei jedem Lauf von `build_knowledge_graph.py` neu generiert.

Stand: **2026-05-14 21:33 UTC**

## 🧮 Matrix: Komponente × Projekt

| Komponente | conformis | packcheck | running_app | Σ |
|---|---|---|---|---|
| [[10_infrastruktur/Docker|Docker]] `infra` | ✅ | ✅ | ✅ | 3 |
| [[10_infrastruktur/Hostinger VPS|Hostinger VPS]] `infra` | ✅ | ✅ | ✅ | 3 |
| [[10_infrastruktur/PostgreSQL|PostgreSQL]] `db` | ✅ | ✅ | ✅ | 3 |
| [[10_infrastruktur/Caddy - Let's Encrypt|Caddy / Let's Encrypt]] `infra` | ✅ | ✅ |   | 2 |
| [[10_infrastruktur/Next.js|Next.js]] `frontend` | ✅ | ✅ |   | 2 |
| [[10_infrastruktur/React|React]] `frontend` | ✅ | ✅ |   | 2 |
| [[10_infrastruktur/Tailwind CSS|Tailwind CSS]] `frontend` | ✅ | ✅ |   | 2 |
| [[10_infrastruktur/Three.js|Three.js]] `frontend` | ✅ | ✅ |   | 2 |
| [[10_infrastruktur/TypeScript|TypeScript]] `frontend` | ✅ | ✅ |   | 2 |
| [[10_infrastruktur/Apple Health|Apple Health]] `external` |   |   | ✅ | 1 |
| [[10_infrastruktur/Archon|Archon]] `ai` | ✅ |   |   | 1 |
| [[10_infrastruktur/bcrypt|bcrypt]] `backend` |   | ✅ |   | 1 |
| [[10_infrastruktur/Brevo|Brevo]] `email` | ✅ |   |   | 1 |
| [[10_infrastruktur/Claude API|Claude API]] `ai` | ✅ |   |   | 1 |
| [[10_infrastruktur/Companies House|Companies House]] `external` | ✅ |   |   | 1 |
| [[10_infrastruktur/DIP (Bundestag)|DIP (Bundestag)]] `external` | ✅ |   |   | 1 |
| [[10_infrastruktur/DuckDNS|DuckDNS]] `infra` | ✅ |   |   | 1 |
| [[10_infrastruktur/FastAPI|FastAPI]] `backend` |   |   | ✅ | 1 |
| [[10_infrastruktur/Firebase Cloud Messaging|Firebase Cloud Messaging]] `comms` |   |   | ✅ | 1 |
| [[10_infrastruktur/Flutter|Flutter]] `frontend` |   |   | ✅ | 1 |
| [[10_infrastruktur/Garmin|Garmin]] `external` |   |   | ✅ | 1 |
| [[10_infrastruktur/Google Fit|Google Fit]] `external` |   |   | ✅ | 1 |
| [[10_infrastruktur/GSAP|GSAP]] `frontend` | ✅ |   |   | 1 |
| [[10_infrastruktur/Instagram (Native Share)|Instagram (Native Share)]] `external` |   |   | ✅ | 1 |
| [[10_infrastruktur/Mapbox|Mapbox]] `frontend` |   |   | ✅ | 1 |
| [[10_infrastruktur/OpenRouter|OpenRouter]] `ai` | ✅ |   |   | 1 |
| [[10_infrastruktur/OSM Overpass|OSM Overpass]] `external` | ✅ |   |   | 1 |
| [[10_infrastruktur/pgcrypto|pgcrypto]] `db` |   |   | ✅ | 1 |
| [[10_infrastruktur/Playwright|Playwright]] `external` | ✅ |   |   | 1 |
| [[10_infrastruktur/PostGIS|PostGIS]] `db` |   |   | ✅ | 1 |
| [[10_infrastruktur/Strava API|Strava API]] `external` |   |   | ✅ | 1 |
| [[10_infrastruktur/Stripe|Stripe]] `payment` | ✅ |   |   | 1 |
| [[10_infrastruktur/Telegram Bot|Telegram Bot]] `comms` | ✅ |   |   | 1 |
| [[10_infrastruktur/Tranco|Tranco]] `external` | ✅ |   |   | 1 |

## 🔁 Gemeinsame Muster (in ≥ 2 Projekten)

- **Docker** (infra) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/packcheck/übersicht|packcheck]], [[20_projekte/running_app/übersicht|running_app]]
- **Hostinger VPS** (infra) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/packcheck/übersicht|packcheck]], [[20_projekte/running_app/übersicht|running_app]]
- **PostgreSQL** (db) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/packcheck/übersicht|packcheck]], [[20_projekte/running_app/übersicht|running_app]]
- **Caddy / Let's Encrypt** (infra) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/packcheck/übersicht|packcheck]]
- **Next.js** (frontend) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/packcheck/übersicht|packcheck]]
- **React** (frontend) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/packcheck/übersicht|packcheck]]
- **Tailwind CSS** (frontend) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/packcheck/übersicht|packcheck]]
- **Three.js** (frontend) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/packcheck/übersicht|packcheck]]
- **TypeScript** (frontend) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/packcheck/übersicht|packcheck]]

## ✨ Unique pro Projekt

**conformis:**
  - Archon
  - Brevo
  - Claude API
  - Companies House
  - DIP (Bundestag)
  - DuckDNS
  - GSAP
  - OSM Overpass
  - OpenRouter
  - Playwright
  - Stripe
  - Telegram Bot
  - Tranco

**packcheck:**
  - bcrypt

**running_app:**
  - Apple Health
  - FastAPI
  - Firebase Cloud Messaging
  - Flutter
  - Garmin
  - Google Fit
  - Instagram (Native Share)
  - Mapbox
  - PostGIS
  - Strava API
  - pgcrypto

## 🌐 Domain-Cluster

- `#domain/ai-agents` → conformis
- `#domain/b2b-saas` → conformis, packcheck
- `#domain/compliance` → conformis
- `#domain/consumer-mobile` → running_app
- `#domain/geo-spatial` → running_app

## 📜 Letzter Commit pro Projekt

- **conformis** (code/): `720a93a` — 2026-05-14 — _ui(public): Rechte-News-Rebrand + Inter-Font + Stock-Bilder + Sections raus_
- **packcheck**: _(kein git-repo)_
- **running_app** (code/): `40192de` — 2026-05-11 — _fix(mobile): map atmosphere strip — use removeLayer/visibility, build now compiles_
