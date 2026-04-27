# Skill: email-sender


tags: #skill
[[skills.md]][[Conformis - RechteRadar]]

## Funktion
Sendet Outreach-Emails via Brevo API. 300/Tag. 3-5-9 Regel.

## API
`POST https://api.brevo.com/v3/smtp/email` | Header: `api-key: {BREVO_API_KEY}`

## Output
```json
{ "sent": true, "lead_id": 42, "brevo_id": "abc123", "stage": 1, "status": "sent" }
```
