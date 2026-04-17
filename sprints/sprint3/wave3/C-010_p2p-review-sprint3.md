---
deliverable: C-010
sprint: 3
wave: 3
author: QA 工程師（P2P Review 主席）
date: 2026-04-15
status: final
version: v1.0
reviewed_documents:
  - C-009_cdr-package-v1.md（CDR 審查包 v1.0）
  - C-003_fpga-rtl-design-v1.md（FPGA RTL 設計 v1.0）
  - C-004_adcs-control-sim-v1.md（ADCS 控制律模擬 v1.0）
---

# C-010：P2P Review — Sprint 3 最終審查報告

**TASA-NTN-3U CubeSat 專案**

---

## 1. 審查概要

### 1.1 基本資訊

| 項目 | 內容 |
|------|------|
| 審查日期 | 2026-04-15 |
| 審查主席 | QA 工程師（P2P Review Chair）|
| 審查者 A | 通訊酬載工程師（Comm Agent）|
| 審查者 B | 機構熱控工程師（Mech Agent）|
| 會議類型 | Peer-to-Peer Design Review（Sprint 3 CDR 準備）|

### 1.2 審查文件清單

| # | 文件 ID | 文件名稱 | 版本 | 作者 |
|---|---------|---------|------|------|
| 1 | C-009 | CDR 審查包（RTM v2 + V&V 計畫）| v1.0 | 系統工程師 / QA 工程師 |
| 2 | C-003 | FPGA RTL 詳細設計 | v1.0 | SW/FW Agent（徐志豪）|
| 3 | C-004 | ADCS 控制律模擬 | v1.0 | AOCS Agent（黃俊誠）|

### 1.3 審查結論總覽

| 審查者 | 負責範圍 | 結論 |
|--------|---------|------|
| 審查者 A（Comm Agent）| C-009 RTM v2 技術正確性 + C-003 FPGA 模組 | **Conditional Approve** |
| 審查者 B（Mech Agent）| C-009 V&V 計畫完整性 + C-004 ADCS 熱結構耦合 | **Conditional Approve** |
| **P2P Review 整體結論** | — | **Conditional Approve** |

> **通過判定**：兩位審查者均為 Conditional Approve，依通過條件（2/2 Approve 或 Conditional Approve）— **P2P Review 通過**，後續 Action Items 於 Sprint 4 Week 1~2 追蹤。

---

## 2. C-009 CDR 審查包 — 審查意見

### 2.1 審查者 A：C-009 RTM v2 技術正確性核查

#### 2.1.1 SYS-009 / SYS-010 / SYS-011 對應核查

**核查依據**：C-009 RTM v2 Section 2.2 完整追蹤表

| 需求 ID | 需求描述 | RTM v2 追蹤設計文件 | 驗證項目 | 審查意見 |
|---------|---------|------------------|---------|---------|
| SYS-009 | RF 上行 SNR ≥ 10 dB | B-001 Link Budget v2.1、C-002 RF PCB | VA-001 Link Budget（+6.3 dB margin）；VT-001 | **PASS — 對應正確**。VA-001 引用 B-001 v2.1（上行 +6.3 dB），margin 超出最低要求 3 dB。|
| SYS-010 | EMC 符合 CISPR 22 Class B | B-003 RTM v1、C-002 RF PCB（接地與屏蔽設計）| VT-008 EMC 初步測試（計畫 Sprint 4）| **PASS — 對應正確**。設計文件追蹤至 C-002 PCB 接地屏蔽設計，T 類驗證計畫明確（VT-008）。|
| SYS-011 | QPSK 調變 BER ≤ 10⁻⁶ | B-001 Link Budget v2.1、C-003 FPGA RTL（QPSK 解調模組）| VT-002 FPGA QPSK BER 測試（計畫 Sprint 4）| **注意**：C-003 文件（Section 8 需求矩陣）中，SYS-011 的 BER 目標描述為「≥100 bps，QPSK 1/2」，強調資料率。C-003 的 Viterbi BER 設計目標為「≤10⁻⁵ @ Eb/N0 = 4.5 dB（hard decision）」，而 RTM v2 的 VT-002 通過準則為「BER ≤ 10⁻⁶ @ Eb/N0 = 9.8 dB」。RTM v2 BER 通過準則（10⁻⁶ @ 9.8 dB）與 C-003 設計分析估算（10⁻⁵ @ 4.5 dB）之間存在一個數量級的差距（10⁻⁶ vs 10⁻⁵），**需說明差異**：Link Budget 中的 Eb/N0 = 9.8 dB 是系統工作點，在此點硬判決 QPSK 1/2 的理論 BER 約為 10⁻⁸~10⁻⁹，故 10⁻⁶ 目標實際上是保守的，C-003 的 10⁻⁵ @ 4.5 dB 是最低可行點的估算。兩者描述框架不同（系統工作點 vs 最低性能點），但需在文件中明確說明，**否則未來測試驗收時容易造成混淆**。— **標記為 AI-C003-01**。|

