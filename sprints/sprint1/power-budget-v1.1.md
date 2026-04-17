# TASA-NTN-3U Power Budget v1.1

| 項目 | 內容 |
|------|------|
| **文件版本** | v1.1（修正 eclipse fraction、DoD 計算、新增完整能量收支） |
| **前版** | v1.0（Professor Challenger 退回：eclipse 未計算、DoD 矛盾） |
| **專案** | TASA-NTN-3U, 3U CubeSat, 500 km SSO, S-band n236 NTN 透明轉發 |
| **Sprint** | Sprint 1 — Phase A, SRR milestone |
| **作者** | Systems Engineer |
| **日期** | 2026-04-15 |

---

## 1. 軌道週期分析

### 1.1 軌道週期計算

**基本參數：**

| 參數 | 符號 | 數值 |
|------|------|------|
| 地球半徑 | R_e | 6371 km |
| 軌道高度 | h | 500 km |
| 軌道半徑 | r = R_e + h | 6871 km |
| 地球引力參數 | mu | 3.986 x 10^14 m^3/s^2 |

**軌道週期公式：**

```
T = 2 * pi * sqrt(r^3 / mu)
T = 2 * pi * sqrt((6.871 x 10^6)^3 / (3.986 x 10^14))
T = 2 * pi * sqrt(3.244 x 10^20 / 3.986 x 10^14)
T = 2 * pi * sqrt(8.138 x 10^5)
T = 2 * pi * 902.1
T = 5668 s = 94.5 min
```

### 1.2 Eclipse Fraction 計算

**幾何推導（最差情況 beta = 0 deg）：**

當軌道平面通過太陽方向（beta angle = 0 deg），衛星經歷最長 eclipse。此為 SSO 在夏至/冬至附近某些 LTAN 的最差情況。

地球遮蔽半角 rho：

```
rho = arcsin(R_e / r)
rho = arcsin(6371 / 6871)
rho = arcsin(0.9273)
rho = 68.01 deg
```

Eclipse fraction（worst case, beta = 0 deg）：

```
f_eclipse = 2 * rho / 360
f_eclipse = 2 * 68.01 / 360
f_eclipse = 37.8%
```

**替代公式驗證：**

```
f_eclipse = (1/pi) * arccos(sqrt(h^2 + 2*R_e*h) / (R_e + h))
         = (1/pi) * arccos(sqrt((500)^2 + 2*6371*500) / 6871)
         = (1/pi) * arccos(sqrt(6621000) / 6871)
         = (1/pi) * arccos(2573.1 / 6871)
         = (1/pi) * arccos(0.3744)
         = (1/pi) * 68.01 deg
         = 37.8%
```

兩種公式結果一致，驗證正確。

### 1.3 Sunlit / Eclipse 時間

| 項目 | 公式 | 數值 |
|------|------|------|
| 軌道週期 | T | **94.5 min** |
| Eclipse fraction | f_eclipse | **37.8%** |
| Sunlit fraction | 1 - f_eclipse | **62.2%** |
| Eclipse 時間 | T x f_eclipse = 94.5 x 0.378 | **35.7 min** |
| Sunlit 時間 | T x (1 - f_eclipse) = 94.5 x 0.622 | **58.8 min** |

> **Note:** 37.8% 為幾何最差情況（beta = 0 deg）。SSO 的年平均 eclipse fraction 約 33-36%。本文件使用 37.8% 作為設計裕度。

---

## 2. 太陽能板分析

### 2.1 BOL 功率

| 參數 | 數值 | 備註 |
|------|------|------|
| 太陽能板 BOL 功率 | 5.0 W | 3U body-mounted + deployable |
| MPPT 效率 | 90% | GomSpace NanoPower P31u 規格 |
| Sunlit fraction（worst case） | 62.2% | 見 Section 1.3 |

**軌道平均可用功率（BOL）：**

```
P_avg_BOL = P_BOL x f_sunlit x eta_MPPT
P_avg_BOL = 5.0 x 0.622 x 0.90
P_avg_BOL = 2.80 W
```

### 2.2 EOL 降效

| 參數 | 數值 | 備註 |
|------|------|------|
| 年降效率 | 3%/yr | 輻射 + 熱循環（LEO 典型值） |
| 任務壽命 | 3 年 | |
| EOL 降效因子 | (1 - 0.03)^3 = 0.913 | |
| EOL 面板功率 | 5.0 x 0.913 = 4.56 W | |

**軌道平均可用功率（EOL）：**

```
P_avg_EOL = P_EOL x f_sunlit x eta_MPPT
P_avg_EOL = 4.56 x 0.622 x 0.90
P_avg_EOL = 2.56 W
```

### 2.3 太陽能板功率彙總

