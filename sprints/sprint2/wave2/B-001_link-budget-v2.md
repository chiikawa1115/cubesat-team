---
deliverable: B-001
sprint: 2
wave: 2
author: Comm Agent（林志遠）
date: 2026-05-03
status: revised
revision_history:
  - version: v2.1
    date: 2026-05-09
    author: Comm Agent（林志遠）
    change: C-001 修正 — 10° 仰角斜距從 2,126 km 更正為 1,695 km（正確地球幾何公式），FSPL 更正為 163.0 dB，Link Margin 更正為 +8.8 dB
reference_documents:
  - workspace/sprints/sprint1/link-budget-v1.1.md（Sprint 1 基線）
  - workspace/sprints/sprint2/wave1/B-005_power-budget-v2.md（PA 功耗確認：4.0W DC）
  - workspace/sprints/sprint2/wave1/B-002_system-architecture-icd-v1.md（ICD v1，介面確認）
---

# B-001：TASA-NTN-3U Link Budget v2.1（含裕度分析）

## 1. 文件概述

本文件為 TASA-NTN-3U S-band NTN 透明轉發器的**完整 RF 鏈路預算 v2.0**，涵蓋：

1. **UE -> SAT 上行鏈路**（Service Link，完整版含大氣與極化損耗）
2. **SAT -> gNB 下行饋電鏈路**（Feeder Link，新增）
3. **End-to-end cascade C/N0 分析**（透明轉發總鏈路）
4. **裕度敏感度分析**（Margin Sensitivity Matrix）
5. **Doppler 頻移分析**（含星上頻率穩定度需求）
6. **天線選型建議**（含廠商評估）

**Cross-reading 輸入（Wave 1 確認）**：

| 項目 | 數值 | 來源 |
|------|------|------|
| S-band PA DC 功耗上限 | 4.0 W | B-005 Section 6, IF-12 |
| PA RF 輸出功率 | ~1.0 W（+30 dBm），PAE ~25% | B-005 Section 6 / B-002 Section 4.4 |
| Contact Window 系統總功耗 | 10.30 W | B-005 Section 3.1 |
| 電池 EOL 容量 | 8.0 Wh（10 Wh x 80% 退化） | B-005 Section 5.1 |
| Contact Window DoD（EOL worst case） | 28.4%（< 30% 限值） | B-005 Section 5.5 |
| OBC <-> S-band 介面 | SPI 10 Mbps（I/Q data）+ UART 115200（控制） | B-002 IF-04/IF-05 |
| EPS -> PA 供電 | 12V boost，0.4A max（4.0W DC） | B-002 IF-12 |

---

## 2. 系統參數彙總

### 2.1 軌道與任務參數

| 參數 | 數值 | 備注 |
|------|------|------|
| 軌道高度 h | 500 km | SSO（Sun-Synchronous Orbit） |
| 軌道週期 | 94.5 min | |
| 地球半徑 R_E | 6,378 km | |
| 軌道半徑 r | 6,878 km | R_E + h |
| 最差仰角（Service Link） | 10 deg | UE -> SAT，覆蓋邊緣 |
| Feeder Link 仰角 | 30 deg | gNB 追蹤 SAT |
| 接觸窗口 | 4 min/pass | 任務基線 |
| NTN 標準 | 3GPP Rel-17 IoT-NTN | Bent-pipe transparent |
| 調變 | QPSK 1/2 | |
| 目標用戶數據率 | 100 bps（下行） | IoT-NTN 低數據率 |

### 2.2 頻率規劃（Band n256 NTN）

| 鏈路 | 方向 | 頻段 (MHz) | 中心頻率 (MHz) |
|------|------|-----------|--------------|
| Service Link UL | UE -> SAT | 1980 -- 2010 | 1995 |
| Feeder Link DL | SAT -> gNB | 2170 -- 2200 | 2185 |

> **說明**：Band n256 為 3GPP 定義的 S-band NTN 頻段。UE 上行（Service Link）使用 1980-2010 MHz，SAT 透明轉發後下行（Feeder Link）使用 2170-2200 MHz。本文件 FSPL 計算統一取各鏈路中心頻率。

---

## 3. UE -> SAT 上行鏈路（Service Link）

### 3.1 路徑幾何計算

**斜距（Slant Range）計算**：

使用正弦定律，地心角 alpha 與斜距 d 的關係：

```
d = R_E × [sqrt((r/R_E)^2 - cos^2(theta)) - sin(theta)]
```

其中 theta = 仰角。

**仰角 10 deg**（最差情況）：

```
r/R_E = 6878 / 6378 = 1.07836
cos(10 deg) = 0.98481
sin(10 deg) = 0.17365

d = 6378 × [sqrt(1.07836^2 - 0.98481^2) - 0.17365]
  = 6378 × [sqrt(1.16285 - 0.96985) - 0.17365]
  = 6378 × [sqrt(0.19300) - 0.17365]
  = 6378 × [0.43932 - 0.17365]
  = 6378 × 0.26567
  = 1,694.7 km
```

> **[v2.1 C-001 修正]**：Sprint 1 使用 d = 2,126 km，經 QA Agent P2P Review (B-011) 指出此值實際對應 ~4.5° 仰角而非 10°。正確的 10° 仰角斜距公式：
>
> ```
> d = -R_E × sin(ε) + sqrt(R_E² × sin²(ε) + h² + 2 × R_E × h)
>   = -6378 × sin(10°) + sqrt(6378² × sin²(10°) + 500² + 2 × 6378 × 500)
>   = -1107 + sqrt(1,226,208 + 250,000 + 6,378,000)
>   = -1107 + sqrt(7,854,208)
>   = -1107 + 2802
>   = 1,695 km
> ```
>
> 上方正弦定律公式亦得 d = 1,694.7 km，兩種方法吻合。**本文件 v2.1 採用正確值 d = 1,695 km。**

**仰角 30 deg**（Feeder Link）：

```
d = 6378 × [sqrt(1.07836^2 - cos^2(30 deg)) - sin(30 deg)]
  = 6378 × [sqrt(1.16285 - 0.75000) - 0.50000]
  = 6378 × [sqrt(0.41285) - 0.50000]
  = 6378 × [0.64253 - 0.50000]
  = 6378 × 0.14253
  = 909.2 km ≈ 1,000 km（含裕度，取整）
```

> **Feeder Link 設計距離取 1,000 km**，與任務規範一致。