**RTM v2 SYS-009/010/011 總結**：3 條需求追蹤基本正確，SYS-011 BER 目標描述框架差異需補充說明。

#### 2.1.2 VA-001 Link Budget 驗證引用核查

**核查項目**：VA-001 是否正確引用 B-001 v2.1（含 PATCH-P1 極化修正）

| 查核點 | 文件依據 | 審查發現 |
|--------|---------|---------|
| VA-001 交付物版本 | C-009 Section 3.3（A 類驗證表）：「B-001 v2.1」| **PASS** — 明確引用 B-001 v2.1，非舊版 B-001。|
| PATCH-P1 極化修正納入 | B-001 v2.1 含 PATCH-P1 圓極化 –3 dB 修正 → margin 從 +8.8 dB 降至 +6.3 dB | **PASS** — RTM v2 Section 2.2（SYS-009 列）記載「+6.3 dB margin」，與 B-001 v2.1 極化修正後數值一致（PDR → CDR 進度比較 Section 4 亦確認此修正）。|
| CDR Entry Criteria 引用 | C-009 Section 1（Entry Criteria 表）第 4 條引用「B-001 v2.1（上行 +6.3 dB，下行 +6.3 dB）」| **PASS** — 明確且正確。|

**VA-001 引用核查結論**：**全 PASS**，B-001 v2.1 含極化修正已正確納入 CDR 審查包。

#### 2.1.3 CDR-AI-001（RF PCB via 升級）列入核查

**核查項目**：CDR-AI-001（RF PCB 熱過孔陣列升級至 8×8）是否已列入 Open Issues 清單

| 查核點 | 依據 | 審查發現 |
|--------|------|---------|
| CDR-AI-001 是否存在 | C-009 Section 5 Open Issues 表 | **PASS** — CDR-AI-001 已明確列入：「RF PCB 熱過孔陣列升級至 8×8（C-005 建議：每 5.6 W 至少 64 個 via 以確保 Rth < 5°C/W）」，起因文件 C-005，負責人 Comm 子系統，優先 High，期限 Sprint 4 Week 1。|
| 技術內容正確性 | C-005 熱分析 v1.0（被引用）| 技術描述（64 個 via，Rth < 5°C/W）須由 C-005 原文確認，本審查以 C-009 引用為準，**暫 PASS**。C-005 細部審查不在本次 P2P Review 範圍。|
| 優先級是否適當 | High | **PASS** — via 升級影響 PA 散熱路徑，列為 High 優先合理。|

**CDR-AI-001 核查結論**：**PASS**，已列入且追蹤完整。

---

### 2.2 審查者 B：C-009 V&V 計畫完整性核查

#### 2.2.1 VT-005 TVAC 測試電池低溫邊界核查

**核查項目**：VT-005 TVAC 測試是否足夠覆蓋電池低溫 -10°C 邊界

