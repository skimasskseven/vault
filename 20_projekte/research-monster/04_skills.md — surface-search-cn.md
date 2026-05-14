---
type: skill
tags:
  - projekt/research-monster
  - type/skill
  - skill/surface-search-cn
  - domain/surface-search
  - lang/cn
---

# surface-search-cn — Skill

Surface-Web-Suche für chinesische Quellen. Wird genutzt von
[[20_projekte/research-monster/03_agents.md — surface-cn|surface-cn]].

## Suchmaschinen

### Baidu

- URL: `https://www.baidu.com/s?wd=QUERY` (Query URL-encoded!)
- Zugriff: `browser`

### Sogou

- URL: `https://www.sogou.com/web?query=QUERY`
- Zugriff: `browser` — indexiert auch WeChat-Artikel

### Bing CN

- URL: `https://cn.bing.com/search?q=QUERY`
- Zugriff: `browser`

## Workflow

```
1. Query ins vereinfachte Chinesisch übersetzen.
2. Englische Fachbegriffe und Tech-Termini beibehalten.
3. Baidu, Sogou, Bing CN parallel.
4. Treffer extrahieren, deduplizieren, scoren.
5. JSON zurückgeben.
```

## Quellen-Eigenheiten

- **Baidu** zeigt eigene Inhalte (Baike, Zhidao) — valide.
- **Sogou** indexiert WeChat → exklusive Quelle für CN-Insights.
- Zensierte Topics: politische / gesellschaftliche Begriffe oft gefiltert →
  fehlende Treffer als Zensur-Signal werten.
- Taiwan / HK-Quellen (`.tw`, `.hk`) für unzensierte Perspektive einbeziehen.

## Scraping-Snippets

```bash
# Baidu (Query URL-encoded)
curl -s "https://www.baidu.com/s?wd=$(python3 -c 'import urllib.parse; print(urllib.parse.quote("中文查询"))')" \
  | grep -oP 'class="c-showurl".*?href="\K[^"]+'

# Sogou
curl -s "https://www.sogou.com/web?query=QUERY" \
  | grep -oP 'class="text-label".*?'
```

## Quelldatei

`/root/research-monster/skills/surface-search-cn.md`