### 3.2 自由空間路徑損耗 (FSPL)

**FSPL 公式**：

```
FSPL (dB) = 20 × log10(4 × pi × d / lambda)
          = 20 × log10(4 × pi × d × f / c)
```

**UL FSPL（f = 1995 MHz，d = 1,695 km）**：

```
FSPL_UL = 20 × log10(4 × pi × 1,695,000 × 1.995 × 10^9 / 3 × 10^8)
        = 20 × log10(4 × pi × 1,695,000 × 6.65)
        = 20 × log10(4 × pi × 11,271,750)
        = 20 × log10(141,494,978)
        = 20 × 8.1508
        = 163.0 dB
```

> **[v2.1 C-001 修正]**：原 v2.0 沿用 Sprint 1 的 d = 2,126 km 得 FSPL = 165.0 dB。修正為 d = 1,695 km 後 FSPL = 163.0 dB（降低 2.0 dB）。

**DL FSPL（f = 2185 MHz，d = 1,000 km）**：

```
FSPL_DL = 20 × log10(4 × pi × 1,000,000 × 2.185 × 10^9 / 3 × 10^8)
        = 20 × log10(4 × pi × 1,000,000 × 7.2833)
        = 20 × log10(4 × pi × 7,283,300)
        = 20 × log10(91,527,846)
        = 20 × 7.9616
        = 159.2 dB
```

### 3.3 大氣與環境損耗

| 損耗項目 | 數值 (dB) | 來源 / 說明 |
|---------|:---------:|------------|
| 大氣衰減（Atmospheric attenuation） | 0.5 | ITU-R P.676，S-band 2 GHz，仰角 10 deg，晴天 |
| 雨衰（Rain attenuation，worst case） | 0.5 | ITU-R P.618，S-band，0.01% 超時率，仰角 10 deg |
| 電離層閃爍（Ionospheric scintillation） | 0.5 | S-band 在低緯度可達 0.5 dB（ITU-R P.531） |
| 極化失配損耗（Polarization mismatch） | 0.5 | SAT RHCP patch vs UE 線極化，worst case ~3 dB；典型 ~0.5 dB（統計平均） |
| **大氣 + 環境損耗合計** | **2.0** | 保守估計 |

> **說明**：S-band（2 GHz）大氣衰減遠低於 Ka/Ku band。在 10 deg 仰角、晴天條件下，氧氣與水汽吸收合計約 0.3--0.5 dB。雨衰在 S-band 極低（< 0.5 dB even at 0.01% 超時率）。電離層閃爍在 S-band 仍可能有 0.3--0.5 dB 影響。極化失配 0.5 dB 為統計平均（UE 手持設備角度隨機）。

### 3.4 SAT 接收系統

| 參數 | 數值 | 備注 |
|------|------|------|
| SAT Rx 天線增益 | +8 dBi | Patch array，RHCP，nadir-pointing |
| SAT Rx 天線 HPBW | 70 deg（半功率波束寬度） | 對應 +-35 deg 離軸角 |
| Pointing Loss | 1.0 dB | 假設 ADCS 指向誤差 <=5 deg（在 HPBW 內） |
| Feed / Cable Loss | 0.5 dB | SMA 接頭 + 短同軸纜線 |
| LNA Noise Figure | 1.5 dB | SAT 星上 LNA |
| T_ant（天線雜訊溫度） | 100 K | Nadir-pointing，地球熱背景 |
| T_LNA（LNA 等效溫度） | 120 K | T_LNA = T0 × (NF_linear - 1) = 290 × (10^(1.5/10) - 1) = 290 × 0.4125 = 119.6 ≈ 120 K |
| T_backend（後端等效溫度） | 120 K | 混頻器 + IF 放大器（保守估計） |
| T_sys（系統雜訊溫度） | 340 K | Friis cascade: T_ant + T_LNA + T_backend/G_LNA ≈ 100 + 120 + 120 = 340 K |

> **T_sys Friis cascade 詳細計算**：
> ```
> T_sys = T_ant + T_LNA + T_mixer/G_LNA + T_IF/(G_LNA × G_mixer) + ...
> ```
> 若 LNA 增益 G_LNA = 20 dB = 100 倍，mixer NF = 8 dB（T_mixer = 1,540 K）：
> ```
> T_sys = 100 + 120 + 1540/100 + ... = 100 + 120 + 15.4 + ... ≈ 235 K
> ```
> 但 Sprint 1 基線使用 T_sys = 340 K（較保守，含 backend 降額 120 K 而非精確 Friis 展開）。**為與 Sprint 1 基線一致，維持 T_sys = 340 K。**

**G/T 計算**：

```
G/T = G_ant - 10 × log10(T_sys)
    = 8 - 10 × log10(340)
    = 8 - 10 × 2.5315
    = 8 - 25.3
    = -17.3 dB/K
```

### 3.5 UE -> SAT 上行鏈路預算表

| # | 參數 | 數值 | 單位 | 備注 |
|---|------|:----:|------|------|
| **發射端（UE）** | | | | |
| 1 | UE 發射功率 | +20.0 | dBm | IoT-NTN Power Class 5（0.1 W） |
| 2 | UE 天線增益 | 0.0 | dBi | 全向天線 |
| 3 | UE EIRP | +20.0 | dBm | = (1) + (2) |
| **路徑損耗** | | | | |
| 4 | FSPL（1995 MHz，1,695 km） | -163.0 | dB | Section 3.2（v2.1 C-001 修正） |
| 5 | 大氣衰減（晴天 + 氧氣/水汽） | -0.5 | dB | ITU-R P.676，10 deg 仰角 |
| 6 | 雨衰（worst case 0.01%） | -0.5 | dB | ITU-R P.618 |
| 7 | 電離層閃爍 | -0.5 | dB | ITU-R P.531 |
| 8 | 極化失配損耗 | -0.5 | dB | RHCP vs 線極化（統計平均） |
| 9 | 路徑損耗合計 | -165.0 | dB | = (4)+(5)+(6)+(7)+(8) |
| **接收端（SAT）** | | | | |
| 10 | SAT Rx 天線增益 | +8.0 | dBi | Patch array，RHCP |
| 11 | Pointing Loss | -1.0 | dB | ADCS 指向誤差 <=5 deg |
| 12 | Feed / Cable Loss | -0.5 | dB | SMA + 同軸纜線 |
| 13 | 有效接收天線增益 | +6.5 | dBi | = (10)+(11)+(12) |
| **接收信號功率** | | | | |
| 14 | 接收信號功率 C | -138.5 | dBm | = (3)+(9)+(13) = 20 - 165 + 6.5 |
| **雜訊** | | | | |
| 15 | T_sys | 340 | K | Section 3.4 |
| 16 | Boltzmann 常數 k | -228.6 | dBW/(Hz-K) | = -198.6 dBm/(Hz-K) |
| 17 | 雜訊功率密度 N0 | -173.3 | dBm/Hz | = (16) + 10×log10(340) = -198.6 + 25.3 |
| **C/N0** | | | | |
| 18 | **C/N0（UL）** | **+34.8** | **dB-Hz** | = (14) - (17) = -138.5 - (-173.3) |

