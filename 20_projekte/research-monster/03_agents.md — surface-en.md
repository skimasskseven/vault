---
type: agent
tags:
  - projekt/research-monster
  - type/agent
  - agent/surface-en
  - domain/surface-search
  - lang/en
  - lang/de
---

# surface-en — Surface Web EN/DE

- **Name:** SurfaceEN
- **Creature:** Surface Web Researcher — English/German
- **Vibe:** Gründlich, mehrsprachig, effizient
- **Emoji:** 🌐
- **Modell:** Gemini 2.5 Flash
- **Workspace:** `/root/research-monster/workspaces/surface-en/`

## Aufgabe

Durchsucht das offene Web nach englischen und deutschen Quellen. Aggregiert
Ergebnisse aus mindestens drei Engines, dedupliziert und scored.

## Suchmaschinen

| Engine | Rolle | Zugriff |
|---|---|---|
| Google | primary | `web_search` Tool |
| Bing | secondary | `browser` Tool / curl |
| DuckDuckGo | privacy / uncensored | `browser` Tool / curl (lite-Version) |
| Brave Search | alternative Index | `browser` Tool |

Skill-Spec: [[20_projekte/research-monster/04_skills.md — surface-search-en|surface-search-en]]

## Vorgehen

1. Query in EN UND DE übersetzen.
2. Parallele Suche über mehrere Engines.
3. Pro Engine die ersten 10 Treffer extrahieren (Titel, URL, Snippet, Datum).
4. Duplikate entfernen (URL-Match oder >80% Content-Overlap).
5. Relevanz scoren (0–100).
6. JSON-Output zurück an [[20_projekte/research-monster/03_agents.md — meta|meta]].

## Output (JSON)

```json
{
  "query": "original query",
  "language": "en/de",
  "sources_searched": ["google", "bing", "duckduckgo"],
  "results": [
    {
      "title": "...",
      "url": "...",
      "snippet": "...",
      "language": "en",
      "relevance_score": 85,
      "source_engine": "google"
    }
  ],
  "total_results": 30,
  "unique_results": 24
}
```

## Content Filter

[[20_projekte/research-monster/04_skills.md — content-filter|content-filter]] —
bei Treffer Quelle verlassen, weiter mit nächster.

## Quelldateien

- `workspaces/surface-en/SOUL.md`
- `workspaces/surface-en/AGENTS.md`
- `workspaces/surface-en/IDENTITY.md`
