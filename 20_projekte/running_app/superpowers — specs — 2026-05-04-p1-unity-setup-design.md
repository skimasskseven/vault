---
tags:
  - tutgut
  - avatar
  - unity
  - spec
  - p1
  - projekt/running_app
status: in-progress
date: 2026-05-04
implements: P1 of [[adr_003_avatar_genies]]
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# Design: P1 — Unity-Projekt-Setup für Genies-Avatar

## 1. Was ist P1?

Aus [[adr_003_avatar_genies]] § 6, Tabelle Implementierungs-Plan:

> **P1** — Unity-Projekt im `code/`-Repo aufsetzen (Unity 2022.3.62f2, URP, Genies SDK + Art Forge SDK, Bootstrap-Wizard durchlaufen, Anonymous Login konfiguriert) — **Done-Kriterium:** Unity-Editor öffnet Beispielszene mit Genies-Avatar.

Diese Spec konkretisiert, **wie** das passiert: Repo-Layout, Verantwortlichkeiten, exakte Schritt-Reihenfolge, Done-Audit.

## 2. Entscheidungen (aus Brainstorming 2026-05-04)

| # | Frage | Entscheidung | Begründung |
|---|---|---|---|
| 1 | Arbeitsteilung VPS↔Windows | Claude bereitet Repo-Skelett + Setup-Guide auf VPS vor; Max führt Unity-Hand-Schritte auf Windows aus | Max hat keine Unity-Editor-Möglichkeit auf VPS, Claude hat keinen Windows-Desktop |
| 2 | Unity-Version | **Unity 6000.3.14f1** (neuester Patch der von Genies empfohlenen Tech-Stream-Linie 6.3, ursprünglich 6000.3.6f1 in Genies-Doku), nicht 2022.3.62f2, nicht LTS-6.0, nicht TS-6.4 | Vendor-Empfehlung schlägt Bridge-Konservatismus; LTS-6.0 würde 6.3-spezifische APIs riskieren; TS-6.4 zu neu |
| 3 | Repo-Layout | **Eigener Repo `tutgut_unity` als Git-Submodule** in `code/unity/` | Saubere Trennung Unity-Cache von Hauptrepo; Submodule-Komplexität bewusst akzeptiert |
| 4 | Client-Secret-Storage | **Local-File** (`Assets/Settings/GeniesSecret.local.asset`, `.gitignored`); Client ID committed in `Assets/Settings/GeniesConfig.asset` | Backend-Proxy ist Scope-Creep für P1; CI-Strategie kommt mit P2-Build |

Verifiziert in Genies-Doku 2026-05-04: Bootstrap Wizard verlangt **beide** Tokens (Client ID + Client Secret) im "Save Credentials"-Dialog. Anonymous-Login-Doku-Seite ist 404 — Auth-Modus-Detail klärt sich beim Wizard-Durchlauf.

## 3. Repo-Layout

```
github.com/skimasskseven/running_app_code         (= "code/" lokal)
   ├── backend/  mobile/  run_app_frontend/  infra/      (bestehend)
   ├── docker-compose.yml                                  (bestehend)
   └── unity/                                              ← NEU: Submodule-Mountpoint
        │
        └── (pinnt Commit von)
            github.com/skimasskseven/tutgut_unity        (NEU)
            ├── .gitignore                                 (Unity + Secrets)
            ├── README.md                                  (Setup-Guide für Max)
            ├── Assets/
            │   ├── Genies/                               (vom SDK reingelegt)
            │   ├── Scenes/                               (Sample-Scene aus Bootstrap-Wizard)
            │   ├── Settings/
            │   │   ├── GeniesConfig.asset                (Client ID, committed)
            │   │   └── GeniesSecret.local.asset          (Client Secret, .gitignored)
            │   └── Scripts/                              (leer in P1)
            ├── Packages/manifest.json
            └── ProjectSettings/                          (URP, Android-Target, Player-Settings)
```

## 4. Verantwortlichkeiten

| Wer | Wo | Was |
|---|---|---|
| Claude (VPS) | `tutgut_unity` (lokal cloned) | Initial-Skelett: `.gitignore`, `README.md`. Initial commit + push. |
| Claude (VPS) | `code/` | `git submodule add … unity` → 2. Commit der initialen `tutgut_unity`-Commit pinnt. Push. |
| Max (Windows) | Beides geclont | Unity 6000.3.6f1 installieren (Hub → Install Editor → Modules nur Android Build Support). README.md durcharbeiten: Unity-New-Project → Genies SDK importieren → Bootstrap-Wizard mit Client ID + Secret → Sample-Scene öffnen → Push beider Repos. |
| Claude (VPS) | Audit | Pull beider Repos. Verifizieren: `Library/`/`Temp/`/`Obj/`/`Logs/`/`UserSettings/` NICHT im Repo, `Assets/Genies/` vorhanden, `GeniesConfig.asset` committed, `GeniesSecret.local.asset` NICHT committed, `Submodule-Pin` zeigt auf richtigen Commit. |

## 5. Setup-Sequenz (zeitlich)

