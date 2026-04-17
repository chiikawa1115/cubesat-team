# SRS v3 — 系統需求規格書（System Requirements Specification）

| 欄位 | 內容 |
|------|------|
| 文件編號 | SRS-003 |
| 版本 | v3 |
| 日期 | 2026-05-28 |
| 作者 | SE Agent 陳明哲 |
| 狀態 | 已發行（Issued） |
| 分類 | CubeSat 任務系統層級文件 |

---

## 版本歷史

| 版本 | 日期 | 作者 | 摘要 |
|------|------|------|------|
| v1 | 2026-01-15 | SE Agent 陳明哲 | 初版發行，建立任務基線需求（軌道、通訊、結構、熱控、ADCS、輻射） |
| v2 | 2026-03-10 | SE Agent 陳明哲 | 納入 D-001 Link Budget 分析結果，更新通訊需求；新增 SYS-016 ~ SYS-021 |
| v3 | 2026-05-28 | SE Agent 陳明哲 | 依 DCN-003（降速 50 kbps + Driver Amp）及 D-003 v3.1 Link Budget 修訂 SYS-002、SYS-003、SYS-004（拆分為 SYS-004a/b）；回應 P2P Review AI-D003-4 行動項目 |

### v3 修訂說明

本次修訂源自以下兩份文件的分析結果：

- **DCN-003**（設計變更通知 003）：通訊架構降速至 50 kbps，加入 Driver Amplifier，上鏈無 HARQ。
- **D-003 v3.1 Link Budget**：在仰角 60° 條件下，UL 鏈路 Margin +1.2 dB（Viterbi R=1/2 硬判決，無 HARQ）；DL 在仰角 30° 含 HARQ 6× 合併下 Margin ≥ 3 dB。
- **P2P Review AI-D003-4**：要求修訂 SYS-002、SYS-003、SYS-004 三條需求以反映實際鏈路閉合條件。

---

## 1. 範圍（Scope）

本文件規定 CubeSat 任務系統層級需求，涵蓋軌道、通訊、結構、電力、熱控、ADCS、輻射防護及頻率協調等子系統。所有子系統設計文件（D-001 至 D-006）及驗證計畫（V&V Plan）均須追蹤至本文件。

---

## 2. 適用文件

| 文件編號 | 標題 | 版本 |
|---------|------|------|
| DCN-003 | 設計變更通知：通訊降速 50 kbps + Driver Amp | Rev1 |
| D-003 | Link Budget Analysis | v3.1 |
| D-002 | ADCS Monte Carlo Simulation Report | v2 |
| B-006 | ADCS Pointing Budget | Rev1 |
| CubeSat Standard | CubeSat Design Specification | Rev14 |
| IADC-2002-01 | IADC Space Debris Mitigation Guidelines | 2007 |
| 3GPP TS 36.213 | NB-IoT NTN Physical Layer Procedures | Rel-17 |

---

## 3. 系統需求（System Requirements）

### 說明欄位定義

- **驗證方法**：A = 分析（Analysis）、T = 測試（Test）、S = 模擬（Simulation）、I = 檢視（Inspection）
- **[v3 修訂]**：本版本修訂之條目
- **狀態**：TBV = 待驗證、VER = 已驗證

---

### 3.1 軌道（Orbit）

#### SYS-001：軌道參數

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-001 |
| 需求描述 | 衛星應部署於高度 500 km、傾角 97.4° 之太陽同步軌道（SSO）。軌道週期約 94.6 分鐘，LTAN 為 10:30 AM（降交點地方時）。 |
| 依據 | 任務概念（ConOps）Section 2.1，Launch manifest |
| 驗證方法 | A（軌道設計分析）、S（STK/GMAT 模擬） |
| 狀態 | TBV |

---

### 3.2 通訊（Communication）

#### SYS-002：最低服務仰角 [v3 修訂]

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-002 |
| 需求描述 | 系統應在地面站仰角 **≥ 60°** 時提供雙向通訊服務。 |
| 修訂前（v2） | 仰角 ≥ 5°（地面站可視範圍邊緣） |
| 修訂後（v3） | 仰角 ≥ 60° |
| 修訂理由 | D-003 v3.1 Link Budget 顯示：仰角 60° 時 UL Margin = +1.2 dB（Viterbi R=1/2 硬判決，無 HARQ），為雙向鏈路最低可閉合仰角。5° 仰角下 UL 鏈路無法閉合。（DCN-003 + D-003 v3.1）|
| 依據 | DCN-003 Rev1, D-003 v3.1 Table 3-2 |
| 驗證方法 | A（Link Budget 分析）、S（STK 過境模擬） |
| 狀態 | TBV |

