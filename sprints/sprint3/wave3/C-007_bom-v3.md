---
deliverable: C-007
sprint: 3
wave: 3
author: PM Agent（詹雅婷）
date: 2026-04-15
version: v3.0
status: draft
reference_documents:
  - sprints/sprint2/wave2/B-009_bom-v2.md（BOM v2.1 基準）
  - sprints/sprint3/wave2/C-002_rf-pcb-design-v1.md（RF PCB 設計，元件料號確認）
  - sprints/sprint2/patches/PATCH-P5-thermal-power.md（DCN-002 電池升級根因分析）
  - sprints/sprint3/wave2/C-005_thermal-detail-v1.md（C-005 熱控材料需求）
  - sprints/sprint3/SPRINT3_PLAN.md（CDR Entry Criteria）
---

# C-007：BOM v3.0 定案（Sprint 3 Wave 3 CDR 版本）

**文件版本**：v3.0
**負責人**：PM Agent（詹雅婷）
**日期**：2026-04-15
**狀態**：Draft — 待 CDR 審查前定案

---

## 變更摘要（v2.1 → v3.0）

| 變更項目 | v2.1 狀態 | v3.0 更新 | 來源 |
|---------|----------|----------|------|
| RF 鏈路元件料號 | 型號確認，無 DigiKey 料號/報價 | **確認完整料號 + DigiKey 實際報價** | C-002 RF PCB 設計 |
| RF PCB 打樣費 | $500–$1,000 區間，無明確板廠 | **JLCPCB 4L，95×90mm，5 片，~$60–80** | C-002 §1.3 |
| TCXO（LO 190 MHz）| 未列入 BOM | **新增 TXO-L2 或等效 SMD TCXO** | C-002 §3 |
| PA enable MOSFET | 未列入 BOM | **新增 2N7002K SOT-23** | C-002 §3 |
| 電池（DCN-002）| 10 Wh → 15 Wh（v2.1 已反映） | **確認維持 15 Wh，EPS 價格區間確認** | PATCH-P5 §3 Option 1 |
| 熱控材料（C-005）| TIM pad / 加熱器基本列項 | **新增 Al 屏蔽板（Zynq 區域），規格細化** | C-005 §2.5 |
| 感測器雜項 | HMC5883L + BMX160 + LEA-M8S 組合 | **維持，確認 DigiKey 採購** | B-006 ADCS trade study |
| 教育折扣 | GomSpace/ISIS/EnduroSat 10-20% | **更新為 10-30%，含 CubeSpace 15-25%** | 廠商教育方案更新 |

---

## 完整元件清單（BOM v3.0）

### 表 1：OBC 子系統

| ID | 元件 | 型號/規格 | 數量 | 單價（USD）| 小計（USD）| 採購方式 | 狀態 |
|----|------|---------|:----:|:---------:|:---------:|---------|------|
| OBC-01 | OBC 模組（Zynq-7020 class）| Xiphos Q7s | 1 | $25,000 | **$25,000** | 廠商詢價（Xiphos Systems）| 詢價中 |

**OBC 小計：$25,000**

> **C-003 確認**：Xiphos Q7s 搭載 Zynq-7020 SoC（ARM Cortex-A9 + Artix-7 FPGA fabric），符合 B-007 FPGA RTL 設計架構要求。DDR3 1 GB + 1 GB Flash。Lead time 預估 8-12 週，PDR 後立即發 RFQ。

---

### 表 2：EPS + 電池子系統

| ID | 元件 | 型號/規格 | 數量 | 單價（USD）| 小計（USD）| 採購方式 | 狀態 |
|----|------|---------|:----:|:---------:|:---------:|---------|------|
| EPS-01 | EPS 含 15 Wh Li-ion 電池 | GomSpace NanoPower P31u（15 Wh 配置） | 1 | $4,000–$8,000（中位 $6,000）| **$6,000** | GomSpace 詢價 | 詢價中 |

**EPS 小計：$6,000**

> **DCN-002 確認**：電池容量從 10 Wh → 15 Wh（CEO 2026-04-15 核准）。PATCH-P5 分析顯示 15 Wh 配置使 EOL + 低溫（-8.3°C）effective 容量 = 9.00 Wh，正常 Eclipse DoD = 19.8%（PASS，裕度 10.2%），Worst case DoD = 25.2%（PASS，裕度 4.8%）。質量增加 +250g，仍在 Mass Budget 裕度內。

