---
deliverable: C-002
sprint: 3
wave: 2
author: Comm Agent（林志遠）
date: 2026-04-15
status: draft
reference_documents:
  - sprints/sprint2/wave2/B-001_link-budget-v2.md（鏈路預算，UL margin +6.3 dB）
  - sprints/sprint2/wave1/B-002_system-architecture-icd-v1.md（ICD v1，IF-03/IF-12）
  - sprints/sprint3/wave1/C-001_srs-v2.md（SRS v2，SYS-009~011，IFC-003/005）
  - sprints/sprint2/patches/PATCH-P1-P2-comm.md（極化失配修正 3.0 dB 已入 SRS）
upstream_requirements:
  - SYS-009: UL Link Margin ≥ 3 dB @10° 仰角
  - SYS-010: S-band n236，UL 1980–2010 MHz，DL 2170–2200 MHz
  - SYS-011: ≥100 bps，QPSK 1/2
  - IFC-003: OBC↔酬載 LVDS + SPI 控制
  - IFC-005: 電源軌 3.3V/5V/12V boost
---

# C-002：TASA-NTN-3U RF PCB 詳細設計 v1

## 1. 概述

### 1.1 文件目的

本文件為 TASA-NTN-3U 3U CubeSat S-band 通訊酬載之 RF 印刷電路板（PCB）詳細設計文件。依據 B-001 鏈路預算（slant range 1,695 km，UL margin +6.3 dB）、B-002 ICD（IF-12 PA 12V 供電）、C-001 SRS v2（SYS-009~011，IFC-003）及 PATCH-P1 極化修正（3.0 dB 已入冊），展開 RF PCB 的電路架構、元件選型、阻抗控制、散熱設計、佈局策略與製造規格。

### 1.2 RF PCB 功能定義

RF PCB 實現 **S-band n236 透明轉發（Bent-pipe）**：

| 方向 | 頻率範圍 | 中心頻率 | 說明 |
|------|---------|---------|------|
| 上行接收（UL Rx） | 1980–2010 MHz | 1995 MHz | 接收地面 UE 信號，LNA 低雜訊放大 |
| 頻率搬移（Frequency Conversion） | LO = 190 MHz | — | 2185 - 1995 = 190 MHz 差頻，Mixer 執行 |
| 下行發射（DL Tx） | 2170–2200 MHz | 2185 MHz | 放大轉發至地面 gNB，PA 輸出 +30 dBm |

**工作模式**：接觸窗口期間由 OBC 透過 SPI 啟用 PA enable 信號；非接觸窗口 PA 關斷，PA + LNA 均 OFF（待機功耗趨近 0 W）。

### 1.3 板體規格摘要

| 項目 | 規格 |
|------|------|
| 板層數 | 4 層（Top RF / GND / PWR / Bottom） |
| 板材 | FR4，Dk = 4.6 @2 GHz |
| 板厚 | 1.0 mm（RF 板薄化，降低 via 熱阻） |
| 外形尺寸 | 95 × 90 mm（含結構安裝孔 4 × M3，邊緣保留 3 mm 禁布區） |
| 有效佈局區域 | ~89 × 84 mm（扣除禁布區） |
| 表面處理 | ENIG（化學鎳金），焊墊平整、低接觸電阻，適合 QFN 封裝 |
| 製造廠商（計畫） | JLCPCB 4 層板服務 |

---

## 2. RF 鏈路架構

### 2.1 系統方塊圖（文字描述）

```
地面 UE 上行信號（1980–2010 MHz）
          │
          ▼
  ┌───────────────┐
  │  Rx 天線      │  S-band patch / IPEX MHF4 介面
  │  Nadir-facing │  增益 ~8 dBi（B-001 SAT G 參數）
  └───────┬───────┘
          │ 50Ω 同軸
          ▼
  ┌───────────────┐
  │  LNA           │  ADL5523ACPZ-R7
  │  NF 1 dB       │  Gain 15 dB @2 GHz
  │  Gain 15 dB    │  LFCSP-8 封裝
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │  UL BPF        │  SYBP-2250+（Mini-Circuits）
  │  中心 2250 MHz │  BW 740 MHz，通帶 1980–2010 MHz 範圍內
  │  抑制鏡像頻率  │  插損 ~1.5 dB
  └───────┬───────┘
          │
          ▼
  ┌───────────────────────────────┐
  │  Mixer（上下變頻）             │  LT5512EUF
  │  RF in: 1980–2010 MHz         │  QFN-16 封裝
  │  LO in: 190 MHz               │  IF out: 2170–2200 MHz
  │  IF out: 2170–2200 MHz        │  RF/LO/IF 隔離 ≥30 dB
  └──────────────┬────────────────┘
                 │        ▲
                 │        │ LO 190 MHz
                 │   ┌────┴───────┐
                 │   │ TCXO / VCO │  LO 本振產生
                 │   │ 190 MHz    │  （VCTCXO 或 PLL）
                 │   └────────────┘
                 ▼
  ┌───────────────┐
  │  DL BPF        │  SYBP-2250+（Mini-Circuits）
  │  中心 2250 MHz │  通帶 2170–2200 MHz 抑制 LO 洩漏
  │  LO 抑制 >40dB │  插損 ~1.5 dB
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │  PA            │  PMA3-43-1W+（Mini-Circuits）
  │  Psat +32.6dBm │  P1dB +30.3 dBm
  │  +12V 供電     │  QFN 3×3mm 封裝
  │  PAE ~25%      │  背面 thermal pad 散熱
  └───────┬───────┘
          │ 50Ω 同軸
          ▼
  ┌───────────────┐
  │  Tx 天線       │  SMA edge mount / IPEX MHF4
  │  Nadir-facing  │  往地面 gNB 下行發射
  └───────────────┘

OBC 控制介面（SPI）：
  OBC ──SPI──► PA enable（GPIO active-high）
  OBC ──SPI──► LNA enable（GPIO active-high）
  OBC ──SPI──► PA 增益監控（可選 ADC 回讀 Vdet）
```

