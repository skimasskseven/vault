# Skill: website-scanner

tags: #skill
[[04-Skills.md/website-scanner]]
**Genutzt von:** Orchestrator, Website-Scanner, Law-Checker, Screenshot-Tool, alle Workspaces

---

## Funktion
Besucht eine Website und prüft alle 9 Compliance-relevanten Elemente. Erkennt Sprache und Geschäftsmodell.

## Inputs
- `url` (String)
- `country` (String: `DE|CH|UK|US`)

## Geprüfte Elemente
Impressum, Datenschutz, Cookie-Banner, AGB, Widerruf, ODR-Link, Button-Lösung, HTTPS, Accessibility

## Output
```json
{
  "url": "https://example.de",
  "status": "ok|blocked|timeout",
  "lang": "de",
  "business_model": { "category": "online_shop_werkzeug", "confidence": 0.85 },
  "checks": { "impressum": true, "privacy": false, "cookies": true, "agb": true,
               "widerruf": true, "odr": false, "button": true, "https": true, "a11y": false },
  "violations": [{ "type": "odr", "severity": "mittel", "description": "Kein ODR-Link" }]
}
```
