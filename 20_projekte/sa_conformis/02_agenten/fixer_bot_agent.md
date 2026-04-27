# AGENTS.md – Fixer-Bot

Gestartet vom Orchestrator nach Kauf eines One-Time Fix (€29,99).
Erstelle plattformspezifische Fix-Anleitungen für alle dokumentierten Verstöße.
VOLLAUTOMATISCH. Keine Rückfragen.[[agents.md]][[Conformis - RechteRadar]]

---

## Workflow

**1. Daten laden:**
```sql
SELECT l.id, l.company_name, l.url, l.country,
       cs.violations_json, sr.business_model
FROM leads l
JOIN compliance_scores cs ON cs.lead_id = l.id
JOIN scan_results sr ON sr.lead_id = l.id
WHERE l.id = LEAD_ID;
```

**2. Plattform erkennen:**
```bash
curl -sI "https://LEAD-URL" | grep -iE 'x-powered-by|x-generator'
curl -s "https://LEAD-URL" | grep -iE 'wp-content|cdn.shopify|wix.com|squarespace|webflow'
```

| Signal | Plattform |
|--------|-----------|
| `wp-content` | WordPress |
| `cdn.shopify.com` | Shopify |
| `wix.com` | Wix |
| `squarespace.com` | Squarespace |
| `webflow.io` | Webflow |
| Keine Erkennung | Custom Code |

**3. Fix-Methode: Immer BEIDE anbieten (GUI zuerst):**

**Option A – Zugang erbitten:**

| Plattform | Zugang | Rolle |
|-----------|--------|-------|
| WordPress | Temporary Login Plugin (48h) | Editor |
| Shopify | Staff Account | nur Pages + Themes |
| Wix | Contributor | nur Seiten |
| Custom | FTP/SFTP | minimale Rechte |

**Option B – Selbst umsetzen (GUI + Code):**
Schritt-für-Schritt Anleitung für die erkannte Plattform + fertiger Code-Snippet.

**4. Fix-Code pro Verstoß-Typ:**

**ODR-Link (alle Plattformen):**
```html
<!-- CONFORMIS FIX: ODR-Link (Art. 14 ODR-VO) – in Footer oder Impressum einfügen -->
<p>Online-Streitbeilegung: Die EU-Kommission stellt eine Plattform bereit:
<a href="https://ec.europa.eu/consumers/odr" target="_blank">ec.europa.eu/consumers/odr</a>.
Wir nehmen nicht an Streitbeilegungsverfahren vor Verbraucherschlichtungsstellen teil.</p>
```

**Cookie Ablehnen-Button:**
```html
<!-- CONFORMIS FIX: Ablehnen-Button (TTDSG §25) – zum bestehenden Banner hinzufügen -->
<button onclick="document.cookie='cookies_accepted=false;path=/;max-age=31536000';
  document.getElementById('cookie-banner').style.display='none';"
  style="background:#e74c3c;color:white;padding:8px 16px;border:none;border-radius:4px;cursor:pointer;">
  Alle ablehnen
</button>
```

**Impressum-Ergänzung DE:**
```html
<!-- CONFORMIS FIX: Fehlende Pflichtangaben (DDG §5) – Platzhalter [XXX] anpassen -->
Umsatzsteuer-ID: DE[IHRE UST-ID NR.]
Handelsregister: [AMTSGERICHT] HRB [NUMMER]
```

Code-Regeln: Valides HTML5 | Inline-CSS | aria-Labels | Kommentare bei Platzhaltern | Kein externes CDN.

**5. In DB speichern:**
```sql
INSERT INTO client_customizations
  (lead_id, violation_type, platform, customization_type, new_content, instructions, status, created_at)
VALUES (LEAD_ID, 'odr', 'wordpress', 'html_snippet', 'CODE', 'ANLEITUNG', 'ready', NOW());
```

**6. QA-Signal ausgeben (Orchestrator sendet an Telegram):**
```
QA_NEEDED: Lead LEAD_ID | FIRMENNAME | PLATFORM | Verstöße behoben: X
Bitte Vorher/Nachher prüfen. ✅ = freigeben | ❌ = korrigieren
```
Erst nach QA-Freigabe → Full-Report an Kunden.

---

## Abschluss
```
[STATUS: FIX_COMPLETE]
Fixes: X | Plattform: X | QA ausstehend: ja
```
