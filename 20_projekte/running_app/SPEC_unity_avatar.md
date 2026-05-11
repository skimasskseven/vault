---
tags: [avatar, unity, 3d, spec, projekt/running_app]
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# Spec: Unity-basiertes Avatar-Rendering

**Status:** Geplant — wird NACH MVP-Live-Gang in Phase 2 implementiert
**Priorität:** Hoch (User-Engagement + Shop-Monetarisierung hängt am Avatar)
**Verantwortlich:** Claude Code + Owner (Unity-Authoring)

---

## Ziel

Avatar-Rendering von [[Thermion]] (Filament-Wrapper) auf eine echte
**Unity-Engine-Integration** umstellen, damit der Owner eigene Items
(Outfits, Hats, Accessoires) direkt in **Unity** designen, exportieren
und ohne Code-Deploy ins Spiel bringen kann.

Begründung:
- Unity ist das Werkzeug, das der Owner kennt und in dem er ohnehin
  zukünftige Assets bauen will.
- Thermion liefert ein hübsches Modell, aber kein Authoring-Tooling —
  der Owner kann dort nichts selbst verändern.
- Unity hat ein etabliertes Asset-Pipeline-Ökosystem (Asset Store,
  Animator, Avatar-Shader) das wir 1:1 nutzen statt nachzubauen.

---

## Stack-Entscheidung

- **Unity-Version**: Unity 6 LTS (= 6000.0.x), URP, Built-In-Shaders.
- **Flutter-Bridge**: [`flutter_unity_widget`](https://pub.dev/packages/flutter_unity_widget) (≥ 2022.x kompatibel).
- **Asset-Format**: Unity Prefabs als AssetBundles. Pro Slot
  (Hair/Shirt/...) ein Bundle, das beim ersten Equip vom CDN nachgeladen wird.
- **Render-Target**: Auf Android via `UnityPlayerActivity`-Embed,
  iOS via `UnityFramework`. Beides macht `flutter_unity_widget`
  transparent.

Nicht-Stack:
- KEIN Ready-Player-Me — wir wollen eigene Assets, nicht eine fremde
  Bibliothek mit eigenem Look.
- KEIN Native Filament/Thermion mehr im Avatar-Pfad. Wave-Animationen
  laufen dann in Unitys Animator.

---

## Repo-Layout

```
running_app_code/
├── mobile/                       # Flutter
│   ├── android/
│   │   └── unityLibrary/        # generiert von Unity (Android-Export)
│   └── lib/features/avatar/     # Unity-Embed + Editor
└── unity/                        # Unity-Projekt (NEU)
    ├── Assets/
    │   ├── Avatar/Base/         # Base-Body, Skelett
    │   ├── Avatar/Items/        # ein Prefab pro avatar_assets-Eintrag
    │   ├── Scenes/AvatarScene.unity
    │   └── Scripts/AvatarBridge.cs   # JSON-Interface zur Flutter-Seite
    └── ProjectSettings/
```

`unity/` ist ein **eigenes Git-Submodule**, damit der Unity-Cache
(`Library/`, `Temp/`) nicht in den Haupt-Repo-Status leakt.

---

## Datenmodell — keine Änderung

`avatar_slots`, `avatar_assets`, `avatar_layers` bleiben **exakt** wie
heute. Was sich ändert: `avatar_assets.asset_path` zeigt jetzt auf ein
Unity-AssetBundle (`shirt_basic.bundle`) statt auf eine `.glb`. Die
`format`-Spalte bekommt einen neuen Wert `unity_bundle`, damit der
Renderer dispatchen kann (`glb` für Legacy-/Fallback-Modelle).

```sql
-- Phase-2 Migration (NACH Unity-Setup):
ALTER TYPE asset_format ADD VALUE 'unity_bundle';
-- Bestehende Body-Assets bleiben format='glb' bis ein Unity-
-- Equivalent hochgeladen ist; der Renderer mischt beide Pfade.
```

---

## Bridge-Protokoll (Flutter ↔ Unity)

JSON-Messages über `flutter_unity_widget.postMessage`:

```jsonc
// Flutter → Unity: User-Layers anwenden
{
  "type": "applyLayers",
  "layers": [
    { "slot": "hair", "asset_id": "...", "tint": "#3a2a1a" },
    { "slot": "shirt", "asset_id": "...", "tint": "#ff7a3d" }
  ]
}

// Flutter → Unity: gender umstellen (skelett wechseln)
{ "type": "setGender", "gender": "female" }

// Unity → Flutter: bundle download fortschritt
{ "type": "loadProgress", "asset_id": "...", "progress": 0.42 }

// Unity → Flutter: ready
{ "type": "ready" }
```

Unity-Seitig liest `AvatarBridge.cs` die Messages, sucht das passende
Prefab (lokal gecacht oder via `UnityWebRequestAssetBundle` aus dem
CDN), instanziiert es als Child des Base-Skelettons, und wendet den
Tint via Material-Property-Block an.

---

## Authoring-Flow für den Owner

1. In Unity ein Prefab im Slot-Folder anlegen (z.B.
   `Assets/Avatar/Items/hair_pony.prefab`).
2. Beliebige Mesh + Skinning + Material darunter — alles, was Unity
   unterstützt, geht.
3. Build → AssetBundle → Upload via Admin-Dashboard
   (`POST /api/v1/admin/avatar/assets/{id}/bundle`).
4. Asset wird `is_active = TRUE` gesetzt → erscheint im Editor.

Kein App-Update nötig. Das ist **der** Grund für Unity.

---

## Wave-Animation

Statt Thermions GLB-Animationen läuft die Wave als **Unity-Animator
State**. Der Base-Body bringt eine `Wave`-Clip mit; alle 15 s triggert
`AvatarBridge` einen Trigger im Animator, der zur Wave springt und
zurück zum Idle blendet.

---

## Implementierungs-Reihenfolge

1. **Unity-Projekt anlegen** (Owner): Base-Skelett (Mixamo) + Idle/Wave
   Animations + leeres Prefab pro Slot.
2. **Unity-Export einbinden** (Claude Code):
   `flutter_unity_widget` zu `pubspec.yaml`, `unityLibrary` als
   Gradle-Module, `UnityFramework` als CocoaPod.
3. **`AvatarBridge.cs`** schreiben (Claude Code, im Unity-Projekt).
4. **`avatar_screen.dart`** umbauen: `ViewerWidget` → `UnityWidget`.
5. **AssetBundle-Endpoint** (Claude Code, Backend): Upload, Versionierung,
   CDN-Auslieferung über `/uploads/`.
6. **Migration** auf `format='unity_bundle'` (per-Asset).
7. **Thermion entfernen** aus pubspec wenn alle Assets migriert sind.

Geschätzte Komplexität: **5–7 Tage Claude Code + 2–3 Tage Owner**
(Unity-Authoring eines Mini-Sets von ~10 Items zum Live-Gang).

---

## Offene Fragen

- AssetBundle-Cache-Invalidierung: per-Asset `version_hash` in
  `avatar_assets` mitführen?
- Multi-Plattform-Bundles: Android (ETC2), iOS (ASTC), zwei separate
  Builds pro Asset oder ein crunched-DXT-Cross-Format-Bundle?
- Performance: gleichzeitig laufende Mapbox + Unity auf Low-End-Android
  — RAM-Profil auf einem 4 GB Gerät checken bevor wir ausrollen.
