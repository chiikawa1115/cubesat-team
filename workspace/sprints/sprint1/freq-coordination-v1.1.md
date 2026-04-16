# TASA-NTN-3U 頻率協調可執行路徑分析 v1.1

> **Document ID:** FC-v1.1  
> **Date:** 2026-04-15  
> **Author:** Comm Payload Engineer (Rudy)  
> **Status:** Sprint 1 / Phase A / SRR Deliverable  
> **Changelog v1.0 -> v1.1:**  
> - **[NEW]** 三條合法路徑完整分析（ITU RR 4.4 / NCC 學術執照 / Amateur Satellite 備案）  
> - **[NEW]** 風險 RPN 重新評估  
> - **[NEW]** 課程報告建議策略

---

## 1. 頻段現況

| 項目 | 值 | 備注 |
|------|-----|------|
| 目標頻段 | S-band n236 | 3GPP NTN Rel-17 |
| UL | 1980 -- 2010 MHz | |
| DL | 2170 -- 2200 MHz | |
| ITU 業務分配 | Mobile Satellite Service (MSS) / IMT | ITU RR Article 5, Region 3 |
| 台灣 NCC 分配 | 行動通訊（IMT）頻段 | 已標售予電信業者 |
| 台灣目前使用者 | 中華電信、遠傳 | 3G/4G 頻段，部分已 refarming |

### 核心問題
S-band n236 是**商業 IMT 頻段**，在台灣已由 NCC 標售予行動通訊業者。學術 CubeSat 專案**無法直接合法使用**，需要透過例外機制或替代頻段取得合法發射權。

---

## 2. 三條可執行路徑分析

### 路徑 A：ITU Radio Regulations No. 4.4（非符合業務研究例外）

**法規依據：**
> ITU RR No. 4.4: "Administrations of the Member States shall not assign to a station any frequency in derogation of either the Table of Frequency Allocations [...] or of the other provisions of these Regulations, except on the express condition that such a station, when using such a frequency assignment, **shall not cause harmful interference** to, and **shall not claim protection** from harmful interference caused by, a station operating in accordance with the provisions of the Constitution, the Convention and these Regulations."

**白話解釋：**
- 任何 ITU 會員國可以在「非符合業務」的頻段上發射
- 條件：(1) 不對合法使用者造成有害干擾 (2) 不要求受到保護
- 常見用途：學術研究、實驗性衛星、短期任務

**適用性分析：**

| 項目 | 評估 | 說明 |
|------|------|------|
| 功率限制 | OK | 衛星 EIRP < +1 dBW (1W PA, 8dBi antenna)，S-band 地面干擾可忽略 |
| 時間限制 | OK | LEO 500km 每次通過地面站僅 2-4 min，低 duty cycle |
| 地面干擾風險 | 低 | 100 bps narrowband, QPSK 1/2, 頻寬極窄 (~200 Hz)，功率密度極低 |
| 主管機關配合 | 需確認 | 台灣 NCC 需代表向 ITU 提交 No. 4.4 通知（非強制但建議） |

**執行步驟：**
1. 計算 EIRP power flux density (PFD) 於地表之值，確認低於 ITU RR Art. 21 限值
2. 撰寫 non-interference declaration
3. 透過 TASA/NCC 向 ITU Radiocommunication Bureau 提交 No. 4.4 通知
4. 取得「注意但不保護」之國際登記

**時程估計：** 3-6 個月（含 TASA 內部審查）

**限制：**
- No. 4.4 通知**不等於頻率執照**，仍需台灣國內法配合
- 若電信業者投訴干擾，必須立即停止發射
- 不具法律保護力

---

### 路徑 B：NCC 學術實驗執照（電信管理法第 50 條）

**法規依據：**
> 電信管理法（2019 年修正）第 50 條：  
> 「為學術研究、科技研發或實驗之目的，得向主管機關申請核發實驗研發專用電信網路設置使用執照，其頻率使用、功率、區域及期限，由主管機關定之。」

> 台灣 NCC 射頻器材管理辦法另有學術研究用頻率核准之相關規定。

**適用性分析：**

