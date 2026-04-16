---
deliverable: B-003
sprint: 2
wave: 3
authors: SE Agent（陳建宏）+ QA Agent（林宜靜）
date: 2026-05-10
status: final
---

# B-003：PDR 審查包 v1（Preliminary Design Review Package）
## TASA-NTN-3U CubeSat — Sprint 2 Phase B 完成

---

## 1. PDR Entry Criteria 符合度確認

| # | Entry Criteria | 狀態 | 對應文件 | 備注 |
|---|---------------|------|---------|------|
| 1 | 系統需求基線（SRS）已核准 | PASS | A-002 SRS v1（Sprint 1） | |
| 2 | ConOps 已確立 | PASS | A-001 ConOps v1（Sprint 1） | |
| 3 | 系統架構方塊圖 + ICD | PASS | B-002 ICD v1 | 6 子系統、15 組介面定義 |
| 4 | 所有子系統初步設計文件 | PASS | B-001/006/007/008/004 | 通訊/ADCS/OBC/熱控/結構 |
| 5 | Power Budget（能量收支正值） | PASS | B-005：BOL +0.404 Wh/orbit | EOL -0.040 Wh 微幅赤字需 M1/M2 緩解 |
| 6 | Mass Budget（≤4.0 kg） | PASS | B-004：2,180 g（45.5% 餘裕） | |
| 7 | Link Budget（Margin ≥ 3 dB） | PASS | B-001 v2.1：+8.8 dB（10° 仰角）| C-001 斜距修正後 |
| 8 | BOM 初版 + 成本估算 | PASS | B-009：$61,853 硬體中位數 | 教育折扣後 ~$51k–$55k |
| 9 | Risk Register（高風險有緩解） | PASS | B-010：最高 RPN=32 | 7 項風險，無 Critical 級 |
| 10 | P2P Review Gate（核心文件） | PASS | B-011：3/3 通過 | B-001 C-001 已修正（v2.1） |

**PDR Entry 結論：10/10 Criteria 滿足 → PDR PASS**

---

## 2. 設計彙整（Design Summary）

### 2.1 任務概述

TASA-NTN-3U 為一顆 3U CubeSat，運行於 500 km 太陽同步軌道（SSO），軌道週期 94.5 分鐘。主酬載為 S-band NTN 透明轉發器（3GPP Rel-17 IoT-NTN bent-pipe），支援 100 bps IoT 下行數據率，調變方式 QPSK 1/2。衛星全星質量 2,180 g（含 10% contingency），太陽能板 BOL 峰值 6.5 W（DCN-001 升級），電池容量 10 Wh。設計壽命 3 年，具備三軸姿態穩定（MTQ×3 + RW×1）與 TMR/Scrubbing SEU 防護的 Zynq-7020 SoC OBC。

### 2.2 系統架構摘要

系統架構定義於 B-002 ICD v1，包含 6 個子系統：OBC（Zynq-7020，ARM+FPGA 雙功能）、EPS（GomSpace P31u，MPPT + 10 Wh Li-ion）、ADCS（MTQ×3 + CubeWheel Nano）、S-band 酬載（LNA + BPF + Mixer + PA 1W RF）、TT&C（GomSpace AX100 UHF，AX.25）、結構/熱控（Al 6061-T6 3U 框架 + MLI + Kapton 加熱器）。OBC 作為中央控制節點，透過 I2C（EPS）、SPI（ADCS、S-band 基帶）、UART（TT&C、S-band 控制）、GPIO（加熱器、天線部署）與各子系統通訊。ICD v1 定義 15 組介面（IF-01 至 IF-15），涵蓋資料、電力、與離散信號。

### 2.3 關鍵設計參數表（Key Design Parameters）

