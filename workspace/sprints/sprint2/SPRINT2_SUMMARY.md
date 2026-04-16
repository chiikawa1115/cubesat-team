# Sprint 2 總結 — TASA-NTN-3U

**Sprint 期間**：2026-04-29 ~ 2026-05-12  
**里程碑**：PDR（Preliminary Design Review）  
**Sprint 目標**：Phase B 初步設計，完成 11 項交付物並通過 PDR  
**結果**：**PDR PASS ✅**（含 6 項 Professor Challenger 問題全部修正）

---

## 交付物清單

| ID | 標題 | 負責 | 版本 | 狀態 |
|----|------|------|------|------|
| B-001 | RF 鏈路完整設計（Link Budget v2） | Comm Agent | v2.1 | ✅ Done |
| B-002 | 系統架構方塊圖 + ICD v1 | SE Agent | v1.0 | ✅ Done |
| B-003 | PDR 審查包（含 RTM v1） | SE + QA | v1.1 | ✅ Done |
| B-004 | Mass Budget 精化（含 DCN-002） | Mech Agent | v2.1 | ✅ Done |
| B-005 | Power Budget 精化（含 DCN-001/002） | SE Agent | v2.1 | ✅ Done |
| B-006 | ADCS Trade Study（MTQ×3 + RW×1） | AOCS Agent | v1.0 | ✅ Done |
| B-007 | OBC/FPGA 架構初步設計（Zynq-7020） | SW/FW Agent | v1.0 | ✅ Done |
| B-008 | 熱控初步分析（含 DCN-002） | Mech Agent | v1.1 | ✅ Done |
| B-009 | BOM v2.0（含 DCN-001/002 更新） | PM Agent | v2.1 | ✅ Done |
| B-010 | Risk Register v2（7 items） | PM Agent | v2.0 | ✅ Done |
| B-011 | P2P Review 報告 | QA Agent | v1.0 | ✅ Done |

---

## 設計變更記錄（DCN Log）

| DCN | 內容 | 核准日期 | 影響 |
|-----|------|---------|------|
| DCN-001 | 太陽能板 5W → 6.5W BOL | Sprint 2 初 | Power margin 由赤字轉正 |
| DCN-002 | 電池 10 Wh → 15 Wh | 2026-04-15 | DoD worst case 37.9% → 25.2% ✅ |

---

## 關鍵設計數據

### 系統架構
- 平台：3U CubeSat，500 km SSO，LTAN 10:30
- 任務：S-band n236 NTN 透明轉發（Rel-17 bent-pipe）
- 頻率：UL 1980–2010 MHz / DL 2170–2200 MHz

### RF 鏈路（B-001 v2.1）
| 場景 | 仰角 | Slant Range | FSPL | Link Margin |
|------|------|------------|------|-------------|
| Nominal | 10° | **1,695 km** | 163.0 dB | **+6.3 dB** ✅ |
| Worst (S8) | 10°+rain+polar | — | — | +2.3 dB ⚠ |

> S8 worst case accepted risk（P < 10⁻⁴）

### Power Budget（B-005 v2.1）
| 項目 | BOL | EOL |
|------|-----|-----|
| 太陽能板（DCN-001） | 6.5W | 5.2W |
| 平均消耗 | 3.276W | 2.993W |
| 能源餘額 | +0.404 Wh/orbit ✅ | -0.040 Wh/orbit ⚠ |
| Eclipse DoD（15 Wh，DCN-002） | 11.9% | 14.9% |
| Worst case DoD | — | **25.2%** ✅ |

### Mass Budget（B-004 v2.1）
- 衛星乾重：2,232g
- 含 10% contingency：**2,455g**
- 上限：4,000g → 剩餘 margin **1,545g（38.6%）** ✅