#### SYS-003：資料速率 [v3 修訂]

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-003 |
| 需求描述 | 上鏈（UL）及下鏈（DL）資料速率應 **≥ 50 kbps**。 |
| 修訂前（v2） | ≥ 200 kbps |
| 修訂後（v3） | ≥ 50 kbps |
| 修訂理由 | 依 DCN-003，通訊架構重新定位為 NTN IoT Bent-Pipe，符合 3GPP Rel-17 NB-IoT NTN 最大速率 ≤ 127 kbps 之規範定位。200 kbps 無法在現有 RF 預算下實現。（DCN-003 + D-003 v3.1）|
| 依據 | DCN-003 Rev1, 3GPP TS 36.213 Rel-17 |
| 驗證方法 | T（RF 鏈路測試）、A（Link Budget 分析） |
| 狀態 | TBV |

#### SYS-004a：上鏈 Link Margin [v3 修訂]

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-004a |
| 需求描述 | 上鏈（UL）Link Margin 應 **≥ 0 dB**，條件：仰角 ≥ 60°、調變 Viterbi R=1/2 硬判決、無 HARQ。 |
| 修訂說明 | 原 SYS-004 拆分為 SYS-004a（UL）及 SYS-004b（DL），以反映 UL/DL 不同鏈路條件。（DCN-003 + D-003 v3.1）|
| 依據 | D-003 v3.1 Table 3-2（UL Margin = +1.2 dB @60°） |
| 驗證方法 | A（Link Budget）、S（系統模擬） |
| 狀態 | TBV |

#### SYS-004b：下鏈 Link Margin [v3 修訂]

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-004b |
| 需求描述 | 下鏈（DL）Link Margin 應 **≥ 3 dB**，條件：仰角 ≥ 30°、含 HARQ 6× 合併。 |
| 修訂說明 | 原 SYS-004 拆分，DL 可藉由 HARQ 合併增益補償低仰角損耗，故最低服務仰角放寬至 30°。（DCN-003 + D-003 v3.1）|
| 依據 | D-003 v3.1 Table 3-3（DL Margin = +3.8 dB @30° with HARQ 6×） |
| 驗證方法 | A（Link Budget）、S（系統模擬） |
| 狀態 | TBV |

#### SYS-012：頻率協調

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-012 |
| 需求描述 | 衛星無線電頻率應通過 ITU 協調程序，S-band 上鏈 1995 MHz、下鏈 2185 MHz。 |
| 依據 | 頻率申請文件 FR-001 |
| 驗證方法 | I（ITU 協調文件審查） |
| 狀態 | TBV |

#### SYS-016：天線增益

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-016 |
| 需求描述 | 星載天線增益應 ≥ 0 dBi（含所有方向性損失）。 |
| 依據 | D-003 v3.1 |
| 驗證方法 | T（天線測量）、A（分析） |
| 狀態 | TBV |

#### SYS-017：接收機雜訊指數

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-017 |
| 需求描述 | 星載接收機雜訊指數（NF）應 ≤ 3 dB。 |
| 依據 | D-003 v3.1 Noise Figure Budget |
| 驗證方法 | T（接收機 NF 量測）、A（雜訊分析） |
| 狀態 | TBV |

---

### 3.3 結構與機械（Structure & Mechanical）

#### SYS-005：衛星質量

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-005 |
| 需求描述 | 衛星發射質量（含燃料）應 ≤ 4000 g。 |
| 依據 | Launch Provider ICD |
| 驗證方法 | T（整星秤重） |
| 狀態 | TBV |

#### SYS-018：CubeSat Standard 符合性

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-018 |
| 需求描述 | 衛星外型、P-POD 介面及電氣介面應符合 CubeSat Design Specification Rev14。 |
| 依據 | CubeSat Standard Rev14 |
| 驗證方法 | I（文件符合性審查）、T（介面配合試驗） |
| 狀態 | TBV |

