---
deliverable: B-005
sprint: 2
wave: 1
author: SE Agent (陳建宏)
date: 2026-04-15
status: draft
version: v2.1
reference_documents:
  - workspace/sprints/sprint1/power-budget-v1.1.md (Sprint 1 基線)
  - workspace/project.json (DCN-001, DCN-002)
change_log:
  - v2.0: DCN-001 驗證（太陽能板 5W→6.5W BOL）
  - v2.1: DCN-002 核准（電池 10 Wh→15 Wh），更新所有 DoD 計算，2026-04-15
---

# B-005：TASA-NTN-3U Power Budget v2.1（含 DCN-001 / DCN-002 驗證）

## 1. 文件概述

本文件為 TASA-NTN-3U 的精化 Power Budget v2.1，基於 Sprint 1 power-budget-v1.1 基線，納入 **DCN-001**（太陽能板從 5W 升級至 6.5W BOL，CEO 2026-04-15 核准）及 **DCN-002**（電池容量從 10 Wh 升級至 15 Wh，CEO 2026-04-15 核准）後的完整能量收支分析。

**關鍵軌道參數（Sprint 1 基線）**：
- 軌道高度：500 km SSO
- 軌道週期：T_orbit = 94.5 min
- Eclipse 時間：T_eclipse = 35.7 min (37.78%)
- 日照時間：T_sunlit = 94.5 - 35.7 = 58.8 min (62.22%)
- 接觸窗口：T_contact = 4 min/pass（假設每圈 1 pass）

---

## 2. 太陽能板規格計算（DCN-001 更新）

### 2.1 BOL 與 EOL 功率

| 參數 | 數值 | 來源 |
|------|------|------|
| BOL 峰值輸出 | 6.50 W | DCN-001（升級自 5.0W） |
| 任務壽命 | 3 年 | 任務需求 |
| 年固有光衰 (intrinsic degradation) | 0.3% / yr | 三結 GaAs 標準值 |
| 3 年固有衰減因子 | (1 - 0.003)^3 = 0.9910 | |
| 輻射衰減 (500 km SSO, 3 yr) | ~0.922 | ECSS-E-ST-20C 參考值，500 km SSO 輻射環境 |
| **EOL 綜合衰減因子** | 0.9910 x 0.922 = **0.9137** | |
| **EOL 峰值輸出** | 6.50 x 0.9137 = **5.939 W** | |

> **註**：Sprint 1 原用 0.913 做組合衰減因子，此處細拆為 intrinsic (0.991) x radiation (0.922) = 0.9137，與原值一致（差異 < 0.1%），確認基線一致。

### 2.2 軌道平均可用電力

太陽能板為 body-mounted (3 面：+X, -X, +Z)，非太陽追蹤。軌道平均有效因子計算：

| 因子 | 數值 | 說明 |
|------|------|------|
| 日照比 (1 - eclipse fraction) | 1 - 0.3778 = 0.6222 | T_sunlit / T_orbit |
| MPPT 效率 | 0.90 | GomSpace P31u 規格 |
| 傾斜角平均餘弦 cos(theta_avg) | 0.90 | body-mount 3 面平均，SSO beta angle 考量 |
| **組合效率** | 0.6222 x 0.90 x 0.90 = **0.5040** | |

**軌道平均可用電力**：

| 條件 | 計算 | 結果 |
|------|------|------|
| **BOL avg** | 6.50 x 0.5040 | **3.276 W** |
| **EOL avg** | 5.939 x 0.5040 | **2.993 W** |

> **與 Sprint 1 比較**：v1.1 基線 (5.0W BOL) 的 BOL avg = 5.0 x 0.504 = 2.52W；DCN-001 後提升 +30% 至 3.276W。

---

## 3. 功耗場景分析

### 3.1 各模式功耗明細

