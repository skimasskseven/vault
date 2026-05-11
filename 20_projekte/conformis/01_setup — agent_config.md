---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# ⚙️ Agent Config

up:: [[../00-Index/🛡️ Conformis – RechteRadar]]
tags: #config #openclaw

---

## openclaw.json – Struktur

```json
{
  "meta": {
    "lastTouchedVersion": "2026.3.31",
    "lastTouchedAt": "2026-04-26T09:00:00.000Z"
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/nvidia/nemotron-3-super-120b-a12b:free"
      },
      "timeoutSeconds": 900,
      "sandbox": {
        "mode": "off"
      }
    },
    "list": [
      {
        "id": "orchestrator",
        "workspace": "/root/.openclaw/workspaces/orchestrator",
        "default": true
      },
      {
        "id": "lead-finder",
        "workspace": "/root/.openclaw/workspaces/lead-finder"
      },
      {
        "id": "website-scanner",
        "workspace": "/root/.openclaw/workspaces/website-scanner"
      },
      {
        "id": "screenshot-tool",
        "workspace": "/root/.openclaw/workspaces/screenshot-tool"
      },
      {
        "id": "law-checker",
        "workspace": "/root/.openclaw/workspaces/law-checker"
      },
      {
        "id": "law-monitor",
        "workspace": "/root/.openclaw/workspaces/law-monitor"
      },
      {
        "id": "report-builder",
        "workspace": "/root/.openclaw/workspaces/report-builder"
      },
      {
        "id": "email-sender",
        "workspace": "/root/.openclaw/workspaces/email-sender"
      },
      {
        "id": "fixer",
        "workspace": "/root/.openclaw/workspaces/fixer"
      },
      {
        "id": "ux-auditor",
        "workspace": "/root/.openclaw/workspaces/ux-auditor"
      }
    ]
  },
  "browser": {
    "enabled": true,
    "headless": true,
    "noSandbox": true
  },
  "acp": {
    "enabled": true,
    "dispatch": { "enabled": true },
    "backend": "acpx",
    "allowedAgents": [
      "*"
    ]
  },
  "gateway": {
    "mode": "local",
    "bind": "lan",
    "port": 18789,
    "auth": {
      "mode": "token",
      "token": "3f28a71a95d228f1762c66eccb8ce5733aa8966e3702a133"
    },
    "controlUi": {
      "enabled": true,
      "allowedOrigins": [
        "http://localhost:18795",
        "http://127.0.0.1:18795",
        "*"
      ]
    }
  },
  "plugins": {
    "entries": {
      "acpx": {
        "enabled": true,
        "config": {
          "permissionMode": "approve-all"
        }
      },
      "browser": {
        "enabled": true
      }
    }
  },
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": [
        "orchestrator",
        "lead-finder",
        "website-scanner",
        "law-checker",
        "screenshot-tool",
        "email-sender",
        "law-monitor",
        "report-builder",
        "ux-auditor",
        "fixer"
      ]
    }
  }
}```

---

## Gateway

| Setting | Wert |
|---------|------|
| Mode | `local` |
| Bind | `lan` |
| Port | `18789` |
| Auth | Token-basiert |
| Control UI | enabled, allowedOrigins: `*` |

---

## Browser

```json
{
  "browser": {
    "enabled": true,
    "headless": true,
    "noSandbox": true
  }
}
```

---

## ACP (Agent-to-Agent)

```json
{
  "acp": {
    "enabled": true,
    "backend": "acpx",
    "allowedAgents": ["*"]
  },
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": [
        "lead-finder", "website-scanner", "law-checker",
        "screenshot-tool", "email-sender", "law-monitor",
        "report-builder", "ux-auditor", "fixer"
      ]
    }
  }
}
```

---

## Wichtige Pfade im Container

| Pfad | Inhalt |
|------|--------|
| `/root/.openclaw/openclaw.json` | Haupt-Konfiguration |
| `/root/.openclaw/workspaces/` | Agent-Workspaces |
| `/root/.openclaw/screenshots/` | Beweis-Screenshots |
| `/root/.openclaw/reports/` | Kundendokumente |
| `/root/.openclaw/data/` | Laufzeitdaten |

---

## Modell-Defaults

| Setting | Wert |
|---------|------|
| Primär-Modell | `openrouter/minimax/minimax-m2.5:free` |
| Timeout | 900 Sekunden (15 Min) |
| Sandbox | `off` |
| Tool-Policy | `execute` (alle Tools erlaubt) |