```
T0 (jetzt parallel):
  Max:    Unity Hub 3.17.3 installiert ✓
          Unity-Account angelegt
          GitHub-Repo skimasskseven/tutgut_unity angelegt ✓ (leer, private)
          Genies-Hub-Account anlegen → App "tutgut-dev" registrieren
          → Client ID + Client Secret in Passwort-Manager speichern

T1 (Claude, VPS, ~5 min, parallel zu Max's Genies-Account-Setup):
  - git clone tutgut_unity → /root/dev/tutgut_unity
  - Schreibe .gitignore  (Unity-Standard + Build/ + *.local.asset)
  - Schreibe README.md   (Setup-Guide für Max, Schritt-für-Schritt)
  - git add, commit ("chore: initial unity project skeleton"), push
  - cd /root/dev/running_app/code
  - git submodule add https://…/tutgut_unity.git unity
  - git add .gitmodules unity, commit ("chore: add tutgut_unity as submodule"), push

T2 (Max, Windows, nachdem Unity-Editor-Download durch ist):
  - git clone running_app_code lokal (falls noch nicht vorhanden)
    ODER  git pull && git submodule update --init --recursive
  - Unity Hub: "New Project" → Template "Universal 3D" (URP)
    Project Name: tutgut_unity
    Location: C:\Unity\  (NICHT C:\Unity\tutgut_unity\ — Hub legt den Unterordner selbst an)
    → Hub warnt "directory not empty", Continue Anyway → Unity füllt Projekt
  - Im Editor: Window → Package Manager → "Packages: My Assets" → Genies Avatar SDK suchen → Download → Import All
    (vorher: assetstore.unity.com/packages/tools/game-toolkits/genies-avatar-sdk-336166 → "Add to My Assets")
  - Bootstrap-Wizard läuft automatisch nach Import:
      • Graphics API config bestätigen
      • TextMesh Pro Essential Resources importieren
      • Input handling system updates akzeptieren
      • Optional demo scene: ✓ importieren
      • Client ID + Client Secret aus Passwort-Manager einfügen → "Save Credentials"
  - Sample-Scene öffnen: Assets/Genies/Demo/SampleScene.unity (oder vergleichbar)
  - Play-Button drücken → Genies-Avatar erscheint im Game-View
  - cd C:\Unity\tutgut_unity && git add -A && git commit -m "feat: bootstrap Genies SDK, sample scene runs" && git push
  - cd ..\..\…\code && git add unity && git commit -m "chore: bump unity submodule to bootstrapped state" && git push

T3 (Claude, VPS, Audit, ~5 min):
  - git pull (code/ + tutgut_unity)
  - Audit-Checkliste durchgehen (siehe § 6)
  - Status-Report an Max
```

## 6. Done-Kriterium (Audit-Checkliste)

P1 ist abgeschlossen, wenn alle folgenden Punkte ✓ sind:

- [ ] `tutgut_unity` Repo enthält `.gitignore` mit Unity-Standard-Patterns
- [ ] `tutgut_unity` enthält `Assets/Genies/` Verzeichnis mit SDK-Files
- [ ] `tutgut_unity` enthält `ProjectSettings/` mit URP-Config (`GraphicsSettings.asset` zeigt URP-Asset)
- [ ] `tutgut_unity` enthält `Assets/Settings/GeniesConfig.asset` mit Client ID
- [ ] `tutgut_unity` enthält **NICHT**: `Library/`, `Temp/`, `Obj/`, `Logs/`, `UserSettings/`, `*.csproj`, `*.sln`, `Build/`, `Assets/Settings/GeniesSecret.local.asset`
- [ ] `code/.gitmodules` enthält `tutgut_unity` als Submodule unter `unity/`
- [ ] `code/unity/` zeigt auf den korrekten `tutgut_unity`-Commit
- [ ] Max bestätigt: Beispielszene öffnet im Unity-Editor, Avatar wird im Game-View gerendert

## 7. Risiken + Mitigationen

| Risiko | Wahrscheinlichkeit | Mitigation |
|---|---|---|
| Unity-Hub "directory not empty" Warning verwirrt Max | hoch (kommt sicher) | README erklärt's wörtlich ("Continue Anyway klicken"). |
| Genies SDK Asset-Store-Download verlangt Unity-Login | hoch | README weist darauf hin, dass Unity-Account-Login im Hub Pflicht ist. |
| Bootstrap-Wizard verändert Player-Settings die später Mapbox brechen | mittel | Wir akzeptieren das jetzt; Mapbox-Konflikt-Test kommt erst in P5. URP-Pflicht ist von beiden Seiten, daher kein direkter Konflikt erwartet. |
| Max committed versehentlich `GeniesSecret.local.asset` | mittel | `.gitignore` muss `*.local.asset` von Anfang an enthalten; README warnt explizit. |
| Submodule-Detached-HEAD beim ersten Pull | hoch | README hat Cheat-Sheet: nach `git submodule update` immer `cd unity && git checkout main`. |
| PAT in Repo-URL leakt (gh-Token im git remote) | niedrig (privater Repo) | Heads-up im Status-Report; eigener Refactor (Credential-Helper) ist eigene Aufgabe, nicht P1-Scope. |

## 8. Was diese Spec NICHT festlegt

- **flutter_unity_widget-Integration** — kommt in P2 (separate Spec)
- **AvatarBridge.cs** (C#-Side der Bridge) — kommt in P2
- **Backend-Schema-Änderungen** (`user_avatars`-Tabelle, RPM-Tabellen droppen) — kommt in P4 (separate Migration `0019_…`)
- **Mobile-Code-Änderungen** — `mobile/lib/features/avatar/*` und `pubspec.yaml` (`thermion_flutter` raus) bleiben in P1 unangetastet, kommen erst mit P4
- **CI-Build-Pipeline** für Codemagic — Genies Client Secret als CI-Secret reichen — kommt mit P2

## 9. Cross-Refs

- [[adr_003_avatar_genies]] — übergeordnete Avatar-Stack-Entscheidung
- [[SPEC_unity_avatar]] — alte Phase-2-Spec, durch ADR-003 + diese P1-Spec teilweise abgelöst
- Genies Avatar SDK Doku: https://docs.genies.com/docs/sdk-avatar/getting-started/installation
- Genies Hub: https://hub.genies.com
- Unity Asset Store Page: https://assetstore.unity.com/packages/tools/game-toolkits/genies-avatar-sdk-336166
