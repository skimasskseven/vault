# AGENTS.md – Law-Monitor

Gestartet vom Orchestrator jeden Montag 04:00 Uhr.
Prüfe alle Regierungsquellen auf neue/geänderte E-Commerce-Gesetze.
VOLLAUTOMATISCH. Keine Rückfragen.
[[agents.md]][[Conformis - RechteRadar]]

---

## Workflow

**1. Bestehende Texte aus DB laden:**
```sql
SELECT regulation_id, name, jurisdiction, checksum FROM law_texts ORDER BY jurisdiction;
```

**2. APIs abfragen (Rate Limit: 1 Req/3 Sek, Timeout: 20s):**

| Quelle | Endpoint | Keywords filtern |
|--------|----------|-----------------|
| 🇪🇺 EU | `https://publications.europa.eu/webapi/rdf/sparql` (SPARQL) | E-Commerce, Datenschutz, Cookie |
| 🇩🇪 DE | `https://search.dip.bundestag.de/api/v1/vorgang?apikey=${HANDELSREGISTER_API_KEY}&format=json&rows=20&sort=datum_desc` | Verbraucherschutz, Impressum, Barrierefreiheit |
| 🇬🇧 UK | `https://www.legislation.gov.uk/new/data.feed` (Atom) | Consumer, Privacy, Accessibility |
| 🇨🇭 CH | `https://www.fedlex.admin.ch/de/official-gazette` | Datenschutz, E-Commerce |
| 🇺🇸 US | `https://www.federalregister.gov/api/v1/documents.json?conditions[term]=e-commerce+privacy+consumer` | Privacy, Consumer |

Bei 429: `sleep 10`, einmal retry.

**3. Neue Gesetze in DB speichern:**
```sql
INSERT INTO upcoming_laws (name, jurisdiction, status, source_url, expected_effective, keywords_matched, created_at)
VALUES ('TITEL', 'DE', 'draft', 'URL', 'DATUM', '{E-Commerce}', NOW())
ON CONFLICT DO NOTHING;
```

**4. Bestehende Texte prüfen:**
Checksum (MD5 aus Titel+Datum) mit DB vergleichen.
Bei Änderung → `UPDATE law_texts SET full_text=..., checksum=..., last_updated=NOW()`.

**5. Bei neuem `approved`-Gesetz mit E-Commerce-Bezug:**
Orchestrator-Alert ausgeben:
```
ORCHESTRATOR_ALERT: Neues Gesetz approved – [NAME] ([JURISDICTION]) – alle Leads neu scannen empfohlen.
```

---

## Abschluss
```
[STATUS: MONITOR_COMPLETE]
Quellen: EU, DE, UK, CH, US | Neu (draft): X | Neu (approved): X | Texte aktualisiert: X
```
