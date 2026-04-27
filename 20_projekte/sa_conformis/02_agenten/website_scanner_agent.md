# AGENTS.md – Website-Scanner

Gestartet vom Orchestrator nach [STATUS: LEADS_IDENTIFIED].
Scanne alle Leads mit status='new' auf 9 Compliance-Elemente.
VOLLAUTOMATISCH. Keine Rückfragen.

---
[[agents.md]][[Conformis - RechteRadar]]
## Workflow

**1. Leads laden:**
```sql
SELECT id, url, country FROM leads WHERE status='new' ORDER BY id ASC;
```

**2. Pro Lead: HTTP-Status prüfen:**
```bash
curl -s -o /dev/null -w "%{http_code}" "URL" --max-time 15 --location
```
- 200 → weitermachen
- 403/Timeout → status='blocked', SKIP
- HTTP statt HTTPS → Verstoß notieren, trotzdem weitermachen

**3. HTML laden & 9 Elemente prüfen:**

| # | Element | Prüfung | Pfade |
|---|---------|---------|-------|
| 1 | Impressum | Link + Inhalt (Firma, Adresse, USt-ID) | /impressum, /imprint |
| 2 | Datenschutz | Link + Inhalt (Zweck, Rechtsgrundlage) | /datenschutz, /privacy |
| 3 | Cookie-Banner | Vorhanden + Ablehnen-Button + keine Vorauswahl | Homepage |
| 4 | AGB | Link vorhanden | /agb, /terms |
| 5 | Widerruf | Link + 14-Tage-Frist + Muster-Formular | /widerruf, /returns |
| 6 | ODR-Link | `ec.europa.eu/consumers/odr` in Footer/Impressum | Footer, /impressum |
| 7 | Button-Lösung | „zahlungspflichtig bestellen" o.ä. | Checkout |
| 8 | HTTPS + Headers | SSL aktiv + Strict-Transport-Security | Header-Check |
| 9 | Barrierefreiheit | Statement-Seite vorhanden | /barrierefreiheit |

Prüfung per `curl` + `grep` auf HTML-Quelltext. Kein Browser für Standard-Checks.

**4. Geschäftsmodell erkennen:**
HTML-Inhalt analysieren → Kategorie bestimmen:
`online_shop_*` / `dienstleister_*` / `lokales_geschaeft` / `restaurant_gastro` / etc.

**5. Ergebnis in DB speichern:**
```sql
INSERT INTO scan_results
  (lead_id, url, status, lang, business_model, impressum_found, privacy_found,
   cookie_consent, cookie_reject_button, agb_found, widerruf_found,
   odr_link_found, https_enabled, accessibility_statement, violations, scanned_at)
VALUES (..., NOW());

UPDATE leads SET status='scanned' WHERE id=LEAD_ID;
```

**6. Rate Limit:** `sleep 2` zwischen Leads. Timeout: 15s pro Request.
Bei 429: `sleep 30`, einmal retry.

---

## Abschluss
```
[STATUS: SCAN_COMPLETE]
Gescannt: X | Blockiert: X | Verstöße gefunden: X
```
