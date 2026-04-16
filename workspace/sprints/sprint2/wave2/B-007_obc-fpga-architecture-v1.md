---
deliverable: B-007
sprint: 2
wave: 2
author: SW/FW Agent (徐志豪)
date: 2026-05-03
status: draft
reference_documents:
  - workspace/sprints/sprint2/wave1/B-002_system-architecture-icd-v1.md
  - workspace/sprints/sprint2/wave1/B-005_power-budget-v2.md
---

# B-007：OBC/FPGA 架構初步設計（Zynq-7020，SEU 緩減策略）

## 1. 硬體平台

### 1.1 Zynq-7020 SoC 概觀

選用 Xilinx Zynq-7020 (XC7Z020) 作為 OBC 核心，結合 ARM Processing System (PS) 與 FPGA Programmable Logic (PL) 於單一晶片：

| 區塊 | 規格 | 用途 |
|------|------|------|
| **PS — ARM Cortex-A9** | 雙核 667 MHz, 256 KB SRAM, DDR3 controller | 飛行軟體 (FSW)：RTOS 排程、FDIR、遙測收集、TC 命令解碼、ADCS 控制迴路 |
| **PL — Artix-7 FPGA** | 53,200 LUT, 106,400 FF, 140 BRAM (36Kb), 220 DSP48E1 | SDR 基帶：QPSK demod/mod、Doppler 預補償、AXI 橋接、Configuration Scrubbing |
| **I/O** | 200+ MIO/EMIO, GTX transceiver x4 | SPI x2, UART x2, I2C x1, GPIO x10+, ADC (XADC) x6 ch |
| **Configuration** | 32 Mbit QSPI boot, 36 Mbit SRAM config | QSPI NOR Flash boot PS → PS 載入 PL bitstream via PCAP/ICAP |

### 1.2 PS/PL 分工原則

