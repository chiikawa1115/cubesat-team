# CubeSat Team — Claude Code Skill

CubeSat 衛星產品開發團隊模擬器。一人操控 8 個 AI agent 角色，模擬完整的衛星產品開發團隊。

## Features

- **8 Agent Roles**: CEO, PM, Systems Engineer, Comm Payload, AOCS, SW/FW, Mech/Thermal, QA
- **gstack-style Workflow**: Think → Plan → Build → Review → Test → Ship
- **Agile Development**: 4 Sprints mapped to NASA Phase A-D
- **Peer Review Gate**: All deliverables require 2-agent P2P review
- **DigiKey BOM Pricing**: Real-time component pricing via WebSearch
- **Google Docs Output**: 25-page CEO report auto-generated to Google Docs
- **TASA Knowledge Base**: Distilled from Taiwan Space Agency course materials

## Installation

```bash
git clone https://github.com/chiikawa1115/cubesat-team.git ~/.claude/skills/cubesat-team
```

## Slash Commands

| Command | Description |
|---------|-------------|
| `/mission-kickoff` | Initialize CubeSat project |
| `/sprint-plan` | Plan next 2-week sprint |
| `/subsystem-status` | Dashboard from all subsystems |
| `/design-review` | Formal SRR/PDR/CDR review |
| `/peer-review` | P2P review gate |
| `/budget-check` | DigiKey BOM pricing |
| `/ceo-report` | Generate 25-page report to Google Docs |

## Agent Roles

| Role | File | Scope |
|------|------|-------|
| CEO | agents/ceo.md | Decisions, reports, Go/No-Go |
| PM | agents/pm.md | Schedule, budget, DigiKey BOM |
| Systems Engineer | agents/systems-engineer.md | V-model, requirements, ICD |
| Comm Payload | agents/comm-payload.md | DVB-S2X, RF, Link Budget |
| AOCS | agents/aocs.md | Attitude control, GMAT sim |
| SW/Firmware | agents/sw-firmware.md | FPGA, FSW, SEU mitigation |
| Mech/Thermal | agents/mech-thermal.md | Structure, thermal, mass budget |
| QA/Test | agents/qa-test.md | V&V matrix, peer review gate |

## Knowledge Base

Distilled from TASA (Taiwan Space Agency) satellite communication course by researcher James Chan (詹鎮宇):
- System Engineering (NASA V-model, review gates)
- AOCS (attitude/orbit control)
- Mission Simulation (GMAT, frequency coordination)
- Communication Design (DVB-S2X, NTN, SDR, FPGA)
- Industry Landscape (Starlink, Kuiper, OneWeb analysis)

## License

MIT