> **替代計算驗證（使用 EIRP + G/T 公式）**：
> ```
> C/N0 = EIRP + G/T + 228.6 - FSPL - L_misc
>      = 20 + (-17.3) + 228.6 - 163.0 - 2.0 - 1.0(pointing) - 0.5(feed)
>      = 20 - 17.3 + 228.6 - 163.0 - 3.5
>      = 64.8 dB-Hz
> ```
>
> **注意**：上式 EIRP 單位為 dBW 時 Boltzmann = 228.6 dBW；EIRP 單位為 dBm 時 Boltzmann = 198.6。
> 修正為 dBm 一致：
> ```
> C/N0 = EIRP(dBm) + G/T + 198.6 - FSPL - L_misc
>      = 20 + (-17.3) + 198.6 - 163.0 - 3.5
>      = 34.8 dB-Hz   ✓ 一致
> ```

### 3.6 UL 所需 C/N0 與 Link Margin

**QPSK 1/2 解調門檻**：

| 參數 | 數值 | 備注 |
|------|------|------|
| 所需 Eb/N0（QPSK 1/2，BER = 10^-5） | 4.0 dB | AWGN，含 Turbo/LDPC 編碼增益 |
| 數據率 R_b | 100 bps = 20.0 dB-Hz | IoT-NTN 低數據率 |
| 所需 C/N0 = Eb/N0 + 10×log10(R_b) | 24.0 dB-Hz | = 4.0 + 20.0 |
| Implementation Loss | 2.0 dB | Doppler offset、timing sync、量化損耗 |
| **總所需 C/N0** | **26.0 dB-Hz** | = 24.0 + 2.0 |

**UL Link Margin**：

```
Margin_UL = C/N0 (received) - C/N0 (required)
          = 34.8 - 26.0
          = +8.8 dB
```

> **與 Sprint 1 比較**：Sprint 1 報告 Margin = +12.1 dB，差異 3.3 dB 來自 v2.1 新增的損耗項目：
> - 大氣 + 雨衰 + 電離層：-1.5 dB（Sprint 1 未計）
> - 極化失配：-0.5 dB（Sprint 1 未計）
> - Pointing Loss：-1.0 dB（Sprint 1 未計）
> - Feed/Cable Loss：-0.5 dB（Sprint 1 未計）
> - 以上合計 -3.5 dB + 計算方法差異（Sprint 1 的 Doppler margin 2 dB 在此歸為 Implementation Loss）
> - v2.1 C-001 修正斜距從 2,126 km -> 1,695 km，FSPL 降低 2.0 dB（回補部分差距）
>
> **結論**：UL Margin = +8.8 dB，**PASS**（需求 >= 3 dB）。

---

## 4. SAT -> gNB 下行饋電鏈路（Feeder Link）

### 4.1 SAT 發射參數

| 參數 | 數值 | 備注 |
|------|------|------|
| PA DC 輸入功率 | 4.0 W | B-005 功耗預算上限 |
| PA 效率 (PAE) | 25% | |
| PA RF 輸出功率 | 1.0 W = +30.0 dBm | 4.0 x 0.25 = 1.0 W |
| SAT Tx 天線增益 | +8.0 dBi | 與 Rx 共用 patch array（Tx/Rx 隔離 by duplexer） |
| Feed / Cable Loss | -0.5 dB | PA -> 天線饋電損耗 |
| Pointing Loss | -1.0 dB | ADCS 指向誤差 <=5 deg |
| **SAT EIRP** | **+36.5 dBm** | = 30.0 + 8.0 - 0.5 - 1.0 |

### 4.2 gNB 地面站接收參數

**天線增益計算（2.4 m Parabolic Dish）**：

```
G = eta × (pi × D / lambda)^2
lambda = c / f = 3×10^8 / 2.185×10^9 = 0.13729 m
G = 0.55 × (pi × 2.4 / 0.13729)^2
  = 0.55 × (54.908)^2
  = 0.55 × 3,014.9
  = 1,658.2
G (dBi) = 10 × log10(1658.2) = 32.2 dBi
```

**gNB 接收系統**：

| 參數 | 數值 | 備注 |
|------|------|------|
| gNB 天線增益 | +32.2 dBi | 2.4 m dish，效率 55%，@2185 MHz |
| gNB 天線 HPBW | ~3.0 deg | = 70 × lambda / D = 70 × 0.137 / 2.4 = 4.0 deg（近似） |
| Pointing Loss（gNB） | -0.3 dB | 地面站追蹤精度高（< 0.5 deg） |
| Feed / Cable Loss（gNB） | -0.5 dB | 地面站同軸纜線（較短） |
| LNA NF（gNB） | 0.5 dB | 地面站低雜訊 LNA（商用級） |
| T_ant（gNB，仰角 30 deg） | 30 K | 對天空，低仰角略高 |
| T_LNA | 35 K | NF = 0.5 dB -> T = 290 × (10^(0.5/10) - 1) = 290 × 0.1220 = 35.4 K |
| T_backend | 50 K | 地面站後端，良好設計 |
| T_sys（gNB） | 115 K | = 30 + 35 + 50 |

**gNB G/T**：

```
G/T_gNB = 32.2 - 10 × log10(115)
        = 32.2 - 20.6
        = +11.6 dB/K
```

### 4.3 Feeder Link 路徑損耗

| 項目 | 數值 (dB) | 備注 |
|------|:---------:|------|
| FSPL（2185 MHz，1,000 km） | 159.2 | Section 3.2 |
| 大氣衰減（仰角 30 deg） | 0.3 | 較 10 deg 路徑短，衰減小 |
| 雨衰（worst case） | 0.3 | S-band，仰角 30 deg |
| 電離層閃爍 | 0.3 | |
| 極化失配 | 0.0 | gNB 使用 RHCP feed，匹配 SAT RHCP |
| **路徑損耗合計** | **160.1** | |