| 項目 | 評估 | 說明 |
|------|------|------|
| 申請資格 | OK | 大學/研究機構 + TASA 合作，符合學術研究目的 |
| 頻段限制 | 需協調 | NCC 可核准在已分配頻段上之學術實驗使用，但需與既有使用者協調 |
| 功率限制 | 可接受 | NCC 通常限制實驗功率 <=1W，本專案 PA 1W 符合 |
| 期限 | 有限 | 實驗執照通常 1-2 年，需續約（符合 3U CubeSat 任務壽命 ~1-3 年） |
| 先例 | 有 | 台灣過去有大學申請 S-band 實驗頻率之案例（成大、中央衛星實驗室） |

**執行步驟：**
1. 由合作大學（或 TASA 代為）向 NCC 提交「實驗研發專用電信網路設置使用申請書」
2. 附件需包含：
   - 頻率使用計畫（中心頻率、頻寬、調變方式、發射功率）
   - 干擾評估報告（EIRP、PFD、與既有使用者之頻率/空間隔離度）
   - 任務描述與時程
   - 實驗結束後頻率歸還承諾
3. NCC 技術審查（約 1-3 個月）
4. 核發實驗頻率使用許可

**時程估計：** 2-4 個月

**優勢：**
- 具有台灣國內法效力
- 明確的法律保護（在核准範圍內）
- 有先例可循

**限制：**
- 需與電信業者協調，可能被要求限制特定時段或區域
- 核准頻寬可能被限縮
- 需定期回報使用狀況

---

### 路徑 C：改用 Amateur Satellite 頻段（UHF 435-438 MHz）作為備案

**法規依據：**
- ITU RR Article 5: UHF 435-438 MHz 分配給 Amateur Satellite Service (Region 3)
- IARU (International Amateur Radio Union) 頻率協調機制
- 台灣 NCC 業餘無線電管理辦法

**技術影響評估：**

| 參數 | S-band n236 (原方案) | UHF 435 MHz (備案) | 影響 |
|------|---------------------|-------------------|------|
| FSPL @1700km | 163.1 dB | 149.8 dB | **改善 13.3 dB** |
| 天線增益 | +8 dBi (patch) | +2 dBi (dipole) | **劣化 6 dBi** |
| T_ant | 100 K | 500-1000 K | **劣化 5-10 dB** (UHF RFI 嚴重) |
| 可用頻寬 | 30 MHz | 3 MHz (協調後) | 限制 data rate |
| 5G NTN 相容 | YES (n236) | NO | **失去 NTN 示範目的** |

**UHF FSPL 計算：**
```
FSPL = 20*log10(1700) + 20*log10(0.435) + 92.45
     = 64.61 + (-7.23) + 92.45
     = 149.83 dB ≈ 149.8 dB
```

**執行步驟：**
1. 透過 IARU 提交衛星頻率協調申請（需業餘無線電執照持有者）
2. IARU Satellite Advisor 審查（約 3-6 個月）
3. 同步向 NCC 申請業餘衛星電台許可
4. 修改 RF 鏈路設計（天線、LNA、PA 需全部更換）

**優勢：**
- 頻率協調流程明確、有大量先例（CubeSat 社群標準做法）
- 無需與商業電信業者協調
- FSPL 大幅降低（低頻優勢）

**致命缺點：**
- **完全失去 5G NTN 展示目的** -- 本專案核心價值是 3GPP Rel-17 NTN 透明轉發
- RF 硬體全部重新設計
- UHF 頻段人為干擾嚴重（T_ant 大幅升高）
- 不符合專案名稱 "NTN" 定位

---

## 3. 路徑比較矩陣

| 評估項目 | 路徑 A (ITU 4.4) | 路徑 B (NCC 學術執照) | 路徑 C (Amateur UHF) |
|---------|----------------|---------------------|---------------------|
| 法律效力 | 弱（國際通知，非執照） | **強（國內法執照）** | 中（業餘衛星協調） |
| 5G NTN 相容 | **YES** | **YES** | NO |
| 執行難度 | 中（需 TASA 協助） | 中（需大學行政配合） | 低（社群成熟流程） |
| 時程 | 3-6 個月 | 2-4 個月 | 3-6 個月 |
| 干擾風險 | 低（但無保護） | **低（有保護）** | 中（UHF RFI） |
| 硬體重設計 | 不需要 | 不需要 | **全部重設計** |
| 先例 | 少（台灣學術衛星） | **有（成大、中央等）** | 多（全球 CubeSat） |
| 課程報告適合度 | 好 | **最佳** | 可接受但偏題 |