| 查核點 | 依據 | 審查發現 |
|--------|------|---------|
| VT-005 通過準則 | C-009 Section 3.3（T 類測試表）：「全功能通過，-20°C ~ +60°C」| **部分問題** — VT-005 通過準則為「-20°C ~ +60°C 全功能通過」，未明確指出電池低溫 -10°C 邊界作為**特別監控點**。VA-005 熱分析（C-005）顯示冬至最壞情況電池溫度 -8°C，距 -10°C 邊界僅 2°C 裕度（CDR-AI-006 已標示）。**VT-005 測試程序應在 -10°C 電池溫度點加入明確的電池容量與充放電功能驗收準則**，否則 TVAC 通過但電池低溫問題未能被測試捕獲。— **標記為 AI-C009-01**（建議加入，不阻擋本次 CDR）。|
| CDR-AI-006 連結 | C-009 Section 5：「CDR-AI-006 電池加熱器 0.75 W 方案評估」| **PASS** — CDR-AI-006 已明確列入，SE + Mech 負責，Sprint 4 Week 2，優先 Medium。此 AI 確保加熱器評估後會更新 VT-005 測試條件，缺口已有追蹤機制。|
| TVAC 設施確認 | CDR-AI-008：聯繫 NSPO 或國研院確認測試窗口 | **PASS** — 已識別風險並列入 AI（低優先，Post-CDR 規劃）。|

**VT-005 電池邊界核查結論**：**條件 PASS** — CDR-AI-006 已追蹤加熱器評估，但 VT-005 本身測試程序需在加熱器方案確定後補充電池 -10°C 電容量驗收準則（AI-C009-01）。

#### 2.2.2 VA-005 熱分析引用核查

**核查項目**：VA-005 熱分析是否正確引用 C-005（PA 散熱 + 電池 DCN-002）

| 查核點 | 依據 | 審查發現 |
|--------|------|---------|
| VA-005 交付物 | C-009 Section 3.3（A 類驗證表）：「A — C-005 v1.0 — PA max +52°C，電池 -8°C（冬至）」| **PASS** — VA-005 明確引用 C-005 v1.0 作為分析交付物，結果數字（PA +52°C, 電池 -8°C）已記錄。|
| DCN-002 電池修正 | DCN-002 為電池 DoD 修正（B-005 Power Budget），熱分析中 DCN-002 對電池散熱影響是否已納入 C-005 | **注意** — VA-005 引用 C-005 v1.0，但 C-009 本文並未明確說明 C-005 是否已納入 DCN-002 的電池規格修正（如電池型號或容量調整後的發熱量）。C-005 細部文件不在本次審查範圍，但此點建議後續確認。— **標記為 AI-C009-02**（低優先，建議確認）。|
| SYS-012 對應 | RTM v2 SYS-012 操作溫度 -20°C ~ +60°C → VA-005 + VT-005 | **PASS** — 追蹤完整。|

**VA-005 引用核查結論**：**大致 PASS**，DCN-002 電池熱影響是否納入 C-005 建議補充確認（AI-C009-02，低優先）。

#### 2.2.3 CDR-AI-006（電池加熱器 0.75W 評估）列入核查

**核查項目**：CDR-AI-006（加熱器 0.75W 評估）是否已列入

| 查核點 | 依據 | 審查發現 |
|--------|------|---------|
| CDR-AI-006 是否存在 | C-009 Section 5 Open Issues 表 | **PASS** — CDR-AI-006 已列入：「電池加熱器 0.75 W 方案評估（C-005：冬至最壞情況電池 -8°C，需確認加熱器設計）」，負責人 SE + Mech，優先 Medium，期限 Sprint 4 Week 2。|
| 0.75 W 功率來源 | C-005 熱分析估算 | 數值可接受，C-005 細部確認留至 Sprint 4。|
| Power Budget 衝擊 | 0.75 W 加熱器是否已納入 B-005 v2.1 Power Budget | **潛在問題** — C-009 未說明 0.75 W 加熱器功耗是否已包含在 B-005 v2.1（DoD 25.2%）的電力預算內。若加熱器為新增負載，可能影響 DoD 計算（0.75 W 連續運轉將使電池蝕刻期間負擔加重）。建議 CDR-AI-006 評估時同步更新 Power Budget。— **已包含在 AI-C009-01 建議中，補充為子項目**。|

**CDR-AI-006 核查結論**：**PASS**，已列入且追蹤明確。建議評估時同步確認 Power Budget 衝擊。

---

## 3. C-003 FPGA RTL — 審查意見

### 3.1 審查者 A（Comm Agent）

#### 3.1.1 QPSK 調變/解調規格符合 B-001 v2.1 核查

