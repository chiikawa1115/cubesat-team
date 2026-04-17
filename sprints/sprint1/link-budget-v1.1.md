# TASA-NTN-3U Link Budget v1.1

> **Document ID:** LB-v1.1  
> **Date:** 2026-04-15  
> **Author:** Comm Payload Engineer (Rudy)  
> **Status:** Sprint 1 / Phase A / SRR Deliverable  
> **Changelog v1.0 -> v1.1:**  
> - **[FIX]** T_sys 改為從 LNA NF 推導，不再假設 300 K  
> - **[FIX]** 新增 Implementation Margin 2 dB（含 Doppler 補償）  
> - **[FIX]** Required Eb/No 修正為 6 dB（QPSK 1/2 + implementation margin）

---

## 1. 任務情境

| 參數 | 值 | 備注 |
|------|-----|------|
| 軌道高度 | 500 km | SSO |
| 最小仰角 | 10° | Worst case |
| Slant range (仰角 10°) | 1,932 km | 見 Section 2 計算 |
| UL 頻段 | 1980 -- 2010 MHz | 3GPP n236 UL |
| DL 頻段 | 2170 -- 2200 MHz | 3GPP n236 DL |
| 架構 | Transparent Bent-pipe (Rel-17) | UE -> SAT -> gNB |
| 目標資料率 | 100 bps | IoT-NTN narrowband |
| 調變 / 編碼 | QPSK, code rate 1/2 | |
| BER 需求 | <= 1 x 10^-6 | |

---

## 2. Slant Range 計算（仰角 10° worst case）

地球半徑 R_E = 6,371 km，軌道高度 h = 500 km，仰角 theta = 10°。

```
Slant range d = sqrt((R_E + h)^2 - (R_E * cos(theta))^2) - R_E * sin(theta)
```

數值代入：
```
R_E + h = 6,871 km
R_E * cos(10°) = 6,371 * 0.9848 = 6,274.2 km
R_E * sin(10°) = 6,371 * 0.1736 = 1,106.0 km

d = sqrt(6,871^2 - 6,274.2^2) - 1,106.0
  = sqrt(47,210,641 - 39,365,585) - 1,106.0
  = sqrt(7,845,056) - 1,106.0
  = 2,800.9 - 1,106.0
  = 1,694.9 km
```

> **注意：** 上述為幾何最短路徑。考慮大氣折射與實際軌道偏差，取保守值 **d = 1,700 km** 用於 FSPL 計算。  
> （天頂 zenith case: d = 500 km，用於 best case 驗算。）

---

## 3. Uplink Budget（UE -> Satellite）

### 3.1 傳輸端（UE 端）

| 參數 | 值 | 單位 | 計算 / 來源 |
|------|-----|------|-------------|
| UE Tx Power (P_tx) | +23 | dBm | 3GPP TS 38.101 power class 3 (NTN UE max) |
| UE Tx Power (P_tx) | -7.0 | dBW | 23 dBm - 30 = -7 dBW |
| UE Antenna Gain (G_tx) | 0 | dBi | 手持終端 omnidirectional |
| UE Feed Loss (L_tx) | 0 | dB | 手持裝置，無饋線 |
| **EIRP** | **-7.0** | **dBW** | P_tx + G_tx - L_tx = -7 + 0 - 0 |

### 3.2 傳播損耗

| 參數 | 值 | 單位 | 計算 / 來源 |
|------|-----|------|-------------|
| 頻率 (f) | 2.0 | GHz | n236 UL 中心頻率 ~1995 MHz |
| Slant Range (d) | 1,700 | km | 仰角 10° worst case（見 Section 2） |
| **FSPL** | **159.1** | **dB** | 20*log10(1700) + 20*log10(2.0) + 92.45 = 64.61 + 6.02 + 92.45 = 163.08 ... (修正見下) |

**FSPL 精算：**
```
FSPL = 20*log10(d_km) + 20*log10(f_GHz) + 92.45
     = 20*log10(1700) + 20*log10(2.0) + 92.45
     = 64.61 + 6.02 + 92.45
     = 163.08 dB
```

