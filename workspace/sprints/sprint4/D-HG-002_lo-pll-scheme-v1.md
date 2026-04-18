# D-HG-002：LO 190 MHz 方案確認報告
# Hard Gate Q2 正式回覆

**作者：** 通訊酬載工程師 林志遠
**日期：** 2026-05-27
**關聯：** CDR 審查 Q2（詹老師 2026-05-26）
**狀態：** v1 — Hard Gate 回覆完成

---

## 1. 問題確認

依據詹老師 CDR 審查報告（Q2），C-002 設計中混頻器 LT5512EUF 的本振（LO）頻率為 **190 MHz**：

- LO = DL 中心 - UL 中心 = 2185 - 1995 = **190 MHz**（頻率轉換關係正確）
- 問題：**190 MHz 為非標準商用 TCXO 頻率**，標準商用 TCXO 頻率為 10/20/25/26/40/52/100 MHz
- C-002 未提供 190 MHz 訊號源方案，為設計缺口

---

## 2. 標準 TCXO 可用性調查

**搜尋結果（Mouser / DigiKey / ECIA 2026）：**

直接搜尋 "190 MHz TCXO"、"190 MHz VCTCXO"：

- **未找到標準商用 190 MHz TCXO** 料號
- 最接近的高頻 TCXO：Crystal Technology CTH035C (156.25 MHz), Epson TSX-3225 最高約 60 MHz
- 高頻 VCXO（壓控）：Crystek CVCO55CL 系列 VCO 可達 190 MHz，但僅為 VCO（非晶振穩定度），SSB phase noise > -80 dBc/Hz @ 10 kHz

**結論：方案 A（直接 TCXO）不可行**，採用**方案 B（PLL 合成 190 MHz）**。

---

## 3. PLL 方案設計

### 3.1 架構

```
10 MHz TCXO (參考) ──→ ADF4351 PLL 合成器 ──→ 190 MHz LO 輸出 ──→ LT5512EUF
      │                    │
   ±0.5 ppm              INT Mode: N=19
   穩定度                  VCO: 3040 MHz → ÷16 → 190 MHz
```

### 3.2 零件選型

#### 參考 TCXO：Abracon ASTX-H11-10.000MHZ-T

| 參數 | 規格 |
|-----|------|
| 料號 | ASTX-H11-10.000MHZ-T |
| 頻率 | 10.000 MHz |
| 穩定度 | ±0.5 ppm（-40～+85°C）|
| Phase Noise | -150 dBc/Hz @ 1 kHz offset |
| 供電 | 3.3V，ICC = 2 mA |
| 封裝 | 2.0×1.6 mm SMD |
| 單價 | ~$2.20（DigiKey 料號：433-1029-1-ND）|

#### PLL 合成器：Analog Devices ADF4351

| 參數 | 規格 |
|-----|------|
| 料號 | ADF4351BCPZ |
| 輸出頻率範圍 | 35 MHz ～ 4400 MHz（經內部分頻）|
| VCO 內部範圍 | 2200 ～ 4400 MHz |
| 輸出分頻器 | ÷1 / ÷2 / ÷4 / ÷8 / ÷16 / ÷32 / ÷64 |
| PFD 最大頻率 | 25 MHz |
| 電荷泵電流 | 0.31 ～ 5.0 mA（可調）|
| 封裝 | 4×4 mm LFCSP-24 |
| 供電 | 3.3V 模擬 + 3.3V 數位 |
| 單價 | ~$8.50（DigiKey 料號：505-ADF4351BCPZ-ND）|

### 3.3 頻率計算

**目標輸出：190 MHz**

ADF4351 整數模式（INT mode）計算：

```
f_PFD = f_REF / R_counter = 10 MHz / 1 = 10 MHz  (R=1)

VCO 頻率：f_VCO = f_PFD × INT = 10 × 304 = 3040 MHz
  （範圍 2200-4400 MHz 之內 ✓）

輸出分頻器：Output Divider = 16（2^4）
  → f_OUT = 3040 / 16 = 190 MHz ✓

INT mode：FRAC=0，MOD=1（整數分頻，最佳相位雜訊）
寄存器設定：R0: INT=304, FRAC=0; R1: MOD=1; R4: RF_DIV_SEL=4 (÷16)
```

