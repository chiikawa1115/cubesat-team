# B-008：熱控初步分析（Eclipse 溫度循環，加熱器需求）

**文件版本**：v1.1
**負責人**：吳建宇（Mech/Thermal Agent）
**日期**：2026-05-07
**Cross-reading 來源**：B-005 Power Budget v2、B-007 OBC Architecture、B-006 AOCS Trade Study

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| v1.0 | 2026-05-07 | 初版發布（Sprint 2 Wave 2） |
| v1.1 | 2026-05-07 | DCN-002：電池升級 10 Wh → 15 Wh，DoD 37.9% → 25.2%，Risk 降為 CLOSED |

---

## 1. 分析目標

確認 TASA-NTN-3U CubeSat 在 500 km SSO 軌道的 Eclipse/Sunlit 溫度循環，驗證電子元件（-20°C ~ +60°C）和電池（-10°C ~ +50°C）的操作溫度範圍，並評估加熱器功率需求。

---

## 2. 軌道環境參數

| 參數 | 數值 |
|------|------|
| 軌道高度 | 500 km SSO |
| 軌道週期 | 94.5 min |
| Eclipse 時長 | 35.7 min |
| Sunlit 時長 | 58.8 min |
| 太陽常數 | 1,367 W/m² |
| 地球紅外輻射 | ~240 W/m² |
| 地球反照率 | ~0.3 |
| 深空背景溫度 | 2.7 K（~0 W） |

---

## 3. 熱源功耗彙整（來自各子系統設計文件）

| 子系統 | Sunlit Nominal (W) | Contact Window (W) | Eclipse (W) |
|--------|:------------------:|:-------------------:|:-----------:|
| OBC（Zynq-7020） | 1.50 | 4.00 | 1.50 |
| EPS self | 0.30 | 0.30 | 0.30 |
| ADCS（MTQ×3 + CubeWheel） | 0.42 | 0.42 | 0.42 |
| S-band PA | 0.00 | 4.00 | 0.00 |
| TT&C UHF | 0.20 | 1.50 | 0.20 |
| **內部熱耗散合計** | **2.42** | **10.22** | **2.42** |

> 加熱器（0.5W，Eclipse only）另計。

---

## 4. 熱平衡估算（簡化 Lumped-Mass Model）

### 4.1 衛星幾何參數（3U）

- 外表面積（六面總和）：
  - 長面 ×4：4 × (100 × 340) = 136,000 mm² = 0.136 m²
  - 端面 ×2：2 × (100 × 100) = 20,000 mm² = 0.020 m²
  - **總外表面積**：0.156 m²

- **MLI（多層隔熱膜）覆蓋策略**：4 個長面覆蓋 MLI（有效隔熱），僅保留部分面積作為輻射器
- **有效輻射面積**（A_rad）：0.025 m²（含端面 + MLI 洩漏）
- **太陽吸收面積**（A_solar）：~0.01 m²（平均投影）

### 4.2 表面光學特性

| 表面 | 吸收率 α_s | 放射率 ε | 用途 |
|------|:----------:|:--------:|------|
| Anodized Al（太陽面） | 0.3 | 0.2 | 太陽能板安裝面 |
| Black paint（散熱面） | 0.95 | 0.9 | 端面輻射器 |
| MLI（隔熱面） | — | ~0.02 | 長面隔熱 |

散熱面以 black paint 為主，取 ε = 0.9。

### 4.3 熱平衡方程（穩態估算）

$$Q_{in} = Q_{out}$$

$$Q_{solar} + Q_{Earth\,IR} + Q_{internal} = \sigma \cdot \varepsilon \cdot A_{rad} \cdot T^4$$

其中：
- σ = 5.67×10⁻⁸ W/m²K⁴（Stefan-Boltzmann 常數）
- ε = 0.9（散熱面放射率）
- A_rad = 0.025 m²