#### SYS-020：質量（與 SYS-005 對齊）

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-020 |
| 需求描述 | 衛星乾質量（不含推進劑）應 ≤ 4000 g，與 SYS-005 一致。 |
| 依據 | Launch Provider ICD |
| 驗證方法 | T（整星秤重） |
| 狀態 | TBV |
| 備注 | SYS-005 與 SYS-020 同值，子系統 BOM 質量總和應留有 ≥ 10% 裕量。 |

#### SYS-021：重心偏移

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-021 |
| 需求描述 | 衛星重心（CG）距幾何中心之偏移應 < 20 mm（三軸）。 |
| 依據 | CubeSat Standard Rev14 Section 4.2 |
| 驗證方法 | T（CG 量測試驗）、A（結構模型分析） |
| 狀態 | TBV |

---

### 3.4 電力（Power）

#### SYS-006：功耗（Science Mode）

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-006 |
| 需求描述 | 衛星在 Science Mode（通訊酬載啟動）下之平均功耗應 ≤ 8 W。 |
| 依據 | D-004 System Budget Table 3（電力預算） |
| 驗證方法 | T（功耗量測）、A（電力預算分析） |
| 狀態 | TBV |

---

### 3.5 軌道壽命（Mission Lifetime）

#### SYS-007：軌道壽命

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-007 |
| 需求描述 | 衛星應在軌執行任務 ≥ 1 年，並符合 IADC 25 年自然除軌規範（500 km SSO 自然除軌 < 25 年）。 |
| 依據 | IADC-2002-01, D-001 軌道分析 |
| 驗證方法 | A（大氣阻力除軌分析）、S（STK 軌道衰減模擬） |
| 狀態 | TBV |

---

### 3.6 ADCS

#### SYS-008：指向精度

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-008 |
| 需求描述 | ADCS 在 Nadir-pointing 模式下，指向精度應 ≤ 5°（3σ）。 |
| 依據 | D-002 ADCS Design, B-006 Pointing Budget |
| 驗證方法 | S（Monte Carlo 模擬）、T（ADCS HIL 測試） |
| 狀態 | TBV |
| 備注 | D-002 v2 Monte Carlo 結果：日照段 ±2.9°、食月段 ±3.4°，均符合本需求（詳見 B-006 Rev1）。 |

#### SYS-009：Detumbling 時間

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-009 |
| 需求描述 | 衛星分離後，ADCS 應在 ≤ 60 分鐘內完成 Detumbling（角速度 ≤ 0.5°/s）。 |
| 依據 | D-002 ADCS Design Section 5 |
| 驗證方法 | S（ADCS 模擬）、T（地面試驗） |
| 狀態 | TBV |

#### SYS-014：ADCS 模式序列

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-014 |
| 需求描述 | ADCS 應支援以下自動模式轉換序列：Detumbling → Sun-pointing → Nadir-pointing。各模式轉換條件由 OBC 依感測器狀態自動判斷。 |
| 依據 | D-002 ADCS Design Section 4 |
| 驗證方法 | S（模式轉換模擬）、T（全系統整合測試） |
| 狀態 | TBV |

---

### 3.7 熱控（Thermal）

#### SYS-010：溫度範圍

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-010 |
| 需求描述 | 所有星載電子元件應在以下溫度範圍內正常運作與存放：運作溫度：-20°C ~ +60°C；存放溫度：-40°C ~ +80°C。 |
| 依據 | Component datasheets, ECSS-Q-ST-70-08 |
| 驗證方法 | T（熱真空試驗）、A（熱分析） |
| 狀態 | TBV |

---

### 3.8 輻射防護（Radiation）

#### SYS-011：SEU 防護

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-011 |
| 需求描述 | 系統應具備 SEU（Single Event Upset）防護機制，包含：EDAC（錯誤偵測與更正）、WDT（Watchdog Timer）週期 1 s、SAA（South Atlantic Anomaly）期間 FPGA 動態 scrubbing 週期 ≤ 1 ms。 |
| 依據 | D-005 Radiation Design Note |
| 驗證方法 | T（輻射照射試驗）、A（SEE 分析） |
| 狀態 | TBV |

#### SYS-013：TID 耐受

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-013 |
| 需求描述 | 所有星載元件之 Total Ionizing Dose（TID）耐受值應 ≥ 5 krad（Al 屏蔽，1 年任務期間累積劑量）。 |
| 依據 | D-005 Radiation Design Note, SPENVIS 分析 |
| 驗證方法 | T（TID 照射試驗）、A（劑量估算分析） |
| 狀態 | TBV |

