---
type: skill
tags:
  - projekt/research-monster
  - type/skill
  - skill/account-creation
  - domain/account-automation
  - status/prepared
---

# account-creation — Skill

**Status:** ⚠️ **PREP** — dokumentiert, ohne aktive API-Keys.

Wird genutzt von [[20_projekte/research-monster/03_agents.md — accounts|accounts]].

## Stack

### 1. Nstbrowser — Fingerprint-Spoofing

| | |
|---|---|
| URL | https://nstbrowser.io |
| Funktion | Einzigartige Browser-Fingerprints pro Session |
| Spoofed | Canvas, WebGL, User-Agent, Screen Resolution, Fonts, Timezone, WebRTC |
| Kosten | Free Tier: unlimited profiles |
| API | Verfügbar für Automation |
| Proxy | Integrierter Proxy-Stack + eigene Proxies möglich |
| Aktiv wenn | `NSTBROWSER_API_KEY` in `.env` |

### 2. FreeCustom.Email — Disposable Mail + OTP

| | |
|---|---|
| URL | https://freecustom.email |
| API | `https://api.freecustom.email` |
| Funktion | Disposable Inboxes, OTP-Auto-Extract |
| Kosten | Free, ~1 Inbox/Sekunde |
| Features | CLI, REST, WebSocket, OTP-Parsing |
| Aktiv wenn | `FCE_API_KEY` in `.env` |

CLI:
```bash
fce inbox add random
fce otp <address>
fce inbox remove <address>
```

Python SDK:
```python
from freecustom_email import FreeCustomEmail
fce = FreeCustomEmail()
email = f"bot-{int(time.time())}@ditmail.info"
await fce.inboxes.register(email)
otp = await fce.otp.wait_for(email, timeout=30)
await fce.otp.unregister(email)
```

### 3. CapSolver — Captcha-Solving

| | |
|---|---|
| URL | https://capsolver.com |
| Typen | reCAPTCHA v2/v3, Cloudflare Turnstile, hCaptcha, GeeTest |
| Preise | reCAPTCHA v2: ~$0.80/1000, Turnstile: ~$1.20/1000 |
| Speed | <10 s pro Captcha |
| Aktiv wenn | `CAPSOLVER_API_KEY` in `.env` |

API-Call:
```python
import capsolver
capsolver.api_key = "CAPSOLVER_API_KEY"

solution = capsolver.solve({
    "type": "ReCaptchaV2Task",
    "websiteURL": "https://example.com",
    "websiteKey": "SITE_KEY"
})
# {"token": "...", "userAgent": "..."}
```

## Workflow (wenn aktiv)

```
1. Nstbrowser: Unique Fingerprint generieren
2. Proxy zuweisen (Residential / Datacenter)
3. FCE: Disposable Inbox erstellen
4. Browser mit Fingerprint öffnen
5. Registrierungsformular ausfüllen (spoofed Daten)
6. Captcha erkennen → CapSolver → Token injizieren
7. Formular absenden
8. OTP aus Inbox extrahieren
9. Verifizierung abschließen
10. Session-Cookies persistieren (data/sessions/)
```

## Kosten pro Account (Schätzung)

| Komponente | Kosten |
|---|---|
| Nstbrowser | $0 |
| Proxy | $0.01 – $0.05 |
| E-Mail | $0 |
| Captcha | ~$0.001 |
| **Total** | **~$0.011 – $0.051** |

## Quelldatei

`/root/research-monster/skills/account-creation.md`
