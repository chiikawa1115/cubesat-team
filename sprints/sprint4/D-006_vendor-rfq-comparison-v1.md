# D-006：多廠商比價表（Vendor RFQ Comparison）
# Sprint 4 Wave 1 — BOM 硬體採購估價

**文件版本：** v1
**日期：** 2026-05-28
**作者：** PM Agent 黃俊榮
**關聯文件：** D-HG-001（BPF 選型）、D-HG-002（LO PLL 方案）、DCN-003（Driver Amp 變更）、C-007（BOM v3.0 繼承）
**狀態：** Draft — Sprint 4 W1 採購規劃用

---

## 執行摘要

本文件為 Sprint 4 Wave 1 RF 鏈路硬體更新的多廠商比價報告（虛擬 RFQ 模擬）。
比價涵蓋三家供應商：DigiKey（美系標準料基準）、Mouser Electronics（競爭定價）、Arrow Electronics（量產大宗）。

**Sprint 4 BOM 新增元件共 10 項**，加計繼承自 Sprint 3 的基礎 BOM（$1,930），
整機 BOM 最優採購估價約 **$2,373**（不含 GaAs 太陽能板，原型機未列）。
若含 GaAs 太陽能板 16 片，整機 BOM 約 **$6,053**。

---

## 1. 比價範圍說明

### 1.1 廠商特性

| 廠商 | 類型 | 定價特性 | MOQ 典型 | 優勢領域 |
|-----|-----|---------|---------|---------|
| **DigiKey** | 分銷商（美系）| 標準定價，單件可買 | 1 件起 | 庫存齊全、交期短（1-3 天）|
| **Mouser Electronics** | 分銷商（美系）| 通常比 DigiKey 便宜 5-15% | 1 件起 | 小批量靈活、新料齊 |
| **Arrow Electronics** | 大型分銷商 | 大宗 10-20% 折扣，但 MOQ 較高 | 10-25 件起 | 量產報價、授權代理 |

### 1.2 特殊注意事項

- **Reactel 4C5-2185 BPF**：客製陶瓷同軸元件，須直接向 Reactel Inc. 或 K&L Microwave 發 RFQ，非標準分銷商庫存料，Lead Time 8-12 週，本表以廠商參考報價列入。
- **GaAs 太陽能板**：AzurSpace / Spectrolab / SolAero 直接採購，本表以 AzurSpace 3G30C 市場參考價列入。
- 所有價格為**虛擬市場參考價**，符合 2026 年市場現實水準，僅供專案規劃用途。

---

## 2. 元件比價總表

### Sprint 4 新增元件（RF 鏈路更新 + 電源）

| # | 料號 | 元件描述 | 數量 | DigiKey<br>單價(USD) | Mouser<br>單價(USD) | Arrow<br>單價(USD)<br>（MOQ） | 備注 |
|---|------|---------|:---:|:-------------------:|:-------------------:|:-------------------:|------|
| 1 | TSS-53LNB+ | Mini-Circuits Driver Amp<br>G=27 dB, P1dB=+20 dBm | 1 | $16.50 | $15.20 | $13.80<br>（MOQ:10） | DCN-003 新增 |
| 2 | ADF4351BCPZ | Analog Devices PLL Synthesizer<br>35 MHz-4.4 GHz | 1 | $8.50 | $7.80 | $6.90<br>（MOQ:25） | D-HG-002 新增 |
| 3 | SAFC1G98EA0F0A | Murata SAW BPF<br>1980 MHz, UL BPF | 1 | $3.50 | $3.10 | $2.80<br>（MOQ:50） | D-HG-001 取代 SYBP-2250+ |
| 4 | 4C5-2185<br>（Reactel 客製）| Reactel / TTE 陶瓷同軸 BPF<br>2185 MHz, 5-pole, ≥50 dB rejection | 1 | — | — | — | **客製 RFQ**<br>Lead Time 8-12 週<br>估價：~$45-80 |
| 5 | PMA3-43-1W+ | Mini-Circuits PA<br>700-4200 MHz, P1dB=+33 dBm | 1 | $22.50 | $20.80 | $18.50<br>（MOQ:10） | Sprint 3 確認延續 |
| 6 | LT5512EUF | Analog Devices Mixer<br>10-3000 MHz | 1 | $12.40 | $11.20 | $10.30<br>（MOQ:10） | Sprint 3 確認延續 |
| 7 | ADL5523<br>（LFCSP-8）| Analog Devices LNA<br>400-4000 MHz, NF=0.6 dB | 1 | $9.80 | $8.90 | $7.80<br>（MOQ:25） | Sprint 3 確認延續 |
| 8 | ASTX-H11-10.000MHZ-T<br>（或等效 10 MHz TCXO）| Abracon TCXO 10 MHz<br>±0.5 ppm, 3.3V SMD | 1 | $2.20 | $2.00 | $1.80<br>（MOQ:25） | D-HG-002 新增<br>PLL 參考振盪器 |
| 9 | 3G30C（4cm×4cm）<br>AzurSpace 或等效 | GaAs Triple-Junction Solar Cell<br>Spectrolab/AzurSpace, η≈30% | 16 | $320.00/片 | $305.00/片 | $280.00/片<br>（MOQ:16） | 4 面 × 4 片/面<br>高單價，直採廠商 |
| 10 | Samsung INR18650-35E | 18650 Li-ion 3.5 Ah<br>飛行電池 2S2P | 4 | $8.50/顆 | $7.80/顆 | $6.90/顆<br>（MOQ:10） | EPS 電池組用 |

