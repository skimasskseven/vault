---
type: skill
tags:
  - projekt/research-monster
  - type/skill
  - skill/report-generator
  - domain/reporting
---

# report-generator — Skill

Aggregiert Ergebnisse aller Agenten, dedupliziert, scored, und gibt einen
kohärenten Markdown- + JSON-Report aus. Wird ausgeführt von
[[20_projekte/research-monster/03_agents.md — meta|meta]].

## Deduplizierung

- Gleiche URL → Duplikat (entfernen).
- Gleiche Domain **und** Titel-Similarity > 80 % → Duplikat.
- **Andere Sprache → KEIN Duplikat** (gleiche Info in anderer Sprache ist
  wertvoll).

## Scoring (0–100)

Pro Treffer kombiniert aus:

- **Keyword-Match** — wie viele Query-Keywords in Titel/Snippet?
- **Autorität** — ist die Quelle vertrauenswürdig?
- **Aktualität** — wie neu ist die Information?
- **Relevanz** — beantwortet sie direkt die Query?

| Score | Bedeutung |
|---|---|
| 90–100 | Exakter Match, autoritativ |
| 70–89 | Relevant |
| 40–69 | Ergänzend |
| <40 | Wird verworfen |

## Markdown-Output

```markdown
# Research Report: [Thema]

## Query
[Original Query]

## Zusammenfassung
[2–3 Sätze, die die wichtigsten Findings zusammenfassen]

## Top-Ergebnisse (Score 70+)
| # | Titel | Quelle | Sprache | Score |
|---|-------|--------|---------|-------|
| 1 | ...   | ...    | EN      | 95    |
| 2 | ...   | ...    | CN      | 88    |

## Alle Ergebnisse (Score 40–69)
| # | Titel | Quelle | Sprache | Score |
|---|-------|--------|---------|-------|
| 1 | ...   | ...    | RU      | 55    |

## Deep Findings
[Wenn deepweb-Agent Treffer hatte]

## Quellen nach Sprache
- EN: X
- CN: X
- RU: X

## Datenbasis
- Insgesamt gescrapte Quellen: X
- Unique Ergebnisse: X
- Blockierte URLs: X
- Suchmaschinen verwendet: ...
- Tor verwendet: Ja/Nein
- Zeitstempel: ISO-8601
```

## JSON-Output (SQLite-Persistierung)

```json
{
  "query": "...",
  "query_type": "...",
  "timestamp": "ISO-8601",
  "agents_used": ["surface-en", "deepweb"],
  "languages": ["en", "cn"],
  "total_sources_scraped": 45,
  "unique_results": 30,
  "results_by_score": {
    "high": 10,
    "medium": 15,
    "low": 5
  },
  "tor_used": false,
  "urls_blocked": 0,
  "findings": [
    {
      "title": "...",
      "url": "...",
      "language": "en",
      "score": 95,
      "source_agent": "surface-en",
      "source_engine": "google"
    }
  ]
}
```

## Konsumenten

- [[20_projekte/research-monster/03_agents.md — meta|meta]] — final synthesis
- SQLite-DB `/root/research-monster/db/research.db` — Persistierung

## Quelldatei

`/root/research-monster/skills/report-generator.md`