### 4.4 Feeder Link Budget 表

| # | 參數 | 數值 | 單位 | 備注 |
|---|------|:----:|------|------|
| **發射端（SAT）** | | | | |
| 1 | SAT PA 輸出功率 | +30.0 | dBm | 1.0 W |
| 2 | SAT Tx 天線增益 | +8.0 | dBi | Patch array，RHCP |
| 3 | SAT Feed/Cable Loss | -0.5 | dB | |
| 4 | SAT Pointing Loss | -1.0 | dB | ADCS <=5 deg |
| 5 | SAT EIRP | +36.5 | dBm | = (1)+(2)+(3)+(4) |
| **路徑損耗** | | | | |
| 6 | FSPL（2185 MHz，1,000 km） | -159.2 | dB | |
| 7 | 大氣 + 雨衰 + 電離層 | -0.9 | dB | 仰角 30 deg |
| 8 | 極化失配 | 0.0 | dB | RHCP-RHCP 匹配 |
| 9 | 路徑損耗合計 | -160.1 | dB | = (6)+(7)+(8) |
| **接收端（gNB）** | | | | |
| 10 | gNB 天線增益 | +32.2 | dBi | 2.4 m dish |
| 11 | gNB Pointing Loss | -0.3 | dB | 地面站追蹤 |
| 12 | gNB Feed/Cable Loss | -0.5 | dB | |
| 13 | 有效接收天線增益 | +31.4 | dBi | = (10)+(11)+(12) |
| **接收信號功率** | | | | |
| 14 | 接收信號功率 C | -92.2 | dBm | = (5)+(9)+(13) = 36.5 - 160.1 + 31.4 |
| **雜訊** | | | | |
| 15 | T_sys（gNB） | 115 | K | |
| 16 | N0 | -178.0 | dBm/Hz | = -198.6 + 10×log10(115) = -198.6 + 20.6 |
| **C/N0** | | | | |
| 17 | **C/N0（DL Feeder）** | **+85.8** | **dB-Hz** | = (14) - (16) = -92.2 - (-178.0) |

**DL Feeder Link Margin**：

```
所需 C/N0 = Eb/N0 + 10×log10(R_b) + Implementation Loss
          = 4.0 + 20.0 + 2.0
          = 26.0 dB-Hz

Margin_DL = 85.8 - 26.0 = +59.8 dB
```

> **結論**：Feeder Link Margin = **+59.8 dB**，遠超 3 dB 需求。這是因為 SAT PA 功率 +30 dBm 遠高於 UE 的 +20 dBm，加上 gNB 大口徑碟形天線（+32.2 dBi >> UE 0 dBi），以及路徑距離短（1,000 km vs 1,695 km）。
>
> **Feeder Link 非瓶頸**：透明轉發鏈路的瓶頸在 UE -> SAT 上行段，與預期一致。

---

## 5. End-to-end Cascade C/N0 分析（透明轉發）

### 5.1 透明轉發 C/N0 合成

透明轉發器（bent-pipe）不做解調/再調，雜訊直接級聯。總 C/N0 由上行與下行 C/N0 合成：

```
(C/N0)_total^(-1) = (C/N0)_UL^(-1) + (C/N0)_DL^(-1)
```

**數值計算**：

```
(C/N0)_UL = 34.8 dB-Hz = 10^(34.8/10) = 3,020 Hz
(C/N0)_DL = 85.8 dB-Hz = 10^(85.8/10) = 380,189,396 Hz

(C/N0)_total^(-1) = 1/3,020 + 1/380,189,396
                   = 3.3113 × 10^(-4) + 2.6303 × 10^(-9)
                   = 3.3113 × 10^(-4)

(C/N0)_total = 1 / 3.3113 × 10^(-4) = 3,019.7 Hz

(C/N0)_total (dB-Hz) = 10 × log10(3,019.7) = 34.80 dB-Hz
```

> **分析**：End-to-end C/N0 = **34.80 dB-Hz**，幾乎等於上行 C/N0（34.8 dB-Hz）。這是因為下行 Feeder Link C/N0（85.8 dB-Hz）遠高於上行，下行對總雜訊的貢獻可忽略（差 51 dB）。
>
> **結論**：透明轉發鏈路完全由 **UE -> SAT 上行段主導**，Feeder Link 不構成瓶頸。

### 5.2 End-to-end Link Margin

```
End-to-end Margin = (C/N0)_total - (C/N0)_required
                  = 34.80 - 26.0
                  = +8.8 dB
```

### 5.3 Link Budget 摘要

| 鏈路 | C/N0 (dB-Hz) | 所需 C/N0 (dB-Hz) | Margin (dB) | 判定 |
|------|:------------:|:-----------------:|:----------:|:----:|
| UL（UE -> SAT） | 34.8 | 26.0 | **+8.8** | **PASS** (>= 3 dB) |
| DL（SAT -> gNB） | 85.8 | 26.0 | **+59.8** | **PASS** (>> 3 dB) |
| **End-to-end** | **34.80** | **26.0** | **+8.8** | **PASS** |

---

## 6. 裕度敏感度分析（Margin Sensitivity Analysis）

### 6.1 敏感度矩陣

以 End-to-end Margin 基線 = **+8.8 dB** 為基準，逐一變動參數觀察裕度變化：

| # | 參數變動 | 變動量 | 新 C/N0_UL (dB-Hz) | 新 Margin (dB) | Margin 變化 (dB) | 判定 |
|---|---------|:------:|:-------------------:|:--------------:|:----------------:|:----:|
| S1 | UE EIRP -1 dB | -1 dB | 33.8 | +7.8 | -1.0 | PASS |
| S2 | UE EIRP +1 dB | +1 dB | 35.8 | +9.8 | +1.0 | PASS |
| S3 | SAT G/T -1 dB | -1 dB | 33.8 | +7.8 | -1.0 | PASS |
| S4 | SAT G/T +1 dB | +1 dB | 35.8 | +9.8 | +1.0 | PASS |
| S5 | 大氣衰減 +2 dB（暴雨） | +2 dB atm | 32.8 | +6.8 | -2.0 | PASS |
| S6 | 仰角 10 deg -> 5 deg | FSPL +5.1 dB | 29.2 | +3.2 | -5.6 | **MARGINAL** |
| S7 | S1 + S3 同時（worst case） | -1 -1 | 32.8 | +6.8 | -2.0 | PASS |
| S8 | S1 + S3 + S5 | -1 -1 +2 atm | 30.8 | +4.8 | -4.0 | PASS |

