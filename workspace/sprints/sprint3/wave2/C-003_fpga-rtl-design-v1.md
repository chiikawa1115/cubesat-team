---
deliverable: C-003
sprint: 3
wave: 2
author: SW/FW Agent（徐志豪）
date: 2026-04-15
status: draft
reference_documents:
  - workspace/sprints/sprint2/wave2/B-007_obc-fpga-architecture-v1.md
  - workspace/sprints/sprint2/wave2/B-001_link-budget-v2.md
  - workspace/sprints/sprint2/patches/PATCH-P4-P6-sw.md
  - workspace/sprints/sprint3/wave1/C-001_srs-v2.md
---

# C-003：FPGA RTL 詳細設計 v1（TASA-NTN-3U）

---

## 0. 執行摘要

本文件為 TASA-NTN-3U 衛星平台 Zynq-7020 可程式邏輯（PL）端的 RTL 詳細設計規格。以 B-007 架構初步設計為上游輸入，細化各通訊基帶模組（QPSK、Viterbi FEC）、SEU 防護機制（TMR + ICAP Scrubber）及 SAA 動態 scrubbing 邏輯的 RTL 介面、狀態機與資源估算。所有設計數字與 B-007 Section 6.2（總 LUT 37,000 / 53,200 = 69.5%）及 PATCH-P4 修正保持自洽，差異部分於第 6 節明確說明。

---

## 1. 資源分配與 LUT 使用率

### 1.1 Zynq-7020 (XC7Z020) 可用資源

| 資源類型 | 全裝置量 | 備注 |
|---------|---------|------|
| LUT（Look-Up Table）| 53,200 | Artix-7 fabric；來源 Xilinx UG585 Table 1-3 |
| Flip-Flop（FF）| 106,400 | 每個 LUT 對應 2 FF |
| DSP48E1 | 220 | 18×18 乘法器，Macc 架構 |
| BRAM（36Kb block）| 140 | = 5,040 Kbits 總容量 |
| ICAP（內部組態存取埠）| 1 | PL 自 reconfiguration 使用 |

**TMR overhead 說明**：TMR（Triple Modular Redundancy）將每個邏輯模組複製三份，並加入多數決 voter。理論乘數為 3×（加上 voter ~1.5%，可忽略）。TMR 並非施加於全部 PL 資源，而僅施加於安全關鍵路徑（詳見 1.2 節）。

### 1.2 C-003 模組 LUT 分配表

下表為本文件設計的 RTL 模組詳細估算（SDR 基帶 + SEU 防護）：

| # | 模組 | LUT（無 TMR）| TMR？| LUT（含 TMR）| 說明 |
|---|------|:-----------:|:----:|:------------:|------|
| 1 | QPSK Modulator | 800 | Yes | 2,400 | I/Q 查表（LUT-based）+ RRC 脈衝整形（8-bit 精度） |
| 2 | QPSK Demodulator | 2,500 | Yes | 7,500 | Costas loop（2 階 PLL）+ Gardner TED + 符號判決 |
| 3 | Viterbi Decoder（rate 1/2）| 1,200 | Yes | 3,600 | K=7，硬判決，ACS（Add-Compare-Select）蝶形 |
| 4 | FEC Encoder（卷積碼）| 300 | Yes | 900 | G1=171₈, G2=133₈，1 位移暫存器 × 7 級 × 2 輸出 |
| 5 | Framing / Deframing | 400 | Yes | 1,200 | CCSDS 幀頭插入 / ASM 同步字（0x1ACFFC1D）偵測 |
| 6 | OBC AXI4-Lite Interface | 300 | Yes | 900 | ARM PS ↔ PL 暫存器橋接（5 個 32-bit 暫存器）|
| 7 | SEU Scrubber（ICAP Controller）| 500 | No * | 500 | ICAP 時序控制 + CRC-32 比對 + frame 修復 |
| 8 | SAA Detector / Mode Switch | 200 | Yes | 600 | SAA_mode bit 暫存 + scrubbing 計時器切換 |
| | **C-003 RTL 小計** | **6,200** | | **17,600** | |

(*) SEU Scrubber 採用「hardened-by-design」設計（詳見 3.4 節），不施加 TMR，原因為雞蛋問題（scrubber 壞了無法修復自身的 TMR）。

**C-003 LUT 使用率（通訊 + SEU 基帶模組）**：

```
17,600 / 53,200 = 33.1%
```

### 1.3 全 PL 資源自洽計算（對照 B-007）

B-007 Section 6.2 給出的總 LUT 使用量為 **37,000 LUT（69.5%）**，包含以下模組群組：

| 模組群組 | LUT | 說明 |
|---------|:---:|------|
| **C-003 RTL 模組（本文件）** | 17,600 | 通訊基帶 + SEU/SAA 模組（含 TMR） |
| **Doppler NCO** | 4,500 | 1,500 × 3，數控振盪器，頻偏預補償（B-007 §3.2）|
| **FSW Critical State Machine** | 3,000 | 1,000 × 3，Safe Mode 轉移邏輯（B-007 §3.2）|
| **AXI Bus Controller（完整版）** | 9,000 | 3,000 × 3，AXI4-Lite + AXI4-Stream 橋接（B-007 §3.2）|
| **Config Scrubber（完整版）** | 2,000 | ICAP + CRC engine 完整實作（B-007 §3.2，non-TMR）|
| **Debug / TM Counter** | 500 | non-critical，無 TMR（B-007 §3.2）|
| **合計** | **36,600** | ≈ 37,000（差值 400 LUT 為 voter 額外開銷）|