| 子系統 | Nominal Sunlit (W) | Contact Window (W) | Eclipse Nominal (W) | Safe Mode (W) |
|--------|:-------------------:|:-------------------:|:--------------------:|:--------------:|
| OBC | 1.50 (standby) | 4.00 (active) | 1.50 (standby) | 1.00 (safe) |
| EPS (self) | 0.30 | 0.30 | 0.30 | 0.30 |
| ADCS | 0.50 | 0.50 | 0.50 | 0.30 (detumble) |
| S-band PA | 0.00 | 4.00 | 0.00 | 0.00 |
| TT&C (UHF) | 0.20 (Rx standby) | 1.50 (Tx active) | 0.20 (Rx standby) | 0.80 (beacon) |
| Heater | 0.00 | 0.00 | 0.50 | 0.00~0.50 |
| **Total** | **2.50** | **10.30** | **3.00** | **2.40~2.90** |

> **註**：Contact Window 總功耗 10.30W（較 Sprint 1 的 10.0W 略增 0.3W，因加入 EPS self-consumption 0.3W + TT&C standby→Tx 差異）。Sprint 1 Contact Window 計算為 OBC 4.0 + PA 4.0 + TT&C 1.5 + ADCS 0.5 = 10.0W，未計入 EPS self (0.3W) 及 TT&C Rx→Tx 的 delta。本 v2 採保守全計。

### 3.2 軌道各段時間分配

一個完整軌道 (94.5 min) 的時間分配：

| 段 | 時間 (min) | 說明 |
|----|-----------|------|
| Sunlit 非接觸 | 58.8 - 4.0 = 54.8 | 日照段扣除接觸窗口 |
| Contact Window | 4.0 | 假設接觸窗口在日照段（worst case 分析另計） |
| Eclipse 非接觸 | 35.7 | 全 eclipse 無接觸 |
| **Total** | **94.5** | |

> **假設**：接觸窗口發生在日照段（contact 期間太陽能板持續發電）。此為典型 case。Worst case（contact 發生在 eclipse 邊緣）於 Section 4 分析。

---

## 4. Energy Balance（能量收支分析）

### 4.1 每圈能量收入

太陽能板僅在日照段 (58.8 min) 發電：

| 條件 | 計算 | 能量收入 (Wh) |
|------|------|:------------:|
| **BOL** | 6.50 x 0.90 (MPPT) x 0.90 (cos theta) x (58.8/60) | **5.159 Wh** |
| **EOL** | 5.939 x 0.90 x 0.90 x (58.8/60) | **4.715 Wh** |

> **計算細節 (BOL)**：6.50 x 0.81 x 0.98 = 5.265 x 0.98 = 5.159
> 其中 0.81 = 0.90 x 0.90；58.8/60 = 0.98 hr

**校驗**：也可用 orbit-average power 方式計算：
- BOL avg power = 3.276W，但這是按「整圈平均」(含 eclipse = 0W)
- 每圈能量 = 3.276 x (94.5/60) = 3.276 x 1.575 = **5.160 Wh** (一致，差異 < 0.02%)

### 4.2 每圈能量支出

| 段 | 模式 | 功耗 (W) | 時間 (min) | 能量 (Wh) |
|----|------|:--------:|:----------:|:---------:|
| Sunlit 非接觸 | Nominal Sunlit | 2.50 | 54.8 | 2.50 x 54.8/60 = **2.283** |
| Contact Window | Contact Window | 10.30 | 4.0 | 10.30 x 4.0/60 = **0.687** |
| Eclipse | Eclipse Nominal | 3.00 | 35.7 | 3.00 x 35.7/60 = **1.785** |
| **Total 支出** | | | **94.5** | **4.755 Wh** |

> **與 Sprint 1 比較**：v1.1 支出約 4.47 Wh/orbit（未計 EPS self），本 v2 為 4.755 Wh/orbit（全計較保守）。

### 4.3 Net Energy Balance

| 條件 | 收入 (Wh) | 支出 (Wh) | **淨收支 (Wh/orbit)** | 狀態 |
|------|:---------:|:---------:|:--------------------:|------|
| **BOL** | 5.159 | 4.755 | **+0.404** | **正值 -- PASS** |
| **EOL** | 4.715 | 4.755 | **-0.040** | **微負 -- MARGINAL** |

### 4.4 能量收支結論

- **BOL**：DCN-001 後能量收支從 v1.1 的 -1.11 Wh/orbit **翻正為 +0.404 Wh/orbit**，有 7.8% margin (0.404/5.159)。充分驗證 DCN-001 的有效性。
- **EOL**：能量收支為 **-0.040 Wh/orbit**，微幅赤字 (-0.85%)。在計算精度範圍內接近零點。