**核查依據**：C-003 Section 2、B-001 v2.1（SYS-011：QPSK 1/2，符號率）

| 規格項目 | B-001 v2.1 要求 | C-003 實作 | 核查結果 |
|---------|---------------|----------|---------|
| 調變方式 | QPSK | QPSK（Gray code 映射）| **PASS** |
| 碼率（FEC）| 1/2（卷積碼）| rate 1/2 K=7 卷積碼（G1=171₈, G2=133₈）| **PASS** |
| 符號率 | 200 kSps（B-001 BW = 200 kHz）| 200 kSps（C-003 Section 2.2 時序參數）| **PASS** |
| 資料率 | ≥ 100 bps | 200 kSps × 1/2（FEC）= 100 kbps >> 100 bps | **PASS**（大幅超過）|
| BER 目標（SYS-011）| ≤ 10⁻⁶ | 設計分析估算：10⁻⁵ @ Eb/N0 = 4.5 dB（最低點）；系統工作點 Eb/N0 = 9.8 dB 時理論 BER << 10⁻⁶ | **注意** — 見 2.1.3 之 AI-C003-01，需在 C-003 文件補充說明兩個 BER 數字的框架差異。|
| 極化方式 | 圓極化（PATCH-P1）| C-003 為數位基帶設計，極化由 C-002 RF PCB 天線實現；C-003 無需直接實作極化 | **PASS**（層次正確，責任分工明確）|

**QPSK 規格核查結論**：**大致 PASS**，主要規格與 B-001 v2.1 一致。BER 描述框架差異（AI-C003-01）為文件說明問題，非設計缺陷。

#### 3.1.2 Doppler 補償範圍核查

**核查項目**：Doppler 補償範圍 ±25 kHz 是否覆蓋 B-001 的 ±50.6 kHz UL Doppler

**關鍵問題分析**：

B-001 v2.1 指出：
- UL Doppler 最大值：±50.6 kHz（500 km SSO，1995 MHz，v_max ≈ 7.6 km/s）

C-003 Section 2.3（Costas Loop 設計）描述：
- ARM 端 Doppler 預測精度：±25 kHz（TLE 傳播誤差）
- Costas loop 負責剩餘 ±25 kHz acquisition（迴路頻寬 10 kHz）
- ARM 預補償 + Costas loop 捕獲範圍：±25 kHz（ARM）+ ±25 kHz（Costas）= **±50 kHz 總補償範圍**

| 查核點 | 分析結果 | 審查意見 |
|--------|---------|---------|
| 總補償範圍 | ARM 預補償 ±25 kHz + Costas loop ±25 kHz = ±50 kHz | **接近但略不足** — 需求 ±50.6 kHz，實際設計 ±50 kHz，差距 0.6 kHz（1.2%）。|
| ARM 預補償精度假設 | 「TLE 傳播誤差 ±25 kHz」 | **問題** — C-003 未說明 ±25 kHz TLE 傳播誤差的來源依據（最新 TLE 的傳播精度、TLE 更新頻率）。若實際 TLE 誤差 > ±25 kHz，Costas loop 的 ±25 kHz acquisition range 可能不足以捕獲殘餘 Doppler。|
| Costas loop 捕獲範圍 | 迴路頻寬 10 kHz → 捕獲時間 0.3 ms；捕獲範圍未明確量化 | **問題** — Costas loop 的「capture range」（頻率拉入範圍）不等於迴路頻寬。二階 PLL 的捕獲範圍（pull-in range）約為 ωn²/K（與增益和頻寬相關），C-003 未給出此數值，無法驗證 ±25 kHz 殘餘 Doppler 能否在接觸窗口開始時被捕獲。|
| DOPPLER_COMP 暫存器位寬 | 16-bit signed，範圍 -32768 ~ +32767 Hz（約 ±32.77 kHz）| **PASS** — 暫存器範圍足夠覆蓋 ±25 kHz ARM 預補償輸入，無溢位問題。|

