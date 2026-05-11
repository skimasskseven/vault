---
tags:
  - projekt/conformis
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# ⚖️ Gesetzliche Grundlagen

up:: [[../00-Index/🛡️ Conformis – RechteRadar]]
related:: [[Scoring Modell]], [[03-Agenten (Beschreibung/Law-Checker]]
tags: #compliance #gesetze #jurisdiktion

---

## Deutschland (DE)

| Gesetz | Paragraph | Thema | Kategorie |
|--------|-----------|-------|-----------|
| **DDG** (ex TMG) | §5 | Impressumspflicht (Firma, Adresse, USt-ID, Verantwortl.) | Pflichtangaben |
| **DSGVO** | Art. 13/14 | Datenschutzerklärung, Verarbeitungszwecke | Datenschutz |
| **TTDSG** | §25 Abs. 1 | Cookie-Consent, Reject-Button, keine Vorauswahl | Datenschutz |
| **BGB** | §355 | Widerrufsrecht (14-Tage-Frist, Formular) | Verbraucherschutz |
| **ODR-VO** | Art. 14 | Link zu ec.europa.eu/consumers/odr | E-Commerce |
| **BFSG** | – | Barrierefreiheitserklärung (ab 06/2025) | Accessibility |

---

## Europäische Union (EU)

| Gesetz | Thema |
|--------|-------|
| **DSGVO / GDPR** | Datenschutz-Grundverordnung |
| **VO (EU) Nr. 524/2013** | ODR-Verordnung (Online Dispute Resolution) |
| **ePrivacy-RL** | Cookie-Consent Grundlage |

---

## Großbritannien (UK)

| Gesetz | Thema |
|--------|-------|
| **Companies Act** | §82 – Pflichtangaben auf Websites |
| **UK GDPR** | Datenschutz (post-Brexit) |
| **CCR 2013** | Consumer Contracts Regulations (Widerrufsrecht) |
| **Equality Act 2010** | Accessibility |

---

## Schweiz (CH)

| Gesetz | Thema |
|--------|-------|
| **neuDSG** | Datenschutzgesetz (ab Sept. 2023) |
| **UWG Art. 3** | Pflichtangaben, Transparenz |
| **WAG** | Verbraucherschutz |

---

## USA (US)

| Gesetz | Thema |
|--------|-------|
| **CCPA** | California Consumer Privacy Act |
| **FTC Guidelines** | E-Commerce Transparenz |
| **ADA** | Americans with Disabilities Act (Accessibility) |

---

## Typische Verstöße → Gesetz-Mapping

| Verstoß | Gesetz | Schwere |
|---------|--------|---------|
| Impressum fehlt komplett | DDG §5 | kritisch |
| USt-ID fehlt | DDG §5 Nr. 6 | schwer |
| Kein Ablehnen-Button (Cookie) | TTDSG §25 Abs. 1 | schwer |
| Cookie-Banner mit Vorauswahl | TTDSG §25 Abs. 1 | schwer |
| Kein ODR-Link | Art. 14 ODR-VO | mittel |
| Kein Widerrufsformular | BGB §355 Abs. 2 | schwer |
| Kein Barrierefreiheits-Statement | BFSG | leicht |
| Kein HTTPS | – (Best Practice) | mittel |
| Kein HSTS | – (Best Practice) | leicht |

---

## Überwachte Quellen (Law-Monitor)

| Land | Quelle |
|------|--------|
| 🇪🇺 EU | EUR-Lex (SPARQL) |
| 🇩🇪 DE | DIP Bundestag API |
| 🇬🇧 UK | legislation.gov.uk |
| 🇨🇭 CH | Fedlex |
| 🇺🇸 US | Federal Register API |
