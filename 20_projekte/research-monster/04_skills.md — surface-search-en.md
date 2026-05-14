---
type: skill
tags:
  - projekt/research-monster
  - type/skill
  - skill/surface-search-en
  - domain/surface-search
  - lang/en
  - lang/de
---

# surface-search-en — Skill

Surface-Web-Suche für EN/DE. Wird genutzt von
[[20_projekte/research-monster/03_agents.md — surface-en|surface-en]].

## Suchmaschinen

### Google (primary)

- Zugriff: `web_search` Tool des OpenClaw-Agents
- Sprache: EN + DE

### Bing

- EN: `https://www.bing.com/search?q=QUERY&cc=us&setlang=en`
- DE: `https://www.bing.com/search?q=QUERY&cc=de&setlang=de`
- Zugriff: `browser` Tool oder `exec` mit curl + HTML-Parsing

### DuckDuckGo

- Standard: `https://duckduckgo.com/?q=QUERY`
- Lite (besser scrapebar): `https://lite.duckduckgo.com/lite/?q=QUERY`
- Zugriff: `browser`

### Brave Search

- URL: `https://search.brave.com/search?q=QUERY`
- Zugriff: `browser`

## Workflow

```
1. Query in EN und DE übersetzen (falls nicht schon EN/DE).
2. web_search Tool für Google.
3. Parallel: Bing, DuckDuckGo, Brave via browser/curl.
4. Extrahieren: Titel, URL, Snippet.
5. Dedup (gleiche Domain oder >80% Content-Overlap).
6. Relevanz scoren (0–100).
7. JSON zurückgeben.
```

## Scraping-Snippets

```bash
# DuckDuckGo Lite
curl -s "https://lite.duckduckgo.com/lite/" \
  --data-urlencode "q=QUERY" \
  | grep -oP 'class="result__a".*?href="\K[^"]+'

# Bing
curl -s "https://www.bing.com/search?q=QUERY" \
  | grep -oP 'cite">.*?</cite'
```

## Scoring

| Score | Kriterium |
|---|---|
| 90–100 | Exakter Keyword-Match, aktuelle Quelle, autoritativ |
| 70–89 | Gute Übereinstimmung |
| 40–69 | Teilweise relevant |
| <40 | Verwerfen |

## Quelldatei

`/root/research-monster/skills/surface-search-en.md`