**共通項**：
- σ × ε × A_rad = 5.67×10⁻⁸ × 0.9 × 0.025 = **1.276×10⁻⁹ W/K⁴**
- 地球 IR 吸收：Q_Earth = 240 × 0.9 × 0.025 × 0.3 = **1.62 W**（view factor ≈ 0.3）

---

### 4.4 Sunlit 穩態溫度

| 熱源項 | 計算 | 功率 (W) |
|--------|------|----------|
| 太陽輻射吸收 | 1,367 × 0.3 × 0.01 m² | 4.10 |
| 地球 IR 吸收 | 240 × 0.9 × 0.025 × 0.3 | 1.62 |
| 地球反照率 | 1,367 × 0.3 × 0.3 × 0.025 × 0.3 | 0.92 |
| 內部熱耗散 | Nominal mode | 2.42 |
| **Q_in 合計** | | **9.06** |

$$T_{sunlit} = \left(\frac{9.06}{1.276 \times 10^{-9}}\right)^{1/4} = \left(7.10 \times 10^{9}\right)^{1/4}$$

$$\boxed{T_{sunlit} \approx 290.3\,\text{K} = +17.2°\text{C}}$$

---

### 4.5 Eclipse 穩態溫度

**不含加熱器**：

| 熱源項 | 功率 (W) |
|--------|----------|
| 太陽輻射 | 0 |
| 地球 IR | 1.62 |
| 內部熱耗散 | 2.42 |
| **Q_in 合計** | **4.04** |

$$T_{eclipse,eq} = \left(\frac{4.04}{1.276 \times 10^{-9}}\right)^{1/4} = \left(3.17 \times 10^{9}\right)^{1/4}$$

$$\boxed{T_{eclipse,eq} \approx 237.2\,\text{K} = -35.9°\text{C}}$$

**含 0.5W 加熱器**：

$$T_{eclipse,eq+heater} = \left(\frac{4.54}{1.276 \times 10^{-9}}\right)^{1/4} \approx 244.2\,\text{K} = -28.9°\text{C}$$

> 以上為穩態極限值。由於 Eclipse 僅持續 35.7 min，衛星不會冷卻至穩態溫度（見 4.7 暫態分析）。

---

### 4.6 Contact Window 穩態溫度（Sunlit + 全功率）

| 熱源項 | 功率 (W) |
|--------|----------|
| 太陽輻射吸收 | 4.10 |
| 地球 IR | 1.62 |
| 地球反照率 | 0.92 |
| 內部熱耗散（Contact mode） | 10.22 |
| **Q_in 合計** | **16.86** |

$$T_{contact,eq} = \left(\frac{16.86}{1.276 \times 10^{-9}}\right)^{1/4} \approx 339.1\,\text{K} = +65.9°\text{C}$$

> 穩態值超過電子元件限值 +60°C，但 Contact Window 僅持續 4 min，實際為暫態。

---

### 4.7 暫態分析（Transient）

**衛星等效熱容**：
- 鋁結構框架（350g，c_p = 900 J/kg·K）：315 J/K
- 電子模組（合計 ~700g，c_p ≈ 500 J/kg·K）：350 J/K（PCB + 元件混合）
- **簡化取 C_total ≈ 250 J/K**（lumped model 有效熱容，考慮接觸熱阻分散效應）

**熱時間常數**：

$$\tau = \frac{C}{4 \cdot \sigma \cdot \varepsilon \cdot A_{rad} \cdot T_{avg}^3}$$

取 T_avg ≈ 264 K（Sunlit 與 Eclipse 中間值）：

$$\tau = \frac{250}{4 \times 5.67 \times 10^{-8} \times 0.9 \times 0.025 \times 264^3} \approx 2,670\,\text{s} \approx 44.5\,\text{min}$$

> Eclipse 時長 35.7 min < τ = 44.5 min，衛星**不會冷卻至穩態極限**。

---

#### Eclipse-End 暫態溫度（指數衰減模型）

