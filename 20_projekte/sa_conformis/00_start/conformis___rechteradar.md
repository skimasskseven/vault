# 🛡️ Conformis – RechteRadar Scanner
> Automatisierter B2B-Compliance-Service für EU, UK, US und CH.

## Was ist Conformis?
Conformis scannt automatisch Websites, prüft sie auf rechtliche Lücken (Impressum, DSGVO, Cookie-Banner, AGB etc.), erstellt Beweis-Screenshots und kontaktiert Unternehmen mit einem kostenlosen Verbesserungsangebot.

---

## 🗺️ Vault Übersicht

### System
- [[Docker Setup]] – Container, Ports, Volumes
- [[Environment Variables]] – API Keys & Konfiguration
- [[02-Architektur/System Übersicht]] – Gesamtarchitektur, Datenfluss
- [[08-Config/Agent Config]] – `openclaw.json` & `config.json`

### Agenten (9)
| Agent | Datei |
|-------|-------|
| 🧠 Orchestrator | [[Orchestrator]] |
| 🔍 Lead-Finder | [[03-Agenten (Beschreibung/Lead-Finder]] |
| 🌐 Website-Scanner | [[03-Agenten (Beschreibung/Website-Scanner]] |
| 📸 Screenshot-Tool | [[03-Agenten (Beschreibung/Screenshot-Tool]] |
| ⚖️ Law-Checker | [[03-Agenten (Beschreibung/Law-Checker]] |
| 📡 Law-Monitor | [[03-Agenten (Beschreibung/Law-Monitor]] |
| 📧 Email-Sender | [[03-Agenten (Beschreibung/Email-Sender]] |
| 🔧 Fixer-Bot | [[Fixer-Bot]] |
| 🎨 UX-Auditor | [[03-Agenten (Beschreibung/UX-Auditor]] |

### Skills
- [[04-Skills.md/website-scanner]] · [[04-Skills.md/lead-finder]] · [[04-Skills.md/law-checker]]
- [[04-Skills.md/law-monitor]] · [[04-Skills.md/email-sender]] · [[04-Skills.md/screenshot-tool]]
- [[report-builder]] · [[fixer]] · [[04-Skills.md/ux-auditor]]

### Workflow & Business
- [[05-Workflow/Daily Batch Workflow]] – Tagesablauf 06:00–08:00
- [[05-Workflow/Outreach 3-5-9 Regel]] – Kontaktstrategie
- [[05-Workflow/State Machine]] – Orchestrator Zustandsmaschine
- [[06-Pricing/Produkte & Preise]] – One-Time Fix, Basic Guard, Premium Audit
- [[07-Compliance/Scoring Modell]] – 100-Punkte-System
- [[07-Compliance/Gesetzliche Grundlagen]] – DDG, DSGVO, TTDSG, ODR-VO

---

## 🚀 Schnellstart

```bash
# 1. API Keys eintragen
nano .env

# 2. Container starten
cd /app/compliance-guard
docker-compose up -d

# 3. UI aufrufen
http://<SERVER-IP>:18792
```

---

## ⚠️ Wichtige Hinweise
- **Keine Rechtsberatung** – Alle Outputs enthalten Disclaimer
- **DSGVO-konform** – Daten werden nach 30 Tagen gelöscht
- **Free-Tier-Modelle** – Gemini 2.5 Flash, OpenRouter Free Models

---

*Tags: #conformis #compliance #multi-agent #openclaw*