| 參數 | 值 | 單位 | 計算 / 來源 |
|------|-----|------|-------------|
| **FSPL** | **163.1** | **dB** | @1700 km, 2.0 GHz |
| 大氣吸收損耗 (L_atm) | 0.5 | dB | ITU-R P.676, S-band 仰角 10°, dry air |
| 降雨衰減 (L_rain) | 0.3 | dB | ITU-R P.618, S-band, 0.01% exceedance, Region 3 subtropical |
| 閃爍損耗 (L_scint) | 0.5 | dB | ITU-R P.531, 仰角 10°, S-band |
| 極化損耗 (L_pol) | 0.3 | dB | RHCP/Linear mismatch (UE 線性 vs SAT 圓極化) |
| **傳播總損耗** | **164.7** | **dB** | 163.1 + 0.5 + 0.3 + 0.5 + 0.3 |

### 3.3 接收端（衛星端）

| 參數 | 值 | 單位 | 計算 / 來源 |
|------|-----|------|-------------|
| Rx Antenna Gain (G_rx) | +8.0 | dBi | S-band patch array（EnduroSat / ISISPACE 規格） |
| 指向損耗 (L_point) | 1.0 | dB | ADCS +-3° 指向精度 vs HPBW +-30°，保守取值 |
| 饋線 / 連接器損耗 (L_feed) | 0.5 | dB | 短饋線 (<10 cm PCB trace + SMA) |
| **有效接收增益** | **+6.5** | **dBi** | 8.0 - 1.0 - 0.5 |

### 3.4 系統雜訊溫度（從 NF 推導 — v1.1 修正重點）

**Friis 雜訊溫度公式：**
```
T_component = T_0 * (F - 1)    where T_0 = 290 K, F = 10^(NF_dB/10)
```

**LNA: ADL5523ACPZ-R7**
```
NF_LNA = 1.5 dB  (datasheet worst case @2 GHz，保守值)
F_LNA  = 10^(1.5/10) = 10^0.15 = 1.413
T_LNA  = 290 * (1.413 - 1) = 290 * 0.413 = 119.8 K ≈ 120 K
LNA Gain = 15 dB → G_LNA = 10^(15/10) = 31.62
```

**天線雜訊溫度（T_ant, 仰角 10° worst case）：**
```
T_ant ≈ T_sky + T_ground_spillover
T_sky  ≈ 20 K  (S-band cosmic + atmospheric, 仰角 10°)
T_spillover ≈ 80 K  (side/back lobe 接收地球熱輻射 ~290 K, 受天線效率加權)
T_ant  = 20 + 80 = 100 K  (worst case estimate for 仰角 10°)
```

> **來源：** ITU-R P.372-16 (Radio Noise)；S-band 天空溫度 ~10-30 K；  
> 地球背景輻射 290 K 透過 antenna sidelobe coupling 貢獻 ~60-100 K @低仰角。

**後端雜訊溫度（T_backend）：**
```
NF_mixer ≈ 10 dB (LT5512, 保守值)
F_mixer  = 10^(10/10) = 10
T_mixer  = 290 * (10 - 1) = 290 * 9 = 2,610 K

NF_filter ≈ 1.5 dB (BPF insertion loss, treated as NF)
F_filter = 10^(1.5/10) = 1.413
T_filter = 290 * (1.413 - 1) = 120 K
```

**Friis 級聯公式（LNA 為第一級）：**
```
T_sys = T_ant + T_LNA + T_filter/G_LNA + T_mixer/(G_LNA * G_filter)

其中 G_filter ≈ 0.71 (insertion loss 1.5 dB → gain = 10^(-1.5/10) = 0.708)

T_sys = 100 + 120 + 120/31.62 + 2610/(31.62 * 0.708)
      = 100 + 120 + 3.8 + 116.6
      = 340.4 K
```

> **等等 — 這比 300 K 高？** 是的。因為 mixer NF 10 dB 很高，即使被 LNA 壓制仍有顯著貢獻。  
> 但注意：透明轉發架構中，實際 T_sys 計算到 mixer 後的 IF 段即可，PA 雜訊不計入接收鏈。

**保守設計值：T_sys = 340 K**

