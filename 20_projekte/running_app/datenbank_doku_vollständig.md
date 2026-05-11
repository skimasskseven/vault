---
tags:
  - projekt/running_app
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

[[ADR-002 Aktualisierung]] [[ADR-001_Masterplan]]
### Vollständige DB-Dokumentation

---

#### AUTH & USER

---

**`users`** Zentrales Nutzerprofil. Basis für alles. Felder: ID, Email, Passwort-Hash, Rolle (superadmin/trainer/athlete), Anzeigename, Bio, Profilbild-Pfad, Level, Punkte, Lifetime-EP, aktiver Title, Settings (JSONB: Ghost-Mode, Units, Karten-Sichtbarkeit, Zeitversatz), DSGVO-Felder, Soft-Delete. _How to implement:_ Erste Tabelle die erstellt wird. Alle anderen Tabellen referenzieren sie. `password_hash` via bcrypt in FastAPI hashen, nie plaintext. `settings` als JSONB damit neue Einstellungen ohne Schema-Migration ergänzt werden können.

---

**`sessions`** Aktive Login-Sessions pro Gerät. Felder: ID, UserID, Token-Hash, Gerätename, OS, IP-Adresse, letzte Aktivität, Ablaufdatum. _How to implement:_ Bei jedem Login neuen Eintrag erstellen. Flutter speichert Token lokal (flutter_secure_storage). Bei Logout Eintrag löschen. "Überall ausloggen" = alle Sessions des Users löschen.

---

**`push_tokens`** Firebase FCM Device-Tokens für Push-Notifications. Felder: ID, UserID, Token, Device-OS (ios/android), aktiv/inaktiv. _How to implement:_ Flutter holt FCM-Token beim App-Start via firebase_messaging Package und sendet ihn an FastAPI. FastAPI speichert ihn. Beim Senden einer Notification: FastAPI → FCM REST API → Gerät. Firebase Projekt kostenlos anlegen unter console.firebase.google.com.

---

**`admin_roles`** Granulare Rechte für Super-Admins. Felder: UserID, can_manage_clubs, can_manage_users, can_view_audit_log, can_manage_shop. _How to implement:_ Nur für User mit Rolle `superadmin`. Wird manuell gesetzt. FastAPI prüft diese Tabelle bei jedem Admin-Dashboard Request.

---

**`trainer_profiles`** Erweiterungsprofil für Trainer. Felder: UserID, Spezialisierung, Zertifikate (Array), Website, Instagram. _How to implement:_ Wird beim Trainer-Onboarding durch Super-Admin angelegt. 1:1 zu `users`.

---

**`athlete_profiles`** Erweiterungsprofil für Athleten. Felder: UserID, TrainerID, Geburtsdatum, Gewicht, Größe, Fitness-Level (1–5), Beitrittsdatum. _How to implement:_ Wird nach Invite-Code-Einlösung automatisch erstellt. TrainerID verknüpft Athlet mit seiner Trainerin.

---

**`follows`** Social-Graph — wer folgt wem. Felder: FollowerID, FollowingID, Datum. _How to implement:_ Composite Primary Key verhindert doppelte Follows. Basis für den Community-Feed und die Karten-Ansicht (nur Follows sehen Routen voneinander).

---

#### CLUBS & B2B

---

**`clubs`** Eine Trainer-Community als eigene Entität. Felder: ID, TrainerID, Name, Beschreibung, aktiv, maximale Athleten-Anzahl, Soft-Delete. _How to implement:_ Wird vom Super-Admin im Admin-Panel angelegt. TrainerID bestimmt wer der Besitzer ist. `max_athletes` wird durch Subscription-Plan gesetzt.

---

**`club_branding`** Visuelles Individualisierung pro Club. Felder: ClubID, Primärfarbe (HEX), Banner-Pfad, Logo-Pfad, Motto. _How to implement:_ 1:1 zu `clubs`. Farbe bestimmt die Routen-Farbe auf der Karte für diesen Club. Banner wird in Flutter auf dem Club-Screen angezeigt.

---