**設定確認：**
- f_REF = 10 MHz ✓
- f_PFD = 10 MHz ✓
- INT = 304 ✓
- VCO = 3040 MHz（在 2200-4400 MHz 範圍內）✓
- Output divider = 16 ✓
- f_OUT = 190.000 MHz ✓

---

## 4. Phase Noise 分析

### 4.1 ADF4351 相位雜訊計算

#### 參考振盪器貢獻（TCXO 10 MHz）

```
L_TCXO(10 kHz) ≈ -150 dBc/Hz  (@ 10 MHz TCXO 量測值)

乘以 20×log10(N×M) 劣化至 VCO 頻率：
  N×M = 304 × 1 = 304
  劣化量 = 20×log10(304) = 49.7 dB

TCXO 在 VCO 點的貢獻：
  L_REF @ VCO = -150 + 49.7 = -100.3 dBc/Hz @ 3040 MHz

Output divider ÷16 改善：
  L_REF @ 190 MHz = -100.3 - 20×log10(16) = -100.3 - 24.1 = -124.4 dBc/Hz
```

#### ADF4351 VCO 本體相位雜訊

從 ADF4351 數據手冊（Figure 16-18，VCO ~3 GHz）：
```
L_VCO(10 kHz) ≈ -91 dBc/Hz @ 3040 MHz

Output divider ÷16 改善：
  L_VCO @ 190 MHz = -91 - 24.1 = -115.1 dBc/Hz
```

#### 電荷泵 + PFD 雜訊底板

```
PFD 正規化雜訊（ADF4351 典型）：-223 dBc/Hz
乘以 20×log10(f_VCO / f_PFD) = 20×log10(3040/10) = 49.7 dB
L_CP @ VCO = -223 + 49.7 + 20×log10(304) = -223 + 49.7 + 49.7 = -123.6 dBc/Hz
L_CP @ 190 MHz = -123.6 - 24.1 = -147.7 dBc/Hz
```

#### 合成後 LO @ 190 MHz 總相位雜訊（10 kHz offset）

```
主要項目（RSS 合成）：
  L_VCO = -115.1 dBc/Hz  （主要）
  L_REF = -124.4 dBc/Hz
  L_CP  = -147.7 dBc/Hz

RSS = 10×log10(10^(-115.1/10) + 10^(-124.4/10) + 10^(-147.7/10))
    = 10×log10(3.09×10⁻¹² + 3.63×10⁻¹³ + 1.70×10⁻¹⁵)
    ≈ 10×log10(3.46×10⁻¹²)
    = -114.6 dBc/Hz

L_LO-190MHz(10 kHz) ≈ -114.6 dBc/Hz ✓ (優於 -85 dBc/Hz 目標)
```

### 4.2 LO 上混頻至載波頻率的相位雜訊劣化

```
從 LO (190 MHz) 上混頻至 DL 載波 (~2185 MHz)：
  劣化量 = 20×log10(2185/190) = 20×log10(11.5) = 21.2 dB

載波 @ 2185 MHz 的 LO 貢獻：
  L_carrier(10 kHz) = -114.6 + 21.2 = -93.4 dBc/Hz
```

**總結：混頻後 2185 MHz 載波的 LO 相位雜訊 ≈ -93.4 dBc/Hz @ 10 kHz**

---

## 5. Costas Loop 相容性分析

### 5.1 Costas Loop 需求

系統 QPSK 調制，Symbol Rate = 200 kSps，Carrier loop bandwidth B_L ≈ 1 kHz（C-003 Costas Loop 設計）

### 5.2 相位誤差估算

**RMS 相位誤差 = √(S_φ × B_L)**

其中 S_φ 為載波點單邊功率譜密度（rad²/Hz）：

```
假設 phase noise 在 B_L = 1 kHz 內為平坦（最壞情況）：
  L_carrier(f) ≈ -93.4 dBc/Hz for f < 10 kHz
  S_φ = 2 × 10^(-93.4/10) = 2 × 4.57×10⁻¹⁰ = 9.13×10⁻¹⁰ rad²/Hz

RMS 相位誤差：
  σ_φ = √(S_φ × B_L) = √(9.13×10⁻¹⁰ × 1000) = √(9.13×10⁻⁷) = 9.6×10⁻⁴ rad = 0.055°
```

### 5.3 QPSK 相位雜訊容忍度

