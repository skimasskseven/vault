---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# AGENTS.md – UX-Auditor (Premium)

Gestartet vom Orchestrator bei Premium Audit (€119/Mo) oder `premium audit [URL]`.
Vollständige UX-Analyse in 6 Kategorien, Score 0–100.
VOLLAUTOMATISCH. Keine Rückfragen.

---
[[agents.md]][[Conformis - RechteRadar]]
## Workflow

**1. Daten laden:**
```sql
SELECT l.id, l.url, l.company_name, l.country, sr.business_model
FROM leads l JOIN scan_results sr ON sr.lead_id = l.id
WHERE l.id = LEAD_ID;
```

**2. Screenshots & Performance-Daten sammeln:**
```bash
mkdir -p /root/.openclaw/ux-audits/LEAD_ID

# Desktop
cd /app && npx playwright screenshot --full-page "URL" /root/.openclaw/ux-audits/LEAD_ID/desktop.png

# Mobile (375x812)
cd /app && npx playwright screenshot --viewport-size="375,812" \
  --user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)" \
  "URL" /root/.openclaw/ux-audits/LEAD_ID/mobile.png

# PageSpeed
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL&key=${GOOGLE_API_KEY}&strategy=mobile" \
  > /root/.openclaw/ux-audits/LEAD_ID/pagespeed.json
```

**3. 6 Kategorien prüfen (je 0–10 Punkte):**

| # | Kategorie | Kriterien (+Punkte) |
|---|-----------|-------------------|
| 1 | **Farbschema** | Konsistente Palette <5 Farben (+3), WCAG AA Kontrast 4.5:1 (+3), Markenfarben durchgehend (+2), kein reines Schwarz/Weiß (+2) |
| 2 | **Lesbarkeit** | Body min 16px (+4), Zeilenhöhe min 1.5x (+2), Absatzabstände ok (+2), Max-Width Textspalte (+2) |
| 3 | **Mobile** | Viewport-Meta vorhanden (+2), min 3 Breakpoints (+3), Touch-Targets ≥44×44px (+3), kein horizontales Scrollen (+2) |
| 4 | **Loading Speed** | PageSpeed >90 (+10), 75–90 (+7), 50–74 (+4), <50 (+0–3) |
| 5 | **Conversion** | Klarer CTA above fold (+3), Trust-Signale sichtbar (+3), Checkout ≤3 Schritte (+2), kein Pop-up on load (+2) |
| 6 | **Accessibility** | ≥90% Alt-Texte (+3), Keyboard-Nav (+2), ARIA-Labels (+2), semantisches HTML5 (+2), sichtbarer Focus (+1) |

**4. Gesamt-Score berechnen:**
```
GESAMT = (Summe aller 6 Kategorien) × 1.67
Beispiel: (7+6+8+5+6+7) × 1.67 = 65
```

| Score | Klasse |
|-------|--------|
| 85–100 | `excellent` |
| 65–84 | `good` |
| 40–64 | `needs_work` |
| 0–39 | `poor` |

**5. Top 3 Prioritäten:** Die 3 Kategorien mit niedrigstem Score → impact + effort bewerten.
Priorisierung: high impact + low effort = sofort angehen.

**6. In DB speichern:**
```sql
INSERT INTO ux_audits
  (lead_id, score_color, score_read, score_mobile, score_speed, score_conv, score_a11y,
   total_score, score_class, top3_json, screenshots_path, created_at)
VALUES (LEAD_ID, 7, 6, 8, 5, 6, 7, 65, 'needs_work', '[...]',
        '/root/.openclaw/ux-audits/LEAD_ID/', NOW());

UPDATE leads SET status='audited' WHERE id=LEAD_ID;
```

**7. Top-3-Empfehlungen ins Admin-Dashboard einreihen:**
Jede Top-3-Priorität wird zusätzlich als `client_customizations`-Eintrag mit
`delivery_mode` angelegt – gleiche 3-Modi-Pipeline wie [[fixer_bot_agent|Fixer-Bot]].
Auslieferung an den Kunden erst nach Operator-Freigabe im
[[admin_dashboard|Admin-Dashboard]].

```sql
INSERT INTO client_customizations
  (lead_id, violation_type, platform, delivery_mode,
   new_content, instructions,
   before_screenshot_path, after_screenshot_path,
   qa_status, created_at)
VALUES
  (LEAD_ID, 'cta_above_fold_missing', 'shopify', 'dashboard_access',
   NULL,
   'CTA-Button ins Hero-Banner einfügen, Theme-Settings → Hero',
   '/root/.openclaw/ux-audits/LEAD_ID/desktop.png',
   '/root/.openclaw/ux-audits/LEAD_ID/mockups/cta_after.png',
   'pending_review', NOW());
```

Modus-Heuristik analog zum Fixer-Bot: technische Snippets → `code_snippet`,
inhaltliche Empfehlungen → `instruction_only`, Theme-/Layout-Eingriffe → `dashboard_access`.

---

## Abschluss
```
[STATUS: AUDIT_COMPLETE]
Lead: FIRMENNAME | Score: X/100 (KLASSE)
Farbe: X | Lesbarkeit: X | Mobile: X | Speed: X | Conversion: X | A11y: X
Top-Priorität: ISSUE (impact: X, effort: X)
```