**Doppler 核查結論**：**發現 2 個問題**，均標記為 Action Items：
1. **AI-C003-02**（Medium）：C-003 需補充說明 Costas loop 的 pull-in range 量化分析（以 ωn 和增益計算），確認 ±25 kHz 殘餘 Doppler 可被捕獲。
2. **AI-C003-03**（Medium）：C-003 需說明 ARM 端 TLE 傳播誤差 ±25 kHz 的假設來源，並分析最壞情況（如 TLE 較舊、軌道異常）下的 Doppler 補償能力。

> **注**：上述問題為設計分析不完整，非設計原理錯誤。ARM 預補償 + Costas loop 的架構本身合理，主要缺失是文件中的量化論證不足。

#### 3.1.3 AXI 暫存器介面與 B-002 ICD IF-03 一致性核查

**核查項目**：C-003 AXI 暫存器介面是否與 ICD 一致

**說明**：C-003 參考文件列表中引用的是「B-008 ICD v1」（而非「B-002」）。C-009 RTM v2 中 IFC-001 追蹤至「B-008 ICD v1」，IFC-002 追蹤至「C-003 FPGA（EPS 通訊模組）」。本審查以 C-003 實際設計內容核查 AXI 介面完整性。

| 查核點 | C-003 設計 | 審查意見 |
|--------|-----------|---------|
| AXI 介面類型 | AXI4-Lite Slave（5 個 32-bit 暫存器）| **PASS** — AXI4-Lite 為標準 ARM/Xilinx 介面協定，符合 Zynq-7020 PS-PL 橋接規範。|
| 暫存器定義完整性 | CTRL（0x00）、STATUS（0x04）、SEU_COUNT（0x08）、DOPPLER_COMP（0x0C）、BER_EST（0x10）| **PASS** — 5 個暫存器均有完整位元定義、存取類型、預設值說明。|
| OBC 需求對應 | IFC-001（UART/SPI OBC↔RF 介面）、IFC-002（I²C EPS↔OBC 介面）| **注意** — RTM v2 中 IFC-001 定義為「UART/SPI OBC↔RF 介面」，但 C-003 設計的是 AXI4-Lite 介面（ARM PS 端）+ SPI DAC/ADC 介面（PL 端）。AXI 為 Zynq 內部 PS-PL 介面，與 OBC 外部 UART/SPI 介面不同。C-003 Section 8 需求矩陣的 SW-001 追蹤此點，但 IFC-001 的「UART/SPI」是指 OBC 板對板介面還是 Zynq 內部 PS-PL 介面，文件層次不夠清晰。— **標記為 AI-C003-04**（低優先，澄清介面層次定義）。|
| RTL Port 宣告 | `axi4l_slave_bridge` module port list 完整（含 AW/W/B/AR/R 五通道）| **PASS** — AXI4-Lite 五通道介面宣告符合 AMBA AXI4-Lite 規範。|

**AXI 介面核查結論**：**大致 PASS**，介面設計本身正確，IFC-001 介面層次定義需澄清（AI-C003-04，低優先）。

---

## 4. C-004 ADCS 控制律 — 審查意見

### 4.1 審查者 B（Mech Agent）

#### 4.1.1 場景 D 極區 RW 68% 消耗量核查

**核查項目**：場景 D（極區）RW 68% 消耗量是否與 PATCH-P3 數字一致

| 查核點 | C-004 數據 | PATCH-P3 引用 | 審查意見 |
|--------|-----------|-------------|---------|
| RW 角動量容量 | 0.25 mNms（CubeWheel Nano 規格）| PATCH-P3 更新後規格（B-006 v1.1 + PATCH-P3）| **PASS** — C-004 一致採用 0.25 mNms。|
| 極區 RW 消耗量計算 | 0.4×10⁻⁶ Nm × 426 s = 0.17 mNms = 68% 容量 | — | **計算驗算**：0.4 μNm × 426 s = 0.170 mNms；0.170 / 0.25 = 68% — **計算正確**。|
| 426 s 極區停留時間 | |lat| > 80°，持續 7.1 min/orbit = **426 s** | 符合 SSO 500 km 軌道在極區（>80°緯度）的典型停留時間 | **PASS — 合理**。|
| 0.4 μNm 殘磁力矩 | 殘留磁偶極 m = 0.01 Am²，極區 B ≈ 40 μT，力矩 = m × B = 0.01 × 40×10⁻⁶ = **0.4 μNm** | PATCH-P3 Part B 殘磁預算 | **PASS** — 數值自洽，與 PATCH-P3 殘磁設計假設一致。|
| PATCH-P3 明確引用 | C-004 Section 4 指出「本表為 PATCH-P3 誤差預算的控制模擬版本」| 間接引用 PATCH-P3 | **PASS** — 明確聲明與 PATCH-P3 的繼承關係。|