**`club_settings`** Konfigurationseinstellungen pro Club. Felder: ClubID, Follows erlaubt, Leaderboard sichtbar, eigene Challenge-Kategorien. _How to implement:_ 1:1 zu `clubs`. Trainer kann diese im Dashboard anpassen.

---

**`club_memberships`** Welcher Athlet gehört zu welchem Club. Felder: ClubID, UserID, Beitrittsdatum. _How to implement:_ Wird beim Invite-Code-Einlösen automatisch erstellt. Ein Athlet kann theoretisch in mehreren Clubs sein (spätere Skalierung).

---

**`club_leaderboards_cache`** Vorberechnete wöchentliche/monatliche Rangliste pro Club. Felder: ClubID, UserID, Zeitraum (week/month), km_total, runs_total, ep_total, Ranking-Position. _How to implement:_ Cron-Job jeden Montag 01:00 → FastAPI-Endpoint berechnet aus `run_summary_cache` die Rangliste und schreibt sie hier rein. Flutter liest nur diesen Cache — keine Live-Berechnung.

---

**`subscriptions`** Trainer-Abo via Stripe. Felder: ID, ClubID, Stripe-Customer-ID, Stripe-Subscription-ID, Plan (starter/pro/elite), Status (active/cancelled/past_due/trialing), Periode-Ende. _How to implement:_ Stripe-Account anlegen. Webhook-Endpoint in FastAPI: `POST /webhooks/stripe`. Stripe sendet Events (payment_succeeded, subscription_cancelled etc.) → FastAPI updated diese Tabelle → Club wird aktiviert/deaktiviert.

---

**`invite_codes`** Einladungscodes für exklusiven App-Zugang. Felder: ID, Code (unique), ClubID, TrainerID, verwendet von (UserID), verwendet am, Ablaufdatum. _How to implement:_ Trainer generiert Codes im Dashboard. FastAPI generiert zufälligen 8-stelligen Code. Flutter-Onboarding-Screen: Code eingeben → FastAPI prüft ob gültig, nicht abgelaufen, noch nicht verwendet → Account-Erstellung freigegeben.

---

#### GPS & LAUFEN

---

**`runs`** Metadaten eines einzelnen Laufs. Felder: ID, UserID, Titel, Start/Ende, Distanz (Meter), Dauer (Sekunden), Durchschnittspace, Höhenmeter, Kalorien, öffentlich/privat, Strava-Activity-ID, Bounding Box (PostGIS Polygon), Soft-Delete. _How to implement:_ Run-Start: POST /runs erstellt Eintrag mit `started_at`. Run-Ende: PATCH /runs/{id} befüllt alle Metriken. `bounding_box` wird serverseitig aus GPS-Punkten berechnet (PostGIS ST_Envelope). Wird für Karten-Queries genutzt.

---

**`gps_points`** Einzelne GPS-Koordinaten eines Laufs. Herzstück der Karte. Felder: ID (BigSerial), RunID, Zeitstempel, Location (PostGIS POINTZ — Lat/Lon/Höhe), Herzrate, Kadenz, Geschwindigkeit. _How to implement:_ Flutter sammelt GPS-Punkte alle 3–5 Sekunden lokal im Gerätespeicher während des Laufs und schickt **alle 5 Minuten einen Mini-Batch-POST** an FastAPI (Endpoint `POST /runs/{id}/gps_points`). Nach Run-Ende: finaler Batch-POST mit den seit dem letzten Mini-Batch gesammelten Punkten plus `PATCH /runs/{id}` für Metriken. Server dedupliziert über `(run_id, recorded_at)` — Mini-Batches sind idempotent retrybar bei Netzwerkabbruch. Modell ist explizit nicht Per-Point-Streaming: Mini-Batches schützen den Server vor Überlast und ermöglichen gleichzeitig, dass andere Nutzer aktive Läufe auf der Karte mit max. 5 min Verzögerung sehen. Spatial Index auf `location` ist Pflicht für Performance. Flutter GPS via geolocator Package.

---

