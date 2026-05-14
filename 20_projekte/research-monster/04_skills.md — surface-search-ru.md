---
type: skill
tags:
  - projekt/research-monster
  - type/skill
  - skill/surface-search-ru
  - domain/surface-search
  - lang/ru
---

# surface-search-ru — Skill

Surface-Web-Suche für den russischsprachigen Raum. Wird genutzt von
[[20_projekte/research-monster/03_agents.md — surface-ru|surface-ru]].

## Suchmaschinen

### Yandex

- RU: `https://yandex.ru/search/?text=QUERY`
- Intl: `https://yandex.com/search/?text=QUERY`
- Zugriff: `browser`

### Bing RU

- URL: `https://www.bing.com/search?q=QUERY&cc=ru&setlang=ru`
- Zugriff: `browser`

### Mail.ru

- URL: `https://go.mail.ru/search?q=QUERY`
- Zugriff: `browser`

## Workflow

```
1. Query ins Russische übersetzen.
2. Englische Fachbegriffe beibehalten.
3. Yandex, Bing RU, Mail.ru parallel.
4. Treffer extrahieren, deduplizieren, scoren.
5. JSON zurückgeben.
```

## Quellen-Eigenheiten

- **Yandex** ist die mit Abstand beste RU-Suchmaschine — auch bessere
  Bildersuche als Google für RU-Inhalte.
- Domain-Priorität: `.ru`, `.su`, `.рф`.
- Bei Relevanz: `.ua`, `.by`, `.kz` einbeziehen.

## Scraping-Snippets

```bash
# Yandex
curl -s "https://yandex.ru/search/?text=QUERY" \
  | grep -oP 'class="OrganicTitle-Link".*?href="\K[^"]+'

# Mail.ru
curl -s "https://go.mail.ru/search?q=QUERY" \
  | grep -oP 'class="results__link".*?href="\K[^"]+'
```

## Quelldatei

`/root/research-monster/skills/surface-search-ru.md`