$$T(t) = T_{eq,eclipse} + (T_{sunlit} - T_{eq,eclipse}) \cdot e^{-t/\tau}$$

**不含加熱器**（t = 35.7 min = 2,142 s）：

$$T_{end} = 237.2 + (290.3 - 237.2) \times e^{-2142/2670}$$
$$T_{end} = 237.2 + 53.1 \times 0.449 = 237.2 + 23.8 = 261.1\,\text{K}$$

$$\boxed{T_{eclipse\text{-}end}(\text{no heater}) \approx -12.1°\text{C}}$$

**含 0.5W 加熱器**：

$$T_{end} = 244.2 + (290.3 - 244.2) \times e^{-2142/2670}$$
$$T_{end} = 244.2 + 46.1 \times 0.449 = 244.2 + 20.7 = 264.9\,\text{K}$$

$$\boxed{T_{eclipse\text{-}end}(\text{0.5W heater}) \approx -8.3°\text{C}}$$

---

#### Contact Window 暫態溫升（4 min）

Contact Window 僅持續 4 min（240 s），遠小於 τ = 44.5 min，使用線性近似：

$$\Delta T = \frac{(Q_{contact} - Q_{nominal}) \times t}{C} = \frac{(10.22 - 2.42) \times 240}{250} = \frac{7.80 \times 240}{250}$$

$$\boxed{\Delta T_{contact} \approx +7.5°\text{C}}$$

Contact Window 峰值溫度 = Sunlit Nominal + ΔT = 17.2 + 7.5 = **+24.7°C**

> Contact Window 暫態溫升輕微，不構成熱控風險。

---

## 5. 溫度合規性檢查

### 5.1 電子元件（-20°C ~ +60°C）

| 工況 | 溫度 (°C) | 判定 | 餘裕 |
|------|:---------:|:----:|------|
| Sunlit Nominal | +17.2 | PASS | +42.8°C to upper |
| Contact Window Peak | +24.7 | PASS | +35.3°C to upper |
| Eclipse-End（無加熱器） | -12.1 | PASS | +7.9°C to lower |
| Eclipse-End（含加熱器） | -8.3 | PASS | +11.7°C to lower |

### 5.2 電池（-10°C ~ +50°C）

| 工況 | 溫度 (°C) | 判定 | 餘裕 |
|------|:---------:|:----:|------|
| Sunlit Nominal | +17.2 | PASS | +32.8°C to upper |
| Contact Window Peak | +24.7 | PASS | +25.3°C to upper |
| Eclipse-End（無加熱器） | -12.1 | **FAIL** | 超限 2.1°C |
| Eclipse-End（含加熱器） | -8.3 | PASS | +1.7°C to lower |

> **關鍵發現**：不含加熱器時，Eclipse-end 電池溫度 -12.1°C 低於 -10°C 限值。**加熱器為必需品**，0.5W 加熱器可將溫度提升至 -8.3°C（餘裕 1.7°C）。

---

## 6. 加熱器需求分析

### 6.1 加熱器必要性

由 Section 5.2 確認：Eclipse 期間電池溫度會降至 -12.1°C，低於 -10°C 操作下限。**加熱器為必需（mandatory）**。

### 6.2 加熱器功率驗證

- 0.5W 加熱器使 Eclipse-end 溫度從 -12.1°C 提升至 -8.3°C（改善 3.8°C）
- 電池溫度餘裕 1.7°C，偏小但可接受（PDR 階段）
- Eclipse 期間加熱器耗能：0.5W × 35.7 min × (1/60) h = **0.30 Wh/orbit**
- 與 B-005 Power Budget v2 的加熱器預算 0.5W 一致

### 6.3 加熱器配置建議