> **v1.0 vs v1.1 比較：**  
> - v1.0: T_sys = 300 K（猜測值）  
> - v1.1: T_sys = 340 K（NF 推導，Friis 級聯）  
> - 差異：10*log10(340/300) = 0.55 dB（G/T 劣化 0.55 dB）  
> - **結論：** 原始 300 K 偶然接近但方向相反（實際更高），v1.1 修正後更保守。

### 3.5 G/T 計算

```
G/T = G_rx_effective - 10*log10(T_sys)
    = 6.5 - 10*log10(340)
    = 6.5 - 25.31
    = -18.81 dB/K
```

| 參數 | 值 | 單位 | 計算 |
|------|-----|------|------|
| G_rx (effective) | +6.5 | dBi | 8.0 - 1.0 - 0.5 |
| T_sys | 340 | K | Friis cascade 推導 |
| 10*log10(T_sys) | 25.31 | dB(K) | |
| **G/T** | **-18.8** | **dB/K** | 6.5 - 25.31 |

### 3.6 C/N_0（載噪比密度）

```
C/N_0 = EIRP - L_total + G/T - k

其中：
  EIRP   = -7.0 dBW
  L_total = 164.7 dB  (FSPL + 大氣 + 雨衰 + 閃爍 + 極化)
  G/T    = -18.8 dB/K
  k      = -228.6 dBW/K/Hz  (Boltzmann constant)

C/N_0 = -7.0 - 164.7 + (-18.8) - (-228.6)
      = -7.0 - 164.7 - 18.8 + 228.6
      = 38.1 dB-Hz
```

| 參數 | 值 | 單位 |
|------|-----|------|
| **C/N_0** | **38.1** | **dB-Hz** |

### 3.7 Eb/No 計算

```
Eb/No = C/N_0 - 10*log10(R_b)

其中 R_b = 100 bps（IoT-NTN narrowband data rate）

Eb/No = 38.1 - 10*log10(100)
      = 38.1 - 20.0
      = 18.1 dB
```

### 3.8 Link Margin 計算

| 參數 | 值 | 單位 | 備注 |
|------|-----|------|------|
| Received Eb/No | 18.1 | dB | 計算值 |
| Required Eb/No (theoretical) | 4.0 | dB | QPSK 1/2, BER 1e-6, AWGN |
| Implementation Margin | 2.0 | dB | **v1.1 新增：** Doppler +-50 kHz 補償、振盪器相位雜訊、ADC 量化雜訊 |
| **Required Eb/No (total)** | **6.0** | **dB** | 4.0 + 2.0 |
| **Link Margin** | **+12.1** | **dB** | 18.1 - 6.0 |

---

## 4. Link Budget 彙總表（UL: UE -> Satellite, 仰角 10°）

| # | 參數 | 值 | 單位 | 備注 |
|---|------|-----|------|------|
| **Tx (UE)** | | | | |
| 1 | UE Tx Power | +23.0 | dBm | 3GPP Power Class 3 |
| 2 | UE Tx Power | -7.0 | dBW | 23 - 30 |
| 3 | UE Antenna Gain | 0.0 | dBi | Omnidirectional |
| 4 | UE Feed Loss | 0.0 | dB | Handheld, no feed |
| 5 | **EIRP** | **-7.0** | **dBW** | 2 + 3 - 4 |
| **Path Loss** | | | | |
| 6 | FSPL (@1700 km, 2 GHz) | 163.1 | dB | 20log(1700)+20log(2)+92.45 |
| 7 | Atmospheric Absorption | 0.5 | dB | ITU-R P.676 |
| 8 | Rain Attenuation | 0.3 | dB | ITU-R P.618, 0.01% |
| 9 | Scintillation Loss | 0.5 | dB | ITU-R P.531 |
| 10 | Polarization Mismatch | 0.3 | dB | Linear-to-RHCP |
| 11 | **Total Path Loss** | **164.7** | **dB** | sum(6:10) |
| **Rx (Satellite)** | | | | |
| 12 | Rx Antenna Gain | +8.0 | dBi | S-band patch array |
| 13 | Pointing Loss | 1.0 | dB | ADCS +-3° |
| 14 | Feed / Connector Loss | 0.5 | dB | PCB trace + SMA |
| 15 | **Effective Rx Gain** | **+6.5** | **dBi** | 12 - 13 - 14 |
| **Noise** | | | | |
| 16 | T_ant (仰角 10°) | 100 | K | Sky 20K + spillover 80K |
| 17 | T_LNA (NF=1.5dB) | 120 | K | 290*(10^0.15 - 1) |
| 18 | T_backend (referred to LNA input) | 120.4 | K | Friis cascade through BPF+Mixer |
| 19 | **T_sys** | **340** | **K** | 100 + 120 + 120.4 |
| 20 | 10*log10(T_sys) | 25.3 | dB(K) | |
| 21 | **G/T** | **-18.8** | **dB/K** | 15 - 20 |
| 22 | Boltzmann Constant (k) | -228.6 | dBW/K/Hz | |
| **C/N_0** | | | | |
| 23 | **C/N_0** | **38.1** | **dB-Hz** | 5 - 11 + 21 - 22 |
| **Eb/No & Margin** | | | | |
| 24 | Data Rate (R_b) | 100 | bps | IoT-NTN |
| 25 | 10*log10(R_b) | 20.0 | dB(Hz) | |
| 26 | **Received Eb/No** | **18.1** | **dB** | 23 - 25 |
| 27 | Required Eb/No (theoretical) | 4.0 | dB | QPSK 1/2, BER 1e-6, AWGN |
| 28 | Implementation Margin | 2.0 | dB | Doppler, oscillator, quantization |
| 29 | **Required Eb/No (total)** | **6.0** | **dB** | 27 + 28 |
| 30 | **Link Margin** | **+12.1** | **dB** | 26 - 29 |

