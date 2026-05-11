---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# 💰 Produkte & Preise

up:: [[../00-Index/🛡️ Conformis – RechteRadar]]
tags: #business #pricing

---

## Produktübersicht

| Produkt | Preis | Laufzeit | Leistung | Agent |
|---------|-------|----------|----------|-------|
| **One-Time Fix** | €29,99 | einmalig | Einmalige Behebung einer Lücke + Full-Report | [[Fixer-Bot\|Fixer-Bot]] |
| **Basic Guard** | €14,99/Mo | **6 Monate Mindestlaufzeit**, danach monatlich kündbar (1 Mo. Frist) | Dauer-Monitoring + Predictive Compliance | Orchestrator + Law-Monitor |
| **Premium Audit** | €119,00/Mo | monatlich kündbar (1 Mo. Frist) | Volle Compliance + monatliches UX-Audit | [[03-Agenten (Beschreibung/UX-Auditor\|UX-Auditor]] |

---

## Customer Journey

```
Lead entdeckt (Scan ergibt Verstöße)
    ↓
Stage 1 Email: Kostenloser Hinweis
    ↓
[Interesse] Full-Report anfordern
    ↓
One-Time Fix kaufen (€29,99) ────────── Fixer-Bot liefert Code/Anleitung
    ↓
Upsell: Basic Guard (€14,99/Mo) ─────── Dauerhaftes Monitoring
    ↓
Upsell: Premium Audit (€119/Mo) ─────── UX-Analyse + Top Compliance
```

---

## Report-Typen

| Typ | Inhalt | Verfügbarkeit |
|-----|--------|--------------|
| **Teaser** | 1 Verstoß + 1 Screenshot | Kostenlos (Stage 1 Email) |
| **Full-Report** | Alle Verstöße + Fix-Vorschläge | €29,99 |
| **Premium-Report** | Compliance + UX-Audit + Priorisierung | €119/Mo |

---

## Report-Details

- Speicherpfad: `/home/node/.openclaw/reports/{lead_id}_{date}.html`
- Ablauf: 48h nach Erstellung (`expires_at`)
- Format: HTML (per Link versendbar)