**仰角 5 deg 路徑損耗計算**：

```
仰角 5 deg 時，斜距增大（球面幾何計算）：
d(5 deg) ≈ 3,040 km（球面幾何，仰角 5 deg 接近地平線）

FSPL(5 deg) = 20 × log10(4 × pi × 3,040,000 × 1.995×10^9 / 3×10^8)
            = 20 × log10(4 × pi × 3,040,000 × 6.65)
            = 20 × log10(4 × pi × 20,216,000)
            = 20 × log10(253,970,000)
            = 20 × 8.4048
            = 168.1 dB

大氣衰減（5 deg 仰角，路徑更長）：~1.0 dB

FSPL + atm = 168.1 + 1.0 + 0.5(rain) + 0.7(iono) + 0.5(pol) = 170.8 dB
C/N0(5 deg) = 20 + 6.5 - 170.8 + 173.3 = 29.0 dB-Hz
Margin(5 deg) = 29.0 - 26.0 = +3.0 dB
```

> **修正**：上方 S6 採用更精確計算，5 deg 仰角 Margin ≈ +3.0--3.2 dB，勉強通過 3 dB 門檻。

### 6.2 敏感度分析結論

1. **UE EIRP 與 SAT G/T**：各 +-1 dB 變動對 Margin 影響為 1:1（線性），單獨退化不會跌破 3 dB 門檻。

2. **大氣衰減**：暴雨情境 (+2 dB) 使 Margin 從 8.8 降至 6.8 dB，仍可接受。即便同時疊加其他退化（S8 場景），Margin = 4.8 dB 仍 PASS（>= 3 dB）。

3. **仰角退化**：5 deg 仰角是鏈路的**臨界邊界**，Margin ≈ 3 dB，幾乎無裕度。建議：
   - **最低運作仰角設定為 10 deg**（設計基線）
   - **5 deg 仰角僅作為降級模式**（降低數據率或增加重傳）

4. **Worst case（S8）**：UE EIRP -1 dB + SAT G/T -1 dB + 暴雨 +2 dB 同時發生時，Margin = +4.8 dB，仍 PASS（>= 3 dB）。v2.1 斜距修正後此極端場景已不再跌破門檻。

### 6.3 風險與建議

| 風險 | 嚴重度 | 概率 | 建議對策 |
|------|:------:|:----:|---------|
| 多重退化同時發生（S8） | 低 | 低 | v2.1 修正後 S8 Margin = +4.8 dB，已 PASS。仍建議確保 UE EIRP 穩定、SAT 天線定期校準 |
| 5 deg 仰角運作 | 高 | 中 | 設計最低仰角 = 10 deg；5 deg 時切換至更強健調變（BPSK 1/3） |
| 暴雨期間鏈路退化 | 低 | 低 | S-band 雨衰極低，非主要風險 |

---

## 7. Doppler 頻移分析

### 7.1 軌道速度計算

500 km SSO 的軌道速度：

```
v = sqrt(GM / r)
  = sqrt(3.986 × 10^14 / (6,378,000 + 500,000))
  = sqrt(3.986 × 10^14 / 6,878,000)
  = sqrt(5.7950 × 10^7)
  = 7,612.5 m/s
  ≈ 7.613 km/s
```

> **驗證**：典型 LEO 500 km 軌道速度約 7.6 km/s，結果合理。

### 7.2 最大 Doppler 頻偏計算

最大 Doppler 偏移發生在衛星水平通過頭頂時（仰角 = 0 deg，即地平線），此時徑向速度最大：

```
f_d_max = f × v / c    （衛星直接朝向/遠離觀測者時）
```

但更精確地，最大徑向速度取決於軌道幾何：

```
v_radial_max = v_orbit × cos(仰角_min)
```

在仰角 = 0 deg 時，cos(0) = 1，此時衛星沿地平線方向移動，但實際上最大徑向分量出現在仰角較低但非零的情況。精確計算：

```
v_radial_max = v_orbit × cos(仰角_grazing) × (R_E / (R_E + h))
```

對於 LEO 簡化，最大 Doppler 偏移近似：

```
f_d_max ≈ f × v_orbit / c
```

**UL（1995 MHz）**：

```
f_d_max_UL = 1995 × 10^6 × 7612.5 / (3 × 10^8)
           = 1995 × 10^6 × 2.5375 × 10^(-5)
           = 50,623 Hz
           ≈ ±50.6 kHz
```

**DL（2185 MHz）**：

```
f_d_max_DL = 2185 × 10^6 × 7612.5 / (3 × 10^8)
           = 2185 × 10^6 × 2.5375 × 10^(-5)
           = 55,444 Hz
           ≈ ±55.4 kHz
```

### 7.3 Doppler 變化率

Doppler 變化率（Doppler rate）在頭頂通過時最大：

```
df/dt_max ≈ v^2 × f / (c × (R_E + h))
          = 7612.5^2 × 1995 × 10^6 / (3 × 10^8 × 6,878,000)
          = 5.795 × 10^7 × 1.995 × 10^9 / (2.0634 × 10^15)
          = 1.1561 × 10^17 / 2.0634 × 10^15
          = 56.0 Hz/s
          ≈ 56 Hz/s（UL）
```

DL 的 Doppler rate：

```
df/dt_max_DL ≈ 56 × (2185/1995) = 61.3 Hz/s
```

### 7.4 NTN Rel-17 Doppler 補償機制

根據 3GPP TS 38.300 / 38.211（NTN）：

| 項目 | Rel-17 NTN 規範 |
|------|----------------|
| UE Doppler pre-compensation | **不要求**（IoT-NTN UE 無需補償） |
| gNB Doppler compensation | **gNB 負責**全部 Doppler 補償（基於星曆） |
| SAT 星上需求 | 透明轉發器不做頻率轉換補償 |
| 頻率穩定度要求（SAT LO） | 需容納 ±55 kHz Doppler 而不失鎖 |

### 7.5 星上頻率合成器需求

**需求分析**：

SAT 透明轉發器內的 Local Oscillator（LO）用於上/下變頻（UL 1995 MHz -> DL 2185 MHz，LO 頻率 = 190 MHz 或使用中頻方案）。LO 頻率穩定度需求：

