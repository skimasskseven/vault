---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# AGENTS.md – Report-Builder

Gestartet vom Orchestrator nach [STATUS: SCREENSHOTS_COMPLETE].
Erstelle HTML-Teaser-Reports für alle Leads mit Compliance-Score < 85.
VOLLAUTOMATISCH. Keine Rückfragen.
[[agents.md]][[Conformis - RechteRadar]]

---

## Workflow

**1. Leads laden:**
```sql
SELECT l.id, l.company_name, l.url, l.email, l.country,
       cs.score_total, cs.score_class, cs.violations_json,
       array_agg(s.file_path) as screenshots
FROM leads l
JOIN compliance_scores cs ON cs.lead_id = l.id
LEFT JOIN screenshots s ON s.lead_id = l.id
WHERE l.status='ready_for_outreach' AND cs.score_total < 85
GROUP BY l.id, l.company_name, l.url, l.email, l.country,
         cs.score_total, cs.score_class, cs.violations_json;
```

**2. Schwersten Verstoß auswählen (für Teaser):**
Severity-Priorität: `kritisch` → `schwer` → `mittel` → `leicht`
Bei Gleichstand: höchster `points_deducted` Wert gewinnt.

**3. Teaser-Regel (KRITISCH):**
- **1–2 Verstöße:** Keinen konkreten Verstoß nennen → nur „möglichen Hinweis" andeuten
- **3+ Verstöße:** Genau EINEN zeigen (schwersten) + EINEN Screenshot. Rest hinter Paywall.

**4. Report als HTML erstellen:**
```bash
mkdir -p /root/.openclaw/reports
# Report-Datei: /root/.openclaw/reports/{lead_id}_teaser_{YYYYMMDD}.html
```

Report-Struktur:
- Header: Conformis Logo + Firmenname
- Score-Box: `SCORE/100 – SCORE_LABEL` (farbig: grün/gelb/rot/schwarz)
- Verstoß-Block: Bezeichnung + Gesetz + Screenshot (nur 1!)
- CTA-Button: „Vollständigen Report anfordern (€29,99)"
- Footer-Disclaimer: „Keine Rechtsberatung."

Score-Farben: `green=#2ecc71` | `yellow=#f39c12` | `red=#e74c3c` | `black=#2c3e50`

**5. In DB speichern:**
```sql
UPDATE leads SET
  teaser_report_path = '/root/.openclaw/reports/LEAD_ID_teaser_DATUM.html',
  report_generated_at = NOW()
WHERE id = LEAD_ID;
```

**Full-Report** (nur nach Kauf): Alle Verstöße + alle Screenshots + Fix-Vorschläge.
Ablauf: 48h nach Erstellung (`expires_at = NOW() + INTERVAL '48 hours'`).

---

## Abschluss
```
[STATUS: REPORT_GENERATED]
Reports erstellt: X | Pfad: /root/.openclaw/reports/
```
