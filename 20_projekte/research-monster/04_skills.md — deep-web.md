---
type: skill
tags:
  - projekt/research-monster
  - type/skill
  - skill/deep-web
  - domain/deep-web
  - domain/osint
---

# deep-web — Skill

Aggregierte Deep-Web-Funktionen: Archive, Academic, Infrastruktur, Gov-Daten,
Tor. Wird primär von [[20_projekte/research-monster/03_agents.md — deepweb|deepweb]] genutzt.

## 1. Archive & Historie

### Archive.org / Wayback Machine

```bash
# Verfügbarkeit prüfen
curl -s "http://archive.org/wayback/available?url=example.com"

# Snapshot direkt laden
curl -s "https://web.archive.org/web/2024/https://example.com"

# Alle Snapshots (CDX API)
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&fl=timestamp,original,statuscode&limit=20"
```

### Google Scholar

- URL: `https://scholar.google.com/scholar?q=QUERY`
- Zugriff: `browser` Tool

### Semantic Scholar (API)

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=QUERY&limit=10&fields=title,authors,year,abstract,citationCount,url"
```

### arXiv (API)

```bash
curl -s "http://export.arxiv.org/api/query?search_query=QUERY&max_results=10"
```

## 2. Infrastruktur

### Shodan (API-Key)

```bash
curl -s "https://api.shodan.io/shodan/host/IP?key=SHODAN_API_KEY"
curl -s "https://api.shodan.io/shodan/host/search?key=SHODAN_API_KEY&query=QUERY"
```

### Censys (API-Key)

```bash
curl -s "https://search.censys.io/api/v2/hosts/search?q=QUERY" \
  -u "API_ID:API_SECRET"
```

### WHOIS

```bash
whois example.com
# Oder API:
curl -s "https://whois-api.domaintools.com/v1/example.com/whois/?api_key=KEY"
```

### DNS-Records

```bash
dig example.com ANY +short
dig example.com MX  +short
dig example.com TXT +short
dig example.com NS  +short
```

## 3. Government & Open Data

| Quelle | URL | Zugriff |
|---|---|---|
| US Gov Data | https://data.gov | `browser` |
| DE Gov Data | https://govdata.de | `browser` |
| EU Open Data | https://data.europa.eu | `browser` |
| SEC EDGAR | https://sec.gov/cgi-bin/browse-edgar | `browser` + API |
| USPTO Patents | https://ppubs.uspto.gov | `browser` |
| EPO Patents | https://worldwide.espacenet.com | `browser` |
| CourtListener | https://www.courtlistener.com | `browser` |
| ClinicalTrials | https://clinicaltrials.gov | `browser` |

## 4. Tor / .onion

Voraussetzung: Tor SOCKS5 auf `localhost:9050`. Details:
[[20_projekte/research-monster/04_skills.md — tor-onion-search|tor-onion-search]].

```bash
curl --socks5-hostname 127.0.0.1:9050 \
  "https://ahmia.fi/search/?q=QUERY"

curl --socks5-hostname 127.0.0.1:9050 \
  "http://example.onion"
```

## Relevanz-Scoring

| Score | Bedeutung |
|---|---|
| 90–100 | Exakt, autoritativ |
| 70–89 | Gute Übereinstimmung |
| 40–69 | Ergänzend |
| <40 | Verwerfen |

## Content Filter

[[20_projekte/research-monster/04_skills.md — content-filter|content-filter]] —
bei Fund Quelle verlassen, URL blockieren.

## Quelldatei

`/root/research-monster/skills/deep-web.md`