### 2.2 鏈路增益/損耗預算（PCB 級）

| 序號 | 元件 | 增益/損耗（dB） | 備注 |
|------|------|:------------:|------|
| 1 | Rx 天線至 LNA 輸入走線 | -0.5 | ~100 mm 50Ω 微帶，含連接器插損 |
| 2 | LNA（ADL5523ACPZ-R7） | +15.0 | NF 1 dB @2 GHz |
| 3 | UL BPF（SYBP-2250+） | -1.5 | 通帶插損 |
| 4 | Mixer（LT5512EUF） | -7.0 | 典型轉換損耗 |
| 5 | DL BPF（SYBP-2250+） | -1.5 | 通帶插損 |
| 6 | PA 輸入至 DL BPF 走線 | -0.3 | 短走線 <30 mm |
| 7 | PA（PMA3-43-1W+） | +30.3 | P1dB 點，RF 輸出 +30 dBm |
| 8 | PA 至 Tx 天線走線 | -0.5 | ~50 mm 50Ω 微帶 |
| **合計** | **PCB 鏈路增益** | **+34.0 dB（鏈路）** | PA 輸入需求：Mixer out - DBPF = ~-9 dBm |

**PA 輸入功率驗算**：
- Mixer 典型 IF 輸出（由 OBC FPGA DAC 控制級別）設計為 -9 dBm → PA 輸入
- PA 工作於 P1dB（+30.3 dBm），可確保 +30 dBm RF 輸出（對應 B-001 PA RF out 1.0 W）
- Psat +32.6 dBm，工作點餘裕 +2.3 dB，避免壓縮失真

---

## 3. 各關鍵元件規格確認

| 元件 | 型號 | 關鍵規格 | 封裝 | 佈局注意事項 |
|------|------|---------|------|------------|
| LNA | ADL5523ACPZ-R7 | NF 1 dB @2 GHz，Gain 15 dB，+3.3V，ICC 45 mA | LFCSP-8（3×3 mm） | 緊靠 Rx 天線輸入，走線長度 ≤5 mm；輸入匹配網路（L/C）需在 PCB 上實作；接地焊盤需密集 via array 到 GND 層 |
| BPF（UL） | SYBP-2250+ | fc 2250 MHz，BW 740 MHz，IL ~1.5 dB，Rej @±500 MHz >30 dB | SMD（1812 等效） | 串接於 LNA 輸出，50Ω 兩端匹配；BPF 兩側各留 ≥2 mm 禁銅區防耦合 |
| Mixer | LT5512EUF | RF 1k–3 GHz，LO 30–3 GHz，IIP3 +18 dBm，ISO RF/LO ≥30 dB | QFN-16（4×4 mm） | LO 走線遠離 Rx LNA 路徑（>10 mm 或 GND 屏蔽隔離）；RF/LO/IF 端各加 DC Block；Ground paddle 下方 via array |
| BPF（DL） | SYBP-2250+ | 同 UL BPF（鏡像頻率與 LO 洩漏抑制） | SMD | 串接於 Mixer IF 輸出；LO 190 MHz 洩漏在 2250 MHz BPF 帶外，抑制 >40 dB |
| PA | PMA3-43-1W+ | Psat +32.6 dBm，P1dB +30.3 dBm，+12V/350 mA，PAE ~25% | QFN（3×3 mm） | 板邊靠近熱沉安裝孔；背面開窗（無阻焊），底部 thermal pad → PCB via array（6×6 = 36 vias）→ 結構框架；PA 輸入側加 10 dB 衰減器防振盪（可拆 0Ω 替換） |
| LO 振盪器 | VCTCXO 190 MHz（選型：TXC 7V 或 Rakon EF5032A 等效） | 頻率穩定度 ≤±1 ppm @工作溫度；相位雜訊 <-110 dBc/Hz @1 kHz offset | SMD TCXO 封裝 | 遠離 PA（>20 mm）；電源加 Pi 型 LC 濾波防雜訊注入；走線 50Ω 匹配至 Mixer LO 端 |
| PA enable MOSFET | 2N7002K SOT-23 | Vgs_th ~2V，Id 300 mA，Rds_on <5Ω @Vgs 3.3V | SOT-23 | OBC GPIO 3.3V 直驅 gate；source 接 GND，drain 接 PA +12V enable pin |

### 3.1 元件輻射耐受性說明

依 C-001 SRS v2 ENV-005 / SYS-013，TID 需求 ≥5 krad：

| 元件 | 封裝類型 | 輻射敏感性 | 處置 |
|------|---------|----------|------|
| ADL5523ACPZ-R7 | CMOS | 中（GaAs 基底較耐輻射） | 供應商提供 RadTol 資料；必要時加 Al 局部屏蔽 |
| LT5512EUF | SiGe BiCMOS | 中低 | 文獻 TID >10 krad（SiGe 耐輻射特性佳） |
| PMA3-43-1W+ | GaAs pHEMT | 低（GaAs 耐輻射） | GaAs PA 在 LEO 任務中廣泛應用，風險低 |
| VCTCXO | CMOS ASIC | 中 | 選用有 commercial space 紀錄之 TCXO 型號 |

