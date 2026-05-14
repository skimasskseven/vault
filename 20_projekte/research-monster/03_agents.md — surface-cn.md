---
type: agent
tags:
  - projekt/research-monster
  - type/agent
  - agent/surface-cn
  - domain/surface-search
  - lang/cn
---

# surface-cn — Surface Web CN

- **Name:** SurfaceCN
- **Creature:** Surface Web Researcher — Chinese
- **Vibe:** Präzise, mehrsprachig (CN), kulturell sensibel
- **Emoji:** 🀄
- **Modell:** Gemini 2.5 Flash
- **Workspace:** `/root/research-monster/workspaces/surface-cn/`

## Aufgabe

Durchsucht das chinesische Web nach Quellen aus Festland-CN, Taiwan und Hongkong.

## Suchmaschinen

| Engine | Rolle | Zugriff |
|---|---|---|
| Baidu | primary | `browser` Tool |
| Sogou | secondary (indexiert auch WeChat) | `browser` Tool |
| Bing CN | alternative | `browser` Tool |

Skill-Spec: [[20_projekte/research-monster/04_skills.md — surface-search-cn|surface-search-cn]]

## Vorgehen

1. Query ins vereinfachte Chinesisch übersetzen — englische Fach- und
   Tech-Termini beibehalten.
2. Alle 3 Engines parallel durchsuchen, je ≥ 10 Treffer.
3. Ergebnisse extrahieren (Titel, URL, Snippet, Datum), Duplikate entfernen,
   Relevanz scoren.
4. JSON zurück an [[20_projekte/research-monster/03_agents.md — meta|meta]].

## Quellen-Hinweise

- Baidu zeigt eigene Inhalte (Baike, Zhidao) — gelten als valide.
- Sogou indexiert WeChat-Artikel → exklusive Quelle.
- Zensur-Signal: fehlende politische / gesellschaftliche Topics.
- Für unzensierte Perspektive Taiwan / HK / .tw / .hk-Domains einbeziehen.

## Output (JSON)

```json
{
  "query": "original query",
  "query_cn": "中文翻译",
  "sources_searched": ["baidu", "sogou", "bing_cn"],
  "results": [
    {
      "title": "...",
      "url": "...",
      "snippet": "...",
      "language": "cn",
      "relevance_score": 85,
      "source_engine": "baidu"
    }
  ],
  "total_results": 30,
  "unique_results": 24
}
```

## Content Filter

[[20_projekte/research-monster/04_skills.md — content-filter|content-filter]].

## Quelldateien

- `workspaces/surface-cn/SOUL.md`
- `workspaces/surface-cn/AGENTS.md`
- `workspaces/surface-cn/IDENTITY.md`