#### SYS-015：TID 裕量

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-015 |
| 需求描述 | 元件 TID 耐受值對任務期間估算劑量之裕量應 ≥ 2×（即元件 TID ≥ 2 × 任務劑量）。 |
| 依據 | ECSS-E-ST-10-12, D-005 |
| 驗證方法 | A（劑量-耐受比值分析） |
| 狀態 | TBV |

#### SYS-019：SAA Scrubbing 週期

| 欄位 | 內容 |
|------|------|
| 需求 ID | SYS-019 |
| 需求描述 | 在 SAA 過境期間，FPGA configuration scrubbing 週期應 ≤ 10 ms，以限制 SEU 累積造成功能異常之概率。 |
| 依據 | D-005 Radiation Design Note Section 6.2 |
| 驗證方法 | T（FPGA scrubbing 功能測試）、A（SEU 率分析） |
| 狀態 | TBV |

---

## 4. 需求追蹤矩陣（Requirements Traceability Matrix）

| 需求 ID | 描述摘要 | 驗證方法 | 下游文件 | v3 狀態 |
|---------|---------|---------|---------|---------|
| SYS-001 | 500 km SSO, 97.4° | A, S | D-001 | 無修訂 |
| SYS-002 | 最低服務仰角 ≥ 60° | A, S | D-003, B-005 | **[v3 修訂]** |
| SYS-003 | 資料速率 ≥ 50 kbps | T, A | D-003 | **[v3 修訂]** |
| SYS-004a | UL Margin ≥ 0 dB @≥60° | A, S | D-003 | **[v3 新增/拆分]** |
| SYS-004b | DL Margin ≥ 3 dB @≥30° | A, S | D-003 | **[v3 新增/拆分]** |
| SYS-005 | 質量 ≤ 4000 g | T | D-004, BOM | 無修訂 |
| SYS-006 | 功耗 ≤ 8 W（Science Mode）| T, A | D-004 | 無修訂 |
| SYS-007 | 軌道壽命 ≥ 1 年 | A, S | D-001 | 無修訂 |
| SYS-008 | 指向精度 ≤ 5°（3σ）| S, T | D-002, B-006 | 無修訂 |
| SYS-009 | Detumbling ≤ 60 min | S, T | D-002 | 無修訂 |
| SYS-010 | 溫度範圍 -20°C~+60°C / -40°C~+80°C | T, A | D-006 | 無修訂 |
| SYS-011 | SEU 防護（EDAC + WDT + scrubbing）| T, A | D-005 | 無修訂 |
| SYS-012 | 頻率協調（UL 1995 MHz / DL 2185 MHz）| I | FR-001 | 無修訂 |
| SYS-013 | TID ≥ 5 krad | T, A | D-005 | 無修訂 |
| SYS-014 | ADCS 模式序列 | S, T | D-002 | 無修訂 |
| SYS-015 | TID 裕量 ≥ 2× | A | D-005 | 無修訂 |
| SYS-016 | 天線增益 ≥ 0 dBi | T, A | D-003 | 無修訂 |
| SYS-017 | NF ≤ 3 dB | T, A | D-003 | 無修訂 |
| SYS-018 | CubeSat Standard Rev14 | I, T | 全子系統 | 無修訂 |
| SYS-019 | SAA scrubbing ≤ 10 ms | T, A | D-005 | 無修訂 |
| SYS-020 | 乾質量 ≤ 4000 g | T | BOM | 無修訂 |
| SYS-021 | CG 偏移 < 20 mm | T, A | D-006 | 無修訂 |

---

## 5. 修訂影響分析（v3 Change Impact）

| 受影響文件 | 影響說明 | 負責人 | 預計更新版本 |
|-----------|---------|-------|-------------|
| D-003 Link Budget | 已納入修訂基礎（v3.1），無需追加修訂 | 通訊酬載 Agent | 已完成 |
| D-004 System Budget | Table 通訊欄位速率需更新為 50 kbps | SE Agent | v3 |
| V&V Plan | SYS-002/003/004 驗證方法/條件更新 | QA Agent | Rev2 |
| Test Spec | 鏈路測試條件需改為 60° 仰角基準 | 通訊酬載 Agent | Rev2 |
| ConOps | 通聯視窗計算需改用 60° 最低仰角 | SE Agent | v3 |

---

*文件結束 — SRS v3 / 2026-05-28 / SE Agent 陳明哲*