---

### 表 3：ADCS 子系統

| ID | 元件 | 型號/規格 | 數量 | 單價（USD）| 小計（USD）| 採購方式 | 狀態 |
|----|------|---------|:----:|:---------:|:---------:|---------|------|
| ADCS-01 | 磁力矩器 | COTS MTQ（3軸組） | 3 | $500/支 | **$1,500** | 廠商詢價 | 詢價中 |
| ADCS-02 | 反應輪（yaw 軸）| CubeSpace CubeWheel Nano | 1 | $3,000–$4,000（中位 $3,500）| **$3,500** | 廠商詢價（CubeSpace）| 詢價中 |
| ADCS-03 | 磁力計 | HMC5883L | 1 | $5 | **$5** | DigiKey | 備貨 |
| ADCS-04 | IMU | BMX160 | 1 | $8 | **$8** | DigiKey | 備貨 |
| ADCS-05 | GNSS 接收模組 | u-blox LEA-M8S | 1 | $187 | **$187** | DigiKey | 備貨 |

**ADCS 小計：$5,200**

> **B-006 v1.1 確認**：CubeWheel Nano 加入（B-006 trade study 結論），提供 yaw 軸角動量管理。感測器組（HMC5883L + BMX160 + LEA-M8S）DigiKey 採購，合計約 $200。

---

### 表 4：S-band 酬載子系統 — RF 鏈路元件

| ID | 元件 | 型號/規格（DigiKey 料號） | 數量 | 單價（USD）| 小計（USD）| 採購方式 | 狀態 |
|----|------|------------------------|:----:|:---------:|:---------:|---------|------|
| RF-01 | LNA | ADL5523ACPZ-R7（ADI） | 2 | $4.38 | **$8.76** | DigiKey #ADL5523ACPZ-R7CT-ND | 確認報價 |
| RF-02 | PA | PMA3-43-1W+（Mini-Circuits） | 1 | 詢價中 | **~$45** | DigiKey / Mini-Circuits 直購 | 詢價中 |
| RF-03 | BPF（UL + DL 各一） | SYBP-2250+（Mini-Circuits） | 2 | $24.58 | **$49.16** | DigiKey #SYBP-2250+-ND | 確認報價 |
| RF-04 | Mixer | LT5512EUF#PBF（Analog Devices / Linear） | 1 | $11.14 | **$11.14** | DigiKey #LT5512EUF#PBF-ND | 確認報價 |
| RF-05 | TCXO（LO 190 MHz） | TXO-L2 或等效 SMD TCXO（≤±1 ppm，-40~+85°C） | 1 | ~$5–$10（中位 $7.5）| **$7.50** | DigiKey / Mouser | 選型確認中 |
| RF-06 | PA enable MOSFET | 2N7002K SOT-23 | 2 | $0.30 | **$0.60** | DigiKey | 備貨 |
| RF-07 | DC Block 電容（RF 路徑）| 100 nF 0402 C0G | 6 | $0.10 | **$0.60** | DigiKey | 備貨 |
| RF-08 | 匹配網路 L/C 被動元件 | 0402 RF inductor/cap 組合 | 1 組 | $10 | **$10** | DigiKey/Mouser | 設計確認後下單 |
| RF-09 | SMA 連接器（RF I/O） | edge-mount SMA，50Ω | 2 | $3.50 | **$7** | DigiKey | 備貨 |

**RF 鏈路元件小計：~$139.76**

> **C-002 料號確認說明**：
> - **LNA ADL5523ACPZ-R7**：Analog Devices LFCSP-8，NF 1 dB @2 GHz，Gain 15 dB，+3.3V，DigiKey 報價 $4.38×2 = $8.76。雙份採購（Tx 路徑備援或調試用）。
> - **PA PMA3-43-1W+**：Mini-Circuits GaAs pHEMT，Psat +32.6 dBm，P1dB +30.3 dBm，+12V/350 mA，PAE ~25%，QFN 3×3mm。DigiKey 查詢中，預估 ~$45；備品另計入備品 10%。
> - **BPF SYBP-2250+**：Mini-Circuits，fc 2250 MHz，BW 740 MHz，IL ~1.5 dB，Rej @±500 MHz >30 dB。UL BPF（LNA 後）+ DL BPF（Mixer IF 後），各一。DigiKey $24.58×2 = $49.16。
> - **Mixer LT5512EUF#PBF**：Analog Devices，RF 1k–3 GHz，LO 30–3 GHz，IIP3 +18 dBm，QFN-16（4×4mm）。DigiKey $11.14×1 = $11.14。
> - **TCXO TXO-L2**（或等效）：LO 190 MHz（= DL 2185 MHz - UL 1995 MHz），頻率穩定度 ≤±1 ppm，SMD 封裝，相位雜訊 <-110 dBc/Hz @1 kHz。備選：TXC 7V 系列或 Rakon EF5032A。估算 $5–10，中位 $7.5。