| 條件 | 面板功率 (W) | 軌道平均功率 (W) |
|------|-------------|-----------------|
| BOL worst-case | 5.00 | 2.80 |
| EOL worst-case | 4.56 | 2.56 |

---

## 3. 子系統功耗表

### 3.1 各子系統功耗

| 子系統 | Standby (W) | Active (W) | 備註 |
|--------|-------------|------------|------|
| OBC | 2.0 | 4.0 | Standby: 待機監控; Active: SDR 基帶處理 |
| ADCS | 0.5 | 0.5 | S-band 寬波束天線，指向需求寬鬆 (+-3 deg) |
| TT&C UHF (Rx) | 0.5 | -- | 常時接收 |
| TT&C UHF (Tx) | -- | 2.0 | 僅接觸窗口發射 |
| S-band 酬載 | 0 (OFF) | 4.0 | 僅接觸窗口 active，含 LNA+PA+Mixer |
| 溫控加熱器 | 0 (sunlit) | 0.5 | 僅 eclipse 期間啟動 |

### 3.2 三種運行模式功耗

#### Mode A：Nominal Sunlit（日照段，無接觸窗口）

| 子系統 | 功耗 (W) |
|--------|---------|
| OBC (standby) | 2.0 |
| ADCS | 0.5 |
| TT&C UHF (Rx) | 0.5 |
| S-band 酬載 | 0 |
| 溫控加熱器 | 0 |
| **合計** | **3.0** |

#### Mode B：Nominal Eclipse（陰影段，無接觸窗口）

| 子系統 | 功耗 (W) |
|--------|---------|
| OBC (standby) | 2.0 |
| ADCS | 0.5 |
| TT&C UHF (Rx) | 0.5 |
| S-band 酬載 | 0 |
| 溫控加熱器 | 0.5 |
| **合計** | **3.5** |

#### Mode C：Contact Window（接觸窗口，酬載全功率運作）

| 子系統 | 功耗 (W) |
|--------|---------|
| OBC (active) | 4.0 |
| ADCS | 0.5 |
| TT&C UHF (Tx) | 2.0 |
| S-band 酬載 | 4.0 |
| 溫控加熱器 | 0 (假設日照段) |
| **合計** | **10.5** |

> **關鍵發現：** Contact window 功耗 10.5 W 遠超太陽能板 BOL 輸出 5.0 W。差額 5.5 W 必須由電池補足。

---

## 4. DoD 計算（修正）

### 4.1 問題 3b 回覆：v1.0 版 DoD = 2.4% 為何不正確

**v1.0 版計算（錯誤）：**
```
假設：功耗 5 W x 4 min = 0.333 Wh
DoD = 0.333 / 10 = 3.3%
舊版文件又寫 2.4%，兩個數字互相矛盾
```

**錯誤原因分析：**

1. **舊版 2.4% 的可能來源：** 僅計算 S-band 酬載 RF 鏈路自身功耗（約 3.6 W），未包含 OBC 由 standby 切換至 active 增加的 2 W 及 TT&C 發射功率。計算方式可能為 3.6 x 4/60 / 10 = 2.4%。
2. **舊版 3.3% 的來源：** 假設 「5 W 功耗 x 4 min」，但 5 W 既非子系統合計（10.5 W），也不是電池放電量（5.5 W）。該數字恰好等於太陽能板 BOL 輸出，混淆了發電量與耗電量。

**兩個數字都不正確。**

### 4.2 正確的 DoD 計算

**場景 A：Contact window 在日照段（typical case）**

接觸窗口總功耗 = 10.5 W，太陽能板同時供電 5.0 W（BOL），電池補足差額：

```
P_deficit = P_contact - P_solar = 10.5 - 5.0 = 5.5 W
E_discharge = P_deficit x t_contact = 5.5 x (4/60) = 0.367 Wh
DoD = E_discharge / E_battery = 0.367 / 10.0 = 3.67%
```

**場景 B：Contact window 在陰影段（worst case）**

無太陽能輸入，且需加熱器：

```
P_total = P_contact + P_heater = 10.5 + 0.5 = 11.0 W
E_discharge = 11.0 x (4/60) = 0.733 Wh
DoD = 0.733 / 10.0 = 7.33%
```

### 4.3 DoD 彙整

| 場景 | 電池放電功率 (W) | 時間 (min) | 放電量 (Wh) | DoD (%) |
|------|----------------|-----------|------------|---------|
| Contact (日照段, BOL) | 5.5 | 4 | 0.367 | **3.67%** |
| Contact (日照段, EOL) | 10.5 - 4.56 = 5.94 | 4 | 0.396 | **3.96%** |
| Contact (陰影段, BOL) | 11.0 | 4 | 0.733 | **7.33%** |
| 純 Eclipse (無 contact) | 3.5 | 35.7 | 2.082 | **20.8%** |
| Eclipse + Contact (worst) | 見下方計算 | -- | 2.582 | **25.8%** |

