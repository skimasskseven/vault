---
tags: [feature, mapbox, unity, technical-spec, projekt/running_app]
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# Feature: Interaktive Karte

## Visuelles Design
- Dark-Theme Mapbox Karte.
- Laufstrecken als farbige Polylines (Neon-Grün/Orange).
- 3D-Avatare werden über `flutter_unity_widget` transparent über die Karte gerendert.

## Technische Umsetzung
- **Plugin:** `mapbox_gl` für Flutter.
- **Unity-Bridge:** Synchronisation der Kamera-Zoom-Stufe von Flutter zu Unity, damit der Avatar maßstabsgetreu auf der Karte steht.
- **Interaktion:** Tap auf Nutzer-Marker -> Flutter sendet Message an Unity -> Unity animiert Avatar -> Flutter öffnet Bottom-Sheet.

## Datenquelle
- GPS-Koordinaten-Stream aus der PostGIS-Datenbank.
