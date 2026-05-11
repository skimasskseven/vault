---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# AGENTS.md – Law-Checker

Gestartet vom Orchestrator nach [STATUS: SCAN_COMPLETE].
Berechne Compliance-Score (0–100) für jeden gescannten Lead.
VOLLAUTOMATISCH. Keine Rückfragen. NIEMALS Gesetzestexte erfinden. 
[[agents.md]][[Conformis - RechteRadar]]

---

## Workflow

**1. Scan-Ergebnisse laden:**
```sql
SELECT sr.*, l.country, l.company_name
FROM scan_results sr JOIN leads l ON sr.lead_id = l.id
WHERE l.status='scanned' ORDER BY sr.id ASC;
```

**2. Gesetzestexte aus DB laden (DB-FIRST):**
```sql
SELECT * FROM law_texts WHERE jurisdiction='LAND';
```
Nicht vorhanden → Orchestrator benachrichtigen (law-monitor triggern).

**3. Score berechnen (100 Punkte):**

| Kategorie | Max | Wichtigste Verstöße |
|-----------|-----|-------------------|
| Pflichtangaben | 35 | Kein Impressum (-35), fehlende USt-ID (-5), fehlende Adresse (-10) |
| Datenschutz | 30 | Keine Policy (-30), kein Ablehnen-Button (-5), Cookie-Vorauswahl (-5) |
| Verbraucherschutz | 15 | Kein Widerruf (-15), fehlende 14-Tage-Frist (-8), kein Formular (-7) |
| E-Commerce | 10 | Kein ODR-Link (-5), kein Streitbeilegungstext (-5) |
| Accessibility | 5 | Kein Statement (-5) |
| Technisch | 5 | Kein HTTPS (-3), kein HSTS (-2) |

**4. Jurisdiction → Gesetze:**

| Land | Gesetze |
|------|---------|
| DE | DDG §5, DSGVO, TTDSG §25, BGB §355, ODR-VO Art.14, BFSG |
| CH | neuDSG, UWG Art.3, WAG |
| UK | Companies Act §82, UK GDPR, CCR 2013 |
| US | CCPA, FTC Guidelines, ADA |

**5. Jeden Verstoß exakt dokumentieren:**
```json
{
  "violation": "Kein Link zur ODR-Plattform",
  "law": "Art. 14 VO (EU) Nr. 524/2013",
  "law_text_excerpt": "aus law_texts DB – niemals erfinden",
  "severity": "mittel",
  "points_deducted": 5,
  "screenshot_needed": true,
  "fix": "ODR-Link im Footer einfügen"
}
```

Präzisions-Regel: NIEMALS vage sein.
`"Impressum unvollständig"` ❌ → `"Fehlende USt-ID (DDG §5 Abs.1 Nr.6)"` ✅

**6. Score-Klasse + in DB speichern:**

| Score | Klasse |
|-------|--------|
| 85–100 | `green` |
| 60–84 | `yellow` |
| 30–59 | `red` |
| 0–29 | `black` |

```sql
INSERT INTO compliance_scores
  (lead_id, score_total, score_class, violations_json, jurisdiction, checked_at)
VALUES (LEAD_ID, SCORE, 'yellow', '[...]', 'DE', NOW());

UPDATE leads SET status='scored' WHERE id=LEAD_ID;
```

**Pflicht-Disclaimer in jedem Output:**
> „Dies ist eine automatisierte Prüfung. Keine Rechtsberatung."

---

## Abschluss
```
[STATUS: CHECK_COMPLETE]
Geprüft: X | 🟢 X | 🟡 X | 🔴 X | ⚫ X | Verstöße: X
```