```
┌─────────────────────────────────────────────────────────────┐
│                     Zynq-7020 SoC                           │
│                                                             │
│  ┌──────────────────────┐   AXI4   ┌──────────────────────┐│
│  │   PS (ARM Cortex-A9) │◄────────►│   PL (Artix-7 FPGA) ││
│  │                      │          │                      ││
│  │  - FreeRTOS kernel   │          │  - QPSK Demod (Rx)   ││
│  │  - FSW task manager  │          │  - QPSK Mod (Tx)     ││
│  │  - FDIR / Safe Mode  │          │  - Doppler NCO       ││
│  │  - ADCS ctrl loop    │          │  - AXI-SPI bridge    ││
│  │  - TM/TC handler     │          │  - Config Scrubber   ││
│  │  - EPS I2C driver    │          │  - TMR voter logic   ││
│  │  - Thermal control   │          │                      ││
│  │  - Orbit propagator  │          │                      ││
│  └──────────┬───────────┘          └──────────┬───────────┘│
│             │ MIO/EMIO                        │ PL I/O     │
│  ┌──────────┴───────────┐          ┌──────────┴───────────┐│
│  │ I2C → EPS (IF-01/02) │          │ SPI 10MHz → S-band   ││
│  │ SPI → ADCS (IF-03)   │          │   (IF-04, baseband)  ││
│  │ UART → TT&C (IF-06)  │          │ UART → S-band ctrl   ││
│  │ UART → S-band (IF-05)│          │   (IF-05, backup)    ││
│  │ GPIO → Heater (IF-07)│          │                      ││
│  │ GPIO → Deploy (IF-08)│          │                      ││
│  │ XADC → Temp (IF-09)  │          │                      ││
│  └──────────────────────┘          └──────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**設計決策**：S-band 基帶 I/Q 資料流 (IF-04, SPI 10 Mbps) 由 PL 直接驅動，避免 PS 軟體處理瓶頸。其餘低速介面 (I2C, UART, GPIO, ADC) 由 PS MIO/EMIO 直接處理，不佔用 PL 資源。

---

## 2. OBC 模組選型

針對 3U CubeSat 太空級/準太空級 Zynq-based OBC，評估以下三個候選方案：

| 項目 | **Xiphos Q7s** | **NanoAvionics SatBus OBC** | **Unibap iX5-100** |
|------|:--------------:|:---------------------------:|:-------------------:|
| 處理器 | Zynq-7020 | ARM Cortex-A9 (Zynq-7020 option) | Zynq UltraScale+ |
| FPGA Fabric | Artix-7, 53K LUT | Artix-7, 53K LUT | UltraScale+ 16nm |
| RAM | 1 GB DDR3 | 512 MB DDR3 | 4 GB DDR4 |
| NOR Flash | 256 Mbit QSPI | 128 Mbit QSPI | 512 Mbit QSPI |
| Mass Storage | 32 GB eMMC | 8 GB SD | 64 GB eMMC |
| Form Factor | PC/104 half-card (50x50 mm) | PC/104 (96x90 mm) | PC/104 (96x90 mm) |
| Mass | ~65 g | ~90 g | ~120 g |
| Standby Power | 1.2 W (typical) | 1.0 W (typical) | 2.5 W (typical) |
| Active Power | 3.5 W (typical) | 3.0 W (typical) | 6.0 W (typical) |
| Flight Heritage | ISS payload, LEO missions x5+ | LEO x10+, commercial | ISS, LEO x3 |
| Radiation Tolerance | 20 krad TID (Zynq-7020 bare), SEL immune to 78 MeV-cm2/mg | 20 krad TID | 酬載級, 非 rad-hard |
| Price (USD, est.) | ~$25,000 | ~$18,000 | ~$45,000 |
| TRL | 7-8 (LEO proven) | 7-8 (LEO proven) | 6-7 (ISS demo) |

### 選型結論：推薦 **Xiphos Q7s**

**理由**：

1. **FPGA 容量匹配**：53K LUT 足夠 TMR 後 SDR 基帶（34,500 LUT = 65%），且不需為超規格買單。
2. **功耗匹配**：Standby 1.2W + margin → 1.5W 預算內；Active 3.5W + margin → 4.0W 預算邊緣但可行（ref: B-005 Section 6, OBC Active = 4.0W envelope）。
3. **Form Factor**：50x50 mm 半卡，節省 3U 內部空間給 S-band 酬載。
4. **256 Mbit NOR Flash**：足夠存放 Golden Bitstream（36 Mbit）+ 2 個備份 + FSW image x2。
5. **Flight Heritage**：TRL 7-8，LEO 飛行驗證充分。

**風險**：Unibap iX5-100 功耗 6.0W 超出 4.0W envelope，排除。NanoAvionics 128 Mbit NOR Flash 偏小，僅勉強放 Golden + 1 備份，排除。

---

## 3. SEU 緩減策略

### 3.1 LEO 輻射環境估算

500 km SSO 軌道的質子/重離子環境對 SRAM-based FPGA 的 Single Event Upset (SEU) 影響估算：

| 參數 | 數值 | 來源 |
|------|------|------|
| Zynq-7020 SRAM Configuration bits | 36 Mbit (36 x 10^6 bits) | Xilinx UG470 |
| 典型 SEU cross-section (28nm SRAM) | ~3 x 10^-14 cm^2/bit | NSREC 文獻，Artix-7 28nm |
| 500 km SSO 質子 flux (> 10 MeV) | ~10^6 p/cm^2/day | AP-8 model |
| **期望 SEU rate** | ~3 x 10^-8 upset/bit/day | cross-section x flux |
| **期望 upset/day** | 36 x 10^6 x 3 x 10^-8 = **~1.08 upset/day** | |

**風險評估**：若不做防護，平均每天約 1 次 FPGA configuration bit 翻轉。Configuration bit 錯誤可能導致：
- SDR 基帶邏輯功能異常 → NTN 透明轉發失效
- AXI bus 掛死 → PS-PL 通訊中斷
- I/O routing 改變 → 子系統介面異常

**結論**：必須實施多層 SEU 防護。

### 3.2 TMR（Triple Modular Redundancy）

TMR 策略：將 critical logic 三重化，每個輸出經 majority voter 決定正確值。

**TMR 適用範圍**：

| 模組 | 原始 LUT | TMR 後 LUT | 說明 |
|------|:--------:|:----------:|------|
| QPSK Demodulator (Rx) | 3,500 | 10,500 | SDR 核心，接觸窗口必須正確 |
| QPSK Modulator (Tx) | 2,500 | 7,500 | SDR 核心，下行鏈路關鍵 |
| Doppler NCO | 1,500 | 4,500 | 頻偏補償，直接影響解調正確性 |
| FSW Critical State Machine | 1,000 | 3,000 | Safe Mode 轉移邏輯，不容錯誤 |
| AXI Bus Controller | 3,000 | 9,000 | PS-PL 通道，掛死等於系統失效 |
| **Critical 小計** | **11,500** | **34,500** | TMR 乘以 3x（含 voter ~0.5%） |

**非 TMR 模組**（non-critical，SEU 可靠 scrubbing 修復）：

| 模組 | LUT | 說明 |
|------|:---:|------|
| Config Scrubber (ICAP controller) | 2,000 | 本身需 hardened by design，非 TMR |
| Debug / Telemetry counter | 500 | 錯誤可容忍 |

**TMR 功耗影響**：
- TMR 三重化邏輯增加約 2x 動態功耗（第三份 + voter 額外切換）
- 估計 PL 動態功耗增加 ~0.8W
- Active 模式：PS 1.5W + PL 2.2W (含 TMR) + I/O 0.3W = **4.0W** → 符合 B-005 OBC Active 4.0W envelope

### 3.3 Configuration Scrubbing

SRAM-based FPGA 的 configuration bits 會被 SEU 翻轉，需要週期性比對並修正。

**Scrubbing 機制**：

| 項目 | 規格 | 說明 |
|------|------|------|
| 介面 | Xilinx ICAP (Internal Configuration Access Port) | PL 內部自存取，不需外部控制器 |
| Golden Bitstream 儲存 | NOR Flash (256 Mbit, Xiphos Q7s 內建) | 讀取速度 80 MB/s (Quad SPI mode) |
| Bitstream 大小 | 36 Mbit = 4.5 MB | Zynq-7020 full device |
| 單次 Scrub 時間 | 4.5 MB / 80 MB/s = **56 ms** | 讀取 + 比對 + ECC 修正 |
| Scrubbing 週期 | **100 ms** | 每秒 10 次 scrub |
| Scrub 方式 | Frame-by-frame readback + CRC 比對 | 偵測到 mismatch → 從 Golden 修正該 frame |

**Scrubbing 週期設計依據**：
- 期望 SEU rate = 1 upset/day = 每 86,400 秒 1 次
- 100 ms 週期 → SEU 發生後最遲 100 ms 內被偵測並修正
- 即使在 4 min contact window 內，最多累積 0.04 / 86,400 x 240 = 0.00028 次 SEU → 幾乎不可能有 2 個 SEU 同時影響同一 TMR module

**Scrubbing 功耗**：
- NOR Flash 讀取 + ICAP 寫入：~50 mW（已計入 PL 2.2W 內）
- Duty cycle: 56ms / 100ms = 56% → 平均 ~28 mW

### 3.4 Watchdog + Safe Mode

多層故障偵測與恢復機制：

| 層級 | 機制 | 觸發條件 | 動作 |
|------|------|---------|------|
| L1 — SW Watchdog | FreeRTOS task watchdog | 任何 FSW task 逾時 2 sec | 重啟該 task，紀錄 event |
| L2 — HW Watchdog (OBC) | Zynq PS WDT | ARM core hang > 5 sec | OBC warm reboot (PS reset) |
| L3 — HW Watchdog (EPS) | EPS P31u 內建 WDT | OBC 未餵狗 > 30 sec | EPS power cycle OBC (cold reboot) |
| L4 — Safe Mode | FSW FDIR logic | V_batt < 6.5V / comm loss > 48h / 連續 3 次 EPS fault | 關閉 S-band PA, TT&C beacon 30 sec, 降 OBC clock |

**Safe Mode 功耗**（ref: B-002 Section 5.1）：
- OBC Safe Standby: 1.0W（ARM 降頻至 333 MHz, PL 部分關閉, 僅保留 scrubber + TT&C UART）
- TT&C Beacon: 0.8W（每 30 秒發送 HK packet）
- ADCS Detumble: 0.3W（MTQ-only B-dot 控制）
- 系統總計: 2.4~2.9W → 在 Safe Mode 預算內

---

## 4. FSW 模組架構

Flight Software 架構基於 FreeRTOS，運行於 ARM Cortex-A9 PS 端：

| # | 模組名稱 | 執行頻率 | 優先序 | 功能描述 |
|---|---------|:--------:|:------:|---------|
| 1 | **Task Scheduler** | 1 kHz (tick) | Highest | FreeRTOS kernel tick, 任務排程, 時間管理 |
| 2 | **TM/TC Handler** | Event-driven | High | AX.25 frame 解析 (TC), housekeeping 封裝 (TM), 經 UART 與 TT&C 通訊 (IF-06) |
| 3 | **ADCS Control Loop** | 10 Hz | High | 讀取姿態四元數 (SPI, IF-03), 計算 PD 控制指令, 下達 MTQ/RW torque |
| 4 | **EPS Manager** | 1 Hz | Medium | I2C polling EPS (IF-01/02), 讀取 V_batt/I_solar/T_batt, 功率開關控制 |
| 5 | **Thermal Controller** | 0.5 Hz | Medium | 讀取 6 ch thermistor (XADC, IF-09), PID 控制 heater GPIO (IF-07) |
| 6 | **SDR Manager** | On-demand | Medium | 接觸窗口前 2 min 啟動 PL SDR pipeline, 設定 Doppler 參數, 監控 BER |
| 7 | **FDIR Engine** | 2 Hz | Low | 故障偵測: EPS comm fault counter, 電池電壓監控, 姿態偏差門檻, watchdog 餵狗 |

**記憶體配置**：
- FreeRTOS heap: 128 KB (from 256 KB SRAM)
- FSW image: ~2 MB (stored in QSPI NOR Flash, loaded to DDR3 at boot)
- Telemetry buffer: 16 MB (DDR3, circular buffer for 24h HK data)
- Total DDR3 usage: ~64 MB / 1 GB available → 充裕

---

## 5. Boot Sequence

上電至正常運作的 5 步驟啟動序列：

```
Step 1: Power-on (EPS → OBC 3.3V/5V)
  │  ● EPS P31u output enable → OBC power rails stable (< 100 ms)
  │  ● Zynq BootROM 從 QSPI NOR Flash 讀取 FSBL (First Stage Boot Loader)
  │
  ▼