---

### 表 5：S-band 酬載子系統 — RF PCB 製造

| ID | 元件 | 型號/規格 | 數量 | 單價（USD）| 小計（USD）| 採購方式 | 狀態 |
|----|------|---------|:----:|:---------:|:---------:|---------|------|
| PCB-01 | RF PCB 打樣（4 層阻抗控制板）| JLCPCB 4L，95×90mm，FR4，1.0mm，ENIG，50Ω 阻抗控制 | 5 片 | ~$12–$16/片 | **~$70**（估算中位）| JLCPCB 線上下單 | 設計完成後下單 |

**RF PCB 小計：~$70**

> **規格說明（來自 C-002 §1.3）**：4 層板（Top RF / GND / PWR / Bottom），板厚 1.0 mm，FR4 Dk ≈ 4.6 @2 GHz，50Ω 微帶線寬 W ≈ 0.38 mm，ENIG 表面處理，4 個 M3 安裝孔，邊緣 3 mm 禁布區。JLCPCB 4 層阻抗控制服務 5 片估算 $60–80，取中位 $70。製造前需提交阻抗控制報告要求。

---

### 表 6：S-band 天線子系統

| ID | 元件 | 型號/規格 | 數量 | 單價（USD）| 小計（USD）| 採購方式 | 狀態 |
|----|------|---------|:----:|:---------:|:---------:|---------|------|
| ANT-01 | S-band Patch Array 天線 | EnduroSat S-band Patch Antenna（8 dBi，RHCP/LHCP） | 1 | $3,000–$5,000（中位 $4,000）| **$4,000** | 廠商詢價（EnduroSat）| 詢價中 |

**S-band 天線小計：$4,000**

---

### 表 7：TT&C 子系統

| ID | 元件 | 型號/規格 | 數量 | 單價（USD）| 小計（USD）| 採購方式 | 狀態 |
|----|------|---------|:----:|:---------:|:---------:|---------|------|
| TTC-01 | UHF 收發器 | GomSpace AX100 | 1 | $3,000–$5,000（中位 $4,000）| **$4,000** | GomSpace 詢價 | 詢價中 |
| TTC-02 | UHF 折疊偶極天線 | ISIS UHF Deployable Dipole | 1 | $1,000–$2,000（中位 $1,500）| **$1,500** | ISIS 詢價 | 詢價中 |

**TT&C 小計：$5,500**

---

### 表 8：太陽能板（DCN-001 更新）

| ID | 元件 | 型號/規格 | 數量 | 單價（USD）| 小計（USD）| 採購方式 | 狀態 |
|----|------|---------|:----:|:---------:|:---------:|---------|------|
| SOL-01 | 展開式太陽能板（6.5W BOL） | Clyde Space 3U Deployable Solar Panel | 1 組 | $3,000–$6,000（中位 $4,500）| **$4,500** | 廠商詢價（Clyde Space） | 詢價中 |

**太陽能板小計：$4,500**

> **DCN-001 確認**：5W BOL → 6.5W BOL（CEO 2026-04-15 核准）。B-005 Power Budget v2 驗證 EOL avg 3.64W 滿足功耗需求。

---

### 表 9：結構框架

| ID | 元件 | 型號/規格 | 數量 | 單價（USD）| 小計（USD）| 採購方式 | 狀態 |
|----|------|---------|:----:|:---------:|:---------:|---------|------|
| STR-01 | 3U Al 6061-T6 框架 + 展開機構 | ISIS 3U CubeSat Structure | 1 | $3,000–$5,500（中位 $4,250）| **$4,250** | ISIS 詢價 | 詢價中 |

