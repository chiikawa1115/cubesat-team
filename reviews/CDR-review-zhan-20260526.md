# CDR 正式審查報告 — TASA-NTN-3U CubeSat

**審查人：** 詹鎮宇研究員（國家太空中心 TASA／5G 通訊研究部）
**審查日期：** 2026-05-26
**審查對象：** Sprint 3 交付物 C-001 ～ C-010（Phase C CDR Package）
**最終裁決：CDR CONDITIONAL PASS ✅**

---

## 審查範圍

| 交付物 | 標題 | 審查結果 |
|-------|------|---------|
| C-001 | SRS v2（系統需求規格） | PASS |
| C-002 | RF PCB 細部設計 | **CONDITIONAL — Q1, Q2** |
| C-003 | FPGA RTL 設計 | PASS（建議追蹤） |
| C-004 | ADCS 控制模擬 | **CONDITIONAL — Q3** |
| C-005 | 熱控細部分析 | **CONDITIONAL — Q4** |
| C-006 | SPENVIS 輻射分析 | **CONDITIONAL — Q5（Sprint 4 執行）** |
| C-007 | FSW 架構設計 | PASS |
| C-008 | 機構結構分析 | PASS |
| C-009 | CDR Package | PASS（依 Q1～Q5 解決後確認） |
| C-010 | P2P Review | 2/2 Conditional Approve → 視同 PASS |

---

## 硬性條件（Hard Gate）— Sprint 4 開始前必須解決

### Q1：BPF 選型重新評估 [負責人：通訊酬載工程師 林志遠]

**問題：** C-002 中 UL BPF 與 DL BPF 均選用 Mini-Circuits SYBP-2250+（中心頻率 2250 MHz，3 dB 頻寬 740 MHz，通帶 1880～2620 MHz）。

此頻寬設計導致：
- UL 頻帶 1980～2010 MHz → 落入通帶（正確）
- DL 頻帶 2170～2200 MHz → **同樣落入通帶（錯誤）**

以 SYBP-2250+ 作為 UL 路徑 BPF，無法抑制 DL 頻段干擾訊號，UL/DL 隔離度趨近 **0 dB**，不符合 SYS-003 相關隔離要求。

**要求：**
- 重新選型 UL BPF：中心頻率 ~1995 MHz，BW ≤ 60 MHz，對 2170 MHz 帶外抑制 ≥ 40 dB
- 重新選型 DL BPF：中心頻率 ~2185 MHz，BW ≤ 60 MHz，對 2010 MHz 帶外抑制 ≥ 40 dB
- 提供所選零件的 S-parameter 數據或製造商規格頁，佐證帶外抑制數值
- 更新 Link Budget 加入新 BPF 插損（IL）

### Q2：LO 190 MHz 料號確認 [負責人：通訊酬載工程師 林志遠]

**問題：** C-002 混頻器 LT5512EUF 的 LO 設計為 190 MHz（= 2185 - 1995 MHz），此頻率非標準商用 TCXO 頻率（常規：10/20/25/26/40/52/100 MHz），目前 C-002 未提供 LO 訊號源方案。

**要求（二擇一）：**
- 方案 A：確認是否存在 190 MHz TCXO/VCXO 商用料號，提供 DigiKey/Mouser 料號與規格
- 方案 B：設計 PLL 方案（如 10 MHz TCXO → 鎖相環 × 19 → 190 MHz），提供：
  - PLL 積體電路料號（如 ADF4351 或同等品）
  - Phase noise L(f) 估算，確認 @ 10 kHz offset 優於 -85 dBc/Hz
  - Costas loop 相位雜訊容忍度分析（對 QPSK 2000-2200 MHz 載波的影響）
  - BOM 增量估算（多少元件、多少成本）

---

## 軟性條件（Soft Gate）— Sprint 4 期間追蹤解決

### Q3：ADCS Eclipse Segment 3σ 不一致

**問題：** C-004 EKF 食月段精度 ±1.2°(1σ)，換算 3σ = ±3.6°，超過 B-006 宣稱的 ±3.1°(3σ)。雖仍符合 SYS-008（≤ 5°）需求，B-006 宣稱值與 C-004 分析結果不一致。

**要求：** Sprint 4 ADCS 數值模擬（CDR-AI-005）完成後，更新 B-006 或 C-004 的聲明值，確保一致性。

### Q4：電池熱裕量

**問題：** C-005 最壞情況（冬至 SSO）電池溫度 -9.1°C，距 SYS-012 下限 -10°C 僅剩 0.9°C 裕量，低於熱模型不確定度（通常 ±2～5°C）。

**要求：** Sprint 4 評估加熱器功率由 0.5W 升至 0.75W，TVAC 測試期間驗證電池溫度裕量 ≥ 3°C。

### Q5：SPENVIS 精確模擬

**問題：** C-006 明確說明 SPENVIS 線上模擬留待 Sprint 4 執行；目前 TID 5 krad 為手算估算。

**要求：** Sprint 4 完成 SPENVIS 線上模擬（AE-8, AP-8, CREME96），更新 TID/SEU 精確數值。此項為 FM 零件採購的硬性前置條件（CDR-AI-004）。

### Q6：FR4 微帶線損耗確認

**問題：** C-002 使用 FR4（Dk=4.6 @ 2 GHz, tanδ ≈ 0.018～0.020），微帶線損耗約 0.5～0.8 dB/10 cm；Link Budget 中此插損是否已計入，未明確說明。

**要求：** 在更新 Link Budget 時（隨 Q1 BPF 更新），同步確認 FR4 微帶線插損數值並列出。

### Q7：FEC 增益基礎

**問題：** C-003 提及 Rate 1/2, K=7 Viterbi 可提供約 5.1 dB coding gain；Link Budget Eb/N0 門檻是以 uncoded 或 coded 為基礎未明確聲明。

**要求：** Sprint 4 Link Budget 更新時，明確標示 Eb/N0 門檻為 coded/uncoded，並對應 BER = 10⁻⁶。

---

## 詹老師總評

此次 CDR Package 整體完整度良好，系統需求追蹤（RTM v2, 37 項）、V&V 計畫、各子系統細部設計均有基礎。

**Q1 和 Q2 是真實的 RF 設計缺口**，BPF 選型問題（UL/DL 都在同一個 740 MHz 通帶）和 190 MHz LO 料號問題在產品化時必須解決，此二項為 Sprint 4 的硬性前置條件。

Q3～Q7 為軟性條件，允許在 Sprint 4 期間逐步補強，但必須在 TRR（測試準備審查）前全部關閉。

建議 Sprint 4 開始時先讓通訊酬載工程師林志遠完成 Q1/Q2 正式回覆，其後再啟動整合測試計畫和最終報告撰寫。

---

*本審查報告由 TASA 詹鎮宇研究員出具。CDR Conditional Pass 裁決在 Q1/Q2 解決並獲得 SE 確認後，更新為 CDR PASS。*
