# AGENTS.md – Email-Sender

Gestartet vom Orchestrator nach [STATUS: REPORT_GENERATED].
Versende fällige Outreach-Emails nach der 3-5-9 Regel. Limit: 300/Tag.
VOLLAUTOMATISCH. Keine Rückfragen. [[agents.md]] [[Conformis - RechteRadar]]

---

## Workflow

**1. Fällige Emails ermitteln:**
```sql
SELECT l.id, l.company_name, l.url, l.email, l.country,
       l.outreach_stage, cs.score_total, cs.violations_json,
       l.teaser_report_path
FROM leads l JOIN compliance_scores cs ON cs.lead_id = l.id
WHERE l.status='ready_for_outreach' AND l.email IS NOT NULL
  AND (
    (l.outreach_stage = 0) OR
    (l.outreach_stage = 1 AND l.last_contact_at < NOW() - INTERVAL '3 days') OR
    (l.outreach_stage = 2 AND l.last_contact_at < NOW() - INTERVAL '5 days')
  )
  AND l.outreach_stage < 3
ORDER BY cs.score_total ASC LIMIT 300;
```

**2. Sprache:** DE/CH → Deutsch | UK/US → Englisch

**3. Email via Brevo API senden:**
```bash
curl -s --request POST \
  --url https://api.brevo.com/v3/smtp/email \
  --header "api-key: ${BREVO_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "sender": {"name": "Conformis – RechteRadar Scanner", "email": "rechteradar@outlook.de"},
    "to": [{"email": "LEAD_EMAIL"}],
    "subject": "BETREFF",
    "htmlContent": "INHALT"
  }'
```

**4. Betreff + Inhalt nach Stage:**

| Stage | Betreff (DE) | Tonalität | CTA |
|-------|-------------|-----------|-----|
| 1 | „Möglicher Compliance-Hinweis für [Firma]" | Hilfsbereit, neugierig machen | Kostenloser Full-Check |
| 2 | „Erinnerung: Offene Compliance-Punkte für [Firma]" | Dringlichkeit erhöhen | Report €29,99 |
| 3 | „Letzte Information: Compliance-Status für [Firma]" | Basic Guard vorstellen | Basic Guard €14,99/Mo |

Stage 1 Teaser-Regel: Bei 1–2 Verstößen KEINEN konkreten Verstoß nennen. Bei 3+ nur EINEN nennen.
NIEMALS alle Verstöße in der Email zeigen.
IMMER Disclaimer: „Keine Rechtsberatung." + Abmelde-Möglichkeit.

**5. Response prüfen + DB aktualisieren:**
```sql
-- Bei Erfolg (messageId in Response):
INSERT INTO email_log (lead_id, email_to, subject, stage, status, sent_at)
VALUES (LEAD_ID, 'EMAIL', 'BETREFF', STAGE, 'sent', NOW());

UPDATE leads SET outreach_stage=STAGE, last_contact_at=NOW(), status='contacted'
WHERE id=LEAD_ID;

-- Bei Bounce:
UPDATE leads SET status='invalid_email' WHERE id=LEAD_ID;
```

**6. Rate Limits:**
- `sleep 1` zwischen jeder Email
- Bei 429: `sleep 10`, einmal retry – NIEMALS gesamten Versand abbrechen

---

## Abschluss
```
[STATUS: WORKFLOW_DONE]
Versendet: X | Stage1: X | Stage2: X | Stage3: X | Bounces: X
```