---

### 2.1 各廠商 Sprint 4 新增元件報價小計

（不含 GaAs 太陽能板，不含 Reactel 客製 BPF）

| 料號 | DigiKey 小計 | Mouser 小計 | Arrow 小計（單件）|
|------|:-----------:|:-----------:|:-----------------:|
| TSS-53LNB+ × 1 | $16.50 | $15.20 | $13.80 |
| ADF4351BCPZ × 1 | $8.50 | $7.80 | $6.90 |
| SAFC1G98EA0F0A × 1 | $3.50 | $3.10 | $2.80 |
| Reactel 4C5-2185 × 1 | ~$60（估） | ~$60（估） | ~$55（估） |
| PMA3-43-1W+ × 1 | $22.50 | $20.80 | $18.50 |
| LT5512EUF × 1 | $12.40 | $11.20 | $10.30 |
| ADL5523 × 1 | $9.80 | $8.90 | $7.80 |
| TCXO 10 MHz × 1 | $2.20 | $2.00 | $1.80 |
| Samsung 18650 × 4 | $34.00 | $31.20 | $27.60 |
| **Sprint 4 RF+電池 小計** | **$169.40** | **$160.20** | **$145.50** |
| 被動元件雜項（估）| $5.00 | $4.80 | $4.50 |
| **Sprint 4 合計（不含太陽能）** | **$174.40** | **$165.00** | **$150.00** |

---

### 2.2 GaAs 太陽能板報價（獨立列項）

| 廠商方案 | 單價 | 16 片合計 | 備注 |
|---------|:----:|:--------:|------|
| DigiKey（代理，若有庫存）| $320/片 | $5,120 | 通常無太陽能電池庫存 |
| Mouser（代理）| $305/片 | $4,880 | 少量庫存可能有 |
| Arrow（授權代理）| $280/片 | $4,480 | 建議直接向 AzurSpace 發 RFQ |
| **AzurSpace 直採（推薦）** | **$270/片** | **$4,320** | 教育/研究折扣可至 15-20% |

> 備注：AzurSpace 3G30C 標準市場參考價 $280-350/片（2026 Q2），教育機構可獲 15-20% 折扣。
> Spectrolab（波音子公司）類似規格 $300-450/片，适合有 NASA 合作的機構。
> SolAero Technologies（量產 COTS）可低至 $200-250/片（大宗 ≥32 片），但 Proto 數量不划算。

---

## 3. 推薦採購策略

### 3.1 最優分流採購方案

