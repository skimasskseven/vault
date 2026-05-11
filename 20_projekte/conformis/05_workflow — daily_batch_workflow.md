---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# ⚙️ Daily Batch Workflow

up:: [[../00-Index/🛡️ Conformis – RechteRadar]]
related:: [[Orchestrator]]
tags: #workflow #automation

---

## Tagesablauf (automatisch, täglich)

```
06:00 ─── Lead-Finder ──────────────────────────────────────
           50 neue Firmen aus DE/CH/UK Registern finden
           → DB: leads-Tabelle befüllen

06:30 ─── Website-Scanner ──────────────────────────────────
           Alle heute gefundenen Sites auf Compliance prüfen
           → DB: scan_results befüllen

07:00 ─── Screenshot-Tool ──────────────────────────────────
           Für jeden Verstoß einen Beweis-Screenshot
           → DB: screenshots befüllen

07:30 ─── Law-Checker ──────────────────────────────────────
           Compliance-Score 0-100 + Verstöße dokumentieren
           → DB: compliance_scores befüllen

08:00 ─── Email-Sender ─────────────────────────────────────
           Fällige Emails nach 3-5-9 Regel versenden
           → DB: email_log befüllen, outreach_stage +1
```

---

## Lead-Status-Flow

```
new
 ↓ (Lead-Finder)
scanned
 ↓ (Website-Scanner)
scored
 ↓ (Law-Checker)
screenshoted
 ↓ (Screenshot-Tool)
contacted
 ↓ (Email-Sender Stage 1)
[outreach_stage: 1 → 2 → 3 → 4]
```

---

## Wöchentlich (Montag 04:00 Uhr)

```
Law-Monitor → Alle Regierungsquellen pollen
           → Neue Gesetze in upcoming_laws speichern
           → Bei "approved": Orchestrator benachrichtigen
```

---

## Backup (alle 2 Tage via Cron)

- Volumes + Screenshots separat
- Email-Benachrichtigung: `maximeisner197@gmail.com`
- Alte Backups (> 14 Tage) automatisch löschen