---

## 5. Zenith Case 驗算（仰角 90°, d = 500 km）

快速交叉驗算，確認 best case 合理性：

```
FSPL = 20*log10(500) + 20*log10(2.0) + 92.45
     = 53.98 + 6.02 + 92.45
     = 152.45 dB ≈ 152.5 dB

T_ant (zenith) ≈ 40 K  (低仰角 spillover 大幅降低)
T_sys (zenith) = 40 + 120 + 120.4/31.62 ≈ 40 + 120 + 3.8 + 116.6
              → 重算：T_sys = 40 + 120 + 3.8 + 116.6 = 280.4 K ≈ 280 K

Total Path Loss (zenith) = 152.5 + 0.1 + 0.1 + 0.1 + 0.3 = 153.1 dB
  (大氣、雨衰、閃爍在天頂大幅降低)

G/T (zenith) = 6.5 - 10*log10(280) = 6.5 - 24.47 = -17.97 ≈ -18.0 dB/K

C/N_0 = -7.0 - 153.1 + (-18.0) - (-228.6)
      = -7.0 - 153.1 - 18.0 + 228.6
      = 50.5 dB-Hz

Eb/No = 50.5 - 20.0 = 30.5 dB
Link Margin = 30.5 - 6.0 = +24.5 dB
```

| Case | Slant Range | FSPL | T_sys | G/T | C/N_0 | Eb/No | Margin |
|------|-------------|------|-------|-----|-------|-------|--------|
| **Worst (10°)** | 1,700 km | 163.1 dB | 340 K | -18.8 dB/K | 38.1 dB-Hz | 18.1 dB | **+12.1 dB** |
| **Best (90°)** | 500 km | 152.5 dB | 280 K | -18.0 dB/K | 50.5 dB-Hz | 30.5 dB | **+24.5 dB** |

> 兩個 case 都有充裕 margin (>3 dB)，100 bps IoT-NTN 在 S-band 透明轉發架構下可行性確認。

---

## 6. Implementation Margin 明細（v1.1 新增）

| 損耗來源 | 估算值 | 單位 | 說明 |
|---------|--------|------|------|
| Doppler 頻率偏移殘差 | 0.5 | dB | LEO 500km, v=7.5km/s, max Doppler +-50kHz @2GHz; UE GNSS 預補償後殘差 ~+-1kHz |
| 振盪器相位雜訊 | 0.3 | dB | TCXO +-2.5 ppm @2GHz = +-5kHz; 與 Doppler 殘差疊加 |
| ADC 量化雜訊 | 0.2 | dB | 12-bit ADC, SQNR 74 dB, 可忽略但保守計入 |
| 濾波器群延遲失真 | 0.2 | dB | BPF passband ripple 造成的 ISI |
| Channel estimation error | 0.3 | dB | Pilot-based estimation imperfection |
| 其他 (connector aging, thermal) | 0.5 | dB | 保守預留 |
| **Total Implementation Margin** | **2.0** | **dB** | |