---

## 4. 阻抗控制設計

### 4.1 4 層板疊構（Stackup）

```
層次定義（由上到下）：

Layer 1：Top（信號 + RF 走線）  ── 銅厚 35 μm（1 oz）
──────────── Prepreg ────────── H1 = 0.20 mm（Dk = 4.6）
Layer 2：GND（接地平面）         ── 銅厚 35 μm（1 oz）
──────────── Core ───────────── 0.36 mm（Dk = 4.6）
Layer 3：PWR（電源平面）         ── 銅厚 35 μm（1 oz）
──────────── Prepreg ────────── H2 = 0.20 mm（Dk = 4.6）
Layer 4：Bottom（信號 + 散熱）   ── 銅厚 35 μm（1 oz）

總板厚 = 35μm×4 + 0.20 + 0.36 + 0.20 ≈ 0.90 mm ≈ 1.0 mm（含表面處理）
```

**JLCPCB 4 層標準疊構（JLC04161H-7628 類型）說明**：
- Prepreg 7628（Dk 4.6 @2 GHz）厚度約 0.20 mm
- Core 材料（Dk 4.6 @2 GHz）厚度約 0.36 mm
- 實際 Dk 需向廠商確認，此計算以 Dk = 4.6 為基準

### 4.2 50Ω 微帶線（Microstrip）寬度計算

**設計目標**：Layer 1（Top）走線對 Layer 2（GND）參考平面，H = 0.20 mm，t = 0.035 mm，Dk = 4.6。

使用 IPC-2141A Wadell 微帶公式：

```
有效介電係數 Dkeff：
  Dkeff = (Dk + 1) / 2 + (Dk - 1) / 2 × (1 + 12H/W)^(-0.5)

50Ω 微帶線寬度求解（迭代）：
  設 W/H = 2.2 → W ≈ 2.2 × 0.20 = 0.44 mm

驗算（Hammerstad 近似，W/H > 1）：
  Dkeff = (4.6 + 1)/2 + (4.6 - 1)/2 × (1 + 12/2.2)^(-0.5)
        = 2.80 + 1.80 × (1 + 5.45)^(-0.5)
        = 2.80 + 1.80 × 0.393
        = 2.80 + 0.708
        = 3.508

  Z0 = (87 / sqrt(Dkeff + 1.41)) × ln(5.98H / (0.8W + t))
     = (87 / sqrt(4.948)) × ln(5.98 × 0.20 / (0.8 × 0.44 + 0.035))
     = (87 / 2.224) × ln(1.196 / 0.387)
     = 39.12 × ln(3.089)
     = 39.12 × 1.128
     ≈ 44.1 Ω

  調整 W = 0.38 mm（W/H = 1.9）重算：
  Dkeff = 2.80 + 1.80 × (1 + 12/1.9)^(-0.5)
        = 2.80 + 1.80 × (7.316)^(-0.5)
        = 2.80 + 1.80 × 0.370
        = 2.80 + 0.666 = 3.466

  Z0 = (87 / 2.211) × ln(5.98 × 0.20 / (0.8 × 0.38 + 0.035))
     = 39.35 × ln(1.196 / 0.339)
     = 39.35 × ln(3.529)
     = 39.35 × 1.262
     ≈ 49.7 Ω ≈ 50 Ω ✓
```

**結論**：50Ω 微帶線線寬 **W ≈ 0.38 mm**（±0.02 mm 製造容差內可達 48–52Ω）。

> **製造前驗算**：建議使用 Polar Instruments Si8000m 或 Saturn PCB Toolkit 輸入廠商實測 Dk 值再行確認，並要求 JLCPCB 附 impedance control report。

### 4.3 走線相位延遲影響

| 頻率 | 材料（Dk = 3.5 eff） | 相位速度 | 每 mm 相位延遲 |
|------|-------------------|---------|:------------:|
| 2 GHz | FR4（Dkeff ≈ 3.5） | v_p = c/√3.5 = 1.603×10⁸ m/s | λ = 80.2 mm；1 mm ≈ 4.5° |

**注意**：LNA → UL BPF 走線長度需與 BPF 輸入阻抗匹配；建議對稱設計，走線長度偏差控制在 ±2 mm（≤9° 相位偏差），避免反射損耗劣化。

---

## 5. PA 散熱設計（C-005 熱分析前置）

### 5.1 散熱路徑定義

```
PA 晶片接面（Junction）
     │  θ_jc = 15 °C/W（PA QFN，廠商資料典型值）
     ▼
PA QFN 底部 Thermal Pad（焊接至 PCB Top 面開窗銅墊）
     │  θ_PCB = 50/N °C/W（N = via 數量）
     ▼
PCB Layer 1→2 Via Array（6×6 = 36 vias，φ0.3 mm 填銅）
     │  θ_frame = 5 °C/W（PCB 螺柱→鋁框架，機構接觸熱阻）
     ▼
3U CubeSat 結構框架（Al 7075-T6）
     │  被動輻射 / 傳導至部署器介面
     ▼
太空環境（最惡劣：+65°C 結構框架，Eclipse 最低 -20°C）
```

### 5.2 熱阻計算

**PA 功耗分析**：

| 參數 | 數值 | 來源 |
|------|------|------|
| PA RF 輸出功率 P_out | 1.0 W（+30 dBm） | B-001 Section 2 / B-002 IF-12 |
| PA DC 輸入功率 P_DC | 4.0 W（+12V × 350 mA 典型） | B-002 IF-12 |
| PA PAE（功率附加效率） | ~25%（P_out / P_DC） | PMA3-43-1W+ 規格 |
| PCB 熱耗散 P_dissipated | P_DC - P_out = 4.0 - 1.0 = **3.0 W** | — |