| 採購品項 | 推薦廠商 | 理由 | 單元估價 |
|---------|---------|------|---------|
| ADF4351BCPZ、ADL5523 | **Mouser** | 庫存充裕，比 DigiKey 便宜 8-10%，ADI 授權代理 | $16.70 |
| TSS-53LNB+、PMA3-43-1W+ | **Mouser** | Mini-Circuits 在 Mouser 有官方授權，庫存穩定 | $36.00 |
| LT5512EUF | **DigiKey** | DigiKey 為 Analog Devices 主要授權商，庫存稳定 | $12.40 |
| SAFC1G98EA0F0A | **Mouser** | Murata 在 Mouser 有穩定授權庫存，單價 $3.10 | $3.10 |
| TCXO 10 MHz (Abracon) | **DigiKey** | Abracon 主要分銷在 DigiKey，料號 433-1029-1-ND | $2.20 |
| Reactel 4C5-2185 | **Reactel Inc. 直採 RFQ** | 客製元件，分銷商無庫存，需直送 | ~$60（估）|
| Samsung INR18650-35E | **Mouser** | 可靠電池料，Mouser 有 18650 庫存，$7.80/顆 | $31.20 |
| GaAs 太陽能板 × 16 | **AzurSpace 直採** | 教育折扣 15-20%，直採 $270/片 最優 | $4,320 |

### 3.2 最優 BOM 總計（Sprint 4 新增元件，不含太陽能板）

| 採購項目 | 廠商 | 金額 |
|---------|------|:----:|
| RF 元件（7 項，Mouser 主採）| Mouser | $110.80 |
| LT5512EUF + TCXO（DigiKey）| DigiKey | $14.60 |
| Reactel 4C5-2185（直採 RFQ）| Reactel Inc. | $60.00（估）|
| Samsung 18650 × 4（Mouser）| Mouser | $31.20 |
| 被動元件雜項 | DigiKey/Mouser | $5.00 |
| **Sprint 4 RF+電池 最優小計** | | **$221.60** |

---

## 4. BOM Delta — Sprint 4 vs. Sprint 3

### 4.1 Sprint 4 新增元件（來自設計變更）

| 元件 | 來源設計文件 | Sprint 3 狀態 | Sprint 4 變更 | BOM 影響 |
|------|------------|-------------|--------------|---------|
| TSS-53LNB+ Driver Amp | DCN-003 | 未有 | 新增（TX 鏈路驅動）| +$16.50 |
| ADF4351BCPZ PLL | D-HG-002 | 未有 | 新增（LO 190 MHz 合成）| +$8.50 |
| SAFC1G98EA0F0A SAW BPF | D-HG-001 | SYBP-2250+ @ $5.20 | 取代（UL BPF 隔離升級）| +$3.50（取代 $5.20）|
| Reactel 4C5-2185 陶瓷 BPF | D-HG-001 | SYBP-2250+ @ $5.20 | 取代（DL BPF 升級）| +$60（取代 $5.20）|
| TCXO 10 MHz | D-HG-002 | C-002 列「TXO-L2 等效」但未定料 | 料號確認（Abracon ASTX-H11）| 維持 $2.20 |
| Samsung INR18650-35E × 4 | Sprint 4 電池規格 | EPS 含電池（GomSpace P31u 整包）| 獨立採購電池模組（飛行備用）| +$34 |

### 4.2 Sprint 3 → Sprint 4 BOM 淨變化

| 項目 | 金額 |
|------|:----:|
| Sprint 3 RF BPF 淘汰（SYBP-2250+ × 2）| -$10.40 |
| Sprint 4 新增 Driver Amp | +$16.50 |
| Sprint 4 新增 PLL（ADF4351 + TCXO）| +$10.70 |
| Sprint 4 BPF 升級（SAW + Reactel）| +$63.50 |
| Sprint 4 18650 電池組 | +$34.00 |
| Sprint 4 被動元件增量 | +$5.00 |
| **Sprint 4 BOM 淨增** | **+$119.30** |

---

## 5. Lead Time 風險分析

### 5.1 高風險項目：Reactel 4C5-2185 客製 BPF

| 風險項目 | 詳情 |
|---------|------|
| **元件** | Reactel Inc. 4C5-2185（或等效 K&L Microwave 5BT-2185）陶瓷同軸 BPF |
| **Lead Time** | **8-12 週**（客製元件，需提供規格書、S-parameter 需求）|
| **RFQ 截止** | 若 Sprint 4 W1（2026-06-04）前未發 RFQ，進度計畫將延誤 2-3 個月 |
| **風險等級** | HIGH — 影響 RF 鏈路 PCB 裝配排程 |
| **緩解措施** | 1. PM 於 Sprint 4 W1 立即發 RFQ（Reactel + K&L 兩家），最快者採用<br>2. 備用方案：Mini-Circuits BFCN-2175+（現貨，但抑制 ~35 dB 未達 40 dB 目標，需與 SE 確認接受度）|
| **Action Item** | CDR-AI-003：PM 黃俊榮，期限 Sprint 4 W1 |

