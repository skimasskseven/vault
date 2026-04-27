---
tags: [feature, ui, flutter]
---
# Feature: User Profile

## Aufbau
- **Header:** Profilbild, Name, Standort.
- **Statistik-Grid:** Distanz (km), Anzahl Läufe, Pace.
- **3D-Bereich:** Ein eingebettetes Unity-Widget, das den aktuellen Avatar in einer "Idle"-Animation (Atmen, leichtes Schwanken) zeigt.
- **Aktivitäts-Liste:** Scrollbare Liste der letzten Läufe.

## Logik
- Daten werden via Supabase Realtime-Subscription geladen.
- Verknüpfung zum [[Avatar_Personalisierung]] Modul zur Bearbeitung.