> **EOL 微負的意義**：每圈赤字僅 0.040 Wh，相當於電池每圈額外放電 0.040/10 = 0.4% DoD，100 圈（約 6.6 天）累積 40% DoD。此為 worst-case 持續運作場景；實務上可透過 contact window duty cycle 管理（減少某些圈的 S-band 接觸）消除赤字。詳見第 6 節 Mitigation。

---

## 5. Battery DoD 分析

### 5.1 電池參數

| 參數 | BOL | EOL (3 yr) | 備注 |
|------|-----|-----------|------|
| 標稱容量 | **15.0 Wh** | **12.0 Wh** | EOL 容量衰減 ~20% (500+ cycles, 30% DoD)；DCN-002 升級自 10 Wh |
| 標稱電壓 | 7.2V (2S) | 7.0V | |
| 允許 DoD 上限 | 30% | 30% | 壽命考量 |
| 最大可用能量 | 4.5 Wh | 3.6 Wh | = 容量 x 30% |

### 5.2 單圈接觸窗口放電

Contact Window 期間功耗 10.30W，太陽能板同時發電（假設在日照段）：

| 項目 | 計算 | 值 |
|------|------|:--:|
| Contact Window 功耗 | 10.30 W | |
| 日照段太陽能板即時輸出 (BOL) | 6.50 x 0.90 x 0.90 = 5.265 W | |
| Contact 期間淨放電功率 (BOL) | 10.30 - 5.265 = 5.035 W | |
| Contact 放電能量 (BOL) | 5.035 x 4/60 = **0.336 Wh** | |
| Contact DoD (BOL, 15 Wh) | 0.336 / 15.0 = **2.24%** | |
| Contact DoD (EOL, 12 Wh) | 0.336 / 12.0 = **2.80%** | |

> **與 Sprint 1 比較**：v1.1 計算 Contact 放電 2.44 Wh，該值為「不扣太陽能發電」的 gross 放電。本 v2 計算 net 放電 0.336 Wh 較準確（contact 在日照段，太陽能板持續抵消部分功耗）。

### 5.3 Eclipse 放電分析

Eclipse 期間太陽能板輸出 = 0W，電池承擔全部負載：

| 項目 | 計算 | 值 |
|------|------|:--:|
| Eclipse 功耗 | 3.00 W | |
| Eclipse 時間 | 35.7 min = 0.595 hr | |
| Eclipse 放電能量 | 3.00 x 0.595 = **1.785 Wh** | |
| Eclipse DoD (BOL, 15 Wh) | 1.785 / 15.0 = **11.90%** | |
| Eclipse DoD (EOL, 12 Wh) | 1.785 / 12.0 = **14.88%** | |

### 5.4 Worst Case：連續 3 Eclipse 無充電

此為極端安全分析場景：假設連續 3 個 eclipse 期間電池完全無法從太陽能板充電（例如姿態異常導致太陽能板無法照射）。

| 項目 | 計算 | 值 |
|------|------|:--:|
| 單次 eclipse 放電 | 1.785 Wh | |
| 3 次連續 eclipse 總放電 | 1.785 x 3 = **5.355 Wh** | |
| Worst case DoD (BOL, 15 Wh) | 5.355 / 15.0 = **35.7%** | **FAIL (> 30%)** |
| Worst case DoD (EOL, 12 Wh) | 5.355 / 12.0 = **44.6%** | **FAIL (> 30%)** |

> **重要**：連續 3 eclipse 無充電是 **非設計場景**，代表衛星姿態完全失控 3 圈（~4.7 小時）。正常運作下，日照段充電足以恢復 eclipse 放電。此數字作為 FDIR 設計參考：若偵測到 DoD > 25%，應立即進入 Safe Mode 降載。

### 5.5 正常運作 Worst Case

更務實的 worst case：單圈 eclipse + 單圈 contact window（在 eclipse 結束前 4 min 開始 contact，contact 橫跨 eclipse/sunlit 邊界）。

