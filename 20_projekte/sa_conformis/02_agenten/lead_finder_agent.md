# AGENTS.md – Lead-Finder

Gestartet vom Orchestrator. Finde 50 Firmen mit eigenen Websites und potenziellen Compliance-Lücken.
VOLLAUTOMATISCH. Keine Rückfragen.
[[agents.md]][[Conformis - RechteRadar]]

---

## KRITISCH: Nur HTTP-Tool – NIEMALS Browser/Web Fetch

Alle Register-Abfragen laufen ausschließlich über direkte HTTP-Calls (curl/fetch).
Kein Playwright, kein Chromium für APIs.

---

## Workflow

**1. Quota prüfen:**
```sql
SELECT COUNT(*) FROM leads WHERE DATE(created_at) = CURRENT_DATE;
```
≥ 50 → sofort [STATUS: LEADS_IDENTIFIED]. Sonst: Restquota berechnen.

**2. Leads aus Registern holen (Verteilung: DE 20 / CH 20 / UK 10):**

| Land | Endpoint | Auth |
|------|----------|------|
| DE | `GET https://search.dip.bundestag.de/api/v1/vorgang?apikey=${HANDELSREGISTER_API_KEY}&format=json&rows=20` | API-Key |
| CH | `POST https://www.zefix.admin.ch/ZefixPublicREST/api/v1/firm/search.json` Body: `{"name":"","maxEntries":20,"activeOnly":true}` | Öffentlich |
| UK | `GET https://api.company-information.service.gov.uk/search/companies?q=online+shop&items_per_page=10` | Basic Auth: `${COMPANIES_HOUSE_API_KEY}:` |
| Fallback | Google Places: `https://maps.googleapis.com/maps/api/place/textsearch/json?query=Online+Shop&key=${GOOGLE_PLACES_API_KEY}` | API-Key |

**3. Email finden:**
Impressum → /kontakt → /contact der gefundenen Website parsen.
Kein Email gefunden → Lead SKIP.

**4. Qualitäts-Filter:**
- Website erreichbar (HTTP 200)? Sonst SKIP.
- Eigene Domain (kein ebay/amazon/etsy/instagram)? Sonst SKIP.
- Bereits in DB? (`SELECT id FROM leads WHERE url='...'`) Sonst SKIP.

**5. In DB speichern:**
```sql
INSERT INTO leads (company_name, url, email, country, source, status, created_at)
VALUES ('NAME', 'URL', 'EMAIL', 'DE', 'handelsregister', 'new', NOW())
ON CONFLICT (url) DO NOTHING;
```

**6. Rate Limits einhalten:**
- 1 Req/Sek bei APIs (`sleep 1`)
- 1 Req/3 Sek bei Website-Scraping (`sleep 3`)
- Timeout: 15s pro Request
- Bei 429: `sleep 30`, einmal retry

---

## Abschluss
```
[STATUS: LEADS_IDENTIFIED]
Gefunden: X | DE: X | CH: X | UK: X | Gespeichert: X | Duplikate: X
```
