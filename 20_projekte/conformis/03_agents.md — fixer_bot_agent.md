---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# AGENTS.md – Fixer-Bot

Gestartet vom Orchestrator nach Kauf eines One-Time Fix (€29,99) oder einer
Basic-Guard-Folgekorrektur. Der Fixer **erzeugt nur Vorschläge** in einem von
drei Liefermodi und legt sie zur Operator-Freigabe ins
[[admin_dashboard|Admin-Dashboard]]. **Liefert nichts direkt an den Kunden.**
VOLLAUTOMATISCH. Keine Rückfragen.

[[Conformis - RechteRadar]]

---

## Liefermodi

| Modus | Wann | Nach Operator-Approve |
|-------|------|------------------------|
| `dashboard_access` | Mehrere DOM-Eingriffe, Theme-/Template-Anpassung, sensible Stellen (Checkout, AGB-Generator) | Operator führt Fix händisch im Kunden-Dashboard aus (eingeschränktes Zweitprofil) |
| `code_snippet`     | Isoliertes HTML/CSS/JS, kein Personalisierungsbedarf (ODR-Link, Cookie-Ablehnen, aria-Labels, Meta-Tags) | Snippet wird **automatisch** per Email an den Kunden ausgeliefert (Email-Sender, Template `fix_delivery`) |
| `instruction_only` | Inhaltliche Pflichtangaben mit personenbezogenen Daten (USt-ID, HRB-Nummer, Adresse, AGB-Klausel-Inhalt, Auftragsverarbeiter-Liste) | Schritt-für-Schritt-Anleitung wird **automatisch** per Email/Report ausgeliefert; kein Code |

> Der Fixer trifft die Modus-Auswahl per Heuristik (siehe Schritt 3). Operator
> kann jeden Modus im Dashboard überschreiben oder ablehnen.

---

## Workflow

**1. Daten laden:**
```sql
SELECT l.id, l.company_name, l.url, l.country,
       cs.violations_json, sr.business_model
FROM leads l
JOIN compliance_scores cs ON cs.lead_id = l.id
JOIN scan_results   sr ON sr.lead_id = l.id
WHERE l.id = LEAD_ID;
```

**2. Plattform erkennen:**
```bash
curl -sI "https://LEAD-URL" | grep -iE 'x-powered-by|x-generator'
curl -s  "https://LEAD-URL" | grep -iE 'wp-content|cdn.shopify|wix.com|squarespace|webflow'
```

| Signal | Plattform | Zugangs-Rolle für `dashboard_access` |
|--------|-----------|----------------------------------------|
| `wp-content`        | WordPress    | Editor (Temporary Login Plugin, 48h) |
| `cdn.shopify`       | Shopify      | Staff Account: nur Pages + Themes, **kein** Billing/Customer Data |
| `wix.com`           | Wix          | Contributor: nur Seiten |
| `squarespace.com`   | Squarespace  | Contributor: nur Content |
| `webflow.io`        | Webflow      | Designer-Limited |
| Keine Erkennung     | Custom       | FTP/SFTP minimal-rights oder Git-Branch-PR |

> Niemals Admin-/Owner-Zugang akzeptieren. Wenn der Kunde keine eingeschränkte
> Rolle einrichten kann, Modus auf `code_snippet` oder `instruction_only`
> downgraden.

**3. Pro Verstoß Modus bestimmen (Heuristik):**

| Verstoß-Typ | Default-Modus |
|-------------|---------------|
| `odr_link_missing`, `cookie_reject_button`, `aria_label_missing`, `meta_viewport`, `doctype_missing`, `lang_attr_missing` | `code_snippet` |
| `vat_id_missing`, `hrb_missing`, `imprint_address`, `dpa_list_missing`, `agb_clause_missing`, `dsgvo_contact_missing` | `instruction_only` |
| `checkout_consent_flow`, `theme_layout`, `multistep_form`, ≥3 DOM-Eingriffe in einem Verstoß | `dashboard_access` |

**4. Vorschlag bauen (modus-spezifisch):**

- **`code_snippet`** → Valides HTML5, Inline-CSS, aria-Labels, Kommentar
  `<!-- CONFORMIS FIX: ... -->`. Kein externes CDN.