Step 2: QSPI Boot (FSBL → U-Boot → FreeRTOS)
  │  ● FSBL 初始化 DDR3 controller, clock tree
  │  ● 載入 FSW image 至 DDR3 (2 MB, ~25 ms @ 80 MB/s)
  │  ● CRC32 校驗 FSW image → PASS 則跳轉, FAIL 則載入 backup image
  │  ● 啟動 FreeRTOS kernel
  │  ● 時間：~500 ms
  │
  ▼
Step 3: FSW Initialization
  │  ● 初始化所有 HW driver: I2C, SPI, UART, GPIO, XADC
  │  ● 啟動 EPS Manager → 讀取電池狀態 → 確認 V_batt > 6.5V
  │  ● 啟動 FDIR Engine → 開始 watchdog 餵狗
  │  ● 啟動 TM/TC Handler → TT&C UART ready
  │  ● 時間：~2 sec
  │
  ▼
Step 4: FPGA PL Configuration
  │  ● FSW 從 QSPI NOR Flash 讀取 PL bitstream (4.5 MB)
  │  ● 經 PCAP (Processor Configuration Access Port) 載入 PL
  │  ● Bitstream CRC 校驗 → PASS 則啟用 PL
  │  ● 啟動 Config Scrubber → 100 ms 週期開始
  │  ● 時間：~1 sec (4.5 MB / 80 MB/s + CRC + init)
  │
  ▼