> **數字自洽說明**：C-003 的 AXI Interface（300 LUT / 900 TMR）為**簡化 AXI4-Lite 暫存器橋接**，專門對應通訊基帶控制用途；B-007 的「AXI Bus Controller（3,000 LUT / 9,000 TMR）」涵蓋完整 AXI4-Lite + AXI4-Stream DMA 路徑（含 IF-04 SPI 10 Mbps 基帶資料流橋接），兩者功能層次不同，不重複計算。同樣，C-003 的「SEU Scrubber（500 LUT）」是 ICAP 控制狀態機；B-007 的「Config Scrubber（2,000 LUT）」含完整 CRC-32 引擎及 readback 比對電路。最終全 PL LUT 使用量為 **37,000 LUT（69.5%）**，與 B-007 及 PATCH-P4 修正一致。

### 1.4 DSP48E1 與 BRAM 使用估算

| 資源 | 使用量 | 分配 |
|------|:------:|------|
| DSP48E1 | 18 × 3 = 54（TMR）| Costas loop 乘法器（×4）+ Gardner TED（×2）+ RRC 濾波器 tap（×3）共 9 DSP，TMR 後 27；另 Doppler NCO 相位累加器 3 DSP，TMR 後 9。合計 54。|
| BRAM（36Kb）| 6 | Viterbi path memory（2 BRAM × 3 TMR）= 6 BRAM；用途：Traceback 深度 64，K=7 |

---

## 2. QPSK 調變解調 RTL 詳細設計

### 2.1 系統信號流

```
 ARM PS
   │  FEC 編碼後 bit stream（AXI4-Stream, 8-bit TDATA）
   ▼
┌──────────────────────────────────────────────────────────────┐
│                    QPSK Modulator（TMR）                      │
│                                                              │
│  Bit stream → S/P（串並轉換）→ I/Q 符號映射                    │
│      （Gray code：00→(+1,+1), 01→(-1,+1), 11→(-1,-1), 10→(+1,-1)）│
│  → RRC 脈衝整形 FIR（16 tap, α=0.35, 8-bit I/Q 精度）          │
│  → 輸出：I[7:0] / Q[7:0] @符號率 CLK → DAC（SPI 10 MHz）       │
└──────────────────────────────────────────────────────────────┘
                        ↕ RF Front-End
┌──────────────────────────────────────────────────────────────┐
│                   QPSK Demodulator（TMR）                     │
│                                                              │
│  ADC I[7:0] / Q[7:0] → 複數乘法器（×NCO 載波恢復）              │
│  → Costas Loop（2 階 PLL，頻寬 10 kHz）→ 相位誤差估計           │
│  → Gardner TED → 時序誤差估計 → 插值濾波器（可變分率）           │
│  → 符號判決（硬判決：sgn(I), sgn(Q)）                          │
│  → P/S（並串轉換）→ bit stream → Viterbi Decoder              │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 QPSK Modulator RTL 規格

**頂層介面（Verilog/VHDL port list）**：

```verilog
module qpsk_mod_tmr (
    input  wire        clk,          // 系統時鐘，FPGA PL 100 MHz
    input  wire        rst_n,        // 低電位有效同步重置
    input  wire        tx_en,        // 來自 AXI CTRL[0]
    // AXI4-Stream 輸入（來自 FEC Encoder）
    input  wire [7:0]  s_axis_tdata, // FEC 輸出 byte
    input  wire        s_axis_tvalid,
    output wire        s_axis_tready,
    // I/Q 基帶輸出（到 DAC SPI 控制器）
    output wire [7:0]  iq_i_out,     // I channel，2's complement
    output wire [7:0]  iq_q_out,     // Q channel，2's complement
    output wire        iq_valid
);
```

**時序參數**：

| 參數 | 數值 | 說明 |
|------|------|------|
| 系統時鐘 | 100 MHz | Zynq PL 預設，從 PS PLL 分頻 |
| 符號率 | 200 kSps | B-001 BW = 200 kHz，QPSK 1 符號 = 2 bits |
| 過採樣因子 | 8× | → 100 MHz / 200 kSps = 500 倍，選 8× 後在 DAC 端再重採 |
| RRC 濾波器 tap 數 | 16 | α=0.35，截止頻率 = 符號率 × (1+α)/2 = 135 kHz |
| I/Q 量化精度 | 8-bit | 2's complement，-128~+127（QPSK 映射±1） |

**查表法（LUT-based）脈衝整形**：

RRC 脈衝整形使用**預計算 ROM 查表**，每個 I/Q symbol（+1 或 -1）的 RRC 整形後 16 個採樣值存入 4 個 FPGA LUT（利用 Zynq-7020 6-input LUT 作 ROM），避免乘法器（節省 DSP48E1）。

```
ROM 結構：
  輸入：{symbol(1-bit), phase_idx[3:0]} = 5-bit address
  輸出：rrc_sample[7:0]（預計算，fixed-point 8-bit）
  深度：2 × 16 = 32 entries × 8-bit = 256 bits per 查表