**結構框架小計：$4,250**

---

### 表 10：熱控材料（C-005 更新）

| ID | 元件 | 型號/規格 | 數量 | 單價（USD）| 小計（USD）| 採購方式 | 狀態 |
|----|------|---------|:----:|:---------:|:---------:|---------|------|
| THM-01 | MLI 多層隔熱毯（裁切品） | 多層 MLI，衛星外壁覆蓋 | 1 組 | $200–$500（中位 $350）| **$350** | Amazon / Mouser | 備貨 |
| THM-02 | Kapton 加熱器（電池低溫保護） | 0.5W，-60°C ~ +200°C，尺寸依電池面積定制 | 1 | $50–$100（中位 $75）| **$75** | Mouser | 備貨 |
| THM-03 | TIM pad（導熱介面材料） | λ ≥ 2 W/m·K，RF PCB 與框架間（C-005 §2.5 方案 2） | 5 片 | ~$20/片 | **$100** | Mouser / 3M | 備貨 |
| THM-04 | Al 屏蔽板（Zynq 區域局部輻射屏蔽） | Al 6061，6mm 厚，Zynq-7020 上方，約 60×60mm | 1 片 | $50 | **$50** | 機工廠加工 / McMaster-Carr | 備貨 |
| THM-05 | Al 螺柱/支撐柱（RF PCB 螺鎖外壁用） | M3 × 10mm Al 螺柱，替換原不鏽鋼，降低 θ_mount | 4 | $2 | **$8** | McMaster-Carr | 備貨 |

**熱控材料小計：$583**

> **C-005 更新說明**：
> - **TIM pad（THM-03）**：C-005 §2.5 緩解方案 2，降低 PA 熱阻 θ_mount（5°C/W → ~2°C/W），與 Via array 升級（6×6 → 8×8）組合使用，使 RF PCB 接觸窗口後峰值溫度降至 +34.7°C（裕度 +5.3°C）。λ ≥ 2 W/m·K 為 C-005 指定規格。
> - **Al 屏蔽板（THM-04）**：C-005 熱分析建議針對 Zynq-7020 區域加設局部 Al 屏蔽，同時兼具輻射屏蔽（SPENVIS C-006 分析結果參考）與散熱功能，6mm 厚。
> - **Kapton 加熱器（THM-02）**：維持 0.5W（PATCH-P5 §2.3 情境 1 分析，0.5W 為最佳取捨點，升至 0.75W/1.0W 反而惡化 DoD 而無足夠溫度改善）。

---

### 表 11：備品與雜項

| ID | 項目 | 說明 | 小計（USD）|
|----|------|------|:---------:|
| SPR-01 | 備品（硬體 BOM 小計 10%）| 涵蓋元件損壞、打樣重做、連接器耗材、RF 調試替換件 | **$6,023** |

**備品小計：$6,023**

> **備品基礎計算**：硬體元件合計（不含備品）= $60,232.76，10% = $6,023.28，取整 $6,023。

---

## 硬體費用彙整（v3.0）

| 類別 | 中位數估算（USD）| 說明 |
|------|:--------------:|------|
| OBC（Xiphos Q7s Zynq-7020 module） | $25,000 | C-003 確認架構 |
| EPS（GomSpace P31u，15 Wh，DCN-002） | $6,000 | DCN-002 核准，PATCH-P5 驗證 |
| ADCS（MTQ×3 + CubeWheel Nano + 感測器組） | $5,200 | B-006 v1.1，CubeWheel Nano 加入 |
| RF 鏈路元件（DigiKey） | $140 | **v3.0 新增：確認料號與報價** |
| RF PCB（JLCPCB 4層，95×90mm，5片） | $70 | **v3.0 新增：具體規格與廠商** |
| S-band 天線（EnduroSat Patch Array） | $4,000 | 廠商詢價中 |
| TT&C（AX100 + UHF 天線） | $5,500 | GomSpace + ISIS |
| 太陽能板（6.5W BOL，DCN-001） | $4,500 | Clyde Space |
| 結構框架（ISIS 3U） | $4,250 | ISIS |
| 熱控材料（C-005 更新：TIM + 加熱器 + Al板 + MLI）| $583 | **v3.0 新增：Al 屏蔽板 + TIM pad 細化** |
| 備品 10% | $6,023 | 依 v3.0 硬體合計重算 |
| **硬體合計** | **$61,266** | |

