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

## Teaser-Strategie

```
1-2 Verstöße:
  → Nur andeuten: "Wir haben einen möglichen Hinweis gefunden"
  → KEINE Details, KEIN Screenshot
  → Ziel: Neugier → Full-Report kaufen (€29,99)

3+ Verstöße:
  → EINEN Verstoß konkret nennen (den schwersten)
  → EINEN Screenshot als Beweis anhängen
  → Rest: "Darüber hinaus haben wir weitere Punkte identifiziert..."
  → Full-Report (€29,99) enthält ALLE Verstöße + Fix-Vorschläge
  → After-Fix-Upsell: Basic Guard (€14,99/Mo)
```

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