```
接收信號 Doppler 範圍：±50.6 kHz（UL）
SAT LO 本身頻率誤差需遠小於 Doppler 範圍：
  - LO 精度要求：< ±1 kHz（避免對 Doppler 補償造成額外負擔）
  - 對應 LO 頻率穩定度：1 kHz / 190 MHz = 5.26 × 10^(-6) = 5.26 ppm

或以 2 GHz 為基準：
  - 1 kHz / 2000 MHz = 0.5 ppm
```

**頻率源選型建議**：

| 選項 | 穩定度 (ppm) | 功耗 | 質量 | 成本 (USD) | 建議 |
|------|:----------:|:----:|:----:|:----------:|:----:|
| TCXO（Temperature-Compensated Crystal Oscillator） | ±0.5 -- ±2.0 | 10--50 mW | 1--3 g | $5--$30 | **推薦** |
| OCXO（Oven-Controlled Crystal Oscillator） | ±0.01 -- ±0.05 | 1--3 W | 20--50 g | $100--$500 | 功耗過高，不適合 3U CubeSat |
| 一般 XO（Crystal Oscillator） | ±10 -- ±25 | 1--10 mW | < 1 g | $1--$5 | 穩定度不足 |

**結論**：

- **推薦使用 TCXO**，穩定度 ±1 ppm（或更佳）即可滿足需求。
- TCXO 功耗極低（< 50 mW），不影響 B-005 功耗預算。
- **不需要 OCXO**：OCXO 功耗 1--3W 在 4.0W DC PA 預算下不可接受，且 NTN 架構中 gNB 負責精確 Doppler 補償，SAT 端穩定度需求不嚴格。
- 建議選用航太級 TCXO，例如 Rakon CFPT-9520（±0.5 ppm，-40 ~ +85 degC，20 mW）。

### 7.6 Doppler 對 RF 設計的影響

| 影響項目 | 分析 | 設計對策 |
|---------|------|---------|
| 接收濾波器頻寬 | SAW BPF 需容納 ±50.6 kHz Doppler + 信號頻寬。30 MHz 通道頻寬遠大於 Doppler -> **無影響** | BPF 設計按 30 MHz 通道頻寬，不需加寬 |
| LNA 動態範圍 | Doppler 不影響功率位準 -> **無影響** | 無需調整 |
| PLL 鎖定範圍 | LO PLL 鎖定頻寬需 > ±55 kHz | PLL loop BW 設計 > 100 kHz |
| ADC 取樣時鐘 | FPGA 取樣時鐘的 jitter 需 < 1/(2 × f_Nyquist) | 使用 TCXO 驅動 ADC clock |
| 基帶 Doppler tracking | gNB 負責，SAT 不處理 | 無星上設計需求 |

---

## 8. 天線選型建議

### 8.1 需求規格

| 參數 | 需求 | 備注 |
|------|------|------|
| 頻段 | S-band 1980--2200 MHz（Tx + Rx） | UL + DL 雙頻 |
| 極化 | RHCP | 衛星通訊標準 |
| 增益 | >= +8 dBi | Link Budget 基線 |
| HPBW | >= 70 deg（半功率波束寬度） | 對應 +-35 deg 離軸角 |
| 尺寸限制 | <= 100 x 100 mm（3U CubeSat -Z 面） | Body-mount 或展開式 |
| 質量 | < 100 g（含饋電網路） | CubeSat 質量預算 |
| 溫度範圍 | -40 ~ +85 degC | LEO 環境 |

### 8.2 廠商評估

| 廠商/產品 | 增益 (dBi) | HPBW (deg) | 頻段 (MHz) | 極化 | 尺寸 (mm) | 質量 (g) | 概估價 (USD) | 備注 |
|----------|:---------:|:----------:|:----------:|:----:|:---------:|:--------:|:----------:|------|
| **EnduroSat S-band Patch Antenna** | 6--8 | 70--90 | 2000--2300 | RHCP | 98 x 98 x 8 | 60 | $3,000--5,000 | 飛行驗證品（ISS 部署經驗），3U 面板直接安裝 |
| **ISISPACE S-band Antenna** | 7--9 | 60--80 | 1980--2200 | RHCP | 96 x 96 x 10 | 80 | $4,000--7,000 | 荷蘭 ISIS 旗下，含 duplexer 整合方案 |
| **Anywaves S-band Antenna** | 6--8 | 80 | 2025--2110 / 2200--2290 | RHCP | 80 x 80 x 15 | 70 | $5,000--8,000 | 法國 CNES 旗下，高可靠度但價格較高 |
| **自行設計 2x2 Patch Array** | 8--10 | 60--70 | 1980--2200 | RHCP（Sequential rotation feed） | 100 x 100 x 5 | 40--60 | $500--1,500（PCB 製造） | 需自行設計 + 校準，風險較高 |

### 8.3 選型建議

**首選：EnduroSat S-band Patch Antenna**

| 評估項目 | 評分 | 說明 |
|---------|:----:|------|
| 技術符合度 | 9/10 | 增益 6--8 dBi、HPBW 70--90 deg，滿足需求 |
| 飛行驗證 | 9/10 | ISS 部署驗證，TRL 7--8 |
| 3U 相容性 | 10/10 | 98 x 98 mm 完美匹配 3U 面板 |
| 交期 | 8/10 | 商用現貨，12--16 週 |
| 成本 | 8/10 | $3,000--5,000，合理 |
| 風險 | 低 | 成熟產品 |

**備選：ISISPACE S-band Antenna**（若需整合 duplexer）

> **說明**：EnduroSat 產品技術成熟、尺寸完美匹配 3U 面板、且有飛行驗證紀錄。增益標稱 6--8 dBi，我們 Link Budget 取 8 dBi 為設計基線。若實測增益僅 6 dBi，Margin 從 8.8 dB 降至 6.8 dB，仍 PASS（>= 3 dB）。
>
> 自行設計 2x2 patch array 可達更高增益（10 dBi），但需額外設計工時（2--3 個月）與 anechoic chamber 校準（$5,000+），且 TRL 低（需從 TRL 3 開始驗證）。在 3 年任務壽命的小衛星專案中，建議優先採用商用驗證品。

### 8.4 天線增益 vs 離軸角特性

以 8 dBi Patch Array 典型方向圖估算：