**Worst case eclipse + contact（最差情況）：**

```
Contact in eclipse: 11.0 W x 4 min = 0.733 Wh
Remaining eclipse (no contact): 3.5 W x (35.7 - 4) min = 3.5 x 31.7/60 = 1.849 Wh
Total eclipse drain = 0.733 + 1.849 = 2.582 Wh
DoD = 2.582 / 10.0 = 25.8%
```

> **評估：** DoD 25.8% 在 Li-ion 電池可接受範圍內（一般建議 DoD < 30% 以達 >10,000 cycle 壽命）。然而，能量收支平衡有問題（見 Section 5）。

---

## 5. Power Balance 驗證

### 5.1 每圈能量收支（BOL, worst-case eclipse）

**假設：每圈有一次 4 min contact window，發生在日照段。**

#### 發電量

```
E_generated = P_BOL x eta_MPPT x t_sunlit
E_generated = 5.0 x 0.90 x (58.8/60)
E_generated = 4.41 Wh
```

#### 耗電量

| 模式 | 功耗 (W) | 時間 (min) | 能量 (Wh) |
|------|---------|-----------|----------|
| Nominal sunlit (無 contact) | 3.0 | 58.8 - 4 = 54.8 | 3.0 x 54.8/60 = **2.740** |
| Contact window | 10.5 | 4.0 | 10.5 x 4/60 = **0.700** |
| Nominal eclipse | 3.5 | 35.7 | 3.5 x 35.7/60 = **2.082** |
| **合計** | | **94.5** | **5.522** |

#### 能量收支

```
Balance = E_generated - E_consumed
Balance = 4.41 - 5.52
Balance = -1.11 Wh/orbit   <<<  負值！
```

### 5.2 每圈能量收支（EOL, worst-case eclipse）

```
E_generated_EOL = 4.56 x 0.90 x (58.8/60) = 4.02 Wh
Balance_EOL = 4.02 - 5.52 = -1.50 Wh/orbit   <<<  更嚴重！
```

### 5.3 問題診斷

| 項目 | BOL | EOL |
|------|-----|-----|
| 每圈發電量 | 4.41 Wh | 4.02 Wh |
| 每圈耗電量 | 5.52 Wh | 5.52 Wh |
| 收支平衡 | **-1.11 Wh** | **-1.50 Wh** |
| 軌道平均發電 | 2.80 W | 2.56 W |
| 軌道平均耗電 | 5.52/(94.5/60) = 3.51 W | 3.51 W |

**結論：軌道平均耗電（3.51 W）超過軌道平均發電（BOL 2.80 W / EOL 2.56 W），每圈虧損 1.1-1.5 Wh。電池 10 Wh 容量在 7-9 圈後將完全耗盡。此設計無法維持穩態運行。**

### 5.4 Eclipse 期間電池支撐能力

```
Eclipse 功耗 = 3.5 W
Eclipse 時間 = 35.7 min
Eclipse 能量需求 = 3.5 x 35.7/60 = 2.08 Wh
電池 10 Wh 可支撐 = 10.0/3.5 x 60 = 171 min >> 35.7 min   ✓ OK
```

> Eclipse 支撐能力充足（裕度 4.8 倍），但問題在於日照段發電不足以回充 eclipse 放電量加上日常消耗。

---

## 6. 設計裕度分析與修正建議

### 6.1 問題根源

```
軌道平均發電: 2.80 W (BOL) / 2.56 W (EOL)
軌道平均耗電: 3.51 W
缺口:          0.71 W (BOL) / 0.95 W (EOL)
```

37.8% eclipse fraction 意味著太陽能板有 37.8% 時間無法發電，但所有子系統持續耗電。5 W 面板功率在 worst-case SSO 下只能提供 2.80 W 軌道平均功率，不足以支撐 3.51 W 平均負載。

### 6.2 修正方案（SRR 前須決定）

| 方案 | 改動 | 效果 | 風險 |
|------|------|------|------|
| **A. 增大太陽能板** | BOL 提升至 7 W（加裝 deployable panel） | P_avg = 3.92 W > 3.51 W，收支轉正 | 質量 +200g，成本 +$1,500 |
| **B. 降低待機功耗** | OBC standby 降至 1.0 W（選低功耗 MCU） | 軌道平均耗電降至 2.84 W | 犧牲運算能力，SDR 基帶能力受限 |
| **C. 減少接觸窗口功耗** | S-band PA 降至 0.5 W（降低 EIRP） | Contact 功耗 7.0 W，平均耗電降至 3.28 W | Link margin 減少 ~6 dB |
| **D. 增大電池容量** | 20 Wh Li-ion | 不解決穩態虧損，僅延長存活時間 | 治標不治本 |
| **E. 組合方案（建議）** | 太陽能板 6 W + OBC standby 1.5 W | P_avg = 3.36 W, 耗電 3.18 W, 正裕度 | 最佳 trade-off |