**Doppler 偏移詳細計算：**
```
f_Doppler = f_c * (v / c) * cos(theta)
          = 2e9 * (7500 / 3e8) * cos(0°)    [worst case: 直接接近]
          = 2e9 * 2.5e-5
          = 50,000 Hz = +-50 kHz

Doppler rate: ~800 Hz/s (LEO 500 km)
```

> 3GPP Rel-17 NTN 規定 UE 需使用 GNSS 做 pre-compensation，補償後殘差 < +-1.5 kHz。  
> 衛星端 bent-pipe 不做補償，殘差由地面 gNB 處理。

---

## 7. 敏感度分析

若關鍵參數偏移，Link Margin 如何變化（基於 worst case 12.1 dB baseline）：

| 參數變化 | Margin 變化 | 新 Margin | 是否仍 > 3 dB |
|---------|------------|-----------|--------------|
| LNA NF 劣化至 2.0 dB | -0.4 dB | +11.7 dB | YES |
| T_ant 升至 150 K | -0.5 dB | +11.6 dB | YES |
| Antenna Gain 降至 6 dBi | -2.0 dB | +10.1 dB | YES |
| Tx Power 降至 20 dBm | -3.0 dB | +9.1 dB | YES |
| 所有上述同時發生 | -5.9 dB | +6.2 dB | YES |
| 所有上述 + data rate 1 kbps | -5.9 -10 dB | -3.8 dB | **NO** |

> **結論：** 100 bps 設計對元件退化有極高容忍度。若升至 1 kbps 則需要更高增益天線或更大發射功率。

---

## 8. Assumptions & Caveats

1. **UE 為 3GPP Power Class 3 (+23 dBm)**，若為低功耗 IoT 裝置 (+14 dBm)，margin 降低 9 dB 但仍有 +3.1 dB。
2. **T_ant = 100 K** 為仰角 10° 保守估計；實測值可能更低（60-80 K），可改善 G/T 0.5-1.0 dB。
3. **Bent-pipe 架構**：衛星端不做基帶解碼，雜訊為端到端累積。本 budget 僅計算 UE->SAT 上行段。完整 end-to-end budget 需加入 SAT->gNB 下行段（feeder link），但 feeder link 通常 margin 充足（大型地面站 G/T > 20 dB/K）。
4. **未計入 feeder link degradation**：Phase B 需補上 end-to-end cascade analysis。
5. **Coding gain**：QPSK 1/2 的 4 dB required Eb/No 已包含 turbo/LDPC coding gain。裸 QPSK uncoded 需 ~10.5 dB @BER 1e-6。

---

## 9. 結論與 Action Items

| 結論 | 說明 |
|------|------|
| **Link 可行性** | 100 bps IoT-NTN uplink, QPSK 1/2, worst case margin **+12.1 dB** >> 3 dB 門檻 |
| **T_sys 修正** | 從 NF 推導 T_sys = 340 K（v1.0 的 300 K 偏樂觀，修正後 margin 僅減少 ~0.6 dB） |
| **Implementation Margin** | 2 dB 已計入 Doppler、振盪器、ADC 等實際損耗 |
| **Professor Challenger 問題 1** | RESOLVED -- T_sys 從 NF 推導，G/T = -18.8 dB/K |
| **Professor Challenger 問題 2** | RESOLVED -- Implementation Margin 2 dB 已獨立列出 |

### Action Items for Sprint 2
- [ ] 完成 SAT->gNB feeder link budget（下行段）
- [ ] End-to-end cascade C/N analysis
- [ ] 確認 UE power class（Class 3 vs IoT power-saving class）
- [ ] ADL5523 實測 NF @2 GHz（驗證 datasheet 1.5 dB）
- [ ] 天線 pattern 量測 → 修正 T_ant 與 pointing loss

---

*TASA-NTN-3U / Sprint 1 / Phase A / SRR*