| 離軸角 (deg) | 相對增益 (dB) | 絕對增益 (dBi) | 備注 |
|:------------:|:------------:|:-------------:|------|
| 0（正軸） | 0.0 | 8.0 | 波束中心 |
| 10 | -0.3 | 7.7 | |
| 15 | -0.6 | 7.4 | |
| 20 | -1.0 | 7.0 | **1 dB 點** |
| 25 | -1.5 | 6.5 | |
| 30 | -2.5 | 5.5 | |
| 35 | -3.0 | 5.0 | **HPBW 邊緣（-3 dB 點）** |
| 45 | -6.0 | 2.0 | |
| 60 | -10.0 | -2.0 | |

> **AOCS 指向需求**：
> - **1 dB pointing loss 對應離軸角 ±20.2 deg**（上表內插）
> - Link Budget 分配 Pointing Loss = 1.0 dB -> ADCS 指向誤差需 <= ±20 deg
> - B-002 ICD 中 ADCS 精度目標 = 5 deg -> **遠優於需求**，Pointing Loss 裕度充足
> - 若 ADCS 僅達 10 deg 精度，Pointing Loss ≈ 0.3 dB，仍在 1.0 dB 預算內

---

## 9. Pointing Loss Budget（天線指向損耗預算）

本節專門定義天線指向損耗預算，供 AOCS Agent（B-006）引用。

### 9.1 指向損耗分配

| 項目 | 分配值 (dB) | 對應離軸角 (deg) | 備注 |
|------|:---------:|:--------------:|------|
| Link Budget 中的 Pointing Loss 預算 | 1.0 | ±20 | 設計基線 |
| ADCS 目標指向精度 | -- | ±5 | B-002 Section 4.3 |
| ADCS 達成 5 deg 時的實際 Pointing Loss | 0.3 | ±5 | 增益曲線查表 |
| **Pointing Loss Margin** | **0.7** | -- | = 1.0 - 0.3（充足） |

### 9.2 ADCS 指向需求彙總（for B-006）

| 需求 | 數值 | 來源 |
|------|------|------|
| 最大容許 Pointing Loss | 1.0 dB | Link Budget v2.0 |
| 對應最大離軸角（1 dB 點） | ±20.2 deg | Section 8.4 天線方向圖 |
| ADCS 指向精度需求（嚴格） | <= ±20 deg | Pointing Loss 1.0 dB 不超標 |
| ADCS 指向精度需求（建議） | <= ±5 deg | B-002 基線，留 0.7 dB margin |
| HPBW 半角 | ±35 deg | 天線 -3 dB 波束寬度 |

---

## 10. 完整 Link Budget 彙總表

### 10.1 UL（UE -> SAT，Service Link）

| 項目 | 數值 | 單位 |
|------|:----:|------|
| UE EIRP | +20.0 | dBm |
| FSPL（1995 MHz，1,695 km） | -163.0 | dB |
| 大氣 + 雨衰 + 電離層 + 極化 | -2.0 | dB |
| SAT 有效天線增益（含 pointing + feed loss） | +6.5 | dBi |
| 接收 C | -138.5 | dBm |
| N0 | -173.3 | dBm/Hz |
| **C/N0 (UL)** | **34.8** | **dB-Hz** |
| 所需 C/N0 | 26.0 | dB-Hz |
| **UL Margin** | **+8.8** | **dB** |

### 10.2 DL（SAT -> gNB，Feeder Link）

| 項目 | 數值 | 單位 |
|------|:----:|------|
| SAT EIRP | +36.5 | dBm |
| FSPL（2185 MHz，1,000 km） | -159.2 | dB |
| 大氣 + 雨衰 + 電離層 | -0.9 | dB |
| gNB 有效天線增益（含 pointing + feed loss） | +31.4 | dBi |
| 接收 C | -92.2 | dBm |
| N0 | -178.0 | dBm/Hz |
| **C/N0 (DL)** | **85.8** | **dB-Hz** |
| 所需 C/N0 | 26.0 | dB-Hz |
| **DL Margin** | **+59.8** | **dB** |

### 10.3 End-to-end（透明轉發）

| 項目 | 數值 | 單位 |
|------|:----:|------|
| **(C/N0)_total** | **34.80** | **dB-Hz** |
| 所需 C/N0 | 26.0 | dB-Hz |
| **End-to-end Margin** | **+8.8** | **dB** |
| 瓶頸鏈路 | UE -> SAT（UL） | -- |

---

## 11. 設計建議與行動項目

### 11.1 Sprint 1 行動項目結案

| Sprint 1 行動項目 | 狀態 | 本文件處理 |
|------------------|:----:|-----------|
| SAT->gNB Feeder Link Budget | **完成** | Section 4 |
| End-to-end cascade C/N0 分析 | **完成** | Section 5 |
| 裕度敏感度分析 | **完成** | Section 6 |

### 11.2 Sprint 3 行動項目（建議）

| # | 項目 | 優先級 | 說明 |
|---|------|:------:|------|
| A1 | SAT 天線實測增益方向圖 | 高 | 確認 EnduroSat 天線在 1980-2200 MHz 的實測增益 >= 8 dBi |
| A2 | PA 效率實測 | 高 | 確認 PAE >= 25% at +30 dBm output，1W RF |
| A3 | 5 deg 仰角降級模式定義 | 中 | 定義 5 deg 仰角時的降級策略（BPSK 1/3 或降低 data rate） |
| A4 | LNA + 接收鏈 NF 實測 | 中 | 確認星上 NF <= 1.5 dB（System NF，非 LNA 單體） |
| A5 | Doppler 環路設計 | 低 | FPGA 基帶中的 carrier tracking loop 設計（gNB 補償為主，SAT 端被動） |
| A6 | 干擾分析（co-frequency / adjacent channel） | 中 | S-band n256 與其他 NTN / terrestrial 系統的干擾共存分析 |

### 11.3 關鍵設計決策摘要

| 項目 | 決策 | 理由 |
|------|------|------|
| 最低運作仰角 | 10 deg | 5 deg 仰角 Margin ≈ 3 dB，過薄 |
| SAT 頻率源 | TCXO（±1 ppm） | 功耗低、穩定度足夠，不需 OCXO |
| 天線選型 | EnduroSat S-band Patch | TRL 高、尺寸匹配、價格合理 |
| Link 瓶頸 | UL（UE -> SAT） | DL Feeder Link margin >> 50 dB，非瓶頸 |
| 極化 | RHCP | 衛星通訊標準，與 UE 線極化有 0.5 dB 統計平均損耗 |