**`run_feelings`** Subjektives Befinden nach dem Lauf. Felder: ID, RunID, Feeling (great/good/okay/tired/bad), Tags (Array: "schwere Beine", "zu heiß" etc.), optionale Notiz. _How to implement:_ Flutter zeigt Modal direkt nach Run-Ende, vor dem Post-Run Pop-Up. 5-Sekunden-Timeout → automatisch übersprungen wenn keine Eingabe. FastAPI: POST /runs/{id}/feeling.

---

**`weather_snapshots`** Wetterdaten zum Zeitpunkt des Laufs. Felder: ID, RunID, Temperatur, Gefühlte Temperatur, Luftfeuchtigkeit, Windgeschwindigkeit, Wetterbedingung (Text), Icon-Code. _How to implement:_ FastAPI ruft beim Run-Start automatisch OpenWeatherMap API auf: `api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}`. API-Key in `.env`. Kostenlos bis 1000 Calls/Tag. Fallback: NULL wenn API nicht erreichbar — kein App-Fehler.

---

**`run_tags`** Lauf-Kategorie vom User selbst gesetzt. Felder: RunID, Tag (easy/tempo/interval/recovery/long_run/race/trail). _How to implement:_ Flutter zeigt Tag-Auswahl im Post-Run Pop-Up. Optional. Trainerin sieht Verteilung ihrer Athleten im Dashboard.

---

**`route_templates`** Von der Trainerin vorgegebene Routen. Felder: ID, CreatorID, ClubID, Titel, Beschreibung, Distanz, Schwierigkeitsgrad (1–5), Pfad (PostGIS LineString), Soft-Delete. _How to implement:_ Trainerin zeichnet Route im Dashboard (Mapbox Web-Komponente). FastAPI speichert als LineString. Spatial Index für Proximity-Queries. Flutter kann später prüfen ob Athlet nah an der Route war (ST_Distance).

---

**`run_summary_cache`** Vorberechnete Wochenwerte pro User. Felder: UserID, Wochenstart (DATE), km_total, runs_total, ep_total, duration_s. _How to implement:_ Cron-Job täglich 00:00 → FastAPI berechnet Werte aus `runs` und `ep_transactions` → upsert in diese Tabelle. Flutter liest nur Cache für Freunde-Vergleich im Post-Run Pop-Up. Primary Key auf (UserID, week_start).

---

#### KÖRPER & GESUNDHEIT

---

**`body_metrics`** Zeitreihe körperlicher Messwerte. Felder: ID, UserID, Datum, Gewicht, Ruhepuls, Schlafstunden, Quelle (manual/apple_health/google_fit/garmin). _How to implement:_ Manuell: Flutter-Eingabemaske. Automatisch: Flutter `health` Package (Version 10.x) liest Apple HealthKit (iOS) und Google Fit (Android) aus — kein Server-Token nötig, direkt auf Gerät. `source`-Feld zeigt Herkunft. UNIQUE auf (UserID, Datum) — ein Eintrag pro Tag.

---

#### SOCIAL

---

**`run_likes`** Likes auf Läufe. Felder: UserID, RunID, Datum. Composite Primary Key. _How to implement:_ POST /runs/{id}/like — idempotent. DELETE /runs/{id}/like zum Entfernen. Trigger oder FastAPI-Logik sendet Notification an Run-Besitzer.

---

**`run_comments`** Kommentare auf Läufe. Felder: ID, RunID, UserID, Text, Soft-Delete. _How to implement:_ Flutter: Kommentar-Section im Run-Detail-Screen. Soft-Delete damit Kontext erhalten bleibt ("Kommentar gelöscht"). Notification an Run-Besitzer bei neuem Kommentar.

---

**`user_reports`** Meldungen von Nutzern gegeneinander. Felder: ID, MelderID, GemeldeterID, Grund (spam/inappropriate/harassment/other), Notiz, gelöst am, gelöst von. _How to implement:_ Flutter: "User melden" Button im Profil. Landet im Super-Admin Dashboard als offener Fall. `resolved_by` = AdminID der den Fall bearbeitet hat.

---

#### DOKUMENTE & TRAININGSPLANUNG

---

**`documents`** Dateien (primär PDFs) die Trainer hochladen. Felder: ID, TrainerID, ClubID, Titel, Beschreibung, Dateipfad, Dateityp, Dateigröße. _How to implement:_ FastAPI: Multipart File Upload → Datei auf VPS-Dateisystem speichern unter `/var/laufapp/uploads/documents/`. Pfad in DB. Flutter: PDF-Viewer via flutter_pdfview Package.