Step 5: Subsystem Bring-up
  │  ● 啟動 ADCS Control Loop → SPI link to ADCS verified
  │  ● 啟動 Thermal Controller → Thermistor readback verified
  │  ● SDR pipeline standby（等待接觸窗口觸發）
  │  ● 發送 boot complete TM 至 TT&C
  │  ● 若為首次上電 → 進入 Safe Mode (detumble)
  │  ● 若為正常 reboot → 進入 Nominal Sunlit mode
  │  ● 時間：~1 sec
  │
  ▼
Total Boot Time: ~5 sec (power-on to operational)
```

**Boot 冗餘設計**：
- QSPI NOR Flash 分區：Golden FSW (A) + Backup FSW (B) + Golden Bitstream + Backup Bitstream
- 若 FSW image A CRC 失敗 → 自動切換至 image B
- 若 PL bitstream CRC 失敗 → 3 次重試後進入 PS-only Safe Mode（無 SDR，僅 TT&C beacon）

---

## 6. LUT Utilization 估算

Zynq-7020 (XC7Z020) FPGA fabric 可用資源：**53,200 LUT**

### 6.1 模組 LUT 分配

| # | 模組 | LUT (no TMR) | TMR? | LUT (with TMR) | 說明 |
|---|------|:------------:|:----:|:--------------:|------|
| 1 | QPSK Demodulator (Rx) | 3,500 | Yes | 10,500 | 載波恢復 + 時序恢復 + 符號判決 |
| 2 | QPSK Modulator (Tx) | 2,500 | Yes | 7,500 | 脈衝成形 + I/Q 上混頻 |
| 3 | Doppler NCO | 1,500 | Yes | 4,500 | 數控振盪器, 頻偏預補償 |
| 4 | FSW Critical SM | 1,000 | Yes | 3,000 | 模式轉移 + Safe Mode 狀態機 |
| 5 | AXI Bus Controller | 3,000 | Yes | 9,000 | AXI4-Lite + AXI4-Stream 橋接 |
| 6 | Config Scrubber | 2,000 | No (*) | 2,000 | ICAP controller + CRC engine |
| 7 | Debug / TM Counter | 500 | No | 500 | 效能計數器, non-critical |
| | **Total** | **14,000** | | **37,000** | |

(*) Config Scrubber 使用 hardened-by-design 方法（手動佈局、分散式 coding），不使用 TMR 避免雞生蛋問題。

### 6.2 Utilization Summary

| 項目 | 數值 |
|------|:----:|
| Total LUT used | 37,000 |
| Zynq-7020 available LUT | 53,200 |
| **Utilization** | **69.5%** |
| Remaining LUT | 16,200 |
| Margin | 30.5% |

**評估**：69.5% utilization 在 FPGA 設計最佳實踐範圍內（一般建議 < 80% 以確保 timing closure）。剩餘 16,200 LUT 可供未來功能擴充（如 FEC encoder 升級、進階 Doppler tracking）。

---

## 7. 功耗驗證

對照 B-005 Power Budget v2 的 OBC 功耗 envelope：

### 7.1 各模式功耗拆解

| 模式 | ARM PS (W) | FPGA PL (W) | I/O + Misc (W) | **OBC Total (W)** | Budget (W) | 狀態 |
|------|:----------:|:-----------:|:--------------:|:-----------------:|:----------:|:----:|
| **Standby** | 0.8 | 0.4 (scrubber only, SDR off) | 0.3 | **1.5** | 1.5 | PASS |
| **Active** | 1.5 (full clock) | 2.2 (SDR + TMR + scrubber) | 0.3 | **4.0** | 4.0 | PASS |
| **Safe** | 0.5 (half clock 333MHz) | 0.2 (scrubber only, min) | 0.3 | **1.0** | 1.0 | PASS |
| **Peak** | 1.5 | 2.5 (boot/reconfig transient) | 0.3 | **4.3** | 5.0 | PASS |

### 7.2 功耗細項說明

**Standby Mode (1.5W)**：
- ARM PS 0.8W：雙核之一休眠 (WFI), 時脈降至 500 MHz
- FPGA PL 0.4W：僅 Config Scrubber + AXI minimal logic 運作；SDR pipeline clock-gated
- I/O 0.3W：UART (TT&C Rx standby) + I2C (EPS polling 1 Hz) + XADC (thermistor)

**Active Mode (4.0W)**：
- ARM PS 1.5W：雙核全速 667 MHz, DDR3 active, 所有 FSW task 運行
- FPGA PL 2.2W：SDR 全速 (QPSK demod/mod + Doppler NCO) + TMR overhead + Scrubber
- I/O 0.3W：SPI 10 MHz (S-band baseband, IF-04) + UART + GPIO active

**Mitigation M2 回應**（ref: B-005 Section 7.3）：
- B-005 建議 OBC standby 從 1.5W 降至 1.2W (FPGA clock gating)
- **可行性評估**：若 Standby 時完全關閉 PL clock（PL 0.1W static leakage only），可達 PS 0.8 + PL 0.1 + I/O 0.3 = **1.2W**
- **風險**：PL 完全停鐘後恢復需 ~50 ms（重新啟動 scrubber），期間 SEU 無防護。建議僅在 EOL 能量收支確認需要時啟用此模式。

### 7.3 系統功耗交叉驗證

| 模式 | OBC | EPS | ADCS | S-band PA | TT&C | Heater | **System Total** | B-005 Budget |
|------|:---:|:---:|:----:|:---------:|:----:|:------:|:----------------:|:------------:|
| Nominal Sunlit | 1.5 | 0.3 | 0.5 | 0.0 | 0.2 | 0.0 | **2.5** | 2.5 PASS |
| Contact Window | 4.0 | 0.3 | 0.5 | 4.0 | 1.5 | 0.0 | **10.3** | 10.3 PASS |
| Eclipse Nominal | 1.5 | 0.3 | 0.5 | 0.0 | 0.2 | 0.5 | **3.0** | 3.0 PASS |
| Safe Mode | 1.0 | 0.3 | 0.3 | 0.0 | 0.8 | 0~0.5 | **2.4~2.9** | 2.4~2.9 PASS |

> **註**：EPS self-consumption 0.3W 為 EPS 獨立功耗，不計入 OBC envelope。所有模式功耗均符合 B-005 Power Budget v2 定義。

---

## 8. 介面實作摘要

對照 B-002 ICD v1，OBC 側各介面的實作方式：

| ICD 編號 | 介面 | 實作端 | 驅動方式 | 時脈/速率 | 備注 |
|---------|------|:------:|---------|:--------:|------|
| IF-01/02 | OBC ↔ EPS (I2C) | PS MIO | Linux I2C driver / FreeRTOS task | 100 kHz | 1 Hz polling, slave addr 0x28 |
| IF-03 | OBC ↔ ADCS (SPI) | PS MIO | SPI master, FreeRTOS task | 1 MHz | 10 Hz ADCS control loop |
| IF-04 | OBC ↔ S-band baseband (SPI) | **PL** | AXI-SPI IP core, DMA | 10 MHz | 基帶 I/Q stream, contact window only |
| IF-05 | OBC ↔ S-band ctrl (UART) | PS MIO | UART driver | 115200 baud | PA enable, freq config, gain ctrl |
| IF-06 | OBC ↔ TT&C (UART) | PS MIO | UART driver | 9600 baud | AX.25 frame Tx/Rx |
| IF-07 | OBC → Heater (GPIO) | PS MIO | GPIO output | On/Off | 2 ch, MOSFET gate drive |
| IF-08 | OBC → Antenna Deploy (GPIO) | PS MIO | GPIO output | One-shot | Arm/Fire 雙重確認 + EPS WDT interlock |
| IF-09 | OBC ← Thermistor (ADC) | PS XADC | 12-bit ADC, 6 ch | 1 Hz | Battery, OBC, PA, Struct x2, Solar |

---

## 9. NOR Flash 分區規劃

Xiphos Q7s 內建 256 Mbit (32 MB) QSPI NOR Flash，分區如下：

| 區段 | 起始位址 | 大小 | 內容 |
|------|:-------:|:----:|------|
| FSBL | 0x000000 | 256 KB | First Stage Boot Loader |
| FSW Image A (Golden) | 0x040000 | 4 MB | FreeRTOS + FSW (primary) |
| FSW Image B (Backup) | 0x440000 | 4 MB | FreeRTOS + FSW (backup) |
| PL Bitstream A (Golden) | 0x840000 | 5 MB | FPGA config (primary, 36 Mbit + header) |
| PL Bitstream B (Backup) | 0xD40000 | 5 MB | FPGA config (backup) |
| Config / Parameter | 0x1240000 | 1 MB | 軌道參數, ADCS calibration, Doppler table |
| Telemetry Log | 0x1340000 | 12 MB | 壓縮 HK data (overwrites cyclically) |
| **Reserved** | 0x1F40000 | ~0.75 MB | 未分配, 留作擴充 |
| **Total** | | **32 MB** | |

---

## 10. 結論

### 10.1 設計摘要

1. **處理器平台**：Zynq-7020 (Xiphos Q7s) 提供 ARM Cortex-A9 + 53K LUT FPGA，滿足 FSW + SDR 雙需求於單一 SoC。

2. **SEU 防護三層架構**：
   - **Layer 1 — TMR**：SDR 基帶核心 + FSW 關鍵狀態機三重化，LUT 11,500 → 34,500（佔 65%）
   - **Layer 2 — Config Scrubbing**：ICAP 100 ms 週期，56 ms 完成全 device scrub，SEU 影響時間窗極小
   - **Layer 3 — Watchdog + Safe Mode**：SW/HW/EPS 三級 watchdog，最終 fallback 為 EPS power cycle

3. **LUT Utilization**：37,000 / 53,200 = **69.5%**，在 80% 設計上限內，保留 30.5% margin 供未來擴充。

4. **功耗驗證**：
   - Standby 1.5W — 符合 B-005 envelope
   - Active 4.0W — 符合 B-005 envelope（含 TMR overhead）
   - Safe 1.0W — 符合 B-005 envelope
   - 可選 clock gating 模式進一步降至 1.2W standby（回應 B-005 Mitigation M2）

5. **Boot Time**：Power-on to operational < 5 sec，含 FSW CRC 校驗 + PL bitstream 載入。

### 10.2 Wave 3 待處理項目

| # | 項目 | 負責 Agent | 說明 |
|---|------|-----------|------|
| 1 | OBC 散熱路徑設計 | Mech/Thermal Agent | OBC active 4.0W 集中於 Zynq die (~10x10 mm), 需導熱至結構面板 |
| 2 | SDR 基帶詳細設計 | SW/FW Agent | QPSK demod/mod RTL, Doppler NCO 參數, BER 模擬 |
| 3 | FSW 詳細設計 | SW/FW Agent | FreeRTOS task 優先序調校, FDIR 門檻值校準 |
| 4 | EMC/EMI 評估 | SE Agent | SPI 10 MHz + FPGA switching noise 對 S-band 接收機干擾分析 |
| 5 | Radiation Test Plan | QA Agent | Zynq-7020 TID/SEE 測試需求, TMR 驗證計畫 |
