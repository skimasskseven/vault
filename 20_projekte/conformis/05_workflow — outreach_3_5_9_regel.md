---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# 📬 Outreach 3-5-9 Regel

up:: [[../00-Index/🛡️ Conformis – RechteRadar]]
related:: [[03-Agenten (Beschreibung/Email-Sender]]
tags: #workflow #outreach #email

---

## Zeitplan

| Stage | Timing | Betreff-Strategie | CTA |
|-------|--------|------------------|-----|
| **Stage 1** | Tag 0 (sofort nach Scan) | „Möglicher Compliance-Hinweis für [Firma]" | Kostenlosen Full-Check anfordern |
| **Stage 2** | +3 Tage nach Stage 1 | „Erinnerung: Offene Compliance-Punkte" | Jetzt handeln |
| **Stage 3** | +5 Tage nach Stage 2 | „Letzte Information: Compliance-Status" | Basic Guard buchen |
| **Stage 4** | +9 Tage nach Stage 3 | Kein weiterer Kontakt | — |

---

## Teaser-Strategie (Wirtschaftlichkeits-Prämisse)

```
1 Verstoß:
  → KEINEN konkret nennen, nur einen allgemeinen Hinweis
  → KEIN Screenshot, KEINE Gesetzesreferenz in der Mail
  → Ziel: Neugier → Token-Page öffnen → Pricing sehen

2+ Verstöße:
  → EINEN LEICHTEN Verstoß als Köder nennen (kein schwerer/kritischer!)
  → Anzahl der Punkte nennen ("X regulatorische Punkte aufgefallen")
  → Hinweis auf "weitere Punkte mit Bußgeld-Bezug" in der Vollauswertung
  → Schwere/kritische Verstöße bleiben Verkaufs-Joker auf der Token-Page
```

**Begründung:** Conformis verkauft die Auflösung der Lücke, nicht die Information.
Wer den schwersten Verstoß bereits in der Mail liest, hat keinen Anreiz mehr,
den Full-Report zu kaufen. Ein leichter Verstoß als Köder demonstriert
Glaubwürdigkeit, ohne die Verhandlungs­position aufzugeben.

**Edge-Case:** Wenn nur schwere/kritische Verstöße vorliegen (selten), wird
generisch formuliert ("X Punkte mit Bußgeld-Bezug"), ohne einen konkret zu
nennen.

---

## Email-Regeln

- ✅ Sprache des Empfängers (DE/EN/FR)
- ✅ Persönliche Anrede (Firmenname)
- ✅ Immer Disclaimer: „Keine Rechtsberatung"
- ❌ Niemals bedrohlich
- ❌ Niemals Feiertage/Wochenende? → Laut Code: **erlaubt** (Orchestrator AGENTS.md)
- ❌ Bei Bounce: `invalid_email` setzen, weitermachen

---

## Upsell-Pfad

```
Stage 1 Email
    ↓ Kein Kauf
Stage 2 Email
    ↓ Kein Kauf  
Stage 3 Email → One-Time Fix (€29,99)
    ↓ Kauf
Fixer-Bot → Telegram QA → Report an Kunden
    ↓ Nach Fix
Upsell: Basic Guard (€14,99/Mo)
    ↓
Premium Audit (€119/Mo)
```