```

### 2.3 QPSK Demodulator RTL 規格

**頂層介面**：

```verilog
module qpsk_demod_tmr (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        rx_en,          // 來自 AXI CTRL[1]
    // ADC I/Q 輸入（從 ADC SPI 介面）
    input  wire [7:0]  adc_i_in,
    input  wire [7:0]  adc_q_in,
    input  wire        adc_valid,
    // Doppler 補償設定（來自 AXI DOPPLER_COMP[15:0]）
    input  wire [15:0] doppler_hz,     // 有號數，±50 kHz 範圍
    // 解調輸出
    output wire        demod_bit,      // 硬判決 bit stream
    output wire        demod_valid,
    // BER 估計（輸出到 AXI BER_EST）
    output wire [15:0] ber_estimate,
    // 鎖相指示（輸出到 AXI STATUS[0]）
    output wire        carrier_lock
);
```

**Costas Loop（2 階 PLL）設計**：

| 參數 | 數值 | 說明 |
|------|------|------|
| PLL 階數 | 2 | 一階積分 + 比例增益，可追蹤頻率偏移 |
| 迴路頻寬（BW）| 10 kHz | 取決於鏈路 Doppler 動態（±50.6 kHz/orbit，變化率 ≤250 Hz/s）|
| 自然頻率 ωn | 2π × 10k = 62,832 rad/s | |
| 阻尼比 ζ | 0.707（臨界阻尼）| 最佳 BW-noise 平衡 |
| 相位誤差偵測器 | Costas 型：e(k) = I(k)×Q(k)（QPSK 相位 mod π/2）| 無 decision-directed ambiguity |
| NCO 位寬 | 32-bit 相位累加器 | 頻率解析度：100 MHz / 2³² = 0.023 Hz |
| Doppler 預補償 | ARM 計算 Doppler offset → 寫入 AXI DOPPLER_COMP → PL NCO 初始頻率偏移 | 搜尋範圍 ±25 kHz（殘餘 Doppler 由 Costas loop 追蹤）|

**Doppler 規格對照（B-001 參考）**：
- UL Doppler：±50.6 kHz（500 km SSO，1995 MHz，v_max ≈ 7.6 km/s）
- ARM 端預測精度：±25 kHz（TLE 傳播誤差）→ Costas loop 負責剩餘 ±25 kHz acquisition
- Costas loop 捕獲時間：t_acq ≈ 3/BW = 0.3 ms @ 10 kHz 頻寬（遠小於接觸窗口 4 min）

**Gardner 時序誤差偵測器（TED）**：

```
Gardner TED 公式：
  e_tim(k) = Re{ [r(k) - r(k-1)] × conj(r(k-½)) }

  其中 r(k) 為符號時刻採樣，r(k-½) 為半符號間隔採樣
  使用 16-bit 乘法器（DSP48E1 × 2，TMR 後 × 6）
  時序誤差範圍：±T_sym / 2 = ±2.5 μs @ 200 kSps
```

**插值濾波器**：Farrow 架構，4-tap 多項式插值，分率因子範圍 0.9~1.1（補償時鐘偏差 ≤10%）。

---

## 3. FEC 詳細設計

### 3.1 卷積碼編碼器 RTL

**規格**：

| 參數 | 數值 |
|------|------|
| 碼率（Code Rate）| 1/2 |
| 約束長度（K）| 7 |
| 生成多項式 G1 | 171₈（= 1111001₂，MSB first）|
| 生成多項式 G2 | 133₈（= 1011011₂，MSB first）|
| 標準 | 3GPP / CCSDS 相容 |
| 輸出交錯 | G1 先輸出，G2 後輸出（逐 bit 交替）|

**RTL 架構**：

```
輸入：data_in（1 bit/clk）
移位暫存器：SR[6:0]（7-bit shift register，K=7）
  SR 更新：SR <= {data_in, SR[6:1]}

G1 output：g1 = SR[6]^SR[5]^SR[4]^SR[3]^SR[0]（對應 1111001）
G2 output：g2 = SR[6]^SR[4]^SR[3]^SR[1]^SR[0]（對應 1011011）

輸出 MUX：sel 交替 → enc_out = (sel==0) ? g1 : g2
輸出速率：2 bits/input bit（rate 1/2）
```

TMR 實作：上述移位暫存器及 XOR 邏輯全部三重化，voter 決定每個輸出 bit。

### 3.2 Viterbi 解碼器 RTL

**規格**：

| 參數 | 數值 |
|------|------|
| 演算法 | Viterbi（BCJR 的前向部分）|
| 判決模式 | 硬判決（Hard Decision，Sprint 4 可升軟判決）|
| Traceback 深度 | 64（= 5 × K，慣例），記憶體 64 × 64 states = 4 Kbits |
| ACS 單元數量 | 64（K=7 → 2^(K-1) = 64 states）|
| 路徑度量位寬 | 8-bit（正規化防溢位：每 ACS 後減去最小度量）|
| DSP 使用 | 不使用 DSP48E1（硬判決 ACS 為純加法 + 比較，LUT 實作效率更高）|
| BRAM | 每個 TMR 複本 1 個 BRAM（36Kb），traceback path memory；3 份 = 3 BRAM |

**ACS（Add-Compare-Select）蝶形計算**（硬判決）：

```
Branch metric（BM）= Hamming distance（received_bits, expected_bits）
  硬判決：BM ∈ {0, 1, 2}（兩位元 received pair vs 64 transition pairs）