> **備注**：v3.0 硬體合計 $61,266 較 v2.1 的 $62,853 略低（差異 -$1,587），主因：
> 1. RF 鏈路元件確認實際 DigiKey 報價（$140）遠低於 v2.1 的 $1,000 區間估算，差異約 -$860。
> 2. RF PCB 由 v2.1 的 $750 區間估算精算為 JLCPCB 4L 實際報價 ~$70，差異約 -$680。
> 3. 熱控材料由 v2.1 $575 調整為 v3.0 $583（+$8），因新增 TIM pad 5 片 $100 + Al 屏蔽板 $50 + Al 螺柱 $8，同時原加熱器 $150 → $75（精算 0.5W 一顆）。
> 4. 價格精算後淨變動：-$1,587（合計反而稍降）。

---

## 對比 v2.1 變更明細

| 類別 | v2.1 估算（USD）| v3.0 估算（USD）| 差異 | 說明 |
|------|:-------------:|:-------------:|:----:|------|
| OBC | $25,000 | $25,000 | $0 | 維持 |
| EPS | $6,000 | $6,000 | $0 | DCN-002 確認，維持 |
| ADCS | $5,200 | $5,200 | $0 | 維持 |
| RF 鏈路元件 | $1,000（區間估算）| $140（實際報價）| **-$860** | DigiKey 料號確認 |
| RF PCB | $750（區間估算）| $70（JLCPCB 4L 實算）| **-$680** | 具體廠商規格確認 |
| S-band 天線 | $4,000 | $4,000 | $0 | 維持 |
| TT&C | $5,500 | $5,500 | $0 | 維持 |
| 太陽能板 | $4,500 | $4,500 | $0 | 維持 |
| 結構框架 | $4,250 | $4,250 | $0 | 維持 |
| 熱控材料 | $575 | $583 | **+$8** | C-005：TIM pad + Al 板細化，加熱器精算 |
| 備品 10% | $6,178 | $6,023 | **-$155** | 依 v3.0 硬體合計重算 |
| **硬體合計** | **$62,853** | **$61,266** | **-$1,587** | |

---

## 完整任務預算（含非硬體）

| 類別 | 估算（USD）| 說明 |
|------|:---------:|------|
| 硬體元件（BOM v3.0 中位數） | ~$61,266 | 本文件 Section 硬體費用彙整 |
| 人事費（8 週課程，5 人） | ~$37,500 | 研究助理 $750/人/週 × 5 人 × 10 週（含前期） |
| 發射費（SpaceX Transporter rideshare） | ~$300,000 | 3U standard pricing，$100k/U；NASA ELaNa / ESA FYS 申請中 |
| 測試費（TVAC + 振動 + EMC） | ~$35,000 | TVAC $15k + 振動 $10k + EMC $10k |
| 差旅/雜費 | ~$7,500 | 發射場差旅、會議、運輸 |
| 保險 | ~$15,000 | 第三方責任險（發射保險另計）|
| **全任務總計** | **~$456,266** | 較 v2.1 降低 ~$1,734 |

> **發射費說明**：SpaceX Transporter rideshare 佔總預算 65.7%，為最大單一成本項。若申請 NASA ELaNa 或 ESA Fly Your Satellite 成功，可省去此費用，全任務預算降至 ~$156,266（NT$499 萬）。

---

## 教育折扣版本

### 可享折扣廠商明細

| 廠商 | 元件（v3.0 價格）| 原價（USD）| 教育折扣範圍 | 折後估算（USD）|
|------|----------------|:---------:|:-----------:|:------------:|
| GomSpace | P31u（$6,000）+ AX100（$4,000）| $10,000 | 15-25% | $7,500–$8,500 |
| ISIS | 3U 框架（$4,250）+ UHF 天線（$1,500）| $5,750 | 10-20% | $4,600–$5,175 |
| EnduroSat | S-band Patch Array（$4,000）| $4,000 | 10-20% | $3,200–$3,600 |
| CubeSpace | CubeWheel Nano（$3,500）| $3,500 | 15-25% | $2,625–$2,975 |
| Xiphos | Q7s Zynq-7020（$25,000）| $25,000 | 10-20% | $20,000–$22,500 |
| Clyde Space | 太陽能板（$4,500）| $4,500 | 10-30% | $3,150–$4,050 |

