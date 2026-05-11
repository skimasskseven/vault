---
tags:
  - projekt/running_app
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

tags:

#run-together
#tutgut
#avatar
#features
#decision

[[adr_001_masterplan]]
[[adr_002_aktualisierung]]
[[SPEC_unity_avatar]]

---

# ADR-003 — Avatar-Stack: Genies Avatar SDK (final)

## 1. Entscheidung

**Avatar-Tech für tutgut ist das `Genies Avatar SDK` + `Genies Art Forge SDK`.**

Beide Bestandteile sind laut offizieller Genies-Doku ([FAQ](https://docs.genies.com/docs/sdk-avatar/tools/faq)) **kostenfrei für Entwickler und Endnutzer**, auch in einer kommerziellen App, ohne MAU-Caps und ohne Per-Avatar-Fees. Genies bestätigt im Wortlaut: *"Yes, you can use the Genies Avatar SDK for a commercial project for free."*

Diese ADR überschreibt die noch offen formulierte Avatar-Stack-Wahl in [[SPEC_unity_avatar]] (Phase-2-Spec, generisch Unity-basiert) und ersetzt die Übergangs-Notiz in der internen Memory ("Avatar = Genies Unity SDK über Map als zweiter Layer").

## 2. Verworfene Alternativen

- **Ready Player Me:** Sign-up + Studio Anfang Mai 2026 abgeschaltet — Plattform tot. (Bereits in vorheriger Memory-Notiz festgehalten.)
- **Avaturn:** technisch sauber (REST API + GLB-Export), aber **800 USD/Monat** Pro-Plan — für Indie-Stage zu teuer.
- **Streamoji:** Sales-Termin war terminiert, Pricing nicht öffentlich — Risiko Vendor-Lock-in zu unbekanntem Preis. Mit Genies-gratis-Bestätigung nicht weiter verfolgt.
- **VRoid Studio (VRM):** Anime-Look passt nicht zur Lauf-App-Ästhetik; pixiv-Lizenz verbietet "Apps die Modelle generieren/ausgeben".
- **2D-Sprite-System (Eigenbau):** technisch der einfachste Weg, von Max bewusst verworfen — 3D-Look ist gewollt.

## 3. Akzeptierte Trade-Offs

Genies ist **Unity-only**: kein REST API, kein iOS/Android-Native-SDK, kein Flutter-Plugin, kein offizieller GLB-Export. Die einzige Brücke nach Flutter ist `flutter_unity_widget` (oder das jüngere `flutter_embed_unity`).

Bewusste Inkaufnahme:

- **Unity-Runtime im Mobile-Build** — APK/IPA wird ~80–250 MB statt ~30–60 MB
- **flutter_unity_widget ist faktisch unmaintained** (letzter Stable vor 23 Monaten) → Bridge-Bugs müssen ggf. selbst gefixt werden
- **Mapbox bleibt in Flutter, Unity rendert Avatar als Overlay** → Avatar-Position wird via Platform-Channel synchronisiert (Mapbox-Unity-SDK-URP-Konflikt damit umgangen)
- **Genies Common-Issues warnt vor Crashes bei rapidem Avatar-Spawning** → Spawn-Strategie für Multi-User-Map muss Limit + Pooling implementieren

## 4. Plattform-Risiken (mit Mitigation)

| Risiko | Quelle | Mitigation |
|---|---|---|
| Genies kündigt SDK-Vertrag mit 7 Tagen Vorlauf | EULA Section 12.b | Anonymous-Login-Modus nutzen → Avatar-Daten in eigenem Postgres → Ausstieg möglich, Avatar-IDs bleiben erhalten |
| Zukünftiges Revenue-Share-Modell ("future monetization system") | FAQ + EULA | Premium-Item-Verkauf läuft über eigenes Stripe (Memory: `project_shop_billing_open`) — saubere Trennung „SDK-Funktionalität" vs. „App-Inhalt" |
| Premium-Item-Verkauf vs. EULA Section 7.f ("charge for SDK functionality") | EULA | Vor Premium-Launch schriftliche Freigabe von Genies-Legal einholen — bis dahin nur kostenlose Items |
| Skeleton-Topologie für selbst-modellierte Items nicht öffentlich dokumentiert | Doku-Lücke | Erste Premium-Items über Art Forge SDK (Text+Bild-Prompt) erstellen; manuelle Blender-Items erst nach Spec-Anfrage bei Genies-Support |
| Doku hat 404-Lücken (Slots, FAQ, Tutorials teilweise) | Doku-Audit | Genies-Discord beobachten, eigenes internes Wiki führen sobald Reverse-Engineering passiert |

## 5. Technische Voraussetzungen (offiziell)

Aus [Prerequisites](https://docs.genies.com/docs/sdk-avatar/getting-started/prerequisites):

- **Unity:** `2022.3.62f2` (minimum) oder `6000.3.6f1` (empfohlen) — exakt diese Versionen
- **OS:** Windows 10+ ✅ Max-Setup, oder macOS 15+ M-Series
- **Render Pipeline:** Universal Render Pipeline (URP) ist Pflicht
- **Build-Module:** Android Build Support + iOS Build Support
- **Genies Developer Account:** [hub.genies.com](https://hub.genies.com) (gratis, E-Mail-OTP)
- **Genies App-Registrierung:** Client ID + Client Secret pro App-Projekt

**Offene Voraussetzung:** iOS-Build braucht einen Mac mit Xcode. Nicht Genies-spezifisch, aber blockiert iOS-Release insgesamt.

## 6. Implementierungs-Plan (Reihenfolge der Arbeitspakete)

| # | Paket | Grobaufwand | Risiko | Done-Kriterium |
|---|---|---|---|---|
| P1 | Unity-Projekt im `code/`-Repo aufsetzen (Unity 2022.3.62f2, URP, Genies SDK + Art Forge SDK, Bootstrap-Wizard durchlaufen, Anonymous Login konfiguriert) | 2–3 Tage | niedrig | Unity-Editor öffnet Beispielszene mit Genies-Avatar |
| P2 | `flutter_unity_widget` integrieren, Build-Pipeline für Android + iOS zum Laufen bringen | 1–2 Wochen | **HOCH** — Killer-Test der ganzen Architektur | `flutter run` zeigt einen Genies-Avatar im Flutter-Screen |
| P3 | Avatar-Customization-Screen: 3D-Viewer in Unity, Items aus Genies-Catalog wählbar, Auswahl wird in Postgres persistiert | 1 Woche | niedrig | User dreht Avatar, ändert Outfit, Stand wird beim nächsten App-Start wiederhergestellt |
| P4 | Avatar-Persistenz im eigenen Postgres: Anonymous-Login + Avatar-JSON in `user_avatars(user_id, genies_avatar_payload, updated_at)`. Alte RPM-Migrationen `0003_avatar_and_shop`, `0005_avatar_format_agnostic`, `0007_avatar_gender_and_catalog` und Tabellen `avatars/avatar_slots/avatar_assets/avatar_layers/avatar_outfits` per neuer Migration `0019_drop_rpm_avatar_replace_with_genies` zurückbauen. Code in `backend/app/api/v1/avatar.py`, `admin_avatar.py`, `mobile/lib/features/avatar/*`, `screen-avatar.jsx`, `assets/avatars/default_avatar.glb` analog entfernen oder ersetzen | 2–3 Tage | niedrig | `alembic upgrade head` läuft sauber, Tests grün |
| P5 | Eigener Avatar live auf Mapbox-Karte: Unity-Overlay über Mapbox-Flutter-Widget, GPS-Position via Platform-Channel synchronisiert, Toggle "Avatar an/aus" für Akku-Sparmodus (eigene Sicht, andere sehen den Avatar weiterhin) | 2–3 Wochen | mittel-hoch | Während eines Test-Laufs sieht User seinen Avatar an der eigenen GPS-Position |
| P6 | Andere User-Avatare auf der Map: Spawn-Limit (Default: max. 20 sichtbare Avatare gleichzeitig), LOD, Pooling, sanftes Despawn beim Verlassen des Sichtbereichs | 2–4 Wochen | **HOCH** — Genies-undokumentiertes Terrain | Last-Test mit 30 simulierten anderen Usern crasht Unity nicht |
| P7 | Custom Premium Items: in Art Forge SDK designen (Text+Bild-Prompt) → Item-Definition im eigenen Backend → Inventar-Sync → Anbindung an Stripe-Shop sobald `project_shop_billing_open` entschieden ist | 2–3 Wochen | mittel | Test-User kauft Premium-Item, sieht es am Avatar |

**Realistische Gesamt-Schätzung Vollzeit:** 8–14 Wochen ohne Bridge-Surprises, mit Buffer **3–4 Monate**.

**Meilenstein-Logik:** P2 ist der Killer-Test. Wenn die Flutter-Unity-Bridge nach 2 Wochen nicht stabil läuft, wird vor weiterem Investment neu evaluiert (z. B. doch 2D-Sprite-Fallback). NICHT erst nach P5/P6 die Reißleine ziehen.

## 7. Was diese ADR explizit NICHT festlegt

- **Slot-System für Items:** Genies-Doku hat hier 404-Lücke — wird in P3 reverse-engineered und in einer eigenen Spec dokumentiert
- **Animationen:** Standard-Unity-Humanoid-Rig + Mixamo-Animationen reichen vermutlich; eigene Animationen erst falls nötig
- **Ghost-Mode + 7-Min-Time-Offset für aktive Läufer:** existiert bereits in `users.settings` JSONB (siehe [[datenbank_doku_vollständig]]) — die Avatar-Sichtbarkeit muss in P5/P6 diese Settings respektieren
- **3D-Avatar-in-Instagram-Story-Export:** in [[adr_002_aktualisierung]] erwähnt, kommt nach P6 als eigenes Paket
