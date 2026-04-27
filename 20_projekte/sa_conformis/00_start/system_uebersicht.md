# 🏗️ System Übersicht

up:: [[../00-Index/🛡️ Conformis – RechteRadar]]
tags: #architektur #system #agenten

---

## Agenten-Tabelle

| Agent                                                            | Modell | Aufgabe                          | Status-Token           |
| ---------------------------------------------------------------- | ------ | -------------------------------- | ---------------------- |
| [[Orchestrator\|🧠 Orchestrator]]                                |        | Koordination, Routing, Timing    | `WORKFLOW_DONE`        |
| [[03-Agenten (Beschreibung/Lead-Finder\|🔍 Lead-Finder]]         |        | Firmen in Registern finden       | `LEADS_IDENTIFIED`     |
| [[03-Agenten (Beschreibung/Website-Scanner\|🌐 Website-Scanner]] |        | Websites auf Compliance prüfen   | `SCAN_COMPLETE`        |
| [[03-Agenten (Beschreibung/Screenshot-Tool\|📸 Screenshot-Tool]] |        | Beweis-Screenshots               | `SCREENSHOTS_COMPLETE` |
| [[03-Agenten (Beschreibung/Law-Checker\|⚖️ Law-Checker]]         |        | Compliance-Score 0–100           | `CHECK_COMPLETE`       |
| [[03-Agenten (Beschreibung/Law-Monitor\|📡 Law-Monitor]]         |        | Neue Gesetze überwachen          | `MONITOR_COMPLETE`     |
| [[03-Agenten (Beschreibung/Email-Sender\|📧 Email-Sender]]       |        | Outreach-Emails (3-5-9)          | `WORKFLOW_DONE`        |
| [[Fixer-Bot\|🔧 Fixer-Bot]]                                      |        | Code-Snippets zur Fehlerbehebung | `FIX_COMPLETE`         |
| [[03-Agenten (Beschreibung/UX-Auditor\|🎨 UX-Auditor]]           |        | Design/UX-Analyse (Premium)      | `AUDIT_COMPLETE`       |

---

## Datenbankschema – Tabellen

| Tabelle | Befüllt von | Inhalt |
|---------|------------|--------|
| `leads` | Lead-Finder | company_name, url, email, country, status |
| `scan_results` | Website-Scanner | imprint_found, violations, language |
| `compliance_scores` | Law-Checker | score_total, score_class, violations |
| `screenshots` | Screenshot-Tool | file_path, violation_type |
| `email_log` | Email-Sender | email_to, subject, status, stage |
| `client_customizations` | Fixer | customization_type, new_content |
| `law_texts` | Law-Monitor | Gesetzestexte (jurisdiktionsbasiert) |
| `upcoming_laws` | Law-Monitor | Neue Gesetze (draft/approved) |
| `ux_audits` | UX-Auditor | Kategorie-Scores, Empfehlungen |

---

## Datenfluss (Happy Path)

```
Lead-Finder
    ↓ (50 Leads/Tag)
Website-Scanner
    ↓ (JSON: violations, business_model)
Law-Checker
    ↓ (Score + violations[]  mit law_text_excerpt)
Screenshot-Tool
    ↓ (PNG-Pfade pro Verstoß)
Email-Sender
    ↓ (Stage 1: Erstkontakt)
    → [Tag 5] Stage 2 → [Tag 9] Stage 3
    → [Kauf] Fixer-Bot / UX-Auditor
```

---

## Infrastruktur

```
VPS (IP: 72.61.87.130)
├── Docker Container: compliance-guard (Port 18789)
├── Docker Container: compliance-guard-db (Port 5432)
└── Control UI: Port 18792
```

---

## Workspace-Struktur (je Agent)

```
/root/.openclaw/workspaces/{agent-name}/
├── IDENTITY.md  → Rolle, Prüfkategorien, Output-Format
├── SOUL.md      → Persönlichkeit, Stil, Werte
├── AGENTS.md    → Workflow-Schritt-für-Schritt, Befehle
└── skills/
    └── SKILL.md → Eingebundene Skills (z.B. website-scanner)
```