---

**`document_assignments`** Welches Dokument bekommt welcher Athlet. Felder: DocumentID, AthleteID, zugewiesen am, gelesen am. _How to implement:_ Trainer wählt im Dashboard Athleten aus → FastAPI erstellt Einträge. `read_at` wird gesetzt wenn Athlet das Dokument öffnet. Ungelesen-Badge in Flutter.

---

**`training_plans`** Strukturierte Trainingspläne (über PDFs hinaus). Felder: ID, TrainerID, ClubID, Titel, Beschreibung, Dauer in Wochen, Schwierigkeitsgrad. _How to implement:_ Trainer erstellt Plan im Web-Dashboard. Flutter zeigt Plan als Kalender-View via table_calendar Package.

---

**`training_plan_weeks`** Einzelne Wochen innerhalb eines Plans. Felder: ID, PlanID, Wochennummer, Fokus (z.B. "Grundlagenausdauer"), Notizen. _How to implement:_ Wird beim Plan-Erstellen miterzeugt. 1:n zu `training_plans`.

---

**`training_plan_days`** Einzelne Trainingstage innerhalb einer Woche. Felder: ID, WeekID, Tagesnummer (1–7), Titel, Beschreibung, Distanz, Dauer, Lauf-Typ, Ruhetag. _How to implement:_ Granularste Ebene. Flutter zeigt pro Tag was zu tun ist. `is_rest_day = TRUE` zeigt Erholungs-Icon.

---

**`training_plan_assignments`** Welcher Athlet bekommt welchen Plan ab wann. Felder: PlanID, AthleteID, Startdatum, zugewiesen am. _How to implement:_ Trainer weist Plan + Startdatum zu. FastAPI berechnet aus Startdatum + Wochennummer + Tagesnummer das absolute Datum jeder Einheit. Flutter zeigt im Kalender.

---

#### AVATAR & SHOP

---

**`avatars`** Avatar-Konfiguration pro User. Felder: ID, UserID, base (JSONB: gender, body_type, skin_tone, face_preset, eye_color, eye_shape, hair_style, hair_length, hair_color, extras), equipped (JSONB: shirt, pants, shoes, jacket, hat, accessory, hair_color_special). _How to implement:_ Wird beim Onboarding erstellt. `base` = kostenlos, einmalig wählbar (editierbar in Einstellungen). `equipped` = nur Items aus `user_inventory`. Flutter rendert Avatar als gestapelte SVG-Layer. 3D-Rendering via Flame Engine oder Ready Player Me API — Entscheidung steht noch.

---

**`shop_items`** Alle käuflichen/erwerbbaren Items. Felder: ID, Name, Beschreibung, Typ (digital/physical), Kategorie (shirt/shoes/hat etc.), Asset-Pfad, Preis in € , Preis in Punkten, Challenge-Reward-Flag, aktiv/inaktiv, Soft-Delete. _How to implement:_ Wird vom Super-Admin im Dashboard gepflegt. `is_challenge_reward = TRUE` bedeutet Item ist nicht direkt kaufbar sondern nur via Challenge. Asset-Pfad zeigt auf SVG-Datei auf VPS.

---

**`user_inventory`** Was besitzt ein User. Felder: UserID, ItemID, erworben am, erworben via (purchase/achievement/challenge_reward/gift). _How to implement:_ Composite Primary Key verhindert Duplikate. `acquired_via` für Analytik und spätere Entscheidungen (z.B. "nur via Challenge erworbene Items sind handelbar").

---

#### GAMIFICATION

---

**`level_config`** EP-Schwellen pro Level — ohne Code-Deployment änderbar. Felder: Level (1–10), EP benötigt, Item-Reward, Title-Reward. _How to implement:_ Bereits mit Seed-Daten (Level 1–10) im Schema. FastAPI liest diese Tabelle bei jeder EP-Vergabe. Super-Admin kann Werte im Dashboard anpassen ohne Deployment.

---