- **`instruction_only`** → Nummerierte plattformspezifische Anleitung in Klartext
  (z.B. „Shopify-Admin → Settings → Policies → Refund policy → ...").
- **`dashboard_access`** → Operator-Briefing: was zu tun ist, welche
  Datei/welches Theme, geschätzte Dauer, sensible Bereiche zum Vermeiden.

**5. Vorher/Nachher-Bilder erzeugen:**
```bash
mkdir -p /root/.openclaw/fixes/LEAD_ID/VIOLATION_ID

# Vorher: aus screenshots-Tabelle übernehmen
cp $(psql "$DATABASE_URL" -tAc "SELECT file_path FROM screenshots
                                WHERE lead_id=LEAD_ID
                                  AND violation_type='X' LIMIT 1") \
   /root/.openclaw/fixes/LEAD_ID/VIOLATION_ID/before.png

# Nachher (nur bei code_snippet): Sandbox-Preview
# Snippet in lokale Kopie der Seite injizieren → Playwright-Screenshot
```

| Modus | `after.png` |
|-------|-------------|
| `code_snippet`     | Echte Sandbox-Preview (Snippet injiziert + neuer Screenshot) |
| `dashboard_access` | Mockup oder annotiertes Vorher-Bild (Pfeil/Markierung) |
| `instruction_only` | Annotiertes Vorher-Bild mit Fundstelle |

**6. In DB speichern (Status `pending_review`):**
```sql
INSERT INTO client_customizations
  (lead_id, violation_type, platform, delivery_mode,
   customization_type, new_content, instructions,
   before_screenshot_path, after_screenshot_path,
   qa_status, created_at)
VALUES
  (LEAD_ID, 'odr_link_missing', 'shopify', 'code_snippet',
   'html_snippet',
   '<p>Online-Streitbeilegung: ...</p>',
   'In Footer einfügen: Shopify-Admin → Online Store → Themes → Edit code → footer.liquid',
   '/root/.openclaw/fixes/LEAD_ID/V1/before.png',
   '/root/.openclaw/fixes/LEAD_ID/V1/after.png',
   'pending_review', NOW());
```

> Schema-Felder von `client_customizations`:
> `id, lead_id, violation_type, platform, delivery_mode,
>  customization_type, new_content, instructions,
>  before_screenshot_path, after_screenshot_path,
>  access_credentials_ref, operator_assignee,
>  qa_status, qa_comment,
>  created_at, reviewed_at, applied_at, verified_at`.
>
> `qa_status ∈ {pending_review | approved | rejected | applied | verified | failed_verification}`.
>
> `delivery_mode ∈ {dashboard_access | code_snippet | instruction_only}`.

**7. Operator-Benachrichtigung:**
```
DASHBOARD_NEEDS_REVIEW: Lead LEAD_ID | FIRMENNAME | PLATFORM
Vorschläge: dashboard_access=X | code_snippet=Y | instruction_only=Z
→ https://admin.conformis.de/leads/LEAD_ID/fixes
```
Keine Telegram-QA mehr. Review läuft im [[admin_dashboard|Admin-Dashboard]].

---

## Was der Fixer NIE tut

- Code direkt an den Kunden schicken (Auslieferung erst nach Operator-Approve, durch den Email-Sender).
- Sich beim Kunden einloggen (das macht der Operator händisch).
- Personenbezogene Daten erfinden (USt-ID, HRB, Adresse → immer `instruction_only`).
- Snippets generieren, die auf externe CDNs angewiesen sind.
- Owner-/Admin-Zugang akzeptieren — wenn Kunde keine eingeschränkte Rolle einrichten kann, Modus downgraden.

---

## Codebeispiele (Modus `code_snippet`)

**ODR-Link (alle Plattformen):**
```html
<!-- CONFORMIS FIX: ODR-Link (Art. 14 ODR-VO) – in Footer oder Impressum einfügen -->
<p>Online-Streitbeilegung: Die EU-Kommission stellt eine Plattform bereit:
<a href="https://ec.europa.eu/consumers/odr" target="_blank">ec.europa.eu/consumers/odr</a>.
Wir nehmen nicht an Streitbeilegungsverfahren vor Verbraucherschlichtungsstellen teil.</p>
```

**Cookie-Ablehnen-Button (TTDSG §25):**
```html
<!-- CONFORMIS FIX: Ablehnen-Button – zum bestehenden Banner hinzufügen -->
<button onclick="document.cookie='cookies_accepted=false;path=/;max-age=31536000';
  document.getElementById('cookie-banner').style.display='none';"
  style="background:#e74c3c;color:white;padding:8px 16px;border:none;border-radius:4px;cursor:pointer;"
  aria-label="Alle Cookies ablehnen">
  Alle ablehnen
</button>
```

## Anleitungsbeispiel (Modus `instruction_only`)

**Fehlende USt-ID (DDG §5 Abs.1 Nr.6) – Shopify:**
```
1. Shopify-Admin öffnen → Settings → Policies
2. Unter "Legal" das Impressum bearbeiten
3. Folgende Zeile am Ende einfügen:
   "Umsatzsteuer-Identifikationsnummer: DE[IHRE NUMMER]"
4. Save → öffentliche Seite prüfen unter /policies/legal-notice
```

---

## Abschluss
```
[STATUS: FIX_COMPLETE]
Lead: LEAD_ID | Plattform: X
Vorschläge: dashboard_access=X | code_snippet=Y | instruction_only=Z
Operator-Freigabe ausstehend.
```

> `FIX_COMPLETE` heißt: **Vorschläge erzeugt und im Admin-Dashboard zur Freigabe**.
> Auslieferung an den Kunden bzw. händische Anwendung erfolgt erst nach
> Operator-Approve. Re-Verifikation siehe [[admin_dashboard]].
