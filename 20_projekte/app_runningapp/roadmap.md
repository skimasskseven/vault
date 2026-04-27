---
tags:
  - project-management
  - timeline
---
# **Roadmap: "Run Together" (ca. 10 Wochen)**


## Phase 1: UI-Skelett & Prototyp (Woche 1–2)**

- **Tools:** Claude Design, Claude Code, VS Code, Android Emulator
    
- **Aktionen:** Alle 5 Hauptscreens in Claude Design entwerfen. Export zu Flutter. Navigation und State-Management mit Dummy-Daten einbauen.
    
- **Ziel: Vollständig navigierbarer, optisch fertiger Klick-Dummy im lokalen Emulator.
    
_________________________________________________________
## Phase 2: 3D-Avatare & Unity (Woche 3–4)

- **Tools:** Unity, Ready Player Me (RPM), `flutter_unity_widget`
    
- **Aktionen:** RPM-SDK in leeres Unity-Projekt integrieren. Unity-Szene in Flutter einbetten. Kommunikations-Bridge für Animationen schreiben.
    
- **Ziel:**Der 3D-Avatar wird in der App geladen und reagiert auf Flutter-Eingaben.
    
_________________________________________________________
## Phase 3: Backend & Karte (Woche 5–7)

- **Tools:** Mapbox, VPS, Supabase (Docker/PostgreSQL mit PostGIS)
    
- **Aktionen:** Docker-Setup auf dem VPS ausrollen. Mapbox-Karte in Flutter integrieren. Echtes GPS-Tracking und Zeichnen der Strecken implementieren.
    
- **Ziel:* Interaktive Live-Karte, auf der reale Laufdaten aus der Datenbank angezeigt werden.
    
_________________________________________________________
## Phase 4: CI/CD & Deployment (Woche 8–10)**

- **Tools:** Codemagic, GitHub, Apple TestFlight, Google Play
    
- **Aktionen:** Codemagic-Pipeline an das GitHub-Repo anbinden. Automatisierte Builds für iOS und Android konfigurieren. Letzter Feinschliff.
    
- **Ziel:* Erster erfolgreicher Build und Installation der Beta-Version auf echten Smartphones.
