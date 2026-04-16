# Sprint 3 計畫 — TASA-NTN-3U

**Sprint 期間**：2026-04-16 ~ 2026-04-29
**里程碑**：CDR（Critical Design Review）
**Story Points**：40

## Sprint Goal
完成所有子系統細部設計，通過 CDR 審查，達成 Phase C 里程碑。

## Wave 執行計畫

### Wave 1（即刻啟動）
| ID | 標題 | 負責 | SP |
|----|------|------|-----|
| C-001 | 系統需求規格書凍結 v2 | SE Agent | 3 |

**執行順序理由**：所有 Wave 2 細設都需要以凍結後的需求為基準，SE 先打底。

### Wave 2（Wave 1 完成後並行）
| ID | 標題 | 負責 | SP |
|----|------|------|-----|
| C-002 | RF PCB 詳細設計 | Comm Agent | 5 |
| C-003 | FPGA RTL 詳細設計 | SW/FW Agent | 6 |
| C-004 | ADCS 控制律模擬 | AOCS Agent | 5 |
| C-005 | 熱詳細分析 | Mech Agent | 4 |
| C-006 | SPENVIS 輻射模擬 | SW/FW Agent | 4 |

**跨讀要求**：
- C-002（Comm）需讀 B-001 Link Budget v2.1、B-007 OBC/FPGA（介面定義）
- C-003（SW/FW）需讀 B-007 OBC 架構、B-001 Link Budget（調變規格）
- C-004（AOCS）需讀 B-006 Trade Study、PATCH-P3（±3.1° 誤差預算）
- C-005（Mech）需讀 B-002 ICD（PA 功耗 4W）、B-008 熱分析 v1.1
- C-006（SW/FW）需讀 B-007、PATCH-P4-P6（SAA scrubbing 設計）

### Wave 3（Wave 2 完成後）
| ID | 標題 | 負責 | SP |
|----|------|------|-----|
| C-007 | BOM v3 定案 | PM Agent | 3 |
| C-008 | ConOps v2 | SE Agent | 3 |
| C-009 | CDR 審查包 | SE + QA | 5 |
| C-010 | P2P Review | QA Agent | 2 |

## CDR Entry Criteria（目標全 PASS）
1. 所有子系統細部設計文件完成
2. Mass Budget ≤ 4.0 kg（已 2.455 kg）
3. Power Budget（DCN-002 後 DoD 25.2%）
4. Link Budget margin ≥ 3 dB（已 +6.3 dB）
5. RTM v2（需求→設計完整追蹤）
6. V&V 計畫 v1 完成
7. Risk Register 更新
8. BOM v3 含料號
9. P2P Review 通過
10. ConOps v2 完成

## 風險
| 風險 | 等級 | 緩解 |
|------|------|------|
| RF PCB 阻抗控制困難 | Y | 使用 JLCPCB 4層板，預留 10% 佈局裕度 |
| FPGA RTL 複雜度高 | Y | TMR wrapper 可複用，QPSK 用既有 IP |
| SPENVIS 結果不確定 | G | Sprint 3 為分析，Sprint 4 才整合至設計 |
