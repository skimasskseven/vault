tags:

#run-together
    
#social-media
    
#server-setup
    
#features  
#Social  
#Server

 

---

# Feature-Erweiterung & Server-Struktur – "Run Together"

## 1. Neue App-Features (Social & Gamification)

### 📲 `[[Social Media Sharing]]` (Neu)

- **Konzept:** Nutzer können ihre abgeschlossenen Workouts visuell ansprechend auf externen Plattformen teilen, um Reichweite für die App zu generieren und Erfolge zu feiern.
    
- **Geplante Integrationen:**
    
    - **Instagram:** Fokus auf das Teilen in Instagram Stories (visuelles Overlay aus 3D-Avatar, Karte und Lauf-Statistiken).
        
    - **Zweites Portal (Evaluierung):** Definition eines weiteren relevanten Netzwerks für Läufer.
        
- **Technik:** OAuth-Authentifizierung und Nutzung von nativen Share-Dialogen (iOS/Android) sowie spezifischen Plattform-APIs.
    

### 🏁 `[[Segmente & Challenges]]` (Neu spezifiziert)

- **Konzept:** Fortgeschrittene Gamification-Elemente in Anlehnung an Strava oder Adidas Running.
    
- **Segmente:** Fest definierte GPS-Korridore auf der Karte. Läuft ein Nutzer durch dieses Segment, wird die Zeit automatisch gestoppt und in ein lokales Segment-Leaderboard eingetragen.
    
- **Challenges:** Zeitlich oder distanzgebundene Herausforderungen (z. B. "Laufe 50km im Mai"), bei deren Abschluss Nutzer exklusive Items für ihren Avatar freischalten.
    

## 2. Server & CLI Architektur (Entscheidung)

### ⚙️ `[[Claude Code CLI - Globale Installation]]`

- **Entscheidung:** Die Claude Code CLI wird **nicht** in einzelnen Docker-Containern isoliert, sondern global auf der Host-Ebene des VPS installiert (`npm install -g @anthropic-ai/claude-code`).
    
- **Begründung:** * Erlaubt der KI, serverweite Befehle auszuführen (z. B. `docker compose up`).
    
    - Einmalige API-Key-Authentifizierung.
        
    - Agent kann durch einfachen Verzeichniswechsel flexibel zwischen verschiedenen Repositories (z. B. "Run Together", "Compliance Guard") wechseln (Git-Ansatz).
        

---

### Meine Beratung zur Social-Media-Integration

Die Idee, Workouts zu teilen, ist der wichtigste Wachstumsmotor (Growth Loop) für eine solche App. Hier ist die Realität bei der Umsetzung und mein Vorschlag für das zweite Portal:

**1. Instagram-Logik (Die Realität)**

- Ein direkter "Post-to-Feed"-Ansatz über eine API-Schnittstelle ist bei Instagram für Drittanbieter-Apps extrem restriktiv und oft nicht gewollt.
    
- **Der Best-Practice-Weg:** Nutze **"Deep Linking" in die Instagram Stories**. Deine Flutter-App generiert nach dem Lauf ein schickes Bild (ein Screenshot-artiges Widget). Darauf zu sehen: Die Mapbox-Karte mit der Route, der 3D-Avatar in einer Siegerpose und die Zeiten. Dieses Bild wird über das native "Share Sheet" von iOS/Android direkt an die Instagram-App übergeben. Das spart dir komplizierte API-Logins und ist genau das, was Nutzer wollen.
    

**2. Das zweite Portal: Strava**

- Wenn du eine Lauf-App baust, führt kein Weg an **Strava** vorbei. Es ist das "LinkedIn für Sportler".
    
- **Die Integration:** Du integrierst einen "Connect with Strava" Button (OAuth 2.0). Wenn der Nutzer einen Lauf in "Run Together" beendet, sendet dein Supabase-Backend die rohen GPS-Daten (`.gpx` oder `.fit` Format) über die Strava-API direkt in den Feed des Nutzers.
    
- **Der Vorteil:** Andere Strava-Nutzer sehen, dass das Workout mit "Run Together" aufgezeichnet wurde (inklusive Link zu deiner App).
    

**3. Technische Umsetzung in Flutter**

- Für das Erstellen des Bildes aus deinem UI nutzt man in Flutter Plugins wie `screenshot` oder `repaint_boundary`.
    
- Für das Teilen an Instagram/WhatsApp nutzt man das Plugin `share_plus`.
    
- Für Strava nutzt Claude Code die offizielle REST-API zur Hintergrund-Synchronisation.