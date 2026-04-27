# Skill: report-builder


tags: #skill
[[report-builder]]
## Funktion
Erstellt kundenfähigen HTML/PDF Report aus allen Agenten-Ergebnissen.

## Report-Typen
- `teaser` – 1 Verstoß (kostenlos)
- `full` – Alle Verstöße + Fix-Vorschläge (€29,99)
- `premium` – Compliance + UX-Audit (€119/Mo)

## Speicherpfad
`/home/node/.openclaw/reports/{lead_id}_{date}.html` | Ablauf: 48h

## Output
```json
{ "report_id": "rpt_42_20260425", "score": 83, "violations_count": 4, "url": "/reports/42_20260425.html", "expires_at": "2026-04-27T08:00:00Z" }
```