**`ep_transactions`** Jede EP-Vergabe transparent geloggt. Felder: ID (BigSerial), UserID, Betrag, Grund (run_distance/streak_bonus/achievement/strava_import), RunID, Meta (JSONB: Multiplikator, Streak-Tage etc.). _How to implement:_ FastAPI schreibt nach jedem Lauf-Ende mehrere Einträge (Basis-EP, Streak-Bonus, Morgen-Bonus etc.). Summe aller Einträge = `total_ep` auf `users`. Index auf UserID für schnelle History-Abfragen.

---

**`streaks`** Aktuelle und längste Lauf-Streak pro User. Felder: UserID, current_streak, longest_streak, last_run_date. _How to implement:_ FastAPI prüft nach jedem Lauf: War `last_run_date` gestern? → current_streak + 1. War es früher? → Reset auf 1. Cron-Job täglich 23:59 prüft ob User heute gelaufen ist — wenn nicht, streak reset. Trigger-Animation in Flutter wenn Streak-Milestone erreicht.

---

**`personal_records`** Persönliche Bestleistungen pro Kategorie. Felder: ID, UserID, record_type (fastest_5k/longest_run/best_pace/most_elevation), Wert, RunID, erreicht am. UNIQUE auf (UserID, record_type). _How to implement:_ FastAPI-Job nach jedem Run-Ende: vergleiche neue Werte mit bestehenden PRs. Wenn übertroffen: UPDATE + extra Notification + PR-Animation im Post-Run Pop-Up. UNIQUE Constraint stellt sicher: immer nur ein aktiver PR pro Typ.

---

**`achievements`** Definierte Auszeichnungen mit Bedingungen. Felder: ID, Name, Beschreibung, Icon-Pfad, Bedingungstyp, Bedingungswert, EP-Belohnung, Item-Belohnung. _How to implement:_ Vom Super-Admin im Dashboard gepflegt. FastAPI prüft nach jedem Lauf alle noch nicht erreichten Achievements des Users. Batch-Check via SQL effizienter als Einzelprüfungen.

---

**`user_achievements`** Welcher User hat welches Achievement. Felder: UserID, AchievementID, erreicht am. _How to implement:_ Composite Primary Key. Nach Eintrag: EP gutschreiben via `ep_transactions`, Notification senden, Item vergeben falls vorhanden.

---

**`milestones`** Lifetime-Abzeichen für Gesamtdistanz. Felder: ID, Name (Century Club/Iron Runner etc.), Beschreibung, Icon-Pfad, total_km Auslöser. _How to implement:_ Seed-Daten: 100km, 500km, 1000km, 2500km, 5000km. FastAPI prüft nach jedem Lauf die kumulierte Gesamtdistanz. Milestone-Badge dauerhaft sichtbar auf Profil.

---

**`user_milestones`** Welcher User hat welchen Milestone. Felder: UserID, MilestoneID, erreicht am. _How to implement:_ Composite Primary Key. Sichtbar als permanente Badges im Profil-Screen in Flutter.

---

**`titles`** Prestige-Titel die im Profil und auf der Karte sichtbar sind. Felder: ID, Name, Beschreibung, Bedingungstyp, Bedingungswert, ClubID (NULL = global, gesetzt = Club-spezifisch). _How to implement:_ Globale Titles vom Super-Admin. Club-spezifische Titles von der Trainerin. User aktiviert einen Title unter `users.active_title_id`. Sichtbar als Label unter Avatar-Name auf der Karte.

---

**`user_titles`** Welcher User hat welchen Title verdient. Felder: UserID, TitleID, verdient am. _How to implement:_ Composite Primary Key. User kann im Profil-Screen zwischen verdienten Titles wählen welcher aktiv angezeigt wird.

---

**`challenges`** Zeitlich begrenzte Herausforderungen. Felder: ID, CreatorID, ClubID, Titel, Beschreibung, Typ (distance/runs/duration/elevation), Zielwert, Start/Ende, EP-Belohnung, Item-Belohnung, öffentlich, Soft-Delete. _How to implement:_ Trainer erstellt im Dashboard. `item_reward_id` = exklusives Shop-Item das nur durch diese Challenge erworben werden kann. FastAPI aktualisiert `challenge_participants.current_value` nach jedem Lauf automatisch.