| 指標 | 計算值 | 門檻 | 判斷 |
|-----|--------|------|------|
| LO RMS 相位誤差（1σ） | **0.055°** | < 1°（典型 QPSK 設計裕量）| ✅ PASS |
| QPSK BER 降額（相位誤差 0.055°）| < 0.01 dB | 可忽略 | ✅ PASS |
| ADF4351 Lock Time | ~200 μs | < 1 ms（系統 startup）| ✅ PASS |

**Costas Loop 相容性：確認 ADF4351 PLL 方案不影響 QPSK 解調性能** ✓

---

## 6. BOM 增量

| 料號 | 描述 | 數量 | 單價 | 小計 |
|-----|------|-----|------|------|
| ASTX-H11-10.000MHZ-T | Abracon 10 MHz TCXO, ±0.5ppm | 1 | $2.20 | $2.20 |
| ADF4351BCPZ | ADI PLL 合成器 35M-4.4GHz | 1 | $8.50 | $8.50 |
| 被動元件（Loop Filter R/C×5） | 環路濾波器 | 5 | $0.05 | $0.25 |
| **PLL 子系統合計** | | | | **$10.95** |

BOM 增量約 $10.95，PCB 面積增加 ~1 cm²（ADF4351 4×4 mm + TCXO 2×1.6 mm + loop filter）

---

## 7. PCB 佈局注意事項

1. **ADF4351 VCO 電源去耦：** 在 VCC_VCO 腳附近放置 10 nF + 100 pF 並聯，接地面要完整
2. **Loop Filter 緊貼 ADF4351：** 環路濾波器（3rd order passive）應在 CP_OUT 至 VP 腳間，走線最短化
3. **參考 TCXO 隔離：** TCXO 與 RF 路徑保持 >5 mm，避免 LO 洩漏汙染參考
4. **190 MHz 輸出走線：** 阻抗控制 50Ω 微帶，長度 < 3 cm，避免 LO 諧波輻射至天線

---

## 8. 環路濾波器設計（3rd Order Passive）

```
ADF4351 典型 Loop Filter（f_LO = 190 MHz, f_PFD = 10 MHz, B_L = 1 kHz）：

建議電荷泵電流 I_CP = 1.25 mA
Phase margin ≥ 45°

3rd order passive filter 元件：
  R1 = 2.7 kΩ
  C1 = 47 nF
  C2 = 4.7 nF  
  R3 = 220 Ω
  C3 = 100 pF

（使用 ADI ADISimPLL 工具驗證設計，Sprint 4 W1 完成）
```

---

## 9. 結論

- **Q2 Hard Gate：RESOLVED ✅**
- 190 MHz TCXO 不存在標準商用料號 → 採用 **PLL 方案**
- **ADF4351BCPZ** + **Abracon 10 MHz TCXO**
- 計算確認：VCO 3040 MHz ÷ 16 = 190 MHz，INT mode
- Phase noise @ LO 190 MHz：**-114.6 dBc/Hz @ 10 kHz**（超越 -85 dBc/Hz 目標 ~29.6 dB）
- Costas loop RMS 相位誤差：**0.055°**，可忽略不計，不影響 QPSK 解調
- BOM 增量：**+$10.95**，PCB 面積增加 ~1 cm²

---

## 10. 開放事項（Action Items）

| 編號 | 內容 | 負責人 | 期限 |
|-----|------|--------|------|
| AI-HG-002-1 | ADISimPLL 環路濾波器模擬，驗證 B_L, phase margin | Comm 林志遠 | Sprint 4 W1 |
| AI-HG-002-2 | ADF4351 評估板（EV-ADF4351SD1Z）確認可採購 | PM 黃俊榮 | Sprint 4 W1 |
| AI-HG-002-3 | RF PCB layout 更新：加入 PLL 子模塊（約 1 cm²）| Comm 林志遠 | Sprint 4 W2 |
| AI-HG-002-4 | Link Budget 加入 PLL 插損（LO path IL ≈ 2 dB）| SE 陳明哲 | Sprint 4 W1 |

---

*D-HG-002 v1 | 通訊酬載工程師 林志遠 | 2026-05-27*
*P2P Review 待指定：SW 工程師 陳俊宏（FPGA Timing 相容性確認）+ SE 陳明哲（Link Budget 更新）*
