# AGENTS.md – Screenshot-Tool

Gestartet vom Orchestrator nach [STATUS: CHECK_COMPLETE].
Erstelle Beweis-Screenshots für jeden dokumentierten Verstoß.
VOLLAUTOMATISCH. Keine Rückfragen.
[[agents.md]][[Conformis - RechteRadar]]

---

## KRITISCH: Nur Shell-Befehle via bash

NIEMALS `browser.screenshot` (eingebautes Tool) verwenden.
IMMER `npx playwright` via bash Shell.

---

## Workflow

**1. Verstöße laden:**
```sql
SELECT cs.lead_id, l.url, cs.violations_json, cs.id as score_id
FROM compliance_scores cs JOIN leads l ON cs.lead_id = l.id
WHERE l.status='scored';
```

**2. Locator pro Verstoß-Typ:**

| Verstoß | CSS-Locator | Ziel-URL |
|---------|-------------|---------|
| `cookie_reject` | `.cookie-banner, #cookie-notice, [role='dialog'], .cc-window` | Homepage |
| `odr` | `footer, .footer, #footer` | /impressum |
| `privacy` | `body` | /datenschutz |
| `impressum` | `main, .content` | /impressum |
| `widerruf` | `main, .content` | /widerruf |
| `https` | `body` | HTTP-Version |

**3. Screenshot erstellen – 3-Stufen-Retry:**

```bash
# Versuch 1: Mit Locator
cd /app && timeout 15 npx playwright screenshot \
  --browser chromium --locator="LOCATOR" --timeout=10000 \
  "URL" "/root/.openclaw/screenshots/LEAD_ID_TYPE_TIMESTAMP.png"

# Versuch 2: Mobile Viewport (375x812)
cd /app && timeout 15 npx playwright screenshot \
  --browser chromium --viewport-size="375,812" --locator="LOCATOR" \
  "URL" "/root/.openclaw/screenshots/LEAD_ID_TYPE_TIMESTAMP_mobile.png"

# Versuch 3: Fallback Vollseite
cd /app && timeout 20 npx playwright screenshot \
  --browser chromium --full-page \
  "URL" "/root/.openclaw/screenshots/LEAD_ID_TYPE_TIMESTAMP_full.png"
```

Alle 3 fehlgeschlagen → Lead als `screenshot_failed`, WEITER.

**4. Dateiname-Schema:**
```
{lead_id}_{violation_type}_{unix_timestamp}.png
Beispiel: 42_odr_1745654321.png
```

**5. In DB speichern:**
```sql
INSERT INTO screenshots (lead_id, score_id, violation_type, file_path, status, created_at, expires_at)
VALUES (LEAD_ID, SCORE_ID, 'odr', '/root/.openclaw/screenshots/...', 'complete', NOW(), NOW() + INTERVAL '30 days');

UPDATE leads SET status='ready_for_outreach' WHERE id=LEAD_ID;
```

**Playwright prüfen falls Fehler:**
```bash
cd /app && npx playwright screenshot --browser chromium "https://example.com" /tmp/test.png && echo "OK"
```

---

## Abschluss
```
[STATUS: SCREENSHOTS_COMPLETE]
Erstellt: X | Fehlgeschlagen: X | Pfad: /root/.openclaw/screenshots/
```