| 參數 | 數值 | 來源文件 |
|------|------|---------|
| 軌道 | 500 km SSO，週期 94.5 min，Eclipse 35.7 min | ConOps |
| 衛星質量 | 2,180 g（含 10% contingency） | B-004 |
| 質量餘裕 | 45.5%（限值 4,000 g） | B-004 |
| 太陽能板 BOL | 6.5 W（DCN-001 升級） | B-005 |
| 太陽能板 EOL | 5.939 W（衰減因子 0.9137） | B-005 |
| BOL 軌道平均功率 | 3.276 W | B-005 |
| 電池容量 | BOL 10 Wh / EOL 8 Wh | B-005 |
| BOL 能量收支 | +0.404 Wh/orbit（正值） | B-005 |
| EOL 能量收支 | -0.040 Wh/orbit（M1+M2 緩解後轉正） | B-005 |
| Worst case 單圈 DoD（EOL） | 28.4%（< 30% 限值） | B-005 |
| OBC | Zynq-7020（Xiphos Q7s），ARM Cortex-A9 + 53K LUT FPGA | B-007 |
| OBC 功耗 | Standby 1.5W / Active 4.0W / Safe 1.0W | B-007 |
| FPGA LUT Utilization | 37,000 / 53,200 = 69.5%（含 TMR） | B-007 |
| ADCS 配置 | MTQ×3 + CubeWheel Nano（yaw 軸） | B-006 |
| 指向精度（3σ，穩態） | ±2°（≤ ±5° 需求） | B-006 |
| 指向精度（Polar zone） | ±3°（RW 補償） | B-006 |
| ADCS 功耗 | 0.42W（MTQ 0.30W + RW avg 0.12W） | B-006 |
| Link Margin（UL, 10° 仰角） | +8.8 dB（需求 ≥ 3 dB） | B-001 v2.1 |
| S-band 天線增益 | 8 dBi，HPBW 70°，RHCP（EnduroSat Patch） | B-001 |
| T_sys（保守值） | 340 K | B-001 |
| FSPL（UL, 1,695 km） | 163.0 dB | B-001 v2.1 |
| SEU 防護 | TMR + Configuration Scrubbing 100 ms 週期 | B-007 |
| 熱控溫度範圍 | -8.3°C（Eclipse-end 含加熱器）~ +24.7°C（Contact peak） | B-008 |
| 加熱器功率 | 0.5W，Eclipse only，耗能 0.30 Wh/orbit | B-008 |
| 電池溫度餘裕（Eclipse-end） | 1.7°C（-8.3°C vs -10°C 下限） | B-008 |
| 硬體成本（中位數） | $61,853（教育折扣後 ~$51k–$55k） | B-009 |
| 完整任務預算 | ~$455,000（含發射費 $300k） | B-009 |
| 最高風險 | RISK-001 頻率協調（RPN=32） | B-010 |
| Contact Window 功耗 | 10.30 W，持續 4 min/pass | B-005 |

---

## 3. Requirements Traceability Matrix（RTM v1）

雙向追溯：系統需求 → 設計文件 → 驗證方法

| 需求 ID | 需求描述 | 子系統 | 設計文件 | 目前狀態 | 驗證方法 |
|---------|---------|-------|---------|---------|---------|
| SYS-001 | 3U CubeSat，100×100×340 mm | 結構 | B-004：ISIS 3U Al 6061-T6 框架 | Allocated | Inspection |
| SYS-002 | 軌道：500 km SSO | AOCS/系統 | ConOps / B-006 | Allocated | Analysis |
| SYS-003 | 全星質量 ≤4.0 kg | 結構 | B-004：2,180 g（餘裕 45.5%） | Satisfied | Analysis |
| SYS-004 | 任務壽命 3 年 | 全系統 | B-005 EOL 分析, B-007 SEU 防護 | Allocated | Analysis |
| SYS-005 | 太陽能板 BOL 軌道平均 ≥3W | EPS | B-005：3.276 W | Satisfied | Analysis |
| SYS-006 | 電池 DoD worst case ≤30% | EPS | B-005：28.4%（EOL worst case） | Satisfied | Analysis |
| SYS-007 | S-band UL Link Margin ≥3 dB | 通訊 | B-001 v2.1：+8.8 dB | Satisfied | Analysis |
| SYS-008 | 支援 IoT-NTN 100 bps，QPSK 1/2 | 通訊 | B-001：QPSK 1/2，C/N0 34.8 dB-Hz | Satisfied | Test |
| SYS-009 | ADCS 指向精度 ≤±5°（3σ） | ADCS | B-006：±2°（穩態），margin 60% | Satisfied | Test |
| SYS-010 | Polar zone（|lat|>80°）指向保持 ≤±5° | ADCS | B-006：RW 補償 ±3°，margin 40% | Satisfied | Test |
| SYS-011 | OBC 處理器 ARM Cortex-A9+，FPGA ≥53,200 LUT | OBC | B-007：Zynq-7020（53,200 LUT） | Satisfied | Inspection |
| SYS-012 | SEU 防護：TMR or Configuration Scrubbing | OBC | B-007：兩者均實作（TMR 37,000 LUT + 100 ms scrub） | Satisfied | Test |
| SYS-013 | 電子元件操作溫度 -20°C ~ +60°C | 熱控 | B-008：-8.3°C ~ +24.7°C（全工況 PASS） | Satisfied | Test |
| SYS-014 | 電池操作溫度 -10°C ~ +50°C | 熱控 | B-008：-8.3°C（含加熱器，餘裕 1.7°C） | Satisfied | Test |
| SYS-015 | 頻率協調：符合 ITU/NCC 法規 | 系統 | Freq-Coord v1.1：Path A（ITU RR No.4.4）+ Path B（NCC 學術執照） | Allocated | Demonstration |
| SYS-016 | Contact Window 持續 ≥4 min/pass | 通訊/EPS | B-005：4 min/pass，電池可支撐（DoD 28.4%） | Satisfied | Analysis |
| SYS-017 | 系統功耗 Contact Window ≤12W | 全系統 | B-005/B-007：10.30 W（餘裕 14.7%） | Satisfied | Analysis |

