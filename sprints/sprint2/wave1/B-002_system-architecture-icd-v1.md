---
deliverable: B-002
sprint: 2
wave: 1
author: SE Agent (陳建宏)
date: 2026-04-29
status: draft
reference_documents:
  - workspace/sprints/sprint1/power-budget-v1.1.md (Sprint 1 基線)
  - workspace/project.json (DCN-001)
---

# B-002：TASA-NTN-3U 系統架構方塊圖 + Interface Control Document v1

## 1. 文件概述

本文件定義 TASA-NTN-3U 3U CubeSat 的系統架構基線，包含子系統方塊圖、介面控制文件 (ICD)、子系統功能描述、及運作模式定義。本文件作為 Sprint 2 Wave 2 各 agent 設計展開的共同基準。

**任務摘要**：3U CubeSat，500 km SSO，S-band n236 NTN 透明轉發 (Rel-17 bent-pipe)，支援 100 bps IoT-NTN 下行，QPSK 1/2。

---

## 2. 系統架構方塊圖（文字描述版）

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        TASA-NTN-3U  3U CubeSat                        │
│                        500 km SSO ── S-band NTN                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐    I2C (Telemetry/Cmd)     ┌─────────────────────┐    │
│  │             │◄──────────────────────────► │                     │    │
│  │     EPS     │    3.3V / 5V / Unreg       │       OBC           │    │
│  │  GomSpace   │──────────────────────────► │   (Zynq-class       │    │
│  │   P31u      │                            │    SoC/FPGA)        │    │
│  │             │    Battery Bus (Unreg)      │                     │    │
│  │  Solar In───┤    to all subsystems        │                     │    │
│  │  Battery    │                            └──────┬──┬──┬──┬─────┘    │
│  │  10 Wh      │                                   │  │  │  │         │
│  └──────┬──────┘                                   │  │  │  │         │
│         │ Power Rails                              │  │  │  │         │
│         │ 3.3V / 5V / 12V(boost)                   │  │  │  │         │
│         │                                          │  │  │  │         │
│    ┌────┴────────────────┬──────────────┬──────────┘  │  │  │         │
│    │                     │              │             │  │  │         │
│    ▼                     ▼              ▼             │  │  │         │
│  ┌────────────┐  ┌─────────────┐ ┌──────────┐       │  │  │         │
│  │  S-band    │  │   TT&C      │ │  ADCS    │       │  │  │         │
│  │  酬載      │  │  (UHF)      │ │          │       │  │  │         │
│  │            │  │             │ │ MTQ x3   │       │  │  │         │
│  │ PA (4W DC) │  │ AX.25       │ │ RW  x1   │       │  │  │         │
│  │ LNA+Filter │  │ UHF Tx/Rx  │ │          │       │  │  │         │
│  │ Freq Synth │  │ Dipole Ant  │ │          │       │  │  │         │
│  └─────┬──────┘  └──────┬──────┘ └─────┬────┘       │  │  │         │
│        │                │              │             │  │  │         │
│        │ LVDS/SPI       │ UART         │ SPI         │  │  │         │
│        │ (Baseband      │ (AX.25       │ (Attitude   │  │  │         │
│        │  I/Q data)     │  frames)     │  Cmd/Tlm)   │  │  │         │
│        │                │              │             │  │  │         │
│        └────────────────┴──────────────┴─────────────┘  │  │         │
│                  All connect to OBC                      │  │         │
│                                                          │  │         │
│                            ┌──────────────────┐          │  │         │
│                            │  Thermal Control │◄─────────┘  │         │
│                            │  (Heater x2,     │  GPIO        │         │
│                            │   Thermistor x6) │  (On/Off)    │         │
│                            └──────────────────┘             │         │
│                                                              │         │
│                            ┌──────────────────┐             │         │
│                            │  Structure       │◄────────────┘         │
│                            │  (3U frame,      │  Deploy signal        │
│                            │   solar panels,  │  (GPIO burn-wire)     │
│                            │   antenna deploy)│                       │
│                            └──────────────────┘                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

電力匯流 (Power Bus)：
  EPS ──► [3.3V rail] ──► OBC, ADCS, TT&C (digital)
  EPS ──► [5V rail]   ──► OBC (FPGA core), S-band baseband
  EPS ──► [12V boost] ──► S-band PA (switched, contact window only)
  EPS ──► [Unreg]     ──► Heater (via OBC GPIO switch)