**場景 D 68% 消耗量核查結論**：**PASS**，計算正確，與 PATCH-P3 假設一致。入極前 32% 安全裕度設計合理。

#### 4.1.2 去飽和律增益 K_desat 核查

**核查項目**：去飽和律 `m_dump = -K_desat × (B × h_rw) / |B|²` 是否有增益 K_desat 具體數值

| 查核點 | C-004 內容 | 審查意見 |
|--------|-----------|---------|
| 公式完整性 | Section 2.3.2：`m_MTQ_dump = -K_desat × (B × h_rw) / |B|²` | **PASS** — 物理公式正確，此為標準 B-dot 延伸型去飽和律（Cross-product law for momentum dumping）。|
| K_desat 數值 | C-004 未給出 K_desat 具體數值，僅說明「調整去飽和速率 vs. 姿態擾動 trade-off」| **問題** — K_desat 缺乏具體數值，且無設計約束推導。從去飽和時序分析（Section 2.3.3）可反推：去飽和時間約 3–5 min，h_rw = 0.25 mNms，B ≈ 30 μT，MTQ 偶極矩最大 0.1 Am²/軸。K_desat 的單位應為 [Am²/(T·Nms)] 或等效，缺少此設計值使控制律設計無法被第三方重現或驗證。|
| 待辦事項 | C-004 Section 9（文件待辦）明確列出：「K_MTQ、K_RW、K_d 增益具體數值（需模擬調整後確定）」| K_desat 同樣應列入此待辦，但 Section 9 原文未明確提及 K_desat（只提到 K_MTQ、K_RW、K_d）。|
| 影響評估 | K_desat 缺失不影響 CDR 設計基準線（增益確定在 Sprint 4 模擬後），但應在 Section 9 待辦清單中明確列出 | — |

**K_desat 核查結論**：**發現問題**，K_desat 具體數值缺失且未列入文件待辦清單 — **標記為 AI-C004-01**（Medium 優先）：C-004 需在 Section 9 待辦清單補充「K_desat 增益設計值確定（含 trade-off 分析），Sprint 4 Python 模擬時完成」。

**補充說明**：去飽和時間估算（Section 2.3.2）使用力矩直接積分方法，與 K_desat 參數化方程並行，實際上為「基於最大 MTQ 偶極矩的去飽和時間上界估算」，兩者不矛盾，但正式飛行控制律需要明確的 K_desat 值。

#### 4.1.3 熱彎曲誤差 0.3°（1σ）佐證核查

**核查項目**：熱彎曲誤差 0.3°（1σ）是否有 C-005 熱分析佐證

| 查核點 | C-004 內容 | 審查意見 |
|--------|-----------|---------|
| 誤差數值 | 場景 A 誤差預算表（Section 3 + Section 4）：「熱彎曲（結構）0.3°（1σ），參考：熱分析估算」| — |
| 佐證文件 | C-004 在誤差預算表「參考」欄記載「熱分析估算」，但未明確引用 C-005 文件編號或章節 | **問題** — 誤差預算表應明確引用「C-005 v1.0 Section X.X」而非只寫「熱分析估算」。若 C-005 無法支撐 0.3° 數字（例如 C-005 僅給出溫度分布，未計算熱彎曲角），則此誤差源的量化依據不足。|
| 數值合理性 | 0.3°（1σ）熱彎曲誤差對 3U CubeSat 是否合理？ | 3U CubeSat 結構尺寸小（100×100×340 mm），溫差梯度引起的結構彎曲效應通常在 0.1~0.5° 量級，0.3° 數字量級合理。但「合理」不等於「有佐證」。|
| 影響評估 | 若 0.3° 低估（例如實際 0.5°），則 RSS 結果為 √(0.5²+0.3²+0.8²+1.0²+0.5²+0.5²) = √2.48 ≈ 1.575°，3σ = 4.7°，仍滿足 SYS-008（≤5°），但設計目標 ±3.1° 將不再成立。| 若 0.3° 高估（C-005 計算結果更小），則設計裕度更大。|