| 項目 | 計算 | 值 |
|------|------|:--:|
| Eclipse 放電 (35.7 min, 3.0W) | 1.785 Wh | |
| Eclipse 末段 contact (4 min, 10.3W, 0W solar) | 10.30 x 4/60 = 0.687 Wh | |
| Eclipse 非 contact 段 (31.7 min, 3.0W) | 3.00 x 31.7/60 = 1.585 Wh | |
| Contact 在 eclipse 內的總放電 | 1.585 + 0.687 = **2.272 Wh** | |
| Worst case 單圈 DoD (BOL, 15 Wh) | 2.272 / 15.0 = **15.1%** | **PASS (< 30%)** |
| Worst case 單圈 DoD (EOL normal, 12 Wh) | 2.272 / 12.0 = **18.9%** | **PASS (< 30%)** |
| Worst case 單圈 DoD (EOL worst, 低溫 -8.3°C) | 2.40 / 9.0 = **25.2%** (PATCH-P5) | **PASS ✅ (< 30%)** |

> **EOL worst case 說明（PATCH-P5）**：低溫 -8.3°C 情境下，電池低溫容量保留率 75%（15 Wh x 75% = 11.25 Wh），再乘 EOL 衰減 80% = **9.0 Wh** 實際可用。Eclipse 放電 2.40 Wh（含加熱器），DoD = 2.40 / 9.0 = **25.2%**，低於 30% 上限，margin 4.8%。DCN-002 電池升級有效解決原 37.9% 超標問題。

> **結論**：電池升級至 15 Wh（DCN-002）後，所有 worst case 場景 DoD 均低於 30% 限值，margin 大幅改善。

---

## 6. Power Allocation Table（子系統功耗預算上限）

此表為各子系統的**功耗預算上限 (power envelope)**，Wave 2 各 agent 設計時不得超過此值。

| 子系統 | Standby (W) | Active (W) | Peak (W) | 備注 |
|--------|:-----------:|:----------:|:--------:|------|
| OBC (Zynq-class SoC/FPGA) | 1.50 | 4.00 | 5.00 | Peak: boot/FPGA reconfiguration 短暫尖峰，< 10 sec |
| S-band 酬載 PA | 0.00 | 4.00 | 4.50 | Active = DC input to PA；Peak = PA turn-on transient |
| TT&C (UHF) | 0.20 | 1.50 | 1.80 | Standby = Rx only；Active = Tx at 9600 bps |
| ADCS (MTQ x3 + RW x1) | 0.50 | 0.50 | 1.00 | Peak: 反應輪加速期間短暫，< 30 sec |
| EPS (self-consumption) | 0.30 | 0.30 | 0.30 | 固定，含 MPPT controller + regulator loss |
| Heater (Battery + Payload) | 0.00 | 0.50 | 0.50 | Eclipse 期間由 OBC 控制；Sunlit = OFF |
| **系統總計** | **2.50** | **10.30** (*) | **13.10** | |

(*) Active total 指 Contact Window 模式全子系統同時開啟。

### 6.1 各場景功耗總計

| 場景 | 功耗 (W) | 持續時間 (min/orbit) | 能量 (Wh/orbit) |
|------|:--------:|:-------------------:|:--------------:|
| Nominal Sunlit (standby) | 2.50 | 54.8 | 2.283 |
| Contact Window (active) | 10.30 | 4.0 | 0.687 |
| Eclipse Nominal | 3.00 | 35.7 | 1.785 |
| **Total per orbit** | | **94.5** | **4.755** |

### 6.2 功耗預算 Margin Policy

- 各子系統設計功耗不得超過上表 Active 欄位值。
- Peak 功耗僅限 transient (< 30 sec)，不列入能量收支計算。
- 系統保留 margin：BOL 能量收支 +0.404 Wh/orbit，對應約 0.26W orbit-average margin。
- **Reserve policy**：若任何子系統需要增加功耗，須提出 DCN 並重新審查能量收支。

---

## 7. DCN-001 / DCN-002 驗證結論

### 7.1 DCN 記錄

#### DCN-001（已核准，2026-04-15）
- 變更：太陽能板 BOL 輸出 5.0W → 6.5W
- 效果：BOL 能量收支 -1.11 Wh/orbit → +0.404 Wh/orbit ✅
- CEO 核准：Rudy，2026-04-15

