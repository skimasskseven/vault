---
tags: [feature, gamification, database, projekt/running_app]
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# Feature: Scoreboard & Leaderboard

## Daten-Aggregat
- Abfrage der `runs` Tabelle.
- Filterung nach Zeitraum: Woche, Monat, Jahr.
- SQL-Logik: `SUM(distance) GROUP BY user_id`.

## UI-Elemente
- Top 3 Ansicht mit Gold/Silber/Bronze Icons.
- "Du"-Hervorhebung (Sticky-Leiste unten, falls man nicht in den Top 5 ist).
- Klick auf einen Nutzer öffnet dessen [[User_Profile]].