資料匯流 (Data Bus)：
  OBC ◄──I2C──►  EPS    (100 kHz, telemetry + power switching commands)
  OBC ◄──SPI──►  ADCS   (1 MHz, attitude quaternion + MTQ/RW commands)
  OBC ◄──SPI──►  S-band (10 MHz, baseband I/Q data stream)
  OBC ◄──UART──► TT&C   (9600 baud, AX.25 frames)
  OBC ──GPIO──►  Heater (on/off control, 2 channels)
  OBC ──GPIO──►  Antenna deploy (burn-wire trigger, one-shot)
```

---

## 3. Interface Control Document (ICD) v1

### 3.1 介面總覽矩陣

| # | 介面名稱 | 系統 A | 系統 B | 訊號類型 | 協定 | 電壓位準 | 速率/頻寬 | 接腳數 | 備注 |
|---|---------|--------|--------|---------|------|---------|----------|-------|------|
| IF-01 | OBC ↔ EPS 遙測/指令 | OBC | EPS (P31u) | Digital | I2C | 3.3V CMOS | 100 kbps | 2 (SDA, SCL) + GND | EPS 為 I2C slave (addr 0x28)，OBC 週期性 polling（1 Hz）讀取 V_batt, I_solar, T_batt |
| IF-02 | OBC ↔ EPS 電源開關 | OBC | EPS (P31u) | Digital | I2C (register write) | 3.3V CMOS | On-demand | 同 IF-01 | OBC 透過 I2C 寫入 EPS output channel enable register 控制各子系統供電 |
| IF-03 | OBC ↔ ADCS 姿態/指令 | OBC | ADCS Controller | Digital | SPI | 3.3V CMOS | 1 Mbps | 4 (MOSI, MISO, SCK, CS) + GND | OBC 為 SPI master；ADCS 回傳四元數 (quaternion)、角速度；OBC 下達 MTQ 電流指令 |
| IF-04 | OBC ↔ S-band 基帶資料 | OBC (FPGA) | S-band SDR Frontend | Digital | SPI (high-speed) | 3.3V LVTTL | 10 Mbps | 4 (MOSI, MISO, SCK, CS) + GND | 基帶 I/Q sample stream；FPGA 直接驅動 DAC/ADC；接觸窗口期間啟用 |
| IF-05 | OBC ↔ S-band 控制 | OBC | S-band Module | Digital | UART | 3.3V CMOS | 115200 baud | 2 (TX, RX) + GND | PA enable/disable、頻率設定、增益控制、溫度遙測回讀 |
| IF-06 | OBC ↔ TT&C (UHF) | OBC | UHF Transceiver | Digital | UART | 3.3V CMOS | 9600 baud | 2 (TX, RX) + GND | AX.25 封裝 frame；上行 TC 解碼 + 下行 TM 編碼；beacon 模式自動發送 |
| IF-07 | OBC → Heater 控制 | OBC | Heater (Kapton) | Discrete | GPIO | 3.3V → MOSFET gate | N/A (on/off) | 2 ch (GPIO + GND) | 2 組加熱器：Battery heater + Payload heater；OBC 讀溫度後決定開關 |
| IF-08 | OBC → Antenna Deploy | OBC | Burn-wire Mechanism | Discrete | GPIO | 3.3V → MOSFET gate | One-shot | 1 (GPIO + GND) | 部署後不可逆；需 EPS watchdog confirm + OBC 軟體 arm/fire 雙重確認 |
| IF-09 | OBC ← 溫度感測 | OBC | Thermistor x6 | Analog | ADC (OBC on-chip) | 0~3.3V | 1 Hz sampling | 6 ch (analog in) | 感測點：Battery, OBC, PA, Structure top/bottom, Solar panel back |
| IF-10 | EPS → OBC 供電 | EPS | OBC | Power | Regulated DC | 3.3V / 5V | N/A | 2 pairs (V+, GND) | 3.3V: digital logic (max 0.5A)；5V: FPGA core + I/O (max 1.0A) |
| IF-11 | EPS → ADCS 供電 | EPS | ADCS | Power | Regulated DC | 3.3V | N/A | 1 pair (V+, GND) | Max 0.2A (0.5W steady + 0.2W margin) |
| IF-12 | EPS → S-band PA 供電 | EPS | S-band PA | Power | Switched Boost | 12V | N/A | 1 pair (V+, GND) | Boost converter from battery；max 0.4A (4.0W DC)；OBC 控制 EPS switch ON 才供電 |
| IF-13 | EPS → TT&C 供電 | EPS | UHF Radio | Power | Regulated DC | 3.3V / 5V | N/A | 1 pair (V+, GND) | 3.3V digital + 5V RF PA；Tx max 0.5A (1.5W) |
| IF-14 | EPS → Heater 供電 | EPS | Heater | Power | Unregulated Battery | ~7.2V nom | N/A | 1 pair (V+, GND) | 透過 OBC GPIO MOSFET 開關；max 0.5W |
| IF-15 | Solar Panel → EPS | Solar Cells (body-mount) | EPS MPPT input | Power | Unregulated DC | 4.0~5.5V (2S config) | N/A | 2 pairs (V+, GND per panel) | BOL 6.5W (DCN-001)；MPPT 效率 90%；佈局：+X, -X, +Z 三面 |

### 3.2 介面電壓位準與 ESD 防護

| Rail | 標稱電壓 | 容許範圍 | 最大電流 | 保護措施 |
|------|---------|---------|---------|---------|
| 3.3V | 3.30V | 3.14 ~ 3.46V (5%) | 2.0A (total) | OBC 端每線串聯 ESD TVS (3.3V)；EPS 內建 OVP/OCP |
| 5V | 5.00V | 4.75 ~ 5.25V (5%) | 1.5A (total) | EPS 內建 foldback current limit |
| 12V (boost) | 12.0V | 11.0 ~ 13.0V | 0.4A | 僅 S-band PA 使用；EPS switched output；OBC arm 後才啟用 |
| Battery (unreg) | 7.2V nom | 6.0 ~ 8.4V (2S Li-ion) | 2.0A peak | Battery 內建 PTC + PCM |

### 3.3 匯流排仲裁與錯誤處理

- **I2C (IF-01/02)**：OBC 為唯一 master，無仲裁需求。Timeout 200 ms 無回應 → OBC 紀錄 EPS comm fault，連續 3 次 → 觸發 Safe Mode。
- **SPI (IF-03/04)**：OBC 為 master，CS 選擇。ADCS 與 S-band 使用不同 CS line，無衝突。
- **UART (IF-05/06)**：點對點，無仲裁。TT&C UART 採 AX.25 frame sync (0x7E flag)；S-band UART 採 proprietary command/response protocol。
- **GPIO (IF-07/08)**：單向輸出，OBC 寫入。Antenna deploy 需軟體 arm bit + hardware interlock (EPS watchdog)。

---

## 4. 子系統功能描述摘要

### 4.1 OBC -- On-Board Computer (Zynq-class SoC/FPGA)

執行飛行軟體 (FSW) 與 S-band SDR 基帶處理。ARM 處理器執行 RTOS (FreeRTOS)，管理任務排程、遙測收集、TC 命令解碼、ADCS 控制迴路、故障偵測與隔離恢復 (FDIR)。FPGA fabric 實現 NTN bent-pipe 基帶：數位上/下轉換、QPSK 調變/解調、1/2 率 Turbo/LDPC codec。Standby 1.5W，Active 4.0W（含 FPGA 基帶）。

### 4.2 EPS -- Electrical Power System (GomSpace P31u)

管理太陽能電池陣列 (body-mounted, 3 面) 的 MPPT 充電、Li-ion 電池組 (2S1P, 10 Wh BOL) 充放電保護、以及多路穩壓輸出 (3.3V/5V) 與可切換 boost 輸出 (12V)。提供 I2C 遙測介面回報電池電壓、電流、溫度、各通道功耗。內建 watchdog timer，OBC 逾時未餵狗則自動 power cycle OBC。自用功耗約 0.3W。

### 4.3 ADCS -- Attitude Determination & Control System

三軸姿態穩定，使用 3 組磁力矩器 (MTQ) 做粗調去旋 + 1 組微型反應輪 (RW) 做精穩指向。感測器包含磁力計 (MAG)、太陽感測器 (CSS)、與 MEMS 陀螺儀 (gyro)。透過 B-dot 解耦 + PD 控制器達成 nadir pointing (5 deg 精度目標)。穩態功耗 0.5W；反應輪峰值 ~1.0W（短暫姿態機動期間）。

### 4.4 S-band 酬載 (NTN Transparent Transponder)

NTN Rel-17 bent-pipe 透明轉發器：上行 UL 1980-2010 MHz (n256 UL)，下行 DL 2170-2200 MHz (n256 DL)。接收鏈路含 LNA + SAW BPF + 混頻器；發射鏈路含 DAC + up-converter + PA (DC 4.0W, RF out ~1.0W, PAE ~25%)。Patch antenna (6 dBi, nadir-pointing)。接觸窗口期間 OBC 啟用，非接觸時完全關閉 (0W)。

### 4.5 TT&C -- Telemetry, Tracking & Command (UHF)

UHF 頻段 (437 MHz band) 全向天線 (dipole)，半雙工收發。下行 9600 bps GMSK，上行 1200 bps AFSK。AX.25 協定封裝。Beacon 模式每 60 秒自動發送衛星 ID + 基本 housekeeping。Standby (Rx only) 0.2W，Tx active 1.5W。地面站 UHF 操控用於 commissioning、Safe Mode 恢復、與常規 TM/TC。

### 4.6 Structure & Thermal Control

3U CubeSat 標準結構 (340 x 100 x 100 mm)，Al 7075-T6 骨架。Body-mounted 太陽能板佈置於 +X, -X, +Z 三面。被動熱控為主 (MLI 包覆 + 黑色陽極處理散熱面)，主動加熱器 2 組 (Battery heater + Payload heater)，Eclipse 期間由 OBC 控制啟閉，維持電池溫度 > 0 degC。Antenna deploy mechanism 使用 burn-wire (Nichrome) 釋放 UHF dipole + S-band patch。

---

## 5. 運作模式表

### 5.1 模式定義

| 模式 | 觸發條件 | OBC | EPS | ADCS | S-band 酬載 | TT&C | Heater | 系統功耗 (W) |
|------|---------|-----|-----|------|------------|------|--------|-------------|
| **Nominal Sunlit** | 太陽光照 & 非接觸窗口 | Standby (1.5W) | Active (0.3W) | Active (0.5W) | OFF (0W) | Standby Rx (0.2W) | OFF (0W) | **2.5W** |
| **Contact Window** | AOS (地面站仰角 > 5 deg) | Active (4.0W) | Active (0.3W) | Active (0.5W) | PA ON (4.0W) | Tx Active (1.5W) | OFF (0W) | **10.3W** |
| **Eclipse Nominal** | 進入地球影區 & 非接觸 | Standby (1.5W) | Active (0.3W) | Active (0.5W) | OFF (0W) | Standby Rx (0.2W) | ON (0.5W) | **3.0W** |
| **Safe Mode** | FDIR 觸發 (EPS undervolt / OBC watchdog / comm loss > 48hr) | Safe Standby (1.0W) | Active (0.3W) | Detumble only (0.3W) | OFF (0W) | Beacon only Tx (0.8W) | Auto (0~0.5W) | **2.4~2.9W** |

### 5.2 模式轉移圖

```
                         ┌──────────────┐
          Power-on       │              │
     ───────────────────►│  Safe Mode   │
                         │  (Detumble   │
                         │   + Beacon)  │
                         └──────┬───────┘
                                │
                    Detumble complete
                    + Ground command
                                │
                                ▼
                    ┌───────────────────────┐
                    │                       │
              ┌─────┤   Nominal Sunlit      ├─────┐
              │     │   (OBC Standby)       │     │
              │     └───────────┬───────────┘     │
              │                 │                  │
         Eclipse            AOS trigger       FDIR fault
         entry              (contact)          detected
              │                 │                  │
              ▼                 ▼                  │
    ┌─────────────────┐  ┌──────────────┐         │
    │ Eclipse Nominal │  │   Contact    │         │
    │ (Heater ON)     │  │   Window     │         │
    └────────┬────────┘  │ (S-band ON)  │         │
             │           └──────┬───────┘         │
        Eclipse exit        LOS trigger           │
             │                  │                  │
             └──────────────────┘                  │
                    Back to                        │
                  Nominal Sunlit                   │
                                                   │
                         ┌─────────────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Safe Mode   │
                  │  (any mode   │
                  │   can enter) │
                  └──────────────┘
