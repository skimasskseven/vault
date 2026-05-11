---
tags:
  - type/dashboard
  - meta/pattern-analyse
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# Pattern-Dashboard

Cross-Projekt-Analyse: welche Tech-Bausteine wiederholen sich, welche sind
unique. Wird bei jedem Lauf von `build_knowledge_graph.py` neu generiert.

Stand: **2026-05-11 19:11 UTC**

## 🧮 Matrix: Komponente × Projekt

| Komponente | conformis | running_app | Σ |
|---|---|---|---|
| [[10_infrastruktur/Docker|Docker]] `infra` | ✅ | ✅ | 2 |
| [[10_infrastruktur/Hostinger VPS|Hostinger VPS]] `infra` | ✅ | ✅ | 2 |
| [[10_infrastruktur/PostgreSQL|PostgreSQL]] `db` | ✅ | ✅ | 2 |
| [[10_infrastruktur/Apple Health|Apple Health]] `external` |   | ✅ | 1 |
| [[10_infrastruktur/Archon|Archon]] `ai` | ✅ |   | 1 |
| [[10_infrastruktur/Brevo|Brevo]] `email` | ✅ |   | 1 |
| [[10_infrastruktur/Caddy - Let's Encrypt|Caddy / Let's Encrypt]] `infra` | ✅ |   | 1 |
| [[10_infrastruktur/Claude API|Claude API]] `ai` | ✅ |   | 1 |
| [[10_infrastruktur/Companies House|Companies House]] `external` | ✅ |   | 1 |
| [[10_infrastruktur/DIP (Bundestag)|DIP (Bundestag)]] `external` | ✅ |   | 1 |
| [[10_infrastruktur/DuckDNS|DuckDNS]] `infra` | ✅ |   | 1 |
| [[10_infrastruktur/FastAPI|FastAPI]] `backend` |   | ✅ | 1 |
| [[10_infrastruktur/Firebase Cloud Messaging|Firebase Cloud Messaging]] `comms` |   | ✅ | 1 |
| [[10_infrastruktur/Flutter|Flutter]] `frontend` |   | ✅ | 1 |
| [[10_infrastruktur/Garmin|Garmin]] `external` |   | ✅ | 1 |
| [[10_infrastruktur/Google Fit|Google Fit]] `external` |   | ✅ | 1 |
| [[10_infrastruktur/GSAP|GSAP]] `frontend` | ✅ |   | 1 |
| [[10_infrastruktur/Instagram (Native Share)|Instagram (Native Share)]] `external` |   | ✅ | 1 |
| [[10_infrastruktur/Mapbox|Mapbox]] `frontend` |   | ✅ | 1 |
| [[10_infrastruktur/Next.js|Next.js]] `frontend` | ✅ |   | 1 |
| [[10_infrastruktur/OpenRouter|OpenRouter]] `ai` | ✅ |   | 1 |
| [[10_infrastruktur/OSM Overpass|OSM Overpass]] `external` | ✅ |   | 1 |
| [[10_infrastruktur/pgcrypto|pgcrypto]] `db` |   | ✅ | 1 |
| [[10_infrastruktur/Playwright|Playwright]] `external` | ✅ |   | 1 |
| [[10_infrastruktur/PostGIS|PostGIS]] `db` |   | ✅ | 1 |
| [[10_infrastruktur/React|React]] `frontend` | ✅ |   | 1 |
| [[10_infrastruktur/Strava API|Strava API]] `external` |   | ✅ | 1 |
| [[10_infrastruktur/Stripe|Stripe]] `payment` | ✅ |   | 1 |
| [[10_infrastruktur/Tailwind CSS|Tailwind CSS]] `frontend` | ✅ |   | 1 |
| [[10_infrastruktur/Telegram Bot|Telegram Bot]] `comms` | ✅ |   | 1 |
| [[10_infrastruktur/Three.js|Three.js]] `frontend` | ✅ |   | 1 |
| [[10_infrastruktur/Tranco|Tranco]] `external` | ✅ |   | 1 |
| [[10_infrastruktur/TypeScript|TypeScript]] `frontend` | ✅ |   | 1 |

## 🔁 Gemeinsame Muster (in ≥ 2 Projekten)

- **Docker** (infra) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/running_app/übersicht|running_app]]
- **Hostinger VPS** (infra) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/running_app/übersicht|running_app]]
- **PostgreSQL** (db) — genutzt in: [[20_projekte/conformis/übersicht|conformis]], [[20_projekte/running_app/übersicht|running_app]]

## ✨ Unique pro Projekt

**conformis:**
  - Archon
  - Brevo
  - Caddy / Let's Encrypt
  - Claude API
  - Companies House
  - DIP (Bundestag)
  - DuckDNS
  - GSAP
  - Next.js
  - OSM Overpass
  - OpenRouter
  - Playwright
  - React
  - Stripe
  - Tailwind CSS
  - Telegram Bot
  - Three.js
  - Tranco
  - TypeScript

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
- `#domain/b2b-saas` → conformis
- `#domain/compliance` → conformis
- `#domain/consumer-mobile` → running_app
- `#domain/geo-spatial` → running_app

## 📜 Letzter Commit pro Projekt

- **conformis** (code/): `934bb96` — 2026-05-10 — _fix(cron): daily-status nur einmalig am 11.05.2026 (nicht täglich)_
- **running_app** (code/): `fc38917` — 2026-05-11 — _feat(mobile): like state primed on run detail open + count visible_
