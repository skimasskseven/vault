---
type: skill
tags:
  - projekt/research-monster
  - type/skill
  - skill/tor-onion-search
  - domain/tor
  - domain/deep-web
---

# tor-onion-search — Skill

Tor-Bridge-basierte Suche im Dark Web (.onion). Wird genutzt von
[[20_projekte/research-monster/03_agents.md — deepweb|deepweb]].

## Tor-Bridge

- SOCKS5 Proxy: `socks5://127.0.0.1:9050`
- Läuft im Container über `tor -f /etc/tor/torrc` (Bind-Mount `./tor`)
- **Kein Exit-Node** — ausschließlich Client-Bridge zum .onion-Netzwerk

## Dark-Web-Suchmaschinen

### Ahmia.fi (empfohlen)

- Clearnet: `https://ahmia.fi/search/?q=QUERY`
- Tor: `http://juhanahhfdn4o5lq.onion/search/?q=QUERY`
- Bester Index, filtert CSAM automatisch (zusätzlicher Schutz).

### Torch

- Tor: `http://xmh57jrzrnw6insl.onion/`
- Query: `http://xmh57jrzrnw6insl.onion/search?query=QUERY`
- Größter .onion-Index.

### Haystack

- Tor: `http://haystak5njsmn2hq.onion/`
- Fallback wenn Torch nichts liefert.

## Workflow

```
1. Tor-Verbindung prüfen:
   curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org
2. Ahmia (primary).
3. Torch als Fallback.
4. Ergebnisse extrahieren.
5. Content Filter anwenden.
6. JSON zurückgeben.
```

## Befehle

```bash
# Tor-Check
curl --socks5-hostname 127.0.0.1:9050 \
  "https://check.torproject.org/api/ip"

# Ahmia Search via Tor
curl --socks5-hostname 127.0.0.1:9050 \
  "https://ahmia.fi/search/?q=QUERY" \
  | grep -oP 'class="result".*?'

# .onion direkt
curl --socks5-hostname 127.0.0.1:9050 \
  "http://example.onion"
```

## Content Filter

[[20_projekte/research-monster/04_skills.md — content-filter|content-filter]].
Ahmia filtert CSAM bereits — zusätzlicher Schutz durch eigenen Filter.

## Quelldatei

`/root/research-monster/skills/tor-onion-search.md`