**熱彎曲誤差核查結論**：**發現問題** — **標記為 AI-C004-02**（Medium 優先）：C-004 誤差預算表「熱彎曲」誤差源應補充明確引用「C-005 v1.0」文件編號與具體章節，確認 0.3°（1σ）數字有 C-005 熱結構分析的明確支撐，若 C-005 未包含此計算，需補充熱彎曲角度估算方法。

---

## 5. 總體評審結論

### 5.1 審查者 A（通訊酬載工程師）結論

**評級：Conditional Approve**

**理由**：
- C-009 RTM v2 對 SYS-009、SYS-010、SYS-011 的追蹤基本正確，VA-001 引用 B-001 v2.1（含 PATCH-P1 修正）已確認，CDR-AI-001 已列入追蹤。
- C-003 FPGA RTL 設計架構（QPSK 1/2、200 kSps、TMR + ICAP）正確，符合 B-001 v2.1 系統規格。
- 識別出 3 個中低優先度問題（AI-C003-01：BER 框架說明、AI-C003-02：Costas loop pull-in range 量化、AI-C003-03：TLE 誤差依據），均為文件論證不完整，非設計原理錯誤。
- 無阻擋 CDR Go 的重大問題。

**建議**：
1. C-003 補充 Costas loop pull-in range 量化分析（AI-C003-02），確認 ±25 kHz 殘餘 Doppler 捕獲能力。
2. C-003 與 C-009 RTM v2 就 SYS-011 BER 目標的描述框架（系統工作點 vs 最低性能點）對齊，避免未來 VT-002 測試驗收爭議。

### 5.2 審查者 B（機構熱控工程師）結論

**評級：Conditional Approve**

**理由**：
- C-009 V&V 計畫整體完整，A 類分析（VA-001~005）全部完成，T 類測試計畫清晰。
- CDR-AI-006（電池加熱器評估）已列入且有追蹤，電池低溫問題已識別。
- C-004 ADCS 控制律設計架構合理，場景 D 的 68% 計算與 PATCH-P3 一致，SYS-008 需求在各場景下均符合。
- 識別出 3 個中低優先度問題（AI-C004-01：K_desat 缺失、AI-C004-02：熱彎曲引用缺失、AI-C009-01：VT-005 電池邊界補充），均不影響設計基準線。
- 無阻擋 CDR Go 的重大問題。

**建議**：
1. C-004 Section 9 待辦清單補充 K_desat 增益確定計畫（AI-C004-01）。
2. C-004 誤差預算表明確引用 C-005 章節支撐 0.3° 熱彎曲數字（AI-C004-02）。
3. VT-005 測試計畫在加熱器方案確定後補充電池 -10°C 邊界驗收準則（AI-C009-01）。

### 5.3 P2P Review 最終結論

| 評估維度 | 結論 |
|---------|------|
| 設計完整性 | 三份文件設計框架完整，覆蓋所有關鍵子系統 |
| 技術正確性 | 核心技術數字（Link Budget、QPSK、ADCS 控制律、RW 消耗）計算正確 |
| 需求追蹤 | RTM v2 追蹤至 37 條需求，設計可追蹤性達標 |
| 文件完整性 | 部分引用與論證說明待補充，均為中低優先度 |
| 阻擋問題 | **無** — 無需退回修改 |

**P2P Review 結論：通過（Conditional Approve）**

**CDR Go/No-Go 建議**：支持 CDR Go，進入 Sprint 4。本 P2P Review 識別的 7 個 Action Items 均為軟性條件，不影響設計基準線凍結。

---

## 6. Action Items 匯總