---

## 4. P2P Review Gate 結果（引自 B-011）

| 文件 | 判定 | Critical Issues | Major Issues | 處置 |
|------|------|:--------------:|:------------:|------|
| B-001 Link Budget v2 | Approve（修正後） | C-001：斜距矛盾 | M-001/M-002/M-003 | C-001 已修正（v2.1），M 項列為 PDR AI |
| B-006 ADCS Trade Study v1 | Approve | 0 | M-004/M-005 | M 項列為 PDR AI |
| B-007 OBC/FPGA Architecture v1 | Approve | 0 | M-006/M-007 | M 項列為 PDR AI |

**P2P Gate 結論**：Wave 2 三份核心文件全部通過。B-001 C-001 Critical Issue 已於 v2.1 修正完畢（10° 仰角斜距更正為 1,695 km，Link Margin 從 +6.8 dB 提升至 +8.8 dB）。文件間一致性驗證通過（天線 HPBW 70°、ADCS 功耗 0.42W、OBC Active 4.0W、SPI 10 MHz 等交叉項均吻合）。

---

## 5. PDR Action Items（進入 CDR 前需完成）

| ID | 類別 | 描述 | 來源 | 負責人 | 優先序 | CDR 前完成 |
|----|------|------|------|--------|--------|-----------|
| PDR-AI-001 | 通訊 | T_sys nominal（Friis 235 K）vs worst-case（340 K）需明確區分，在 Link Budget 中標示兩組數字 | B-011 M-001 | Comm Agent（林志遠） | High | 必須 |
| PDR-AI-002 | 通訊 | 極化失配損耗 0.5 dB 需引用 3GPP TR 38.821 或 ITU-R 文獻支持；若無法支持，提高至 ≥1.5 dB | B-011 M-002 | Comm Agent（林志遠） | High | 必須 |
| PDR-AI-003 | 通訊 | 敏感度分析補充 ADCS 指向退化場景（pointing loss @ 15° 指向偏差） | B-011 M-003 | Comm Agent（林志遠） | Medium | 建議 |
| PDR-AI-004 | AOCS | 指向精度 ±2° 需 pointing error budget 支持（磁力矩器 + RW 組合的控制誤差分解，含干擾力矩量化） | B-011 M-004 | AOCS Agent（黃俊誠） | Medium | 建議 |
| PDR-AI-005 | AOCS | RW desaturation 所需磁力矩量化（每圈 polar zone 角動量累積 vs 非 polar zone MTQ desaturation 分析） | B-011 M-005 | AOCS Agent（黃俊誠） | Medium | 建議 |
| PDR-AI-006 | 軟韌體 | 各 SDR 模組 LUT 估算需標明引用來源（IP catalog / 文獻 / Vivado 合成結果） | B-011 M-006 | SW/FW Agent（徐志豪） | Low | 建議 |
| PDR-AI-007 | 軟韌體 | NanoAvionics OBC NOR Flash 16 MB 分區可行性分析（cost reduction opportunity，價差 $7,000） | B-011 M-007 | SW/FW Agent（徐志豪） | Low | 建議 |
| PDR-AI-008 | 熱控 | 電池 Eclipse-end 溫度餘裕僅 1.7°C（-8.3°C vs -10°C 限值），評估加熱器功耗從 0.5W 升至 0.75W 的可行性，需與 Power Budget 交叉確認 | B-008 | Mech Agent（吳建宇）| High | 必須 |
| PDR-AI-009 | EPS/系統 | EOL 能量收支 -0.040 Wh/orbit，M1（每 2 圈接觸 1 次）+ M2（OBC clock gating 1.2W）的具體實作規格與 ConOps 影響評估 | B-005 | SE Agent（陳建宏） | High | 必須 |