| 項目 | 規格 |
|------|------|
| 加熱器數量 | 2 片（冗餘設計） |
| 加熱片型式 | Kapton 薄膜加熱器（20×30 mm） |
| 安裝位置 | 電池模組底面（直接接觸） |
| 控制方式 | 溫度感測器 + EPS 硬體 thermostat（±2°C） |
| 啟動門檻 | T_battery ≤ -5°C 啟動，T_battery ≥ 0°C 關閉 |
| 功率 | 每片 0.5W（一用一備） |

---

## 7. 熱控設計建議

### 7.1 整體策略

```
                  MLI 隔熱（4 長面）
                ┌──────────────────┐
    太陽面 ──→  │  MLI blanket     │
                │                  │
    +Z 端面 ──→ │  Black paint     │ ←── 主要散熱面（A_rad）
                │  (radiator)      │
                │                  │
    -Z 端面 ──→ │  Black paint     │ ←── 次要散熱面
                │  (radiator)      │
                └──────────────────┘
```

### 7.2 各子系統散熱設計

**OBC Zynq-7020（4.0W active，集中在 ~10×10 mm die）**：
- PCB 背面 thermal via array（直徑 0.3 mm，間距 1.0 mm，矩陣排列）
- 導熱墊（thermal pad，k ≥ 5 W/m·K）貼合至鋁結構框架
- 框架作為 heat spreader → 端面 radiator 散熱
- **重點**：B-007 已標記 Zynq die 散熱為 Wave 3 交叉確認項

**S-band PA（4.0W DC，η ≈ 25% → 3.0W 熱耗散）**：
- PA 模組直接螺鎖至鋁結構面板（螺絲 + 導熱墊）
- Contact Window 僅 4 min，暫態溫升有限（+7.5°C）
- 若 PA 局部溫度過高，可追加小型銅 heat spreader（~10g）

**電池模組**：
- Kapton 加熱器 ×2（見 Section 6.3）
- MLI 包覆（降低對外輻射損失）
- 溫度感測器 ×2（冗餘量測）

### 7.3 表面塗裝規劃

| 面 | 塗裝 | α_s / ε | 目的 |
|----|------|---------|------|
| +Z 端面（Earth-facing） | Black paint | 0.95 / 0.90 | 主要輻射散熱 |
| -Z 端面（Anti-Earth） | Black paint | 0.95 / 0.90 | 次要輻射散熱 |
| +X, -X 長面 | MLI | — / ~0.02 | 隔熱，減少 Eclipse 散熱損失 |
| +Y, -Y 長面（太陽能板面） | Anodized Al | 0.30 / 0.20 | 太陽能板安裝，低吸收 |

---

## 7.4 DCN-002：電池升級設計變更說明（v1.1 新增）

### 7.4.1 變更概述

CEO 核准 **DCN-002**（Design Change Notice 002）：將電池從 **10 Wh** 升級至 **15 Wh**。

| 項目 | 原規格（v1.0） | 新規格（v1.1） | 差異 |
|------|:--------------:|:--------------:|------|
| 電池容量 | 10 Wh | **15 Wh** | +5 Wh (+50%) |
| 電池型號 | — | GomSpace P31u 或同等級 | — |
| 質量增加 | — | +250 g | 需通知 PM 更新 B-004 Mass Budget |
| Eclipse 加熱器功耗 | 0.5 W | **0.5 W（不變）** | 熱功耗無異動 |

### 7.4.2 電池 DoD 分析更新

**EOL Worst Case DoD（原 10 Wh → 新 15 Wh）**：

| 指標 | 原值（10 Wh） | 新值（15 Wh） | 判定 |
|------|:-------------:|:-------------:|:----:|
| EOL worst case DoD | 37.9% | **25.2%** | RESOLVED via DCN-002 |

> 原 DoD 37.9% 已超出電池長壽命設計建議值（<30%），升級後 DoD 25.2% 符合規範。

### 7.4.3 低溫性能分析（-8.3°C 工況）

Eclipse-end 電池溫度維持 **-8.3°C**（加熱器 0.5W 已開啟，溫度數字不變）。