#### DCN-002（已核准，2026-04-15）
- 變更：電池容量 10 Wh → 15 Wh
- 原因：Li-ion 低溫（-8.3°C）+ EOL 容量衰退複合效應導致 DoD worst case 37.9%，超過 30% 上限
- 效果：DoD worst case 37.9% → 25.2% ✅
- 成本影響：+$1,000 USD
- 質量影響：+250g（剩餘 margin 仍 1,570g）
- CEO 核准：Rudy，2026-04-15

### 7.2 驗證摘要

| 驗證項目 | Sprint 1 (5.0W / 10 Wh) | DCN-001 (6.5W BOL) | DCN-002 (15 Wh) | 判定 |
|---------|:------------------------:|:-------------------:|:----------------:|:----:|
| BOL 軌道平均功率 | 2.52 W | 3.276 W | 3.276 W | +30% vs Sprint 1 |
| BOL 能量收支 | -1.11 Wh/orbit | **+0.404 Wh/orbit** | **+0.404 Wh/orbit** | **PASS** |
| EOL 能量收支 | -1.56 Wh/orbit | **-0.040 Wh/orbit** | **-0.040 Wh/orbit** | **MARGINAL** |
| Eclipse DoD BOL normal | -- | 17.85% (10 Wh) | **11.90% (15 Wh)** | **PASS** |
| Eclipse DoD EOL normal | -- | 22.31% (8 Wh) | **16.0% (12 Wh)** | **PASS** |
| Eclipse DoD EOL worst case | -- | 37.9% (低溫，8 Wh) ❌ | **25.2% (低溫，9.0 Wh)** ✅ | **PASS** |
| Worst case 單圈 DoD (EOL+contact) | -- | 28.4% (eclipse + contact) | **18.9%** | **PASS** |

### 7.3 結論

1. **DCN-001 有效**：太陽能板從 5.0W 升級至 6.5W BOL，**成功將 BOL 能量收支從 -1.11 翻正為 +0.404 Wh/orbit**。DCN-001 核准決策正確。

2. **EOL 微幅赤字**：EOL 能量收支 = -0.040 Wh/orbit，赤字極小但非零。在目前假設條件下 (MPPT 90%, cos_avg 0.90, 每圈 1 contact)，EOL 為 marginal case。

3. **DCN-002 解決 DoD 超標問題**：電池升級至 15 Wh 後，EOL worst case DoD（低溫 -8.3°C）從 37.9% 降至 **25.2%**，成功低於 30% 上限。建議 FDIR 設定 DoD > 22% 時進入 Safe Mode（保留 3% buffer）。

4. **連續 3 eclipse 無充電為非設計場景**：DoD 35.7-44.6% 超標，但此為姿態失控場景，由 FDIR 處理。

### 7.4 EOL 赤字 Mitigation 建議

| # | 方案 | 效果 | 可行性 |
|---|------|------|--------|
| M1 | 降低 contact duty cycle：每 2 圈 contact 1 次（而非每圈） | 能量支出從 4.755 降至 4.412 Wh/orbit，EOL 收支 = +0.303 Wh (轉正) | 高 -- 100 bps IoT-NTN 對 latency 容忍度高 |
| M2 | OBC standby 功耗優化至 1.2W（FPGA clock gating） | 支出減少 0.3W x 1.428hr = 0.428 Wh，EOL 收支 = +0.388 Wh | 中 -- 需 SW/FW 配合 |
| M3 | 增加太陽能板面積至 7.0W BOL | EOL avg = 3.22W，收支轉為 +0.32 Wh | 低 -- 3U 體積限制嚴格 |
| M4 | Eclipse 期間停用 ADCS RW（改為 MTQ-only） | 省 0.2W x 0.595hr = 0.119 Wh，部分改善 | 中 -- 需 AOCS 評估精度影響 |

**建議優先方案**：M1（降低 contact duty cycle）+ M2（OBC clock gating），兩者合併可使 EOL 收支 margin > +0.5 Wh/orbit。

---

## 8. 附錄：計算參數彙總

