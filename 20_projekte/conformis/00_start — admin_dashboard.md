---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# 🛠️ Admin-Dashboard

up:: [[system_uebersicht]]
tags: #architektur #dashboard #operator

Operator-UI (aktuell alleiniger Operator: Max). Zentraler Review- und
Steuerungspunkt für **alle Fix-Vorschläge** aus Fixer-Bot und UX-Auditor.
**Keine Auslieferung an Kunden ohne Operator-Approve.**

Das Dashboard ist **kein OpenClaw-Agent**, sondern eine separate Webapp, die
direkt auf Postgres zugreift und Agenten gezielt re-triggern kann.

---

## Zweck

1. Fix-Vorschläge aus dem [[fixer_bot_agent|Fixer-Bot]] reviewen
   (Vorher/Nachher-Bilder, Code/Anleitung, Plattform).
2. UX-Auditor-Empfehlungen in dieselbe 3-Modi-Pipeline einreihen.
3. Pro Vorschlag freigeben / ablehnen / zurückweisen.
4. Bei `dashboard_access`: händische Anwendung im Kunden-Dashboard tracken.
5. Re-Verifikation triggern und Ergebnis sehen.

---

## Datenquelle

| Tabelle                  | Lese-Zugriff             | Schreib-Zugriff |
|--------------------------|--------------------------|------------------|
| `client_customizations`  | alle Felder              | `qa_status`, `qa_comment`, `operator_assignee`, `reviewed_at`, `applied_at`, `verified_at` |
| `ux_audits`              | Top-3 Empfehlungen       | – |
| `screenshots`            | für Vorher/Nachher       | – |
| `leads`                  | Kontext                  | `status` (nach `verified` → `fixed`) |
| `email_log`              | Auslieferungsnachweis    | – |
| `lead_credentials`       | encrypted_payload (Klartext nur in Operator-Session) | `expires_at`, `revoked_at`, `last_accessed_at` |

---

## Workflow nach Modus

### `code_snippet` und `instruction_only`

```
Fixer/UX-Auditor → INSERT (qa_status='pending_review')
    ↓
Operator sieht im Dashboard: Vorher-Screenshot, Nachher-Preview, Code/Anleitung, Plattform
    ↓
✅ approve  → qa_status='approved'
   → Email-Sender löst Auslieferung aus (Template `fix_delivery` + Snippet/Anleitung)
   → applied_at = Zeitpunkt Mail-Versand
   → Re-Scan nach 7 Tagen
❌ reject   → qa_status='rejected' + qa_comment
   → Fixer regeneriert (max. 2 Iterationen) ODER Operator wechselt Modus manuell
```

### `dashboard_access`

```
Fixer → INSERT mit Operator-Briefing (qa_status='pending_review')
    ↓
✅ approve  → Operator-Queue
    ↓
Operator fordert Zugang vom Kunden an (plattformspezifisches Standard-Template)
    ↓
Kunde legt Zweitprofil mit eingeschränkten Rechten an, sendet Login
    ↓
Login wird verschlüsselt im Vault abgelegt (access_credentials_ref in DB)
    ↓
Operator führt Fix händisch aus, macht echten Nachher-Screenshot
    ↓
applied_at = Zeitpunkt Anwendung
    ↓
Re-Scan triggern
```

---

## Re-Verifikation (Rückkanal)

Nach `applied_at` triggert das Dashboard automatisch:

```bash
# Gezielter Re-Scan nur des betroffenen Verstoßes
spawn website-scanner --lead LEAD_ID --check VIOLATION_TYPE
spawn ux-auditor      --lead LEAD_ID --re-audit   # nur bei Premium
```

Auswertung:

| Ergebnis | `qa_status` | Folge |
|----------|-------------|-------|
| Verstoß **nicht mehr** in `scan_results.violations` | `verified`            | `verified_at=NOW()`, Lead-Status → `fixed` |
| Verstoß **noch da**                                 | `failed_verification` | zurück in Operator-Queue mit Diff-Kommentar |

---

## UI-Sektionen

| Sektion | Inhalt |
|---------|--------|
| **Inbox**                  | Alle `pending_review`-Vorschläge, sortiert nach `created_at` desc |
| **In Bearbeitung**         | `approved` + `dashboard_access`, noch nicht `applied` |
| **Wartet auf Verifikation**| `applied`, noch kein Re-Scan-Ergebnis |
| **Erledigt**               | `verified` (letzte 30 Tage) |
| **Probleme**               | `rejected`, `failed_verification` |
| **Lead-Detail**            | Pro Lead: alle Verstöße + Status-Timeline + Vorher/Nachher-Galerie |

---

## Schnittstellen

| Quelle/Ziel                | Schnittstelle                                    | Zweck |
|----------------------------|--------------------------------------------------|-------|
| Fixer-Bot → Dashboard      | `client_customizations` insert                   | Vorschlag einliefern |
| UX-Auditor → Dashboard     | `ux_audits` + Top-3 in `client_customizations`   | Audit-Empfehlungen einreihen |
| Dashboard → Email-Sender   | Trigger `auto_deliver_fix(customization_id)`     | Auslieferung Code/Anleitung |
| Dashboard → Website-Scanner| Trigger `re_verify(lead_id, violation_type)`     | Re-Verifikation |
| Dashboard → UX-Auditor     | Trigger `re_audit(lead_id)`                      | Premium-Re-Audit |
| Dashboard → Fixer-Bot      | Trigger `regenerate(customization_id, reason)`   | Bei Reject |

---

## Sicherheit

- Operator-Login: Email + 2FA (TOTP).
- Audit-Log: jede Statusänderung mit Zeitstempel + Operator-ID
  (zukünftig in separater `audit_log`-Tabelle).
- Kunden-Credentials für `dashboard_access`: verschlüsselt mit Master-Key
  (`VAULT_KEY` in `.env`). Klartext nur kurzfristig in der Operator-Browser-Session.
- Zweitprofil-Anforderung an Kunden: **immer** mit eingeschränkten Rechten
  (siehe Tabelle in [[fixer_bot_agent]]). Niemals Admin/Owner-Zugang akzeptieren.
- Disclaimer "Keine Rechtsberatung" in jedem ausgelieferten Snippet/jeder Anleitung.
