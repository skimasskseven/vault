---
tags: [infrastructure, docker, container]
---
[[10_infrastruktur]] [[adr_001_masterplan]]
# INF_Docker_Containers

Hier sind alle laufenden und gestoppten Container dokumentiert.

| Name                    | Status                | Ports                                                      | Image                               |
| :---------------------- | :-------------------- | :--------------------------------------------------------- | :---------------------------------- |
| **compliance-guard**    | Up 24 hours (healthy) | 0.0.0.0:18789->18789/tcp, [::]:18789->18789/tcp            | compliance-guard-openclaw-conformis |
| **compliance-guard-db** | Up 24 hours (healthy) | 0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp                | postgres:16-alpine                  |
| **openclaw-research**   | Up 7 days (healthy)   | 18789/tcp, 0.0.0.0:18790->18790/tcp, [::]:18790->18790/tcp | research-monster:latest             |