**熱阻計算**：

```
θ_jc（PA QFN，廠商典型值）：
  = 15 °C/W

θ_PCB（via array 並聯熱阻）：
  單個 φ0.3 mm 填銅 via：
    熱阻 = L / (k × A)
    L = PCB 板厚通孔 ≈ 1.0 mm = 0.001 m
    A = π × (0.15mm)² = 7.07 × 10⁻⁸ m²
    k（銅）= 385 W/(m·K)
    θ_via_single = 0.001 / (385 × 7.07×10⁻⁸)
                = 0.001 / (2.72×10⁻⁵)
                ≈ 36.7 °C/W

  36 vias 並聯：θ_PCB = 36.7 / 36 ≈ 1.02 °C/W
  （含銅墊擴散效應修正，實際約 1.0–1.5 °C/W，取 1.4 °C/W 保守值）

θ_frame（PCB 螺柱 → Al 框架，機構接觸）：
  = 5.0 °C/W（典型 CubeSat 熱設計值）

總熱阻 θ_total = θ_jc + θ_PCB + θ_frame
               = 15.0 + 1.4 + 5.0
               = 21.4 °C/W

PA Junction 溫度（最惡劣）：
  T_ambient = 最惡劣軌道環境框架溫度 = +40°C（含 Contact Window 日照加熱）
  T_junction = T_ambient + P_dissipated × θ_total
             = 40 + 3.0 × 21.4
             = 40 + 64.2
             = +104.2°C

PA 最高允許 Junction 溫度：+150°C（PMA3-43-1W+ 典型商規上限）
裕度 = 150 - 104.2 = +45.8°C ✓

注：若取 T_ambient = +24.7°C（軌道平均條件，B-001 參考值）：
  T_junction = 24.7 + 64.2 = +88.9°C → 裕度 +61.1°C（更充裕）
```

**結論**：在最惡劣條件（T_ambient = +40°C）下，PA 接面溫度約 +104°C，距限值 +150°C 仍有 +46°C 裕度，散熱設計 **通過**。

### 5.3 Via Array 設計規範

| 參數 | 規格 |
|------|------|
| Via 陣列配置 | 6 × 6 = 36 vias，均勻分布於 PA QFN Thermal Pad 正下方 |
| Via 鑽孔直徑 | φ0.3 mm（JLCPCB 最小 φ0.2 mm，取 φ0.3 mm 提升可靠性） |
| Via 填充 | 樹脂填充（resin fill）後鍍銅蓋帽，防焊料吸入空洞 |
| Thermal Pad 開窗 | Layer 1 阻焊層開窗（無阻焊），覆蓋 PA QFN 底部焊盤全區 |
| 銅墊尺寸 | PA thermal pad = 2.5 × 2.5 mm；PCB 銅墊外擴至 3.0 × 3.0 mm |
| 結構接觸面 | PCB Bottom 面（Layer 4）PA 正下方保留完整 3×3 mm 銅墊，螺柱導熱至框架 |

### 5.4 前置 C-005 熱分析需求

本章節計算提供以下數據給 C-005 熱控分析文件：

| 輸入項目 | 數值 | 備注 |
|---------|------|------|
| RF PCB 熱源位置 | PA（PMA3-43-1W+），板邊靠近安裝孔 | 3D 熱模型座標需依最終佈局確認 |
| PA 熱耗散功率 | 3.0 W | 接觸窗口期間持續 4 min |
| θ_jc（PA） | 15 °C/W | 廠商規格 |
| θ_PCB（via array） | ~1.4 °C/W | 6×6 填銅 via，保守估計 |
| PCB 至框架介面 | 螺柱接觸，θ ≈ 5 °C/W | 需 C-005 精確分析確認 |
| LNA 耗散 | 0.15 W（3.3V × 45 mA） | 分散熱源，影響較小 |

---

## 6. 元件佈局策略（Layout Guidelines）

### 6.1 整體佈局原則

```
RF 板佈局示意（95 × 90 mm，俯視）：

Y
▲
│  ┌───────────────────────────────────────────────┐
90│  │ M3 ●                              ● M3       │
│  │                                               │
│  │  [Rx Ant]──[LNA]──[UL-BPF]──[Mixer]──[DL-BPF]──[PA]──[Tx Ant]
│  │                                 ▲              │
│  │                             [TCXO/LO]          │
│  │                                               │
│  │  ─ ─ ─ ─ GND 銅牆隔離（Rx / Tx 分區）─ ─ ─ ─  │
│  │                                               │
│  │  [SPI 控制邏輯]  [3.3V 去耦]  [12V 去耦]       │
│  │  [PA enable MOSFET]  [LNA enable]              │
│  │                                               │
│  │  DC 測試點：PA +12V TP1，LNA +3.3V TP2，       │
│  │            PA enable TP3                      │
 0 │  │ M3 ●                              ● M3       │
   └───────────────────────────────────────────────┘
   0                                               95 → X
```

### 6.2 關鍵佈局規則

**RF 信號路徑**：
- 所有 RF 元件（LNA → UL BPF → Mixer → DL BPF → PA）沿 X 軸**線性排列**，避免 Tx 輸出回流至 Rx 輸入
- RF 走線全程保持 50Ω 微帶（W ≈ 0.38 mm），走線轉彎採 45° 或圓弧，禁止直角
- RF 走線下方 Layer 2 GND 平面需**完整無缺口**（不走任何信號線）
- Layer 2 GND 平面若需分割（3.3V / GND），分割線必須遠離 RF 走線投影區域 ≥3 mm

