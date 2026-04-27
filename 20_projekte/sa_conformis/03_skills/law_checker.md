# Skill: law-checker


tags: #skill
[[04-Skills.md/law-checker]]
## Funktion
Berechnet Compliance-Score aus Scan-Ergebnissen. DB-First: immer `law_texts` Tabelle prüfen.

## Scoring
Pflichtangaben: 35 | Datenschutz: 30 | Verbraucherschutz: 15 | E-Commerce: 10 | Accessibility: 5 | Technisch: 5

## Output
```json
{
  "compliance_score": 83,
  "score_class": "yellow",
  "violations": [{ "violation": "...", "law": "...", "severity": "mittel", "points_deducted": 5 }],
  "disclaimer": "Keine Rechtsberatung."
}
```