### 5.2 其他 Lead Time 風險

| 元件 | DigiKey/Mouser 現貨 | Lead Time | 風險等級 |
|------|:------------------:|-----------|---------|
| ADF4351BCPZ | ✅ 一般有庫存（1000+ 件）| 1-5 個工作日 | LOW |
| TSS-53LNB+ | ✅ Mini-Circuits 標準料 | 3-7 個工作日 | LOW |
| PMA3-43-1W+ | ✅ Mini-Circuits 標準料 | 3-7 個工作日 | LOW |
| LT5512EUF | ✅ ADI 庫存充裕 | 1-5 個工作日 | LOW |
| ADL5523 | ✅ ADI 庫存充裕 | 1-5 個工作日 | LOW |
| SAFC1G98EA0F0A | ⚠️ 確認 Mouser 庫存（Action AI-HG-001-1）| 5-10 個工作日 | MEDIUM |
| GaAs 太陽能板 × 16 | ❌ 需 AzurSpace 直採 RFQ | **6-10 週** | HIGH |

> **GaAs 太陽能板 Lead Time 說明：**
> AzurSpace 3G30C 為太空級產品，需配合出口管制（EAR/ITAR 確認），
> 學術計畫通常需填寫 End User Certificate，處理時間 2-4 週 + 製造 4-6 週。
> 建議與 Reactel BPF 同步啟動採購程序。

---

## 6. 整機 BOM 費用總估算（Sprint 4 Wave 1 版本）

### 6.1 繼承 BOM（Sprint 3 已確認，維持不變）

| 子系統 | 元件描述 | 小計（USD）|
|--------|---------|:---------:|
| 結構框架 | 3U CubeSat 框架（ISIS / GomSpace）| $450 |
| OBC/SOM | Zynq-7020 SOM（Avnet MiniZed 等效）| $280 |
| ADCS | 三軸 RW + MTQ + IMU（CubeSpace/MAI）| $800 |
| EPS | 電池充放電管理模組 | $180 |
| 天線 | Patch 天線 × 2 | $40 |
| PCB 製造 | RF PCB + OBC PCB 製造費 | $120 |
| 雜項 | 連接器、線束、螺絲等 | $60 |
| **Sprint 3 繼承 BOM 小計** | | **$1,930** |

### 6.2 Sprint 4 新增 BOM（最優採購方案）

| 子系統 | 元件描述 | 小計（USD）|
|--------|---------|:---------:|
| TX Driver Amp | TSS-53LNB+（Mouser）| $15.20 |
| LO PLL | ADF4351BCPZ（Mouser）| $7.80 |
| UL BPF | SAFC1G98EA0F0A SAW（Mouser）| $3.10 |
| DL BPF | Reactel 4C5-2185 客製（直採估）| $60.00 |
| TX PA | PMA3-43-1W+（Mouser）| $20.80 |
| Mixer | LT5512EUF（DigiKey）| $12.40 |
| LNA | ADL5523（Mouser）| $8.90 |
| TCXO | Abracon 10 MHz（DigiKey）| $2.20 |
| 飛行電池 | Samsung INR18650-35E × 4（Mouser）| $31.20 |
| 被動元件 | 雜項 R/C/L（DigiKey/Mouser）| $5.00 |
| **Sprint 4 新增 BOM 小計** | | **$166.60** |

### 6.3 整機 BOM 總計

| 方案 | 金額（USD）| 備注 |
|-----|:---------:|------|
| Sprint 3 繼承 BOM | $1,930 | 已確認 |
| Sprint 4 新增（不含太陽能板）| $166.60 | 最優採購方案 |
| **整機 BOM 小計（不含太陽能板）** | **$2,096.60** | 原型機 Proto |
| GaAs 太陽能板 × 16（AzurSpace 直採）| $4,320 | 教育折扣 15% |
| **整機 BOM 總計（含太陽能板）** | **$6,416.60** | Proto 完整硬體 |