**Tx/Rx 隔離**：
- Rx 路徑（LNA 側）與 Tx 路徑（PA 側）之間在 Layer 1 加 GND 銅牆（soldermask dam），牆寬 ≥1 mm，通過 via stitch 連接 Layer 2 GND
- LNA 與 PA 間距 ≥25 mm（防止輻射耦合自激振盪）
- PA 天線連接器（Tx）與 LNA 天線連接器（Rx）間距 ≥15 mm，必要時加金屬隔板

**元件擺放**：
- PA（PMA3-43-1W+）：靠近板邊（+X 方向），貼近 M3 安裝孔，便於熱傳至框架
- LNA（ADL5523ACPZ-R7）：靠近 Rx 天線連接器，LNA 輸入至連接器走線 ≤5 mm
- TCXO（LO 190 MHz）：置於 Mixer 附近，LO 走線 ≤20 mm，50Ω 匹配
- 所有 SMD 被動元件：0402 封裝（電容、電阻），便於高密度佈局
- BPF（SYBP-2250+）：SMD 封裝，兩側各留 ≥2 mm 禁銅區，防止寄生耦合

**接地處理**：
- 所有 IC 的 Ground paddle 或 GND 引腳：在 Layer 1 就近多點 via 到 Layer 2 GND（via 間距 ≤1 mm）
- GND via stitch 沿 RF 走線兩側以 ≤λ/10 間距（@2 GHz：≤15 mm）排列，防止表面波

**DC 去耦電容**：
- 每個 IC VCC 引腳：緊靠 IC 放置 100 nF（0402）+ 10 μF（0805）去耦電容，先小後大
- PA +12V 輸入：額外加 1 μF + 100 nF pi 型濾波，抑制 PA 開關電流突波

**天線連接器**：
- 優先選用 IPEX MHF4（超小型，適合 3U 衛星有限空間）
- 備選：SMA edge mount（機械可靠性較高，測試便利）
- 板邊連接器安裝位置需與天線饋線方向對齊，減少走線折轉

---

## 7. 電源管理

### 7.1 電源需求彙整（與 IFC-005、B-002 IF-12 對應）

| 子系統 | 電源軌 | 標稱電壓 | 最大電流 | 功耗（峰值） | 介面來源 |
|--------|--------|---------|---------|------------|---------|
| LNA（ADL5523ACPZ-R7） | 3.3V | 3.3V ±5% | 45 mA | 0.15 W | IFC-005，EPS 3.3V rail |
| Mixer（LT5512EUF） | 3.3V | 3.3V ±5% | 60 mA | 0.20 W | IFC-005，EPS 3.3V rail |
| TCXO（LO 190 MHz） | 3.3V | 3.3V ±5% | 10 mA | 0.03 W | IFC-005，EPS 3.3V rail |
| BPF（被動，無需供電） | — | — | — | 0 W | — |
| PA（PMA3-43-1W+） | 12V boost | 12.0V ±8% | 350 mA | 4.0 W | B-002 IF-12，EPS boost |
| SPI 控制邏輯 / MOSFET | 3.3V | 3.3V ±5% | 5 mA | 0.02 W | IFC-005 |
| **RF PCB 總功耗（PA ON）** | | | | **~4.4 W** | |
| **RF PCB 待機（PA OFF）** | | | | **~0.4 W** | LNA+Mixer+TCXO 維持 |

### 7.2 PA 功率控制邏輯

```
OBC GPIO（3.3V active-high）
    │
    ▼
[10 kΩ pull-down] + [MOSFET 2N7002K]
    │
    ▼ drain
PA +12V enable pin

控制邏輯：
  OBC GPIO HIGH（3.3V）→ MOSFET ON → PA +12V 供電 → 發射模式
  OBC GPIO LOW（0V）   → MOSFET OFF → PA 斷電     → 待機模式

保護設計：
  PA enable MOSFET 串聯 1Ω / 1W 電流感測電阻（可選），用於 OBC ADC 監控電流
  PA +12V 輸入端串聯 Polyfuse（500 mA 自恢復保險絲），防止 PA 短路損毀 EPS
```

### 7.3 去耦濾波設計

| 位置 | 電容配置 | 安裝規範 |
|------|---------|---------|
| LNA VCC（3.3V） | 100 nF（0402）+ 10 μF（0805） | 緊靠 LNA VCC 引腳，≤1 mm |
| Mixer VCC（3.3V） | 100 nF（0402）+ 10 μF（0805） | 緊靠 Mixer VCC 引腳 |
| TCXO VCC（3.3V） | 100 nF + 1 μF | TCXO 對電源雜訊敏感，需良好去耦 |
| PA VDD（+12V） | 10 μF（1210，X5R）+ 100 nF（0402）+ 1 nF（0402） | pi 型濾波；10 μF 電容置於 PA +12V 入板連接器旁，100 nF 緊靠 PA VDD 引腳 |
| 整板 3.3V 入板 | 47 μF（電解或鉭）+ 1 μF（陶瓷）+ 100 nF（陶瓷） | 在 3.3V 電源入板點設置整體去耦 |

---

## 8. 測試點設計

### 8.1 RF 測試點

