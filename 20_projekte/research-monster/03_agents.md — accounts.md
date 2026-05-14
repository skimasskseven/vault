---
type: agent
tags:
  - projekt/research-monster
  - type/agent
  - agent/accounts
  - domain/account-automation
  - status/prepared
---

# accounts — Account Creation (PREP)

- **Name:** Accounts
- **Creature:** Account Creation & Access Specialist
- **Vibe:** Effizient, unauffällig, präzise
- **Emoji:** 🎭
- **Modell:** Gemini 2.5 Flash
- **Workspace:** `/root/research-monster/workspaces/accounts/`
- **Status:** ⚠️ **PREP** — keine API-Keys gesetzt, keine aktiven Calls, keine Kosten

## Aufgabe

Automatisierte Account-Erstellung für Zugang zu Login-geschützten Quellen.
Aktuell ausschließlich dokumentiert — Aktivierung über `.env`-Keys.

## Stack-Übersicht

### Nstbrowser — Fingerprint-Spoofing
- URL: https://nstbrowser.io
- Funktion: Canvas, WebGL, UA, Screen, Fonts, Timezone, WebRTC spoofen
- Kosten: Free Tier (unlimited profiles)
- Aktivierung: `NSTBROWSER_API_KEY` in `.env`

### FreeCustom.Email (FCE) — Disposable Email + OTP
- API: `https://api.freecustom.email` (env: `FCE_API_URL`)
- Funktion: Disposable Inboxes, OTP-Auto-Extract via WebSocket
- Kosten: Free, ~1 Inbox/Sekunde
- Aktivierung: `FCE_API_KEY` in `.env`

### CapSolver — Captcha-Solving
- URL: https://capsolver.com
- Funktion: reCAPTCHA v2/v3, Cloudflare Turnstile, hCaptcha, GeeTest
- Kosten: ~$0.80/1000 reCAPTCHA, ~$1.20/1000 Turnstile
- Aktivierung: `CAPSOLVER_API_KEY` in `.env`

Skill-Spec: [[20_projekte/research-monster/04_skills.md — account-creation|account-creation]]

## Workflow (wenn aktiv)

```
1. Fingerprint (Nstbrowser) → 2. Proxy zuweisen
   → 3. Disposable E-Mail (FCE)
   → 4. Registrierungsformular ausfüllen
   → 5. Captcha lösen (CapSolver) → Token injizieren
   → 6. OTP aus Inbox extrahieren
   → 7. Verifizierung abschließen
   → 8. Session-Cookies persistieren (data/sessions/)
```

## Kosten pro Account (Schätzung)

| Komponente | Kosten |
|---|---|
| Nstbrowser | $0 |
| Proxy | $0.01 – $0.05 |
| E-Mail | $0 |
| Captcha | ~$0.001 |
| **Total** | **~$0.011 – $0.051** |

## Output (JSON)

```json
{
  "action": "account_created",
  "platform": "example.com",
  "email": "bot-123@ditmail.info",
  "session_saved": true,
  "cookies_path": "/root/research-db/sessions/example.com_123.json"
}
```

## Sicherheits-Regeln

- API-Keys ausschließlich in `.env`, nie in Code oder Compose.
- Aktuell keine aktiven Calls — Status pro Komponente per Key-Gate.

## Content Filter

[[20_projekte/research-monster/04_skills.md — content-filter|content-filter]].

## Quelldateien

- `workspaces/accounts/SOUL.md`
- `workspaces/accounts/AGENTS.md`
- `workspaces/accounts/IDENTITY.md`