---

## 6. Sprint 2 風險摘要（引自 B-010）

| ID | 風險 | L | I | RPN | 狀態 | 緩解摘要 |
|----|------|:-:|:-:|:---:|------|---------|
| RISK-001 | 頻率協調（ITU/NCC） | 4 | 8 | **32** | Open | Path A: ITU RR No.4.4 + Path B: NCC 學術執照 |
| RISK-002 | EOL 能源赤字 | 3 | 4 | **12** | Mitigated | DCN-001 BOL 翻正；M1 降低 contact duty cycle + M2 OBC clock gating |
| RISK-003 | OBC 成本（Xiphos $25k） | 3 | 4 | **12** | Open | 教育折扣 10-20%，降至 $20k–$22.5k |
| RISK-004 | ADCS RW 壽命 | 2 | 4 | **8** | Watch | 索取 CubeSpace MTTF 數據，設計 MTQ-only graceful degradation |
| RISK-005 | PA 散熱 | 2 | 4 | **8** | Open | Contact Window 僅 4 min，暫態溫升 +7.5°C，B-008 分析 PASS |
| RISK-006 | SEU FPGA 失效 | 3 | 4 | **12** | Mitigated | TMR（37,000 LUT）+ Scrubbing（100 ms 週期），MTBF >1 year |
| RISK-007 | 質量超標 | 1 | 8 | **8** | Low | 2,180 g vs 4,000 g 限值，餘裕 45.5% |

**風險趨勢**：Sprint 1 → Sprint 2 整體 RPN 總和從 144 降至 92（-36%）。最大改善：RISK-001 從 96 降至 32（具體執行路徑確立）；RISK-002 從 48 降至 12（DCN-001 太陽能板升級有效）。Sprint 2 新增 5 項風險均為 Medium/Low 等級，無新增 Critical 級風險。

---

## 7. Phase C 進入建議（Sprint 3 準備）

### 7.1 PDR Exit Criteria 確認

- [x] 所有子系統初步設計完成（B-001/002/004/005/006/007/008）
- [x] RTM v1 建立，17 條需求雙向可追溯
- [x] P2P Review Gate 全部通過（3/3，B-001 C-001 已修正）
- [x] 無未解 Critical Issues（C-001 已於 v2.1 closed）
- [x] PDR Action Items 已識別並分派（9 項，4 項 High Priority）
- [x] Risk Register v2 建立，最高風險 RPN=32（非 Critical 級）
- [x] BOM v2 完成，硬體成本 baseline 確立（$61,853 中位數）

### 7.2 Sprint 3（Phase C — 細部設計）重點任務

| # | 任務 | 負責 Agent | 說明 |
|---|------|-----------|------|
| 1 | RF 鏈路 PCB 詳細設計 | Comm Agent | BOM 定案（ADL5523 + SYBP-2250 + LT5512 + PMA3-43-1W），JLCPCB 4 層 RF 板送樣 |
| 2 | FPGA RTL 設計 | SW/FW Agent | QPSK demod/mod RTL 實作 + SEU scrubber RTL + Vivado 合成驗證 LUT |
| 3 | ADCS 控制律模擬 | AOCS Agent | MATLAB/Simulink 姿態模擬，pointing error budget 量化（回應 PDR-AI-004/005） |
| 4 | 熱控詳細設計 | Mech Agent | Thermal Desktop/ESATAN 3D 節點模型，PA 散熱翼片評估，加熱器功率確認（回應 PDR-AI-008） |
| 5 | EOL Mitigation 實作規格 | SE Agent | M1（contact duty cycle）ConOps 修訂 + M2（OBC clock gating）FSW 規格（回應 PDR-AI-009） |
| 6 | 頻率協調追蹤 | PM Agent | NCC 學術執照申請時程確認，ITU Filing 文件準備（RISK-001） |
| 7 | CDR 審查包（B-103） | SE + QA Agent | 完整 RTM v2 + 所有詳細設計文件 + 測試計畫初版 |

