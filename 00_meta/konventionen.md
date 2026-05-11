---
tags:
  - type/meta
---

# Konventionen

Auto-generierte Dateien tragen oben den Banner:

`> 🤖 Auto-generiert – manuelle Edits werden überschrieben`

Diese Dateien werden bei jedem `build_knowledge_graph.py`-Lauf überschrieben. Wenn du eine kopierte Spec manuell weiter pflegen willst, entferne den Banner — dann respektiert das Script die Datei.

## Tag-Schema

- `projekt/<name>` — Projekt-Zugehörigkeit
- `infra/<slug>` — Infra-Komponente
- `stack-category/<cat>` — frontend/backend/db/ai/...
- `used-in/<projekt>` — Backlink-Tag auf Komponenten
- `domain/<bereich>` — Geschäftsdomäne
- `type/<typ>` — overview/moc/dashboard/meta
