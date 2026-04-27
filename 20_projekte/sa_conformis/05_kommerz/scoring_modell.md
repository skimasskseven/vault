# 📊 Scoring Modell

up:: [[../00-Index/🛡️ Conformis – RechteRadar]]
related:: [[03-Agenten (Beschreibung/Law-Checker]], [[Gesetzliche Grundlagen]]
tags: #compliance #scoring

---

## 100-Punkte-System

| Kategorie | Max Punkte | Gesetze |
|-----------|-----------|---------|
| **Pflichtangaben** | 35 | DDG §5 (ex TMG), Companies Act §82, UWG Art.3 |
| **Datenschutz** | 30 | DSGVO Art.13/14, UK GDPR, neuDSG, CCPA |
| **Verbraucherschutz** | 15 | BGB §355, CCR 2013, WAG |
| **E-Commerce** | 10 | ODR-VO, FTC Guidelines |
| **Accessibility** | 5 | BFSG, Equality Act 2010, ADA |
| **Technisch** | 5 | HTTPS, HSTS, Security Headers |
| **GESAMT** | **100** | |

---

## Score-Klassen

| Score | Klasse | Emoji | Bedeutung |
|-------|--------|-------|-----------|
| 85–100 | Gut konform | 🟢 | Kein dringender Handlungsbedarf |
| 60–84 | Verbesserungsbedarf | 🟡 | Lücken vorhanden |
| 30–59 | Kritische Lücken | 🔴 | Dringend handeln |
| 0–29 | Akuter Handlungsbedarf | ⚫ | Sofortmaßnahmen nötig |

---

## Beispiel-Berechnung (DE)

```
Pflichtangaben (35):
  Firma ja(10) + Adresse ja(10) + Kontakt ja(10) + USt-ID nein(0) + Verantwortl. ja(5) = 35 − 5 = 30
  → Verstoß: "Fehlende USt-ID (§5 DDG Nr. 6)" → −5 Punkte

Datenschutz (30):
  Policy ja(15) + Consent ja(5) + Reject nein(0) + No-Precheck nein(0) + DPO ja(10) = 30 − 10 = 20
  → Verstoß: "Kein Ablehnen-Button (TTDSG §25 Abs. 1)" → −5
  → Verstoß: "Cookie-Banner mit Vorauswahl (TTDSG §25 Abs. 1)" → −5

Verbraucherschutz (15):
  Widerruf ja(8) + Frist ja(7) = 15 → 0 Abzug

E-Commerce (10):
  ODR nein(0) + Streitbeilegung nein(0) = 10 − 10 = 0
  → Verstoß: "Kein Link zur ODR-Plattform (Art. 14 ODR-VO)" → −5
  → Verstoß: "Kein Text zur Streitbeilegung (Art. 14 ODR-VO)" → −5

Accessibility (5): Statement nein(0) → −5
Technisch (5): HTTPS ja(3) + HSTS nein(0) → −2

TOTAL: 83/100 → 🟡 Verbesserungsbedarf
Verstöße: 6 dokumentiert
```

---

## Severity-Stufen

| Stufe | Bedeutung | Typische Verstöße |
|-------|-----------|------------------|
| `leicht` | Kleinere Mängel | Fehlende HSTS-Header |
| `mittel` | Sichtbare Lücken | Kein ODR-Link |
| `schwer` | Klare Verstöße | Impressum unvollständig |
| `kritisch` | Sofortige Gefahr | Kein Impressum, kein Datenschutz |