---

## 8. PDR 結論

**Sprint 2 Phase B 初步設計通過 PDR。**

TASA-NTN-3U CubeSat 已完成從概念設計（Phase A）到初步設計（Phase B）的全面推進。關鍵成就包括：（1）DCN-001 太陽能板升級至 6.5W BOL，成功將 BOL 能量收支從 -1.11 Wh/orbit 翻正為 +0.404 Wh/orbit；（2）ADCS 選定 MTQ×3 + CubeWheel Nano 方案，全軌道指向精度 ±2°~±3° 滿足 ±5° 需求；（3）Zynq-7020 OBC 架構含 TMR + 100 ms Scrubbing 三層 SEU 防護，LUT 利用率 69.5% 在設計安全範圍內；（4）Link Budget v2.1 修正後 UL Margin +8.8 dB，遠超 3 dB 門檻；（5）全星質量 2,180 g，距 4 kg 限值有 45.5% 餘裕。

主要待解項為 EOL 能量收支微幅赤字（-0.040 Wh/orbit，M1+M2 可消除）、電池 Eclipse-end 溫度餘裕偏小（1.7°C）、以及頻率協調外部依賴（RPN=32，非技術阻斷）。9 項 PDR Action Items 已分派，4 項 High Priority 須於 CDR 前完成。

基於以上分析，SE Agent 與 QA Agent 一致建議：**核准進入 Sprint 3 Phase C（細部設計），信心等級：中高（Medium-High）。** 進入 CDR 的關鍵路徑為 PDR-AI-001/002（Link Budget T_sys 與極化損耗釐清）與 PDR-AI-008/009（熱控餘裕與 EOL Mitigation 實作）。

---

## 附錄：Sprint 2 交付物清單

| 交付物 | 名稱 | Wave | 作者 | 狀態 |
|--------|------|:----:|------|:----:|
| B-001 | Link Budget v2.1 | 2 | Comm Agent（林志遠） | Done |
| B-002 | System Architecture + ICD v1 | 1 | SE Agent（陳建宏） | Done |
| B-003 | PDR Package v1（本文件） | 3 | SE + QA Agent | Done |
| B-004 | Mass Budget v2 | 2 | Mech Agent（吳建宇） | Done |
| B-005 | Power Budget v2 | 1 | SE Agent（陳建宏） | Done |
| B-006 | ADCS Trade Study v1 | 2 | AOCS Agent（黃俊誠） | Done |
| B-007 | OBC/FPGA Architecture v1 | 2 | SW/FW Agent（徐志豪） | Done |
| B-008 | Thermal Analysis v1 | 2 | Mech Agent（吳建宇） | Done |
| B-009 | BOM v2 | 3 | PM Agent（詹雅婷） | Done |
| B-010 | Risk Register v2 | 3 | PM Agent（詹雅婷） | Done |
| B-011 | P2P Review Report | 3 | QA Agent（林宜靜） | Done |

---

---

## Revision History

| 版本 | 日期 | 修改者 | 修改內容 |
|------|------|--------|---------|
| v1.0 | 2026-05-10 | SE 陳建宏 + QA 林宜靜 | 初版發行 |
| v1.1 | 2026-05-10 | SW/FW 徐志豪 | **PATCH-P4**：修正 LUT 數字一致性。(1) SYS-011 需求門檻從「≥50K LUT」修正為「≥53,200 LUT」（50K 為 Zynq-7010 規格，本案使用 Zynq-7020 = 53,200 LUT）。(2) SYS-012 與 RISK-006 的 TMR LUT 從「34,500」修正為「37,000」（37,000 為含 TMR + 非 TMR 模組的總 LUT 使用量，與 B-007 Section 6.2 一致）。|

*PDR Package v1.1 — 最後修訂：SW/FW 徐志豪 — 2026-05-10*