---

## 12. 附錄：計算參數彙總

| 參數 | 符號 | 數值 | 單位 |
|------|------|:----:|------|
| 軌道高度 | h | 500 | km |
| 地球半徑 | R_E | 6,378 | km |
| 軌道半徑 | r | 6,878 | km |
| 軌道速度 | v_orbit | 7,612.5 | m/s |
| 重力參數 | GM | 3.986 x 10^14 | m^3/s^2 |
| 光速 | c | 3 x 10^8 | m/s |
| Boltzmann 常數 | k | -228.6 | dBW/(Hz-K) |
| UL 頻率 | f_UL | 1,995 | MHz |
| DL 頻率 | f_DL | 2,185 | MHz |
| UL 斜距（10 deg） | d_UL | 1,695 | km |
| DL 斜距（30 deg） | d_DL | 1,000 | km |
| UL FSPL | FSPL_UL | 163.0 | dB |
| DL FSPL | FSPL_DL | 159.2 | dB |
| UE EIRP | EIRP_UE | +20.0 | dBm |
| SAT EIRP | EIRP_SAT | +36.5 | dBm |
| SAT G/T | G/T_SAT | -17.3 | dB/K |
| gNB G/T | G/T_gNB | +11.6 | dB/K |
| SAT T_sys | T_sys_SAT | 340 | K |
| gNB T_sys | T_sys_gNB | 115 | K |
| C/N0 (UL) | C/N0_UL | 34.8 | dB-Hz |
| C/N0 (DL) | C/N0_DL | 85.8 | dB-Hz |
| C/N0 (total) | C/N0_total | 34.80 | dB-Hz |
| 所需 Eb/N0 | Eb/N0_req | 4.0 | dB |
| 數據率 | R_b | 100 | bps |
| 所需 C/N0 | C/N0_req | 26.0 | dB-Hz |
| UL Margin | M_UL | +8.8 | dB |
| DL Margin | M_DL | +59.8 | dB |
| E2E Margin | M_total | +8.8 | dB |
| UL Doppler max | f_d_UL | ±50.6 | kHz |
| DL Doppler max | f_d_DL | ±55.4 | kHz |
| Doppler rate max | df/dt | ~56 | Hz/s |

---

## Wave 2 Cross-reading 通知 (for AOCS Agent)

**AOCS Agent（B-006 ADCS Trade Study）需從本文件確認：**
- SAT 天線增益 / HPBW（此為指向損耗計算基線）
  - 天線增益：+8 dBi（nadir-pointing，RHCP patch array）
  - HPBW：70 deg（±35 deg 半功率波束寬度）
- 指向損耗預算：Link Budget 中分配 **1.0 dB** 給 Pointing Loss
  - 對應 ADCS 指向誤差容許值 ≤ ±20 deg（天線 1 dB 點）
  - B-002 基線 ADCS 精度 = ±5 deg -> Pointing Loss 僅 0.3 dB，margin 0.7 dB
- 天線增益 vs 偏軸角曲線的 1 dB 點（對應 ADCS 指向誤差規格）
  - **1 dB 點 = ±20.2 deg**（Section 8.4 方向圖表）
  - 3 dB 點 = ±35 deg（HPBW 邊緣）

若 B-006 ADCS 選型後功耗超過 B-005 分配的 0.5W，請在 discussions.json 開 THR-003。

---

---

## C-001 修正說明

### 原錯誤

Sprint 1 Link Budget v1.1 使用 10° 仰角斜距 d = 2,126 km，v2.0 為保守性沿用此值。經 QA Agent P2P Review（B-011）精確驗算，d = 2,126 km 實際對應約 4.5° 仰角，而非 10°。10° 仰角的正確斜距為 ~1,695 km（差異 25%）。

### 正確公式與計算步驟

使用標準地球幾何斜距公式：

```
d = -R_E × sin(ε) + sqrt(R_E² × sin²(ε) + h² + 2 × R_E × h)

其中：
  R_E = 6,378 km（地球半徑）
  h   = 500 km（軌道高度）
  ε   = 10°（最低仰角）

d = -6378 × sin(10°) + sqrt(6378² × sin²(10°) + 500² + 2 × 6378 × 500)
  = -6378 × 0.17365 + sqrt(6378² × 0.03015 + 250,000 + 6,378,000)
  = -1,107 + sqrt(1,226,208 + 250,000 + 6,378,000)
  = -1,107 + sqrt(7,854,208)
  = -1,107 + 2,802
  = 1,695 km
```

正弦定律公式同樣驗證：d = 6378 × [sqrt((6878/6378)² - cos²(10°)) - sin(10°)] = 1,694.7 km，兩種方法吻合。

### 修正影響

| 項目 | 原值（v2.0） | 修正值（v2.1） | 變化 |
|------|:----------:|:------------:|:----:|
| 10° 仰角斜距 d | 2,126 km | 1,695 km | -431 km (-20%) |
| UL FSPL（1995 MHz） | 165.0 dB | 163.0 dB | -2.0 dB |
| UL C/N0 | 32.8 dB-Hz | 34.8 dB-Hz | +2.0 dB |
| UL Link Margin | +6.8 dB | +8.8 dB | +2.0 dB |
| E2E Link Margin | +6.8 dB | +8.8 dB | +2.0 dB |
| S8 Worst Case Margin | +2.8 dB (FAIL) | +4.8 dB (PASS) | +2.0 dB |

### 結論

- **修正方向為更樂觀**：路徑損耗較原估值低 2.0 dB，Link Margin 從 +6.8 dB 提升至 +8.8 dB。
- **設計基線無需修改**：所有 Section 11 的設計決策（最低仰角 10°、天線選型、TCXO 等）在更大裕度下更為穩健。
- **S8 極端場景改善**：原 v2.0 的 S8 場景（多重退化同時）Margin = +2.8 dB 跌破 3 dB 門檻，修正後 S8 = +4.8 dB，全場景均 PASS。
- **保守設計建議**：若團隊希望維持保守性，可沿用 +6.8 dB 作為 margin floor（設計裕度底線），實際性能更佳。
- **數字正確性**：即便結果更樂觀，正確的數字是工程文件的基本要求，PDR 審查包必須使用正確值。

---

*文件結束 -- Comm Agent（林志遠），2026-05-03（v2.1 修正：2026-05-09）*