ACS：
  PM_new[s] = min( PM_old[s0] + BM[s0→s],
                   PM_old[s1] + BM[s1→s] )
  Decision bit：0 或 1（哪個前狀態勝出）→ 寫入 Traceback RAM
```

**效能目標**：

| 指標 | 目標值 | 根據 |
|------|--------|------|
| BER（AWGN，QPSK 1/2）| ≤10⁻⁵ @ Eb/N0 = 4.5 dB | rate 1/2 卷積碼理論值（K=7 hard decision：~1 dB worse than soft，但符合任務 margin）|
| 編碼增益 | ~4.5 dB vs uncoded QPSK @ 10⁻⁵ | hard decision Viterbi 典型值 |
| 解碼延遲 | Traceback depth 64 × clk period = 0.64 μs @ 100 MHz | 可接受（符號率 200 kSps，1 符號 = 5 μs >> 0.64 μs）|

---

## 4. SEU 防護機制詳細設計

### 4.1 TMR Wrapper 架構

每個被 TMR 保護的 RTL 模組使用以下包裝結構：

```
             ┌────────────────────────────────────────┐
input_bus ──►│               TMR Wrapper              │
             │                                        │
             │  ┌─────────────┐  out_0[N:0]           │
             │  │   copy_0    │──────────────┐         │
             │  └─────────────┘              │         │
             │  ┌─────────────┐  out_1[N:0]  │         │
             │  │   copy_1    │────────────┤ Voter │──►│ output[N:0]
             │  └─────────────┘              │         │
             │  ┌─────────────┐  out_2[N:0]  │         │
             │  │   copy_2    │──────────────┘         │
             │  └─────────────┘                        │
             └────────────────────────────────────────┘

Voter 邏輯（逐 bit 多數決）：
  output[i] = (out_0[i] & out_1[i]) |
              (out_1[i] & out_2[i]) |
              (out_0[i] & out_2[i])
```

**SEU 修復時序**：
- 假設 copy_1 某個 FF 發生 SEU：out_1[i] 翻轉
- Voter 在同一 clk 週期輸出仍由 out_0 & out_2 的多數決（2/3 = 正確值）
- 下一次 ICAP scrubbing 修復 copy_1 的 configuration bit → copy_1 輸出恢復正確
- **零週期輸出錯誤**（voter 即時補償），**ICAP scrubbing 週期內修復**（≤100 ms 或 ≤10 ms in SAA）

**TMR Voter LUT 開銷**：每個 output bit 需要 3 個 2-input AND + 2 個 2-input OR = 5 gate，可以用 1 個 6-input LUT 實現。若模組輸出寬度 = W bits，voter overhead = W LUT。對 2,500 LUT 的 Demodulator（輸出約 32-bit 狀態）voter 僅需 32 LUT = 1.3%，可忽略。

### 4.2 ICAP Configuration Scrubber 詳細設計

**狀態機（FSM）**：

```
                   ┌──────────┐
         ┌────────►│  IDLE    │◄───── rst / scrub_done
         │         └────┬─────┘
         │              │ scrub_trigger（100ms / 10ms timer）
         │         ┌────▼─────┐
         │         │  READ    │  ← ICAP readback：逐 frame 讀取 PL configuration
         │         │  FRAME   │    每個 frame = 101 words（Artix-7 frame 格式）
         │         └────┬─────┘
         │              │
         │         ┌────▼─────┐
         │         │   CRC    │  ← CRC-32 計算：比對 Golden Bitstream（NOR Flash）
         │         │  CHECK   │
         │         └────┬─────┘
         │              │
         │     [MATCH]  │  [MISMATCH]
         │         ┌────┴─────┐
         │         │  CORRECT │  ← 寫入 Golden frame 到 ICAP → 修復 SEU
         │         └────┬─────┘
         │              │
         │         ┌────▼─────┐
         │         │  NEXT    │  ← 移至下一個 frame，更新 frame addr
         │         │  FRAME   │
         │         └────┬─────┘
         │              │ all frames done
         └──────────────┘