### 6.3 方案 E 驗算

```
太陽能板 BOL: 6.0 W
OBC standby: 1.5 W → Mode A = 2.5 W, Mode B = 3.0 W
Contact: OBC active 4.0 + ADCS 0.5 + TTC 2.0 + S-band 4.0 = 10.5 W (unchanged)

E_gen = 6.0 x 0.90 x (58.8/60) = 5.29 Wh
E_con = 2.5 x (54.8/60) + 10.5 x (4/60) + 3.0 x (35.7/60)
      = 2.283 + 0.700 + 1.785 = 4.77 Wh
Balance = 5.29 - 4.77 = +0.52 Wh/orbit  ✓ 正值

EOL: E_gen = 5.47 x 0.90 x (58.8/60) = 4.83 Wh
Balance_EOL = 4.83 - 4.77 = +0.06 Wh/orbit  ✓ 勉強正值（裕度僅 1.3%）
```

> **建議：** 方案 E 在 EOL 裕度極薄。若要保守設計，太陽能板應提升至 6.5-7.0 W BOL，確保 EOL 仍有 >= 5% 正裕度。

---

## 7. 結論

### 7.1 Professor Challenger 退回問題回覆

| 問題 | 回覆 |
|------|------|
| **3a: Eclipse fraction** | SSO 500 km worst case (beta=0): **f_eclipse = 37.8%**, eclipse duration = **35.7 min/orbit** |
| **3b: DoD 矛盾** | v1.0 的 2.4% 和 3.3% **均不正確**。正確值：日照段 contact DoD = **3.67%** (BOL)；最差情況 eclipse+contact DoD = **25.8%** |
| **3c: Power Budget** | 完整計算見 Section 1-5。**發現重大問題：current design 每圈虧損 1.11 Wh (BOL)**，無法維持穩態。需在 SRR 前修正太陽能板功率或降低子系統功耗。 |

### 7.2 設計狀態

```
                                  當前設計      建議修正（方案 E）
太陽能板 BOL                      5.0 W         6.0 W
軌道平均發電 (BOL)                2.80 W        3.36 W
軌道平均耗電                      3.51 W        3.18 W
每圈能量收支 (BOL)                -1.11 Wh      +0.52 Wh
每圈能量收支 (EOL)                -1.50 Wh      +0.06 Wh
Eclipse DoD (per orbit)           20.8%         17.8%
Worst case DoD (eclipse+contact)  25.8%         22.8%
狀態                              NOT OK        MARGINAL
```

### 7.3 Action Items（SRR 前必須完成）

1. **[CRITICAL]** 決定太陽能板升級方案（6.0-7.0 W BOL），更新 EPS 規格與 BOM
2. **[CRITICAL]** 確認 OBC standby 功耗是否可降至 1.5 W，與 OBC vendor 確認
3. **[HIGH]** EOL 電池容量衰退分析（Li-ion 3 年 LEO 約 80% 容量保持 → 有效容量 8 Wh）
4. **[HIGH]** 加入電池 EOL 容量至 DoD worst case 重新計算（8 Wh 下 DoD 升至 32.3%，接近上限）
5. **[MEDIUM]** 考慮 duty cycling 策略（非每圈都啟動酬載），降低平均耗電

---

## 附錄 A：計算常數與假設

| 項目 | 數值 | 來源 |
|------|------|------|
| R_e | 6371 km | WGS-84 |
| mu | 3.986 x 10^14 m^3/s^2 | GM_earth |
| h | 500 km | 任務需求 |
| Beta angle (worst case) | 0 deg | SSO 幾何最差情況 |
| 太陽能板降效率 | 3%/yr | LEO 典型值 (GaAs triple-junction) |
| MPPT 效率 | 90% | GomSpace P31u datasheet |
| 電池容量 | 10 Wh | GomSpace P31u spec |
| 接觸窗口 | 4 min/pass | SSO 500 km 地面站仰角 > 10 deg |
| Li-ion cycle DoD 上限 | 30% | >10,000 cycles 壽命需求 |

## 附錄 B：v1.0 vs v1.1 變更對照

| 項目 | v1.0 | v1.1 |
|------|------|------|
| Eclipse fraction | 未計算 | 37.8% (worst case) |
| Eclipse duration | 未計算 | 35.7 min |
| Sunlit duration | 未計算 | 58.8 min |
| DoD per contact (sunlit) | 2.4% / 3.3% (矛盾) | 3.67% (BOL) |
| DoD worst case | 未計算 | 25.8% |
| 每圈能量收支 | 未計算 | -1.11 Wh (BOL) |
| 設計問題揭露 | 無 | 負能量收支，需升級太陽能板 |
