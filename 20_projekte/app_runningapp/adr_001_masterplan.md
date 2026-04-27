---
tags:
  - architecture
  - adr
  - run-together
  - masterplan
Aktualisierung: "[[ADR-002 Aktualisierung]]"
---
# ADR-001: Masterplan Run Together

Dies ist das Hauptdokument für die Entwicklung der "Run Together" App. Von hier aus verzweigen alle technischen Spezifikationen.

## Kern-Architektur
- **Frontend:** Flutter
- **3D-Engine:** Unity (Ready Player Me SDK)
- **Karte:** Mapbox GL
- **Backend:** 
- **Deployment:** Codemagic (Cloud-Build für iOS/Android)

## Struktur der App
- [[Interaktive_Karte]]: Das Herzstück mit 3D-Overlay.
- [[User_Profile]]: Persönliche Statistiken und 3D-Vorschau.
- [[Avatar_Personalisierung]]: Integration von Ready Player Me.
- [[Scoreboard_Leaderboard]]: Gamification & Daten-Logik.
- [[Events_Communities]]: Soziale Features.
- [[Roadmap]]: Der zeitliche Ablauf der Entwicklung.
![[Visuelle Darstellung]]