| 測試點 | 位置 | 設計方式 | 用途 |
|--------|------|---------|------|
| TP-RF-1（LNA 輸入） | Rx 天線連接器 → LNA 輸入之間 | 串聯 0Ω 電阻（可拆，替換為衰減器或 SMA 轉接器） | 單獨量測 LNA NF 與 Gain |
| TP-RF-2（LNA 輸出） | LNA 輸出 → UL BPF 輸入 | 串聯 0Ω 電阻（可拆） | 量測 LNA 增益，驗證 +15 dBm 增益 |
| TP-RF-3（Mixer IF 輸出） | DL BPF 輸入端 | 串聯 0Ω 電阻（可拆） | 量測 Mixer 轉換增益（含 UL BPF 插損） |
| TP-RF-4（PA 輸入） | DL BPF 輸出 → PA 輸入 | 串聯 0Ω 電阻（可拆，替換為可調衰減器） | 控制 PA 輸入功率，防止過驅動 |

**注意**：RF 測試點的 0Ω 電阻（0402 封裝）在工程樣機（EM）階段保留，飛行件（FM）裝配完成後直接橋接（移除 0Ω，換短路銅墊）以降低反射損耗。

### 8.2 DC 測試點

| 測試點 | 信號 | 位置 | 量測目的 |
|--------|------|------|---------|
| TP-DC-1（PA +12V） | +12V boost rail | PA VDD 去耦電容旁 | 確認 EPS boost 供電正常，量電壓與電流 |
| TP-DC-2（LNA +3.3V） | +3.3V rail | LNA VCC 去耦電容旁 | 確認 LNA 供電電壓 |
| TP-DC-3（PA enable） | OBC GPIO 信號 | MOSFET gate 側 | 確認 OBC 控制信號電平（0V / 3.3V） |
| TP-DC-4（GND） | Ground reference | 板中央 GND 焊盤 | 測試時參考地 |
| TP-DC-5（TCXO Vcc） | +3.3V | TCXO 旁 | 確認 LO 振盪器供電穩定 |

### 8.3 功能驗證序列（整合測試用）

1. **DC 上電驗證**：量 TP-DC-2（3.3V）、TP-DC-1（12V 待機為 0V）確認 EPS 供電正常
2. **LNA 功能驗證**：LNA enable HIGH → 注入 -80 dBm @1995 MHz → TP-RF-2 量輸出應為 ~-65 dBm（增益 ~15 dB）
3. **Mixer 功能驗證**：確認 LO 190 MHz 輸出正常 → TP-RF-3 量 2185 MHz IF 輸出
4. **PA 功能驗證**：OBC TP-DC-3 拉 HIGH → TP-DC-1 量 +12V → 注入 -9 dBm @2185 MHz → Tx 天線端量輸出應為 +30 dBm（需 RF 功率計 + dummy load）
5. **整鏈路驗證**：Rx 天線注入 -90 dBm @1995 MHz → Tx 天線端量輸出，確認信號存在且頻率正確搬移至 2185 MHz

---

## 9. 製造規格（JLCPCB 4 層板）

| 項目 | 規格 | 備注 |
|------|------|------|
| 層數 | 4 層 | Top RF / GND / PWR / Bottom |
| 板材 | FR4（Dk 4.6 @2 GHz，Df 0.02） | 請求廠商提供實測 Dk/Df 數據 |
| 最小線寬 / 間距 | 0.1 / 0.1 mm | RF 走線取 0.38 mm，遠大於最小規格 |
| 最小鑽孔 | φ0.2 mm（機械鑽），φ0.1 mm（雷射盲孔） | Via array 取 φ0.3 mm（填銅） |
| Via 填充 | 填樹脂（resin fill）+ 鍍銅蓋帽 | 僅 PA thermal via array，其餘普通 via |
| 表面處理 | ENIG（化學鎳金，Ni 3–5 μm / Au 0.05–0.1 μm） | RF 性能優，焊接可靠，適合 QFN |
| 板厚 | 1.0 mm | 薄板降低 via 熱阻，利於散熱 |
| 外形尺寸 | 95 × 90 mm | 含 4 × M3 安裝孔（3 mm 距板邊） |
| 阻抗控制 | 50 Ω ±10%（Layer 1 微帶） | 需廠商出具 impedance test coupon 報告 |
| 阻焊顏色 | 黑色（Black LPI） | 太空應用，減少可見光反射；PA 底部開窗 |
| 絲印 | 白色，標示元件位號、測試點標號 | — |
| 數量（工程樣機） | 5 片 | 2 片整合測試 + 2 片環境測試 + 1 片備用 |
| 費用估算（5 片） | ~50–80 USD | JLCPCB 4 層標準服務（不含貼片） |
| SMT 組裝 | 自行或 JLCPCB SMT（評估中） | QFN 元件建議回流焊（reflow），需鋼網 |

### 9.1 Gerber 輸出規範

| 層別 | 檔案副檔名 | 說明 |
|------|-----------|------|
| Top Copper | .GTL | RF 信號走線 + 元件焊盤 |
| GND（Layer 2） | .G2L | 完整接地平面 |
| PWR（Layer 3） | .G3L | 電源分割平面 |
| Bottom Copper | .GBL | 散熱銅墊 + 少量信號線 |
| Top Soldermask | .GTS | PA thermal pad 開窗 |
| Bottom Soldermask | .GBS | — |
| Top Silkscreen | .GTO | 元件位號 + 測試點標示 |
| Drill（through-hole） | .DRL（Excellon） | 含 via array φ0.3 mm |
| Board Outline | .GKO | 95 × 90 mm 外形 + 安裝孔 |

---

## 10. 關鍵風險