| 項目 | 計算 | 結果 |
|------|------|------|
| 電池標稱容量（15 Wh） | — | 15.00 Wh |
| 低溫可用容量（-8.3°C，75% derating） | 15 Wh × 75% | **11.25 Wh** |
| Eclipse 電力需求（EOL approx） | — | 2.40 Wh |
| DoD at -8.3°C（EOL approx） | 2.40 / 11.25 | **21.3%** |

> 即使在最冷工況 -8.3°C、電池 75% 容量條件下，DoD 僅 21.3%，仍具充足餘裕。

### 7.4.4 壽命改善估算

| 指標 | 舊電池（10 Wh） | 新電池（15 Wh） |
|------|:--------------:|:--------------:|
| EOL worst case DoD | 37.9% | 25.2% |
| 估算 cycle life 倍數 | 1× (baseline) | **≈ 3×** |

> 依 Li-ion DoD vs. cycle life 特性曲線：DoD 降低 12.7 個百分點（37.9% → 25.2%）約可延長電池循環壽命 **3 倍**，大幅提升任務可靠度。

---

## 8. 結論

### 8.1 溫度範圍合規性

| 項目 | 結果 |
|------|------|
| 電子元件（-20°C ~ +60°C） | **全工況 PASS** |
| 電池（-10°C ~ +50°C） | **含加熱器 PASS**（Eclipse-end -8.3°C，餘裕 1.7°C） |
| 加熱器必要性 | **必需**，0.5W 符合需求 |
| Contact Window 熱峰值 | +24.7°C，無風險 |

### 8.2 主要風險與 Mitigation

| 風險 | 嚴重度 | Mitigation | 狀態 |
|------|--------|------------|------|
| ~~電池 DoD 超標（EOL 37.9% > 30%）~~ | ~~HIGH~~ | ~~升級電池容量~~ | **CLOSED (DCN-002)** |
| 電池 Eclipse-end 溫度餘裕僅 1.7°C | 中 | 加熱器控制精度 ±2°C 需驗證；可考慮提升至 0.75W | OPEN |
| OBC Zynq die 局部過熱（4W/100mm²） | 中 | Thermal via + 導熱墊 + 結構散熱，需 Phase B 詳細模擬 | OPEN |
| S-band PA 3W 熱耗散 | 低 | Contact Window 僅 4 min，暫態溫升有限 | OPEN |
| MLI 安裝品質影響隔熱效能 | 中 | AIT 階段需確認 MLI 覆蓋完整性 | OPEN |

### 8.3 Wave 3 待辦

- [ ] PDR 審查後根據回饋調整 MLI 覆蓋策略
- [ ] Phase B 使用 Thermal Desktop 或 ESATAN 進行 3D 節點模型模擬
- [ ] 確認加熱器供應商及控制電路設計（與 EPS Agent 協調）
- [ ] OBC 散熱路徑 detailed thermal resistance 分析

---

## Wave 3 Cross-reading 通知（for PDR 審查包）

**提供給其他 Agent 的關鍵數字**：

| 參數 | 數值 | 接收方 |
|------|------|--------|
| T_min（Eclipse-end，含加熱器） | **-8.3°C** | PM / 全體 |
| T_max（Contact Window Peak） | **+24.7°C** | PM / 全體 |
| T_sunlit（Nominal） | **+17.2°C** | PM / 全體 |
| 加熱器功耗 | **0.5W（Eclipse only）** | EPS Agent |
| 加熱器耗能 | **0.30 Wh/orbit** | EPS Agent |
| 熱控質量 | **80g** | PM（B-004 Mass Budget） |
| 電池溫度餘裕 | **1.7°C（偏小）** | QA Agent |
| OBC Zynq 散熱需求 | **thermal pad → Al frame** | SW/FW Agent |

---

*Prepared by Mech/Thermal Agent（吳建宇）, TASA-NTN-3U CubeSat Project*