---

## 4. 建議策略

### 主策略：路徑 A + 路徑 B 組合

```
Phase A (Sprint 1-2, now):
  → 以路徑 B (NCC 學術實驗執照) 為主申請路徑
  → 同步準備路徑 A (ITU RR No. 4.4) 文件作為國際登記

Phase B (Sprint 3-4):
  → NCC 執照審查中，路徑 C 作為技術 fallback 準備（不實施，僅保留設計文件）
  
Phase C (Sprint 5+):
  → 取得 NCC 實驗頻率使用許可
  → 向 ITU 提交 No. 4.4 通知完成國際登記
```

**理由：**
1. 路徑 B 具有國內法效力，是最穩固的基礎
2. 路徑 A 補強國際法層面，對 TASA 未來任務有延續價值
3. 路徑 C 僅作為「報告中展示風險意識」的備案分析，不實際執行

### 課程報告建議措辭
> "本專案計畫透過 NCC 電信管理法第 50 條申請學術實驗頻率使用許可，同步依 ITU RR No. 4.4 進行國際頻率通知登記，以確保 S-band n236 NTN 酬載之合法發射權。作為風險緩解，保留 Amateur Satellite UHF 頻段之備案設計。"

---

## 5. 風險評估（FMEA / RPN）

### RPN 計算方法
```
RPN = Severity (S) x Occurrence (O) x Detection (D)
S, O, D: 各 1-10 分
RPN > 40: 需要緩解措施
RPN > 100: 不可接受，必須立即處理
```

### 頻率協調風險項目

| # | 風險描述 | S | O | D | RPN | 緩解措施 |
|---|---------|---|---|---|-----|---------|
| R1 | NCC 拒絕核發學術實驗頻率（路徑 B 失敗） | 8 | 3 | 4 | **96** | 提前與 NCC 非正式諮詢；準備詳細干擾評估報告；TASA 背書信 |
| R2 | 電信業者投訴干擾，要求停止發射 | 7 | 2 | 5 | **70** | 低 EIRP 設計（<1W）；narrowband 100 bps；窄波束 patch 天線；準備頻率變更 SOP |
| R3 | ITU No. 4.4 通知流程延宕，超過 SRR 時程 | 5 | 5 | 3 | **75** | 路徑 A 與路徑 B 平行推進；SRR 報告中標注為 "in progress" |
| R4 | 法規變更（NCC refarming 影響 1980-2010 MHz） | 6 | 2 | 6 | **72** | 監控 NCC 頻率規劃公告；保留 UHF fallback 設計 |
| R5 | 路徑 B+A 都失敗，被迫使用路徑 C (UHF) | 9 | 1 | 3 | **27** | RF 硬體模組化設計，預留 UHF 轉換介面（Phase B 詳細設計） |
| R6 | 學術執照核准頻寬不足（NCC 限縮至 <1 MHz） | 4 | 3 | 5 | **60** | 100 bps 僅需 ~200 Hz 頻寬，即使限縮至 100 kHz 仍綽綽有餘 |
| R7 | IARU 頻率協調延誤（路徑 C 備案） | 3 | 4 | 4 | **48** | 提前提交 IARU 申請（即使不一定使用），保留選項 |

### RPN 分布圖

```
RPN:
  R1 (NCC 拒絕)      ████████████████████████  96  [HIGH - 需立即緩解]
  R3 (ITU 延宕)       ██████████████████░░░░░░  75  [MEDIUM-HIGH]
  R4 (法規變更)       ██████████████████░░░░░░  72  [MEDIUM-HIGH]
  R2 (業者投訴)       █████████████████░░░░░░░  70  [MEDIUM-HIGH]
  R6 (頻寬限縮)       ███████████████░░░░░░░░░  60  [MEDIUM]
  R7 (IARU 延誤)      ████████████░░░░░░░░░░░░  48  [MEDIUM]
  R5 (全部失敗)       ███████░░░░░░░░░░░░░░░░░  27  [LOW]
                      ─────────────────────────
                      0    25   50   75   100
```