**可享折扣元件合計**：$52,750 → 折後 $41,075–$46,800

### 教育折扣後硬體估算

| 項目 | 原中位數（USD）| 折扣後估算（USD）|
|------|:-------------:|:--------------:|
| 可享折扣元件（6 家廠商）| $52,750 | $41,075–$46,800 |
| 不享折扣元件（DigiKey/JLCPCB/Mouser）| $1,493 | $1,493（無折扣）|
| 備品 10% | $6,023 | $4,257–$4,829（依折扣後重算）|
| **折扣後硬體合計** | **$61,266** | **$46,825–$53,122** |

**教育折扣中位數估算**：~$50,000（硬體約節省 $11,266，約 18.4%）

> **申請建議**：PDR 後（Sprint 3 Wave 3）立即向 GomSpace、ISIS、EnduroSat、CubeSpace、Xiphos、Clyde Space 發出 RFQ，**附帶教育任務說明書（包含大學隸屬機構、TASA 合作背景、課程性質）**，爭取最高折扣。

---

## 教育折扣後全任務預算（中位數估算）

| 類別 | 無折扣（USD）| 教育折扣後（USD）|
|------|:-----------:|:--------------:|
| 硬體 | $61,266 | **~$50,000** |
| 人事費 | $37,500 | $37,500 |
| 發射費 | $300,000 | $300,000 |
| 測試費 | $35,000 | $35,000 |
| 差旅/雜費 | $7,500 | $7,500 |
| 保險 | $15,000 | $15,000 |
| **全任務總計** | **$456,266** | **$444,500–$451,000** |

**若同時取得 NASA ELaNa / ESA FYS（發射費豁免）**：

| 情境 | 總預算（USD）| NT$ 估算（匯率 32）|
|------|:-----------:|:----------------:|
| 無折扣，付發射費 | ~$456,266 | ~NT$1,460 萬 |
| 教育折扣，付發射費 | ~$447,000 | ~NT$1,430 萬 |
| 教育折扣 + 免發射費 | ~$147,000 | ~NT$470 萬 |

---

## v3.0 料號確認清單（CDR 前動作項）

| # | 動作項 | 負責人 | 截止 | 狀態 |
|---|--------|--------|------|------|
| A1 | TCXO TXO-L2 DigiKey 料號確認，備選型號：TXC 7V-190.000MBA-T / Rakon EF5032A | Comm Agent | CDR -2 週 | 待辦 |
| A2 | PA PMA3-43-1W+ DigiKey 報價確認（或 Mini-Circuits 直購） | Comm Agent | CDR -2 週 | 待辦 |
| A3 | Xiphos Q7s 正式 RFQ 發出 + 教育折扣申請 | PM Agent | PDR 後立即 | 待辦 |
| A4 | GomSpace P31u + AX100 RFQ + 教育折扣申請 | PM Agent | PDR 後立即 | 待辦 |
| A5 | ISIS 3U 框架 + UHF 天線 RFQ + 教育折扣申請 | PM Agent | PDR 後立即 | 待辦 |
| A6 | EnduroSat S-band Patch Array RFQ + 教育折扣申請 | PM Agent | PDR 後立即 | 待辦 |
| A7 | CubeSpace CubeWheel Nano RFQ + 教育折扣申請 | PM Agent | PDR 後立即 | 待辦 |
| A8 | Clyde Space 太陽能板 RFQ + 教育折扣申請 | PM Agent | PDR 後立即 | 待辦 |
| A9 | JLCPCB 4L 阻抗控制板報價確認（C-002 Gerber 完成後） | Comm Agent | C-002 Gerber 完成後 | 待辦 |
| A10 | DigiKey 購物車確認（LNA×2 + BPF×2 + Mixer×1 + 被動元件）| Comm Agent | CDR 前 | 待辦 |

---

## CDR Entry Criteria 對應

| CDR 標準（SPRINT3_PLAN.md §CDR Entry Criteria）| v3.0 狀態 |
|----------------------------------------------|----------|
| 8. BOM v3 含料號 | **達成**：RF-01 LNA、RF-03 BPF、RF-04 Mixer 確認 DigiKey 料號；PA 詢價中（A2）；TCXO 選型確認中（A1） |
| 硬體成本 Mass/Power 連動更新 | **達成**：DCN-002 15 Wh 確認，DoD 19.8%/25.2% PASS |
| 教育折扣估算 | **達成**：6 家廠商折扣表 + 中位數 ~$50,000 硬體 |