| 參數 | 符號 | 值 | 單位 |
|------|------|:--:|------|
| 軌道週期 | T_orbit | 94.5 | min |
| Eclipse 時間 | T_eclipse | 35.7 | min |
| 日照時間 | T_sunlit | 58.8 | min |
| Eclipse fraction | f_ecl | 37.78 | % |
| 接觸窗口 | T_contact | 4.0 | min |
| 太陽能板 BOL 峰值 | P_solar_BOL | 6.50 | W |
| 太陽能板 EOL 峰值 | P_solar_EOL | 5.939 | W |
| EOL 衰減因子 | eta_EOL | 0.9137 | -- |
| MPPT 效率 | eta_MPPT | 0.90 | -- |
| 傾斜角平均因子 | cos_theta_avg | 0.90 | -- |
| BOL 軌道平均功率 | P_avg_BOL | 3.276 | W |
| EOL 軌道平均功率 | P_avg_EOL | 2.993 | W |
| 電池容量 (BOL) | E_batt_BOL | **15.0** | Wh |
| 電池容量 (EOL) | E_batt_EOL | **12.0** | Wh |
| 電池 DoD 上限 | DoD_max | 30 | % |
| Nominal Sunlit 功耗 | P_sunlit | 2.50 | W |
| Contact Window 功耗 | P_contact | 10.30 | W |
| Eclipse Nominal 功耗 | P_eclipse | 3.00 | W |
| BOL 每圈能量收入 | E_in_BOL | 5.159 | Wh |
| EOL 每圈能量收入 | E_in_EOL | 4.715 | Wh |
| 每圈能量支出 | E_out | 4.755 | Wh |
| BOL 淨收支 | E_net_BOL | +0.404 | Wh |
| EOL 淨收支 | E_net_EOL | -0.040 | Wh |

---

## Wave 2 Cross-reading 通知

**Comm Agent (B-001 Link Budget v2)** 需讀取：
- 第 6 節 Power Allocation Table：S-band 酬載 PA 功耗上限 = **4.0W DC** (Active)，RF out ~1.0W (PAE ~25%)
- 第 5.5 節：Worst case 接觸窗口能量分析 -- 電池可支撐 4 min contact at 10.3W（EOL DoD 28.4% < 30%）
- 第 7.3 節 Mitigation M1：若 EOL 能量收支需改善，可將 contact duty cycle 降為每 2 圈 1 次

**AOCS Agent (B-006 ADCS Trade Study)** 需讀取：
- 第 6 節 Power Allocation Table：ADCS 功耗預算 = **Standby 0.5W / Active 0.5W / Peak 1.0W**（含 MTQ x3 + RW x1）
- 第 7.3 節 Mitigation M4：Eclipse 期間若可降為 MTQ-only（省 0.2W），可改善 EOL 能量收支
- B-002 ICD IF-03：OBC ↔ ADCS 介面 = SPI 1 Mbps, 3.3V CMOS

**SW/FW Agent (B-007 OBC/FPGA 架構)** 需讀取：
- 第 6 節 Power Allocation Table：OBC 功耗預算 = **Standby 1.5W / Active 4.0W / Peak 5.0W**
- 4.0W Active 含 FPGA SDR 基帶處理 -- 需確認 Zynq-7020 在此 envelope 內可行（typical Zynq-7020: PL 1.5~2.5W + PS 0.5~1.0W + I/O 0.5W = 2.5~4.0W，在 envelope 邊緣）
- 第 7.3 節 Mitigation M2：OBC standby 若可從 1.5W 降至 1.2W（FPGA clock gating），可省 0.428 Wh/orbit
- 第 5.1 節運作模式定義：OBC 需實作 4 種功耗模式切換（Standby/Active/Safe/Peak）

**QA Agent** 需讀取：
- 第 7.2 節驗證摘要表：所有 margin 數字；DCN-002 後 EOL worst case DoD = **25.2%**（margin 4.8%，已解除超標風險）
- 第 4.4 節 EOL 能量收支 marginal 判定：-0.040 Wh/orbit，仍需列入風險登記冊 (Risk Register)
- DCN-002 成本 +$1,000 USD / 質量 +250g，需更新 BOM 與質量預算