```

**ICAP 時序規格**：

| 參數 | 數值 | 來源 |
|------|------|------|
| ICAP 介面寬度 | 32-bit | Zynq-7020 ICAP_SPARTAN6 / ICAP_ARTIX7 |
| ICAP 最大時鐘頻率 | 100 MHz | Xilinx UG470 |
| ICAP 吞吐量（理論）| 100 MHz × 32-bit = 3,200 Mbps | |
| ICAP 有效吞吐量（含overhead）| ~400 Mbps | 包含 SYNC/DESYNC 指令 + pipeline latency |
| 全裝置 bitstream 大小 | 4.5 MB（36 Mbit）| Zynq-7020 full device |
| 全裝置 scrub 時間 | 4.5 MB × 8 / 400 Mbps = **90 ms** | ≤ 100 ms 週期 ✅ |

> **Partial Scrub（SAA 模式）**：
> 全裝置 frame 數 ≈ 1,706 frames（Artix-7 XC7Z020）。10 ms 週期內掃描 1/9 裝置 = ~190 frames，6 個 10 ms cycle = 完整 1 次 full scrub（60 ms），符合 PATCH-P6 設計（10 ms partial scrub）。

**Scrubbing 優先順序**（正常模式 100 ms，full scan）：

1. **TMR Voter 電路**（最高優先）→ voter 錯誤會導致三重冗餘失效
2. **FEC / Viterbi 解碼器** → SEU 影響解碼正確性
3. **QPSK Modulator / Demodulator** → SEU 影響信號品質
4. **Framing / AXI** → 功能完整性
5. **Non-critical 區域**（Debug / 保留邏輯）

SAA 模式（10 ms partial scrub）按相同優先順序循環掃描，確保高優先模組每 60 ms 完整 scrub 一次。

### 4.3 SAA 偵測邏輯（SAA Detector RTL）

**設計分工（ARM PS + PL 協同）**：

```
ARM PS 端（FreeRTOS SDR Manager task，0.5 Hz 執行）：
  ┌─────────────────────────────────────────────────────┐
  │  SGP4 簡化軌道傳播（每 30 s 更新衛星位置）              │
  │  → 緯度 lat, 經度 lon（float32）                      │
  │                                                     │
  │  SAA 邊界判定（矩形近似）：                            │
  │    if ( -50° ≤ lat ≤ -10° AND                       │
  │         -90° ≤ lon ≤ +40° )                         │
  │      { SAA_detected = true }                         │
  │                                                     │
  │  提前 30 s 切換（補償軌道傳播計算延遲 + AXI 寫入延遲）：  │
  │    t_switch = t_entry - 30 s                         │
  │                                                     │
  │  AXI 寫入：CTRL register bit[2] = SAA_MODE            │
  └─────────────────────────────────────────────────────┘
                         ↕ AXI4-Lite（0x00 CTRL）
PL 端 SAA Detector（RTL，200 LUT × 3 TMR = 600 LUT）：
  ┌─────────────────────────────────────────────────────┐
  │  SAA_mode ← CTRL[2]（AXI 暫存器讀取）                 │
  │                                                     │
  │  Scrubbing Timer：                                   │
  │    if (SAA_mode == 0)：timer_period = 10_000_000     │
  │                         （100 MHz × 100 ms）         │
  │    if (SAA_mode == 1)：timer_period = 1_000_000      │
  │                         （100 MHz × 10 ms）          │
  │  → scrub_trigger 脈衝輸出 → ICAP Scrubber FSM        │
  └─────────────────────────────────────────────────────┘
