---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# Skill: fixer


tags: #skill
[[Fixer-Bot]]


## Funktion
Liefert Fix-Anleitungen für Verstöße – angepasst an Plattform. GUI zuerst, dann Code.

## Inputs
- `violation` (Object)
- `platform` (String: `wordpress|shopify|wix|custom`)
- `country` (String)

## Output
```json
{ "fixes": [{ "violation_type": "odr", "platform": "wordpress", "code": "<a href='...'>..</a>", "file_path": "footer.php", "instructions": "..." }] }
```