> **備注：**
> - 以上為原型機（1 件）採購估算，不含工程師工時、測試設備、EMI 腔體測試等費用。
> - OBC 若採用 Xiphos Q7s 飛行級模組（C-007 列 $25,000），整機費用將大幅增加；
>   此處 OBC 以 Avnet MiniZed 等效 Dev Board（$280）計，適合 Proto 階段。
> - GaAs 太陽能板為選配，Proto 階段可先用矽基太陽能板（$5-10/片）替代功能驗證。

---

## 7. 推薦 Action Items（PM 執行）

| 編號 | 行動 | 負責人 | 期限 | 優先級 |
|------|------|--------|------|--------|
| D-006-A1 | 向 Reactel Inc. + K&L Microwave 發出 4C5-2185 RFQ（含規格書：2185 MHz, BW 40 MHz, IL ≤ 1.5 dB, 抑制 ≥ 50 dB @ 2010 MHz）| PM 黃俊榮 | Sprint 4 W1（2026-06-04）| **HIGH** |
| D-006-A2 | 向 AzurSpace 發出 3G30C × 16 片 RFQ（含教育機構文件 + 出口管制申請）| PM 黃俊榮 | Sprint 4 W1 | **HIGH** |
| D-006-A3 | Mouser 確認 SAFC1G98EA0F0A 庫存量（AI-HG-001-1）| PM 黃俊榮 | Sprint 4 W1 | MEDIUM |
| D-006-A4 | 在 Mouser 下單：ADF4351、TSS-53LNB+、PMA3-43-1W+、ADL5523、SAFC1G98EA0F0A、Samsung 18650×4 | PM 黃俊榮 | Sprint 4 W2（2026-06-11）| MEDIUM |
| D-006-A5 | 在 DigiKey 下單：LT5512EUF、Abracon TCXO、被動元件 | PM 黃俊榮 | Sprint 4 W2 | MEDIUM |
| D-006-A6 | 確認 Reactel/K&L 報價後更新本文件至 v1.1 | PM 黃俊榮 | Sprint 4 W3（2026-06-18）| MEDIUM |

---

## 附錄 A：料號快速查詢表

| 元件 | DigiKey 料號（參考）| Mouser 料號（參考）|
|------|:------------------:|:------------------:|
| TSS-53LNB+ | TSS-53LNB+-ND | 140-TSS-53LNB+ |
| ADF4351BCPZ | 505-ADF4351BCPZ-ND | 584-ADF4351BCPZ |
| SAFC1G98EA0F0A | 490-SAFC1G98EA0F0A-ND | 81-SAFC1G98EA0F0A |
| PMA3-43-1W+ | PMA3-43-1W+-ND | 140-PMA3-43-1W+ |
| LT5512EUF | LT5512EUF#PBF-ND | 584-LT5512EUF#PBF |
| ADL5523ACPZ | ADL5523ACPZR7-ND | 584-ADL5523ACPZR7 |
| ASTX-H11-10.000MHZ-T | 433-1029-1-ND | 815-ASTXH1110MHZT |
| Samsung INR18650-35E | — | — |

> 備注：料號為參考值，下單前需至各廠商官網即時確認庫存與價格。

---

## 附錄 B：BOM 歷史版本對照

| 版本 | Sprint | 整機 BOM 估算 | 主要差異 |
|-----|--------|:------------:|---------|
| v1.0（B-009）| Sprint 2 | ~$1,650 | 初始概估，無詳細元件 |
| v2.1（B-009）| Sprint 2 | ~$1,780 | 加入 EPS 15 Wh 電池升級 |
| v3.0（C-007）| Sprint 3 | ~$1,930 | RF 元件料號確認，ADCS 細化 |
| **v4.0（本文）** | **Sprint 4** | **$2,097（不含太陽能）** | **BPF 升級、Driver Amp、PLL 新增** |

---

*D-006 v1 | PM Agent 黃俊榮 | 2026-05-28*
*下次版本（v1.1）：Reactel RFQ 回覆後更新實際報價*
*P2P Review：SE 陳明哲（BOM 正確性）+ Comm 林志遠（RF 元件規格確認）*
