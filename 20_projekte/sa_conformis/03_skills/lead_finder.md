# Skill: lead-finder


tags: #skill
[[04-Skills.md/lead-finder]]
## Funktion
Findet gewerbliche Händler mit eigenen Websites aus offiziellen Registern. 50 Leads/Tag.

## Inputs
- `target_country` (String: `DE|CH|UK|US`)
- `batch_size` (Number: 50)

## Filter
- Keine Social Media / Marktplätze
- Nur eigene Domains mit HTTP 200
- Muss E-Mail haben

## Output
```json
{ "leads": [{ "company": "...", "url": "https://...", "country": "DE", "email": "...", "source": "handelsregister" }], "status": "success" }
```