```

### 5.3 模式轉移條件明細

| 轉移 | 來源模式 | 目標模式 | 觸發條件 | 動作 |
|------|---------|---------|---------|------|
| T1 | Power-on / Deploy | Safe Mode | 首次上電或 EPS watchdog reset | OBC boot → detumble → beacon |
| T2 | Safe Mode | Nominal Sunlit | Detumble 完成 + 地面站確認指令 | 啟用 ADCS pointing mode |
| T3 | Nominal Sunlit | Contact Window | AOS (仰角 > 5 deg，由 OBC 軌道預報觸發) | OBC → Active，啟用 S-band PA + TT&C Tx |
| T4 | Contact Window | Nominal Sunlit | LOS (仰角 < 5 deg) 或 timer timeout (5 min guard) | 關閉 S-band PA，OBC → Standby |
| T5 | Nominal Sunlit | Eclipse Nominal | Eclipse entry (太陽感測器 < threshold 或軌道預報) | 啟用 heater (if T_batt < 5 degC) |
| T6 | Eclipse Nominal | Nominal Sunlit | Eclipse exit (太陽感測器 > threshold) | 關閉 heater |
| T7 | Any | Safe Mode | V_batt < 6.5V 或 OBC watchdog timeout 或 comm loss > 48 hr | 關閉所有非必要子系統，進入 beacon |

---

## 6. 系統質量與體積初估（參考用）

| 子系統 | 質量估計 (g) | 體積估計 (U) | 備注 |
|--------|-------------|-------------|------|
| OBC (Zynq board) | 80 | 0.3U (PC104 half-card) | 含 FPGA mezzanine |
| EPS (P31u) | 85 | 0.2U | GomSpace 標準品 |
| Battery (P31u 內建) | 155 | (含在 EPS 中) | 2S1P 18650, 10 Wh |
| ADCS (controller + actuators) | 200 | 0.4U | MTQ x3 整合於結構；RW 獨立模組 |
| S-band 酬載 (SDR + PA + Ant) | 250 | 0.5U | Patch antenna 外掛於 -Z 面 |
| TT&C (UHF radio + Ant) | 60 | 0.1U | Dipole 收合於 rail |
| Structure + Thermal | 800 | 1.5U (frame) | Al 7075 frame + MLI + heaters |
| **Total** | **~1630 g** | **~3.0U** | Margin to 4 kg CubeSat deployer limit: ~59% |

---

## 7. 附錄：Connector/Harness 初步規劃

| 連接器 | 類型 | 位置 | Pin count | 備注 |
|--------|------|------|-----------|------|
| J1: OBC ↔ EPS | PC/104 header (through-board) | Stack connector | 52-pin | 標準 PC/104 bus |
| J2: OBC ↔ ADCS | Hirose DF17 | Flying lead | 10-pin | SPI + power + GND |
| J3: OBC ↔ S-band | Hirose DF17 | Flying lead | 12-pin | SPI + UART + power + GND |
| J4: OBC ↔ TT&C | Hirose DF17 | Flying lead | 6-pin | UART + power + GND |
| J5: S-band RF | SMA (board-mount) | PA → Ant feed | 1 | 50 ohm coax |
| J6: TT&C RF | U.FL | Radio → Ant feed | 1 | 50 ohm micro-coax |
| J7: Solar Panel | JST-PH | Panel → EPS | 2-pin x3 panels | Power only |
| J8: Deploy | Molex Pico-Lock | OBC → Burn-wire | 2-pin | One-shot, fused |

---

## Wave 2 Cross-reading 通知

**Comm Agent (B-001 Link Budget v2)** 需讀取：
- 第 3 節 ICD 表 IF-04/IF-05：OBC ↔ S-band 介面定義（SPI 10 Mbps 基帶 + UART 控制）
- 第 4.4 節：S-band 酬載功能描述（PA DC 4.0W, RF ~1.0W, PAE ~25%, Patch antenna 6 dBi）
- 第 5.1 節 Contact Window 模式：系統功耗 10.3W，持續 4 min

**AOCS Agent (B-006 ADCS Trade Study)** 需讀取：
- 第 3 節 ICD 表 IF-03：OBC ↔ ADCS 介面定義（SPI 1 Mbps, 3.3V CMOS）
- 第 4.3 節：ADCS 功能描述（MTQ x3 + RW x1, nadir pointing 5 deg 目標）
- 第 5.1 節各模式 ADCS 功耗分配：Active 0.5W, Safe (Detumble) 0.3W, 峰值 ~1.0W

**SW/FW Agent (B-007 OBC/FPGA 架構)** 需讀取：
- 第 3 節 ICD 全表：OBC 需實作的所有介面（I2C x1, SPI x2, UART x2, GPIO x3+, ADC x6）
- 第 3.2 節：電壓位準定義（3.3V / 5V rails, 最大電流）
- 第 4.1 節：OBC 功能描述（RTOS + SDR baseband on FPGA）
- 第 5 節模式表：OBC Standby 1.5W vs Active 4.0W vs Safe 1.0W 的功能差異

**Struct/Thermal Agent** 需讀取：
- 第 3 節 ICD 表 IF-07/IF-09：Heater GPIO 控制 + 溫度感測點定義
- 第 6 節：質量/體積初估，作為結構佈局輸入
- 第 7 節：Connector/Harness 規劃，確認空間需求
