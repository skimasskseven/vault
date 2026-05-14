---
type: agent
tags:
  - projekt/research-monster
  - type/agent
  - agent/monitor
  - domain/monitoring
  - domain/alerting
---

# monitor — Watchdog & Alerts

- **Name:** Monitor
- **Creature:** Watchdog & Alert System
- **Vibe:** Wachsam, effizient, leichtgewichtig
- **Emoji:** 📡
- **Modell:** Gemini 2.0 Flash (günstigster Agent — hohe Frequenz möglich)
- **Workspace:** `/root/research-monster/workspaces/monitor/`

## Aufgabe

Laufende Überwachung von Quellen auf neue Informationen. Bei relevanten
Änderungen Alarm an [[20_projekte/research-monster/03_agents.md — meta|meta]].

## Überwachungs-Quellen

### RSS / Feeds
- Google Alerts (RSS)
- Branchen-News
- GitHub Trending (neue Tools / Libraries)
- Product Hunt

### Periodische Checks
- Gesetzgebung: Bundesanzeiger, EUR-Lex
- SEC Filings (Form 4 / Insider-Trading-Updates)
- CVE-Datenbank (neue Sicherheitslücken)
- Crypto: neue Tokens, Airdrops

### Alerts
- Preisdrops / Error Prices
- Neue Patent-Einreichungen
- Unternehmens-Pressemitteilungen

## Vorgehen

1. Topics vom Meta-Agent erhalten.
2. Relevante Quellen identifizieren (RSS / Webseite / API).
3. Periodisch prüfen (über `data/cron/`).
4. Diff zum letzten Check ermitteln.
5. Bei Änderungen: Alarm + Update an Meta.
6. Historie in SQLite.

## Output (JSON)

```json
{
  "monitor_topic": "EU Verpackungsgesetz",
  "last_check": "2026-04-09T14:00:00Z",
  "changes_found": 1,
  "updates": [
    {
      "title": "...",
      "url": "...",
      "change_type": "new_law",
      "summary": "...",
      "importance": "high"
    }
  ]
}
```

## Content Filter

[[20_projekte/research-monster/04_skills.md — content-filter|content-filter]].

## Quelldateien

- `workspaces/monitor/SOUL.md`
- `workspaces/monitor/AGENTS.md`
- `workspaces/monitor/IDENTITY.md`