---

**`challenge_participants`** Fortschritt pro User pro Challenge. Felder: ChallengeID, UserID, current_value, abgeschlossen am, beigetreten am. _How to implement:_ User tritt Challenge bei → Eintrag mit current_value 0. Nach jedem Lauf: FastAPI addiert relevante Werte. Wenn current_value >= target_value → completed_at setzen + Rewards vergeben.

---

**`seasonal_events`** App-weite zeitlich begrenzte Community-Events. Felder: ID, Titel, Beschreibung, Typ, Community-Ziel (Gesamtziel aller), aktueller Wert, Start/Ende, Banner-Pfad. _How to implement:_ Nur Super-Admin kann erstellen. Alle Clubs nehmen teil. Fortschrittsbalken in Flutter auf Hauptscreen. Motiviert Club-übergreifend.

---

**`event_participants`** Beitrag einzelner User zum Seasonal Event. Felder: EventID, UserID, contributed (eigener Beitrag), beigetreten am. _How to implement:_ Automatisch: jeder Lauf während eines aktiven Events addiert Distanz zu `contributed` und zu `seasonal_events.current_value`.

---

#### INTEGRATIONEN

---

**`integrations`** Generische Tabelle für alle externen Dienste. Felder: ID, UserID, Provider (strava/garmin/apple_health/google_fit), Access-Token (verschlüsselt), Refresh-Token (verschlüsselt), Ablauf, externe UserID, Sync aktiv, letzter Sync, Meta (JSONB). _How to implement:_ Tokens via pgcrypto verschlüsselt speichern. Strava/Google Fit: OAuth2-Flow in Flutter (flutter_web_auth Package). Garmin: OAuth1 (komplexer, Phase 3+). Apple Health: kein Token nötig, direkt via health Package auf Gerät. Cron-Job täglich 06:00 → FastAPI refreshed abgelaufene Tokens automatisch.

---

**`strava_imports`** Duplikat-Schutz für Strava-Importe. Felder: ID, UserID, Strava-Activity-ID, RunID, importiert am. UNIQUE auf (UserID, strava_activity_id). _How to implement:_ Vor jedem Import prüfen ob strava_activity_id bereits vorhanden. Wenn ja: überspringen. Verhindert doppelte Läufe in der History.

---

#### SYSTEM

---

**`notifications`** In-App Benachrichtigungen. Felder: ID, UserID, Typ (run_like/comment/achievement/challenge/document/follow/system/milestone/personal_record/title_earned), Titel, Text, Referenz-Typ, Referenz-ID, gelesen, erstellt am. _How to implement:_ FastAPI erstellt Einträge bei relevanten Events. Flutter pollt `/notifications/unread` beim App-Start. Index auf (UserID WHERE is_read = FALSE) für Performance. Kombination mit `push_tokens` für echte Push-Notifications via FCM.

---

**`audit_log`** DSGVO-konformes Aktions-Log. Felder: ID (BigSerial), UserID, Aktion (create/update/delete/login/logout/anonymize/admin_view), Tabellenname, Record-ID, IP-Adresse, Meta (JSONB), erstellt am. _How to implement:_ FastAPI Middleware schreibt automatisch bei kritischen Aktionen. Besonders wichtig: jeder Admin-Zugriff auf User-GPS-Daten wird als `admin_view` geloggt. Unveränderlich — kein Update, kein Delete auf dieser Tabelle. Index auf UserID und created_at.

---

#### VIEWS

---

**`v_weekly_leaderboard`** Vorberechnete Wochenrangliste. _How to implement:_ FastAPI liest diese View für Freunde-Vergleich. Kein JOIN zur Laufzeit nötig.

---

**`v_map_recent_runs`** Läufe der letzten 5 Tage für die Karte. _How to implement:_ Flutter-Karte ruft diese View über FastAPI ab. Gefiltert nach öffentlichen, nicht gelöschten Läufen. Zeitversatz (7 Minuten bei aktiven Läufern) wird in FastAPI-Logik hinzugefügt.