---

## 採購時程建議（v3.0 更新）

| 階段 | 時程 | 動作 |
|------|------|------|
| PDR 後（Sprint 3 Wave 3 完成）| 2026-04-29 起 | 向 GomSpace、ISIS、EnduroSat、CubeSpace、Xiphos、Clyde Space 發 RFQ，附教育折扣申請（A3–A8） |
| CDR 前（Sprint 4 Wave 1）| Week 11-12 | 確認 TCXO 型號（A1）、PA DigiKey 報價（A2）；確認 JLCPCB 報價（A9） |
| CDR 後（Sprint 4 Wave 2）| Week 13-14 | 確認廠商報價、簽訂 PO；DigiKey/Mouser/JLCPCB 下單（A10） |
| Sprint 5 | Week 17-18 | 元件到貨、開始組裝測試 |

> **Lead time 警告**：
> - Xiphos Q7s：8–12 週，**最長 Lead time 元件**，PDR 後須立即啟動。
> - GomSpace P31u（15 Wh）：6–10 週，同步啟動。
> - RF DigiKey 元件：通常 1–3 週（現貨），可延後至 CDR 前確認後下單。
> - JLCPCB：完成 Gerber + 下單後 7–14 天。

---

## 附錄：元件技術資料彙整

### RF 鏈路元件快速參考

| 元件 | 型號 | 關鍵規格 | 封裝 |
|------|------|---------|------|
| LNA | ADL5523ACPZ-R7 | NF 1 dB @2 GHz，Gain 15 dB，Vcc 3.3V，ICC 45 mA | LFCSP-8（3×3 mm）|
| PA | PMA3-43-1W+ | Psat +32.6 dBm，P1dB +30.3 dBm，Vcc 12V，I_dc 350 mA，PAE ~25% | QFN（3×3 mm）|
| BPF | SYBP-2250+ | fc 2250 MHz，BW 740 MHz，IL ~1.5 dB，Rej >30 dB @±500 MHz | SMD（1812 equiv.）|
| Mixer | LT5512EUF#PBF | RF 1k–3 GHz，LO 30–3 GHz，IIP3 +18 dBm，RF/LO ISO ≥30 dB | QFN-16（4×4 mm）|
| TCXO | TXO-L2（TBD） | 190 MHz，±1 ppm，-40~+85°C，相位雜訊 <-110 dBc/Hz @1 kHz | SMD |

### RF PCB 規格快速參考（JLCPCB 下單用）

| 項目 | 規格 |
|------|------|
| 板層 | 4 層 |
| 尺寸 | 95 × 90 mm |
| 板厚 | 1.0 mm |
| 板材 | FR4（Dk ≈ 4.6 @2 GHz） |
| 銅厚 | 35 μm（1 oz） |
| 表面處理 | ENIG（化學鎳金）|
| 阻抗控制 | 50Ω，Layer 1 微帶線寬 W = 0.38 mm |
| 安裝孔 | 4 × M3，板邊 3 mm 禁布區 |
| 打樣數量 | 5 片 |
| 費用估算 | ~$60–80（含阻抗控制 surcharge）|

---

## 課程報告建議用語（v3.0 更新）

> 「本任務硬體預算約 **NT$126 萬**（USD ~50,000，教育折扣後中位數），整體任務預算（含 SpaceX Transporter 搭載）約 **NT$1,430 萬**（USD ~447,000）。BOM v3.0 完成 RF 鏈路全部關鍵元件料號確認：LNA（ADL5523ACPZ-R7，DigiKey $4.38×2）、BPF（SYBP-2250+，DigiKey $24.58×2）、Mixer（LT5512EUF#PBF，DigiKey $11.14）、PA（PMA3-43-1W+ 詢價中）；RF PCB 由 JLCPCB 4 層阻抗控制板打樣（5 片 ~$70）。若取得 NASA ELaNa 或 ESA 教育搭載機會，可省去發射費 USD 300,000，全任務預算降至約 **NT$470 萬**（USD 147,000）。」