> **所有 RPN > 40 的風險項目（R1-R4, R6-R7）皆已列出緩解措施。**  
> **R1 (RPN=96)** 為最高風險，建議 Sprint 2 立即啟動 NCC 非正式諮詢。

---

## 6. PFD 合規計算（支持干擾評估）

衛星對地面之功率通量密度 (Power Flux Density) 需符合 ITU RR Article 21 限值。

```
PFD = EIRP_sat - 10*log10(4 * pi * d^2)

其中：
  EIRP_sat = P_PA + G_ant = 30 dBm + 8 dBi = 38 dBm = 8 dBW
  d = 500 km = 5 x 10^5 m (worst case, 天頂直下點)
  4 * pi * d^2 = 4 * 3.1416 * (5e5)^2 = 3.1416e12 m^2

PFD = 8 - 10*log10(3.1416e12)
    = 8 - 124.97
    = -116.97 dBW/m^2 ≈ -117 dBW/m^2
```

**ITU RR Article 21 限值（1-3 GHz MSS, 仰角 > 5°）：**
```
PFD_limit = -152 + 0.55*(theta - 5) dBW/(m^2 * 4kHz)

@theta = 90° (worst case):
PFD_limit = -152 + 0.55*(90-5) = -152 + 46.75 = -105.25 dBW/(m^2*4kHz)
```

**本專案 PFD 於 4 kHz 頻寬內：**
```
信號頻寬 ≈ 200 Hz (100 bps QPSK)

PFD_4kHz = PFD_total + 10*log10(200/4000)
         = -117 + 10*log10(0.05)
         = -117 + (-13.01)
         = -130.0 dBW/(m^2*4kHz)
```

| 參數 | 值 | 限值 | 合規 |
|------|-----|------|------|
| PFD @4kHz (天頂) | -130.0 dBW/(m^2*4kHz) | -105.3 dBW/(m^2*4kHz) | **YES (裕度 24.7 dB)** |

> **結論：** 本專案 PFD 遠低於 ITU 限值，對地面行動通訊系統之干擾可忽略。此數據為 NCC 申請之重要佐證。

---

## 7. Action Items

| # | 項目 | 負責人 | 目標時程 | 優先度 |
|---|------|--------|---------|--------|
| 1 | 向 NCC 進行非正式諮詢（路徑 B 可行性） | PM + 指導教授 | Sprint 2 Week 1 | HIGH |
| 2 | 撰寫 NCC 學術實驗頻率申請書草案 | Comm Payload | Sprint 2 Week 2 | HIGH |
| 3 | 撰寫干擾評估報告（含 PFD 計算） | Comm Payload | Sprint 2 Week 2 | HIGH |
| 4 | 取得 TASA 背書信（支持 NCC 申請） | PM | Sprint 2 Week 3 | MEDIUM |
| 5 | 準備 ITU RR No. 4.4 通知文件 | Comm Payload + TASA | Sprint 3 | MEDIUM |
| 6 | IARU 頻率協調預申請（路徑 C 備案） | Comm Payload | Sprint 3 | LOW |
| 7 | RF 硬體模組化設計（預留 UHF 介面） | Comm Payload | Sprint 4 (Phase B) | LOW |

---

## 8. 參考文獻

1. ITU Radio Regulations, Edition of 2020, Article 4 (No. 4.4), Article 5 (Table of Frequency Allocations), Article 21 (Power Flux-Density Limits)
2. 3GPP TS 38.101-1 V17.9.0, "User Equipment radio transmission and reception; Part 1"
3. 3GPP TR 38.821 V16.2.0, "Solutions for NR to support non-terrestrial networks"
4. 台灣電信管理法（2019 年 6 月 26 日修正公布），第 50 條
5. NCC 射頻器材管理辦法
6. IARU Satellite Frequency Coordination Guidelines, Rev. 2023
7. ITU-R P.676-13, "Attenuation by atmospheric gases and related effects"
8. ITU-R P.618-14, "Propagation data and prediction methods for earth-space telecommunication systems"
9. ITU-R P.372-16, "Radio noise"

---

*TASA-NTN-3U / Sprint 1 / Phase A / SRR*