| AI ID | 來源文件 | 問題描述 | 優先 | 負責人 | 期限 | 說明 |
|-------|---------|---------|------|-------|------|------|
| AI-C003-01 | C-003 / C-009 SYS-011 | C-003 補充說明 BER 目標描述框架：系統工作點 Eb/N0 = 9.8 dB vs 最低性能點 Eb/N0 = 4.5 dB，對齊 VT-002 測試準則（10⁻⁶）| Medium | SW/FW Agent | Sprint 4 Week 1 | 文件說明問題，非設計缺陷 |
| AI-C003-02 | C-003 Doppler | 補充 Costas loop pull-in range（頻率拉入範圍）量化分析，確認 ±25 kHz 殘餘 Doppler 可在接觸窗口開始前被捕獲 | Medium | SW/FW Agent | Sprint 4 Week 1 | 當前文件僅描述 BW 未給 pull-in range |
| AI-C003-03 | C-003 Doppler | 補充 ARM 端 TLE 傳播誤差 ±25 kHz 假設的來源依據，分析 TLE 較舊情況下的最壞情況 Doppler 補償能力 | Medium | SW/FW Agent | Sprint 4 Week 2 | 確認系統對 TLE 更新頻率的依賴 |
| AI-C003-04 | C-003 AXI / IFC-001 | 澄清 IFC-001「UART/SPI OBC↔RF 介面」與 C-003 AXI4-Lite PS-PL 介面的層次關係，在 ICD（B-008）中明確區分內部介面與外部介面 | Low | SW/FW Agent + SE | Sprint 4 Week 2 | 文件清晰度問題 |
| AI-C004-01 | C-004 去飽和律 | C-004 Section 9 待辦清單補充「K_desat 增益設計值確定（含 trade-off 分析），Sprint 4 Python 模擬完成」| Medium | AOCS Agent | Sprint 4 Week 2 | K_desat 缺乏具體值且未列入待辦 |
| AI-C004-02 | C-004 熱彎曲誤差 | C-004 誤差預算表「熱彎曲 0.3°（1σ）」補充明確引用 C-005 v1.0 文件章節；若 C-005 未包含熱彎曲角計算，需補充估算方法 | Medium | AOCS Agent + Mech Agent | Sprint 4 Week 2 | 確保誤差預算可追蹤 |
| AI-C009-01 | C-009 VT-005 | VT-005 TVAC 測試計畫在 CDR-AI-006 加熱器方案確定後，補充電池 -10°C 電容量驗收準則；同步評估 0.75 W 加熱器對 Power Budget DoD 的影響 | Medium | QA + Mech Agent + SE | Sprint 4 Week 2（CDR-AI-006 完成後）| 確保 TVAC 能捕獲電池低溫失效模式 |
| AI-C009-02 | C-009 VA-005 | 確認 C-005 v1.0 熱分析是否已納入 DCN-002 電池規格修正後的發熱量，若未納入需更新 VA-005 | Low | SE + Mech Agent | Sprint 4 Week 3 | 低優先，不影響現有熱分析結論 |

**Action Items 統計：8 項，Medium 5 項、Low 3 項（含原 CDR-AI 中的追蹤項目）**

> **注**：本報告的 AI-C003-01~04、AI-C004-01~02、AI-C009-01~02 為 P2P Review 新識別的 Action Items，獨立於 C-009 原有的 CDR-AI-001~008 清單，建議合併入 CDR-AI 主清單統一追蹤（CDR-AI-009~016 或依 PM 排序）。

---

## 附錄 A：P2P Review 審查方法說明

本次 P2P Review 採用文件對照審查方式：
1. 閱讀三份審查文件的全文
2. 對照上游參考文件（B-001 v2.1、PATCH-P3、CDR-AI 清單等）逐項核查
3. 計算關鍵數字（RW 消耗量、RSS 誤差預算、Doppler 補償範圍）獨立驗算
4. 標記疑慮項目並歸類為 PASS / 條件 PASS / 問題
5. 無法通過文件核查的項目（如 C-005 熱彎曲計算細節）標記為「建議確認」

---

## 附錄 B：文件版本記錄

| 版本 | 日期 | 修訂摘要 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-04-15 | 初版（完整 P2P Review 報告）| QA 工程師（P2P Review 主席）|

---

*C-010 P2P Review — Sprint 3 Final — QA 工程師 — 2026-04-15*
*TASA-NTN-3U CubeSat 任務 — Sprint 3 Wave 3*