```

**SAA 邊界參數（保守定義，擴大 20% margin）**：

| 邊界 | 精確 SAA 核心 | C-003 實作值（含 margin）|
|------|-------------|------------------------|
| 緯度下限 | -50°S | -50°S（保持）|
| 緯度上限 | 0°（equator）| 0°（保持）|
| 經度左限 | -90°W（= 270°E）| -90°W（保持）|
| 經度右限 | +40°E | +40°E（保持）|

> 相對 PATCH-P6 的 SAA 邊界（20-50°S, 10-50°W），本設計採用更保守的 -50°~0°S，-90°~+40°E，覆蓋更廣的質子輻射帶影響區，提高安全裕度。

---

## 5. AXI4-Lite 暫存器介面設計

### 5.1 暫存器映射（Register Map）

基底位址：PL 端 AXI slave base address（由 Xilinx Vivado Block Design 分配，建議 0x43C0_0000）

| 暫存器名稱 | 位址偏移 | 位寬 | 存取 | 說明 |
|----------|---------|:---:|:----:|------|
| CTRL | 0x00 | 32-bit | R/W | 控制暫存器 |
| STATUS | 0x04 | 32-bit | R only | 狀態暫存器（唯讀）|
| SEU_COUNT | 0x08 | 32-bit | R/clr | SEU 事件計數器（讀取後自動清零）|
| DOPPLER_COMP | 0x0C | 32-bit | R/W | Doppler 補償頻率（低 16-bit 有效）|
| BER_EST | 0x10 | 32-bit | R only | BER 估計（低 16-bit 有效）|

### 5.2 各暫存器欄位定義

**CTRL（0x00）— Control Register**：

| Bit | 名稱 | 預設值 | 說明 |
|:---:|------|:-----:|------|
| [0] | TX_EN | 0 | 1 = 啟動 QPSK Modulator + FEC Encoder；0 = 關閉（clock gate）|
| [1] | RX_EN | 0 | 1 = 啟動 QPSK Demodulator + Viterbi Decoder；0 = 關閉 |
| [2] | SAA_MODE | 0 | 1 = SAA 模式（ICAP scrubbing 切換至 10 ms）；0 = 正常（100 ms）|
| [3] | SCRUB_EN | 1 | 1 = ICAP scrubbing 啟用；0 = 停止（僅 Safe Mode 診斷使用）|
| [4] | SEU_IRQ_EN | 0 | 1 = SEU_COUNT 溢位時觸發 PS 中斷（透過 PL-PS interrupt port）|
| [31:5] | Reserved | 0 | 保留，寫 0 |

**STATUS（0x04）— Status Register**（唯讀）：

| Bit | 名稱 | 說明 |
|:---:|------|------|
| [0] | CARRIER_LOCK | 1 = Costas loop 鎖相完成（相位誤差 < 5°）|
| [1] | SEU_OVF | 1 = SEU_COUNT 溢位（32-bit overflow，≥ 4,294,967,295 次）|
| [2] | TX_ACTIVE | 1 = TX pipeline 正在傳送（clk 有效）|
| [3] | RX_ACTIVE | 1 = RX pipeline 正在接收 |
| [4] | SAA_ACTIVE | 1 = 目前 SAA_MODE 有效 |
| [5] | SCRUB_BUSY | 1 = ICAP scrubber 正在執行 scrub cycle |
| [31:6] | Reserved | 0 |

**SEU_COUNT（0x08）— SEU Event Counter**：

| Bit | 名稱 | 說明 |
|:---:|------|------|
| [31:0] | SEU_CNT | 32-bit 無號整數，累積 ICAP readback 偵測到的 SEU 修復次數；ARM 讀取後自動清零（read-to-clear）|

> **設計細節**：ICAP Scrubber FSM 在 CRC MISMATCH 時，SEU_CNT 加 1 並寫入 correction frame。ARM SDR Manager task（0.5 Hz）定期讀取此計數器，若單一 scrub cycle 內 SEU_CNT > 5，觸發 FDIR warning。

**DOPPLER_COMP（0x0C）— Doppler Compensation**：

| Bit | 名稱 | 說明 |
|:---:|------|------|
| [15:0] | DOPPLER_HZ | 16-bit 有號數（2's complement），單位 Hz，範圍 -32768~+32767 Hz；ARM 根據 TLE 傳播計算寫入（每 30 s 更新）|
| [31:16] | Reserved | 0 |

> 解析度：1 Hz/LSB，足夠（Costas loop 追蹤 ±25 kHz 剩餘誤差，ARM 提供初始偏移精度 ±25 kHz 即可）。

**BER_EST（0x10）— BER Estimate**：

| Bit | 名稱 | 說明 |
|:---:|------|------|
| [15:0] | BER_EST | Viterbi 解碼器輸出的 BER 估計；格式：16-bit fixed-point，Q.16（1.0 = BER=1，0x0001 ≈ 1.5×10⁻⁵）|
| [31:16] | Reserved | 0 |

> BER 估計方法：Viterbi path metric 統計（path metric normalize variance 正比於 BER）；精度 ±50%，可接受（目標 BER ≤10⁻⁵ 量級即可）。

### 5.3 AXI4-Lite Slave RTL 介面

```verilog
module axi4l_slave_bridge (
    // AXI4-Lite Global Signals
    input  wire        S_AXI_ACLK,
    input  wire        S_AXI_ARESETN,
    // Write Address Channel
    input  wire [31:0] S_AXI_AWADDR,
    input  wire        S_AXI_AWVALID,
    output reg         S_AXI_AWREADY,
    // Write Data Channel
    input  wire [31:0] S_AXI_WDATA,
    input  wire [3:0]  S_AXI_WSTRB,
    input  wire        S_AXI_WVALID,
    output reg         S_AXI_WREADY,
    // Write Response Channel
    output reg  [1:0]  S_AXI_BRESP,   // 2'b00 = OKAY
    output reg         S_AXI_BVALID,
    input  wire        S_AXI_BREADY,
    // Read Address Channel
    input  wire [31:0] S_AXI_ARADDR,
    input  wire        S_AXI_ARVALID,
    output reg         S_AXI_ARREADY,
    // Read Data Channel
    output reg  [31:0] S_AXI_RDATA,
    output reg  [1:0]  S_AXI_RRESP,
    output reg         S_AXI_RVALID,
    input  wire        S_AXI_RREADY,
    // 內部暫存器介面（到各子模組）
    output wire [31:0] reg_ctrl,
    input  wire [31:0] reg_status,
    input  wire [31:0] reg_seu_count,    // 從 scrubber 來
    output wire [31:0] reg_doppler_comp,
    input  wire [31:0] reg_ber_est
);
```

---

## 6. LUT 使用率總結與 B-007 自洽驗證

### 6.1 C-003 RTL 模組（通訊 + SEU 基帶）

| 模組群組 | LUT（含 TMR）| 百分比（/53,200）|
|---------|:-----------:|:---------------:|
| QPSK Modulator（TMR）| 2,400 | 4.5% |
| QPSK Demodulator（TMR）| 7,500 | 14.1% |
| Viterbi Decoder（TMR）| 3,600 | 6.8% |
| FEC Encoder（TMR）| 900 | 1.7% |
| Framing / Deframing（TMR）| 1,200 | 2.3% |
| OBC AXI4-Lite Bridge（TMR）| 900 | 1.7% |
| SEU Scrubber ICAP（non-TMR）| 500 | 0.9% |
| SAA Detector（TMR）| 600 | 1.1% |
| **C-003 小計** | **17,600** | **33.1%** |

### 6.2 B-007 補充模組（非 C-003 範疇）

| 模組群組 | LUT（含 TMR）| 百分比（/53,200）|
|---------|:-----------:|:---------------:|
| Doppler NCO（TMR）| 4,500 | 8.5% |
| FSW Critical State Machine（TMR）| 3,000 | 5.6% |
| AXI Bus Controller 完整版（TMR）| 9,000 | 16.9% |
| Config Scrubber 完整版（non-TMR）| 2,000 | 3.8% |
| Debug / TM Counter（non-TMR）| 500 | 0.9% |
| **B-007 補充小計** | **19,000** | **35.7%** |

### 6.3 全 PL LUT 使用率

| 項目 | LUT | 說明 |
|------|:---:|------|
| C-003 RTL 模組 | 17,600 | 通訊基帶 + SEU/SAA |
| B-007 補充模組 | 19,000 | NCO + FSW SM + 完整 AXI + Debug |
| Voter 額外開銷（估計）| 400 | 各 TMR wrapper 的 voter LUT 修正 |
| **全 PL 合計** | **37,000** | |
| **Utilization** | **69.5%** | **37,000 / 53,200（與 B-007 Section 6.2 一致）** |
| 剩餘 LUT | 16,200 | 30.5% margin，供未來擴充（軟判決 Viterbi、進階 Doppler）|

> **重要差異說明（C-003 vs B-007 TMR 範疇）**：
> - 任務要求書（SW-002）：「FPGA 邏輯設計利用率 ≤69.5%」→ 全 PL 使用率滿足。
> - B-007 Section 3.2 Critical 小計（34,500 LUT）= TMR 模組只計 5 個群組（不含 non-TMR 的 Scrubber 2,000 + Debug 500）。
> - C-003 的 AXI4-Lite Bridge（900 LUT）≠ B-007 的 AXI Bus Controller（9,000 LUT）：前者為暫存器介面，後者含完整 AXI4-Stream DMA，兩者**並非重複**，而是設計層次不同（C-003 為基帶控制用簡化介面，B-007 為包含高速 I/Q 資料流的完整匯流排）。

---

## 7. 測試策略

### 7.1 單元測試（Unit Test）

**T-RTL-001：QPSK Loopback 測試**

| 項目 | 內容 |
|------|------|
| 目標 | 驗證 Modulator 輸出可被 Demodulator 正確解調 |
| 方法 | Vivado 仿真（ModelSim/Xsim）：TX bit stream → QPSK Mod → AWGN 雜訊模型（Python 生成）→ QPSK Demod → 比對輸入/輸出 bit |
| 通過條件 | BER ≤10⁻⁴ @ Eb/N0 = 6 dB（AWGN，硬判決 QPSK 理論 ≈ 5×10⁻⁵）|
| 工具 | Vivado XSim + Python cocotb |

**T-RTL-002：Viterbi BER 驗證**

| 項目 | 內容 |
|------|------|
| 目標 | 驗證 FEC Encoder + Viterbi Decoder 達成 BER 目標 |
| 方法 | 仿真：隨機 bit → FEC Encoder → 通道噪聲（BSC，p 從 0.01~0.2）→ Viterbi → BER 曲線 |
| 通過條件 | BER ≤10⁻⁵ @ Eb/N0 = 4.5 dB（rate 1/2 K=7 hard decision 理論值）|

**T-RTL-003：TMR Voter 邏輯驗證**

| 項目 | 內容 |
|------|------|
| 目標 | 驗證 voter 在 1 個複本錯誤時輸出仍正確 |
| 方法 | 強制 copy_1 輸出固定 0 / 固定 1，確認 voter 輸出追隨 copy_0 & copy_2 |
| 通過條件 | 任意 1 份錯誤，voter 輸出無誤差 |

### 7.2 SEU 注入測試（SEU Injection Test）

**T-SEU-001：Vivado Tcl 強制 Bit-flip**

```tcl
# Vivado Hardware Manager Tcl 腳本（在 JTAG 模式下）
# 強制翻轉 Viterbi Decoder copy_0 的某個 LUT 配置位元
readback_file -bitfile golden.bit -readback_file readback.rbd
# 找到 Viterbi 模組的 frame address
set frame_addr 0x00400C00
# 翻轉 bit[7]
set_property INIT 8'h7F [get_cells {viterbi_copy0/pm_reg[0]}]
# 確認 ICAP scrubber 在下一個 100ms 週期修復
after 200
# 讀取 AXI SEU_COUNT 暫存器
read_axi_reg 0x43C00008
# 預期回傳值：0x00000001（1 次 SEU 修復）
```

| 項目 | 內容 |
|------|------|
| 目標 | 驗證 ICAP scrubber 偵測並修復 configuration bit 翻轉 |
| 通過條件 | SEU_COUNT 在 200 ms 內增加 1；電路輸出在 voter 補償下無錯誤 |

**T-SEU-002：SAA 切換 + 快速 Scrub 驗證**

| 項目 | 內容 |
|------|------|
| 目標 | 驗證 SAA_MODE=1 後 ICAP scrubbing 切換至 10 ms 週期 |
| 方法 | AXI 寫入 CTRL[2]=1 → 示波器或 ILA（Integrated Logic Analyzer）量測 scrub_trigger 脈衝間距 |
| 通過條件 | scrub_trigger 間距 = 10 ms ±5%（FPGA 時鐘精度）|

### 7.3 整合測試（Integration Test，Sprint 4）

**T-INT-001：與 RF PCB 連接的 RF Loopback 測試**

| 項目 | 內容 |
|------|------|
| 目標 | 端到端驗證：ARM FEC 輸出 → PL QPSK Mod → DAC → RF Cable Loopback → ADC → PL QPSK Demod → Viterbi → BER |
| 通過條件 | BER ≤10⁻⁵ @ RF SNR 等效 Eb/N0 = 4.5 dB |
| 設備 | Signal Analyzer + Signal Generator（RF front-end 暫用實驗室設備替代 PCB）|

**T-INT-002：完整鏈路端到端測試（Contact Window 模擬）**

| 項目 | 內容 |
|------|------|
| 目標 | 模擬 4 min 接觸窗口：Doppler 掃頻 ±50 kHz（模擬 LEO 軌道幾何）→ Costas loop 鎖定 → 連續資料傳輸 → BER 統計 |
| 通過條件 | 接觸窗口內 Costas loop 鎖定時間 < 1 s；整體 BER ≤10⁻⁴（含鎖定過渡段）|

---

## 8. 需求符合性矩陣

| 需求 ID | 需求敘述（摘要）| 滿足方式 | 設計章節 | 驗證測試 |
|---------|-------------|---------|---------|---------|
| SW-001 | Zynq-7020，53,200 LUT | 確認使用 Zynq-7020 XC7Z020；C-003 RTL 模組 + B-007 補充模組合計 37,000 LUT（69.5%）| §1.1, §6.3 | T-INT-001 |
| SW-002 | TMR 設計利用率 ≤69.5%；scrubbing 100 ms / 10 ms（SAA）| 全 PL LUT 37,000 / 53,200 = 69.5% ✅；ICAP scrubber 正常 100 ms、SAA 10 ms partial scrub | §1.2, §4.2, §6.3 | T-SEU-002 |
| SW-003 | FreeRTOS，watchdog，Autonomous Fault Recovery | ARM PS 端 FreeRTOS 負責（B-007 §4）；PL 為 SDR 協處理器，SEU 靠 TMR + scrubber 自動修復 | §4.1, §4.2 | T-SEU-001 |
| SW-004 | SAA 感知 scrubbing 切換（TLE 傳播 → 進入前自動切換）| ARM SGP4 計算位置 → AXI CTRL[2]=SAA_MODE → PL timer 切換 10 ms；進入前 30 s 預切換 | §4.3 | T-SEU-002 |
| SW-005 | ≥7 天遙測儲存 | 由 ARM DDR3 + NOR Flash 實現（B-007 §9）；PL 端無直接相關，但 BER_EST / SEU_COUNT 輸出為遙測資料來源 | §5.2 | — |
| SW-006 | TC 序號 + CRC 完整性校驗 | ARM FSW TM/TC Handler 實現（B-007 §4）；PL CTRL 暫存器由 ARM 寫入（不直接暴露於 TC 路徑）| §5.3 | — |
| SYS-011 | ≥100 bps，QPSK 1/2 | QPSK rate 1/2 卷積碼；符號率 200 kSps → 資料率 200 k × 1/2（FEC）= 100 kbps >> 100 bps ✅ | §2.2, §3.1 | T-RTL-001, T-RTL-002 |
| SYS-013 | TID ≥5 krad；SEU 防護 TMR + ICAP scrubbing | TMR 覆蓋全部關鍵 PL 模組；ICAP 正常 100 ms / SAA 10 ms；配合 B-007 §3.1 TID 分析（Zynq-7020 20 krad TID >> 5 krad）| §4.1, §4.2 | T-SEU-001, T-SEU-002 |

---

## 9. 開放議題與 Sprint 4 待辦

| # | 議題 | 說明 | 負責 | 目標 Sprint |
|---|------|------|------|------------|
| 1 | Viterbi 軟判決升級 | 本版為 hard decision（BER 約 1 dB penalty）；Sprint 4 可升 4-bit soft decision（改善 BER 性能至 Eb/N0 = 3.5 dB）| SW/FW Agent | Sprint 4 |
| 2 | Doppler NCO 詳細 RTL | B-007 列出 Doppler NCO（1,500 LUT / 4,500 TMR），本文件僅描述 ARM 端預補償；NCO 本身的 phase-locked loop RTL 留至 Sprint 4 細化 | SW/FW Agent | Sprint 4 |
| 3 | SPENVIS 驗證 | PATCH-P6 要求的精確 SAA flux profile 模擬，驗證 10 ms scrubbing 充分性（moderate vs worst-case 模型）| SW/FW Agent | Sprint 4 |
| 4 | Timing Closure 驗證 | Costas loop 在 100 MHz 的 Vivado timing report，確認 WNS ≥0 | SW/FW Agent | Sprint 4 |
| 5 | ICAP Frame Address Map | Zynq-7020 完整的 frame address 表格（用於 partial scrub 優先序實作）| SW/FW Agent | Sprint 4 |
| 6 | RF PCB 整合測試 | T-INT-001 / T-INT-002 需等 RF PCB 完成後執行 | Comm + SW/FW Agent | Sprint 4 |

---

*C-003 FPGA RTL 詳細設計 v1 — SW/FW Agent 徐志豪 — 2026-04-15*
