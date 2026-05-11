---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# 🔄 State Machine (Orchestrator)

up:: [[Orchestrator]]
tags: #workflow #state-machine

---

## Zustandsdiagramm

```
┌─────────────────────────────────────────────┐
│                  DISCOVERY                   │
│  spawn: lead-finder                          │
│  warten: [STATUS: LEADS_IDENTIFIED]          │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│                  SCANNING                    │
│  spawn: website-scanner (eine URL)           │
│  warten: [STATUS: SCAN_COMPLETE]             │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│                  CHECKING                    │
│  spawn: law-checker (JSON aus SCANNING)      │
│  warten: [STATUS: CHECK_COMPLETE]            │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│                  EVIDENCE                    │
│  spawn: screenshot-tool (Verstöße + URLs)    │
│  warten: [STATUS: SCREENSHOTS_COMPLETE]      │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│                  OUTREACH                    │
│  spawn: email-sender / report-builder        │
│  warten: [STATUS: EMAIL_SENT]                │
│       oder [STATUS: REPORT_GENERATED]        │
└──────────────────────┬──────────────────────┘
                       ↓ (nur bei Kauf)
┌─────────────────────────────────────────────┐
│                  FIXING                      │
│  spawn: fixer                                │
│  warten: [STATUS: FIX_COMPLETE]              │
└──────────────────────┬──────────────────────┘
                       ↓
               [STATUS: WORKFLOW_DONE]
```

---

## Error-States

| Fehler | Reaktion |
|--------|---------|
| Agent Timeout | Teilergebnis akzeptieren → nächster State |
| Score < 30 | Immer akzeptieren (auch ohne Screenshots) |
| Screenshot nach 3× fehlgeschlagen | Lead SKIP → nächster Lead |
| URL blockiert (403) | Diese URL SKIP → nächste URL |

---

## Status-Token Übersicht

| Token | Agent |
|-------|-------|
| `[STATUS: LEADS_IDENTIFIED]` | Lead-Finder |
| `[STATUS: SCAN_COMPLETE]` | Website-Scanner |
| `[STATUS: CHECK_COMPLETE]` | Law-Checker |
| `[STATUS: SCREENSHOTS_COMPLETE]` | Screenshot-Tool |
| `[STATUS: AUDIT_COMPLETE]` | UX-Auditor |
| `[STATUS: MONITOR_COMPLETE]` | Law-Monitor |
| `[STATUS: FIX_COMPLETE]` | Fixer-Bot |
| `[STATUS: WORKFLOW_DONE]` | Email-Sender / Orchestrator |