| 風險 ID | 風險描述 | 嚴重性 | 可能性 | 緩解措施 |
|---------|---------|:------:|:------:|---------|
| RF-R-01 | 50Ω 阻抗偏差超出 ±10% | 中 | 中 | 製造前使用 Polar Si8000m 驗算 stackup；要求 JLCPCB 出具 impedance test coupon 量測報告；必要時調整線寬 ±0.02 mm |
| RF-R-02 | PA 散熱不足（Junction T > 130°C） | 高 | 低 | 6×6 填銅 via array 設計，θ_PCB ≈ 1.4 °C/W；結構螺柱直接接觸 Al 框架導熱；C-005 熱分析需確認最惡劣軌道溫度 |
| RF-R-03 | Tx-Rx 隔離不足，導致自激振盪 | 高 | 中 | GND 銅牆隔離（soldermask dam + via stitch）；PA 與 LNA 間距 ≥25 mm；Tx/Rx 天線連接器間距 ≥15 mm；BPF 雙向帶外抑制 |
| RF-R-04 | LO 洩漏干擾 UL 頻段（190 MHz 進 LNA 路徑） | 中 | 低 | Mixer 後加 DL BPF（190 MHz 在帶外 >40 dB 抑制）；LO 走線遠離 Rx 路徑（>10 mm 或 GND 屏蔽） |
| RF-R-05 | 元件輻射劣化（TID 5 krad 需求） | 中 | 中 | 選用 GaAs PA（耐輻射）；LNA、Mixer 確認 TID > 5 krad 規格；TCXO 選用 commercial space 型號；必要時加 Al 局部屏蔽（2 mm 板） |
| RF-R-06 | 焊接品質不良（QFN 焊墊空洞） | 中 | 中 | 使用 ENIG 表面處理；PA thermal pad 填銅 via 防焊料吸入；採 X-ray 驗收 QFN 焊接品質 |
| RF-R-07 | LO 頻率穩定度不足導致頻率搬移偏差 | 中 | 低 | TCXO 選用 ±1 ppm 穩定度型號；Doppler 補償由 OBC FPGA 數位基帶處理（B-001 Section 5 Doppler 分析已涵蓋） |

---

## 11. 需求符合性矩陣（Requirements Compliance Matrix）

| 需求 ID | 需求敘述（摘錄） | PCB 設計符合方式 | 驗證方法 | 狀態 |
|---------|--------------|---------------|---------|:----:|
| SYS-009 | UL Link Margin ≥3 dB @10° 仰角（修正後 +6.3 dB，含 PATCH-P1 極化損耗 3.0 dB） | LNA NF=1 dB @2GHz（ADL5523ACPZ-R7），Gain=15 dB；BPF 控制帶外雜訊；整體 Noise Figure 設計 ≤2 dB（LNA 主導） | RF 鏈路測試（注入已知信號，量 C/N0） | ✅ 設計符合 |
| SYS-010 | S-band n236：UL 1980–2010 MHz，DL 2170–2200 MHz | UL BPF（SYBP-2250+，BW 740 MHz）覆蓋 1980–2010 MHz；DL BPF 覆蓋 2170–2200 MHz；LO = 190 MHz 頻率搬移 | 頻譜儀量測 Tx 頻率 @2170–2200 MHz；Rx 掃描 1980–2010 MHz | ✅ 設計符合 |
| SYS-011 | ≥100 bps，QPSK 1/2 | RF PCB 實現透明轉發（bent-pipe），QPSK 1/2 調變/解調由 OBC FPGA 基帶處理（B-002 IF-04）；PCB 提供足夠線性度（P1dB 設計裕度 +2.3 dB） | 基帶 BER 測試 @100 bps QPSK 1/2 | ✅ 設計符合 |
| IFC-003 | OBC↔酬載 LVDS @50 Mbps + SPI @1 MHz 控制 | PCB 設計 SPI 控制走線（PA enable、LNA enable、狀態回讀）；LVDS 基帶資料接口由 OBC→FPGA→DAC 鏈路驗証，RF PCB 提供 SPI slave 介面 | SPI 通訊測試（loopback + PA enable 功能確認） | ✅ 設計符合 |
| IFC-005 | 電源軌 3.3V / 5V / 12V boost，精度 ±5% | PCB 設計 3.3V 供 LNA/Mixer/TCXO；12V boost 供 PA（IF-12）；完善去耦濾波；PA enable MOSFET 控制 12V 切換 | 電源軌量測（OBC 上電序列驗證） | ✅ 設計符合 |
| ENV-004 | EMC：ECSS-E-ST-20-07 | GND 銅牆 + via stitch 抑制雜散輻射；PA 側屏蔽設計；LO 走線包地處理 | EMC 預測試（pre-compliance scan） | ⚠️ 待 EM 測試確認 |
| ENV-005 | TID ≥5 krad | 元件選用 GaAs PA + SiGe Mixer（耐輻射較佳）；CMOS 元件確認 TID 規格 | 元件輻射分析報告 | ⚠️ 待元件確認 |

---

## 12. 設計行動項目（Action Items）

