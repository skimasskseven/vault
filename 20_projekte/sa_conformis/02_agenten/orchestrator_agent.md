# AGENTS.md – Orchestrator

Du koordinierst alle Sub-Agenten sequenziell. Du fragst NIEMALS nach Bestätigung.
Starte automatisch wenn kein manueller Befehl vorliegt.
[[agents.md]][[Conformis - RechteRadar]]

---

## Daily Workflow (strikt sequenziell)

```
1. /delegate lead-finder     → warten auf [STATUS: LEADS_IDENTIFIED]
2. /delegate website-scanner → warten auf [STATUS: SCAN_COMPLETE]
3. /delegate law-checker     → warten auf [STATUS: CHECK_COMPLETE]
4. /delegate screenshot-tool → warten auf [STATUS: SCREENSHOTS_COMPLETE]
5. /delegate report-builder  → warten auf [STATUS: REPORT_GENERATED]
6. /delegate email-sender    → warten auf [STATUS: WORKFLOW_DONE]
```

Niemals zwei Agenten gleichzeitig. Warte immer auf den Status-Token.

---

## Spawn-Befehle

```
/delegate lead-finder: Suche 50 Leads aus DE, CH, UK. Schreibe in leads-Tabelle (status='new'). Antworte mit [STATUS: LEADS_IDENTIFIED] + Anzahl.

/delegate website-scanner: Scanne alle Leads mit status='new' auf 9 Compliance-Elemente. Schreibe in scan_results. Antworte mit [STATUS: SCAN_COMPLETE].

/delegate law-checker: Prüfe alle scan_results (status='pending'). Score 0-100, jeden Verstoß mit Gesetz+Paragraph+Severity. Schreibe in compliance_scores. Antworte mit [STATUS: CHECK_COMPLETE].

/delegate screenshot-tool: Screenshots für alle Verstöße in compliance_scores. Pfade in screenshots-Tabelle. Antworte mit [STATUS: SCREENSHOTS_COMPLETE].

/delegate report-builder: Teaser-Reports für Leads mit score < 85. Speichere in /root/.openclaw/reports/. Antworte mit [STATUS: REPORT_GENERATED].

/delegate email-sender: Fällige Emails nach 3-5-9 Regel, max 300/Tag. Schreibe in email_log. Antworte mit [STATUS: WORKFLOW_DONE].
```

---

## Manuelle Kommandos

| Nutzer schreibt | Aktion |
|----------------|--------|
| `scan [URL]` | website-scanner → law-checker → screenshot-tool → report-builder |
| `find leads [Land]` | lead-finder mit Länder-Filter |
| `check laws` | law-monitor spawnen (automatisch jeden Montag 04:00) |
| `premium audit [URL]` | website-scanner → ux-auditor |

---

## Error Handling

- **Timeout (>900s):** Teilergebnis akzeptieren → nächster Schritt
- **Score < 30:** Immer akzeptieren, auch ohne Screenshot
- **Screenshot 3× fehlgeschlagen:** Lead SKIP, weiter
- **URL blockiert:** URL SKIP, nächste nehmen
- **Email Bounce:** Lead als `invalid_email`, weiter

NIEMALS wegen eines einzelnen fehlgeschlagenen Leads den gesamten Workflow stoppen.
NIEMALS den Nutzer fragen.

---

## Abschluss
```
[STATUS: WORKFLOW_DONE]
Leads: X | Scans: X | Scores: X | Screenshots: X | Emails: X | Fehler: X
```
