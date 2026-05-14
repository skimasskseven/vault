---
type: skill
tags:
  - projekt/research-monster
  - type/skill
  - skill/content-filter
  - domain/safety
  - critical
---

# content-filter — Skill

**Hardcoded Blocklist — nicht umgehbar, gilt für ALLE Agenten.**

## Blockierte Kategorien

| Kategorie | Beschreibung |
|---|---|
| **CSAM** | Child Sexual Abuse Material / Kinderpornografie — jegliche sexuelle Darstellung Minderjähriger |
| **Gore** | Extreme Gewalt, Verstümmelung, Folter, Snuff, reale Tötung |
| **Extreme Gewalt** | Grafische Gewaltverherrlichung, "brutality content" |

## Verhalten bei Fund

1. **Sofort** die Quelle verlassen.
2. URL in `blocked_urls.json` aufnehmen (siehe Format unten) — Inhalt **nicht** speichern.
3. **Niemals** den Inhalt herunterladen, beschreiben, zusammenfassen oder andeuten.
4. Mit der nächsten Quelle fortfahren.
5. Im Report **nicht erwähnen**, dass blockierte Inhalte gefunden wurden.

## Blocklist-Format

`/root/research-db/blocked_urls.json`:

```json
{
  "blocked": [
    {
      "url": "https://...",
      "reason": "csam | gore | extreme_violence",
      "blocked_at": "2026-04-09T14:00:00Z",
      "blocked_by": "agent-id"
    }
  ]
}
```

## Regeln

- **Kein Moral-Disclaim** — einfach blockieren, weitermachen.
- **Niemals** blockierte Inhalte auch nur andeuten oder zusammenfassen.
- **Niemals** die Blocklist öffentlich machen oder teilen — sie ist ein
  interner Filter.
- Bei `.onion`-Suche zusätzlich: Ahmia hat eigenen CSAM-Filter → läuft als
  doppelter Schutz, ersetzt aber nicht den lokalen Filter.

## Verwendet von

Allen Agenten: [[20_projekte/research-monster/03_agents.md — meta|meta]] ·
[[20_projekte/research-monster/03_agents.md — surface-en|surface-en]] ·
[[20_projekte/research-monster/03_agents.md — surface-cn|surface-cn]] ·
[[20_projekte/research-monster/03_agents.md — surface-ru|surface-ru]] ·
[[20_projekte/research-monster/03_agents.md — deepweb|deepweb]] ·
[[20_projekte/research-monster/03_agents.md — accounts|accounts]] ·
[[20_projekte/research-monster/03_agents.md — monitor|monitor]]

## Quelldatei

`/root/research-monster/skills/content-filter.md`