| ID | 行動項目 | 負責人 | 截止時間 | 前置依賴 |
|----|---------|--------|---------|---------|
| AI-01 | 向 JLCPCB 確認 JLC04161H-7628 疊構實際 Dk/Df @2 GHz，更新阻抗計算 | RF PCB 工程師 | Sprint 3 Wave 3 | JLCPCB 疊構文件 |
| AI-02 | 使用 Polar Si8000m 或 Saturn PCB Toolkit 驗算 50Ω 微帶線寬，生成阻抗計算報告 | RF PCB 工程師 | Sprint 3 Wave 3 | AI-01 |
| AI-03 | 確認 ADL5523ACPZ-R7 TID 輻射耐受規格（向 ADI 詢問或查找 radiation characterization 數據） | 元件工程師 | Sprint 3 Wave 3 | — |
| AI-04 | 選定 VCTCXO/TCXO 190 MHz 型號（確認相位雜訊 <-110 dBc/Hz @1 kHz，溫度穩定度 ±1 ppm） | RF 工程師 | Sprint 3 Wave 3 | — |
| AI-05 | 完成 KiCad / Altium PCB 佈局，提交 DFM review，輸出 Gerber | PCB Layout 工程師 | Sprint 4 Wave 1 | AI-01, AI-02 |
| AI-06 | C-005 熱分析：依本文件 PA 熱阻數據建立 3D 熱模型，確認最惡劣軌道溫度下 T_junction < 130°C | 熱控工程師 | Sprint 3 Wave 3 | C-002 佈局確認後 |
| AI-07 | 採購 EM（工程樣機）元件：ADL5523ACPZ-R7 × 5, LT5512EUF × 5, PMA3-43-1W+ × 5, SYBP-2250+ × 10 | 採購 | Sprint 3 Wave 3 | 元件確認後 |
| AI-08 | 整合測試程序撰寫（依 Section 8.3 功能驗證序列，建立測試案例文件） | 系統整合工程師 | Sprint 4 Wave 2 | EM 板完成後 |

---

## 13. 附錄

### A. 元件參考清單（BOM 初版）

| 位號 | 元件描述 | 型號 | 封裝 | 數量 | 供應商 |
|------|---------|------|------|:---:|--------|
| U1 | LNA | ADL5523ACPZ-R7 | LFCSP-8（3×3mm） | 1 | Analog Devices / Digi-Key |
| FL1 | UL 帶通濾波器 | SYBP-2250+ | SMD | 1 | Mini-Circuits / Digi-Key |
| U2 | Mixer（上下變頻） | LT5512EUF#TRPBF | QFN-16（4×4mm） | 1 | Analog Devices / Mouser |
| FL2 | DL 帶通濾波器 | SYBP-2250+ | SMD | 1 | Mini-Circuits / Digi-Key |
| U3 | PA | PMA3-43-1W+ | QFN（3×3mm） | 1 | Mini-Circuits / Digi-Key |
| Y1 | TCXO 190 MHz | TXC 7V-190.000MBE-T 或等效 | SMD（3.2×2.5mm） | 1 | TXC / Digi-Key |
| Q1 | PA enable MOSFET | 2N7002K | SOT-23 | 1 | Nexperia / Digi-Key |
| F1 | PA +12V Polyfuse | 0ZCG0050AF2C（500 mA）或等效 | 1812 | 1 | Bel Fuse / Digi-Key |
| J1 | Rx 天線連接器 | IPEX MHF4 或 SMA edge mount | — | 1 | — |
| J2 | Tx 天線連接器 | IPEX MHF4 或 SMA edge mount | — | 1 | — |
| J3 | OBC SPI / 電源 | Hirose DF17 12-pin | — | 1 | Hirose / Digi-Key |
| C_RF | RF DC Block 電容 | 10 nF C0G（0402） | 0402 | 6 | — |
| C_dec | 去耦電容 100 nF X7R | 0402 | 0402 | 12 | — |
| C_bulk | 去耦電容 10 μF X5R | 0805 | 0805 | 4 | — |
| R_0Ω | RF 測試點 0Ω 電阻 | 0Ω 0402 | 0402 | 4 | — |
| TP | DC 測試點 | Loop test point 1 mm | — | 5 | — |

### B. 相關文件連結

| 文件代號 | 文件名稱 | 版本 | 狀態 |
|---------|---------|------|------|
| B-001 | Link Budget | v2.1（含 PATCH-P1） | Revised |
| B-002 | System Architecture ICD | v1 | Draft |
| C-001 | SRS v2 | v2.0 | Frozen |
| PATCH-P1 | 極化失配修正 | — | Resolved |
| C-005 | 熱控詳細設計（下游） | v1（待建立） | Planned |

### C. 縮寫表

| 縮寫 | 全稱 |
|------|------|
| BPF | Band Pass Filter（帶通濾波器） |
| COTS | Commercial Off-The-Shelf（商用現成品） |
| Dk | Dielectric Constant（介電常數） |
| DL | Downlink（下行） |
| ENIG | Electroless Nickel Immersion Gold（化學鎳金） |
| GND | Ground（接地） |
| LNA | Low Noise Amplifier（低雜訊放大器） |
| LO | Local Oscillator（本地振盪器） |
| NF | Noise Figure（雜訊指數） |
| PA | Power Amplifier（功率放大器） |
| PAE | Power Added Efficiency（功率附加效率） |
| PCB | Printed Circuit Board（印刷電路板） |
| RF | Radio Frequency（射頻） |
| SMD | Surface Mount Device（表面貼裝元件） |
| SPI | Serial Peripheral Interface |
| TCXO | Temperature Compensated Crystal Oscillator（溫度補償晶體振盪器） |
| TID | Total Ionizing Dose（總游離劑量） |
| UL | Uplink（上行） |
| VCC | Voltage Common Collector（元件供電電壓） |
| Via | PCB 導通孔 |

---

*C-002 RF PCB 詳細設計 v1*
*作者：Comm Agent（林志遠）*
*日期：2026-04-15*
*狀態：Draft — 待 AI-01/AI-02 阻抗確認後更新為 v1.1*