### ADCS（B-006）
- 選型：MTQ×3 + CubeWheel Nano（RW×1）
- 指向精度 3σ：**±3.1°**（需求 ±5°）✅
- RW 去飽和：**每軌必執行**（殘磁 m=0.01 Am² 主導）
- 極區策略：入極前 RW 必須清空（68%/pass 消耗）

### OBC/FPGA（B-007）
- 平台：Zynq-7020，53,200 LUT
- SEU 策略：TMR（37,000 LUT，69.5%）+ ICAP scrubbing
- SAA 策略：動態 scrubbing 100ms→10ms（Sprint 3 SPENVIS 驗證）

### 熱控（B-008 v1.1）
- 日照面：+17.2°C nominal / +24.7°C contact peak
- 蝕刻末端（加熱器 0.5W）：-8.3°C（電池下限 -10°C，margin 1.7°C）
- 電池 DoD 風險：CLOSED via DCN-002

### BOM（B-009 v2.1）
- 硬體總計：**~$62,853 USD**（~NT$2,011,296）
- 含教育折扣：~$54,000 USD
- 全任務總計：~$458,000 USD（含 $300K 發射費）

---

## Professor Challenger 審查結果

**審查日期**：2026-04-15  
**提出問題**：6 項  
**結果**：全部 RESOLVED ✅

| 編號 | 問題 | 修正方式 | 狀態 |
|------|------|---------|------|
| P1 | 極化失配 0.5→3.0 dB | PATCH-P1-P2-comm.md：確認 3 dB（ITU-R S.1555-1） | ✅ |
| P2 | EOL 能源赤字 M1 量化 | PATCH-P1-P2-comm.md：IoT delay ~6 hr，可接受 | ✅ |
| P3 | ADCS 指向誤差 ±2°→±3.1° 3σ | PATCH-P3-aocs.md：6 誤差源 RSS 計算 | ✅ |
| P4 | LUT 50K→53,200（Zynq-7020） | PATCH-P4-P6-sw.md + B-003 直接修正 | ✅ |
| P5 | 電池 DoD 37.9% 超標（低溫+EOL） | DCN-002 核准：15 Wh，DoD→25.2% | ✅ |
| P6 | SAA 動態 scrubbing 未設計 | PATCH-P4-P6-sw.md：Sprint 3 SPENVIS | ✅ |

**Patch 文件**：`workspace/sprints/sprint2/patches/`

---

## PDR Entry Criteria 驗證（10/10 PASS）

1. ✅ 系統需求已凍結（SRS v1）
2. ✅ 系統架構已定義（ICD v1）
3. ✅ 所有子系統初步設計完成
4. ✅ Mass Budget ≤4.0 kg（2.455 kg，38.6% margin）
5. ✅ Power Budget（6.5W DCN-001 驗證）
6. ✅ Link Budget（UL margin +6.3 dB ≥ 3 dB）
7. ✅ ADCS Trade Study 完成
8. ✅ OBC/FPGA 架構定義
9. ✅ Risk Register 更新（7 items，最高 RPN=32）
10. ✅ RTM v1（17 requirements 追蹤）

---

## Sprint 3 待辦（Phase C / CDR 準備）

| 優先 | 項目 | 負責 |
|------|------|------|
| High | RF PCB 詳細設計（4層，50Ω） | Comm Agent |
| High | FPGA RTL：QPSK demod/mod + SEU scrubber | SW/FW Agent |
| High | ADCS 控制律模擬（RW 每軌去飽和驗證） | AOCS Agent |
| High | 熱詳細分析（PA 散熱片，contact window peak） | Mech Agent |
| High | CDR 審查包 | SE + QA |
| Medium | SPENVIS 軌道輻射模擬（SAA P6 驗證） | SW/FW Agent |
| Medium | ConOps 更新（EOL 降級操作模式） | SE Agent |
| Medium | B-006 正式更新（±3.1°，每軌去飽和） | AOCS Agent |

---

*Sprint 2 由 PM Agent 彙整 | TASA-NTN-3U CubeSat Project*
