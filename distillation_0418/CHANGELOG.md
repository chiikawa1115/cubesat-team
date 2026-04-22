# 0418 版蒸餾 CHANGELOG（相對於 0401 舊版）

> 蒸餾日期：2026-04-22
> 來源：`20260422 低軌衛星通訊設計概論_0418.pdf`（共 114 頁）
> 4 段並行蒸餾結果整合

---

## 整體結構變化

| 區塊 | 舊版 (0401/0408) | 新版 (0418) | 變動 |
|------|---------------|-------------|------|
| Fail Cases 章節 | 無 | **10 個案例深度分析 + Gruhl Study** | 🆕 新章節（p.13-30） |
| Link Budget | 概念 + 公式 | **Tranzeo 完整計算案例 + 極端情境對比** | 🔁 數值化 |
| AESA | 無 | **17 頁完整章節**（p.44-60） | 🆕 新章節 |
| PCB IPC | 基本 Class 1/2/3 | **完整 IPC 標準樹 + 42 種鍍銅缺陷 + 間距表** | 🔁 大幅擴充 |
| Baseband + SDR | 介紹 | **Prometheus SoC + 80/20 分流 + NoC** | 🆕 架構深度 |
| 專利分析 | 無 | **US Patent 12,244,396 B1 拆解** | 🆕 IP 防護 |

---

## 數值變動清單（務必同步更新）

| 參數 | 舊值 | 新值 | 影響 |
|------|------|------|------|
| 28 GHz Doppler Shift | ±480 kHz | **±700 kHz** | OFDM 同步、PTRS 設計 |
| Ka 50 mm/h 雨衰 | 未具體 | **-22.0 dB** | Link Budget margin |
| LEO 活躍衛星數 | 未提 | **15,295 顆** (2026/04) | 產業分析 |
| Starlink 數量 | ~4500 | **10,166 顆** | 市場佔 66% |
| Kessler 閾值 | 未提 | **50,000 大型物體** (>10 cm) | 軌道永續性 |
| ITU 申請總數 | 未提 | **>100,000 顆** | 頻譜飽和 |
| ADC/DAC 規格 | 一般 | **12-bit 1.25 Gsps** | 基頻硬體 |
| EVM 目標 | 未具體 | **<3% (-30.5 dB)** | 高階 APSK |
| PER 目標 | 未具體 | **<10⁻⁵** | QoS 保證 |
| LDPC Coding Gain | 未具體 | **8-10 dB** | 邊緣場景 |

---

## Link Budget 極端情境對比（新版核心表，必背）

| 參數 | 最佳 (18 GHz DL, 90°, 晴空) | 極限 (28 GHz UL, 25°, 暴雨) |
|------|---|---|
| EIRP | +50.5 dBW | +50.0 dBW |
| FSPL | -174.2 dB | -184.0 dB |
| Atmospheric/Rain | -0.3 dB | **-22.0 dB** |
| G/T | +15.8 dB/K | +11.5 dB/K |
| **Final C/N** | **29.9 dB** | **-26.9 dB** |
| 模式 | DVB-S2X 256APSK 5.2 Gbps | Spread Spectrum / 10 MHz 窄頻 |

系統需承受 **>50 dB 動態範圍**。

---

## 失敗案例庫（新增 10 個）

| 案例 | 年代 | 斷裂環節 | 損失 |
|------|------|---------|------|
| IRIDIUM | 1990s | 需求工程 | 破產 |
| GLOBALSTAR | 2000s | 架構設計（SAA/TID 不足） | 軌道失效 |
| STARLINK | 2020s | 架構設計 | 2025 全球 150 分鐘斷訊 |
| 千帆星座 | 2024 | 需求工程 | 軌道失效 |
| MCO | 1999 | 介面管理（單位制） | $1.25 億 |
| Ariane 5 | 1996 | V&V（Heritage SW + 16-bit 溢位） | $5 億 |
| Hubble | 1990 | V&V（單一 RNC + 確認偏誤） | $8,600 萬修復 |
| NASA DART | - | 高風險妥協 | 任務全失 |
| Challenger | 1986 | 風險文化（O 環 + 偏差常態化） | 7 命 |
| Columbia | 2003 | 風險文化（泡棉 + 降級警告） | 7 命 |

**INCOSE/NASA AIAA 2024 結論**：60% 太空載具失效源自設計與溝通的系統性缺陷。

---

## Gruhl Study 成本曲線

- **1x** (Phase A 設計) → **5-10x** (Phase B/C 警告) → **21-78x** (Phase D I&T 激增) → **29-1500x** (Phase E 在軌危急紅區)
- NASA 原則：前期 SE 投資每減 1%，總成本 +10-20%
- **The Agile Fallacy**：「快速失敗」在純軟體可行，太空硬體絕對不行

---

## 5 大系統工程斷裂環節

| # | 環節 | 防衛策略 |
|---|------|----------|
| 1 | 需求工程 (Iridium) | 強制可驗證需求 + 市場驗證循環 |
| 2 | 架構設計 (Ariane 5) | HITL + 運作包絡重評估 |
| 3 | V&V (Hubble/MPL) | 獨立驗證工具 + 邊界測試 |
| 4 | 介面管理 (MCO) | 可執行 ICD + 自動化單位轉換 |
| 5 | 風險文化 (Challenger/Columbia) | 獨立技術權威 + 無情異常追蹤 |

---

## AESA 相控陣天線（新章節摘要）

### Beamforming 三架構對比
| 特性 | Analog | **Hybrid** | Digital |
|------|--------|-----------|---------|
| ADC/DAC | 共享 | 子陣列級 | 每單元獨立 |
| 耗電 | 低 | 中 | 極高（8 Tbps @ 1024 單元） |
| 多波束 | 單 | 有限多波束 | 無限 |
| 應用 | 固定回傳 | **LEO 主流** | 高階星上鏈 |

### 掃描損耗
- Boresight 35.8 dBi → 60° 掃描 31.5 dBi（4.3 dB 降幅，cos θ 規律）

### Starlink 終端演進
- Gen 1: 純數位 79 DBF + 8 FEM → Gen 4: 6 顆 DBF 驅動 1536 單元（混合架構量產）

### BFIC 廠商四強
| 廠商 | 產品 | 特色 |
|------|------|------|
| Anokiwave (Qorvo) | AWMF-0221 Gen-4 | CMOS 高整合、平價量產 |
| Renesas | F6122/F6522 | SiGe 雙波束、<100 ns 切換 |
| ADI | ADAR3000 | TTD 整合、4 波束、CSH/CSL 認證 |
| SatixFy/Launchip | Prime 2.0 / TBF0828A | 全數位 DBF ASIC |

### 關鍵挑戰
1. **Beam Squint**（寬帶 >100 MHz 0.5°-2.0° 偏斜）→ TTD 補償
2. **熱管理**（PA 效率 15-25%、645W 終端、λ/2 間距 5 mm、T_junction >150°C 臨界）→ 微流體冷卻 + 異質 3D 整合（GaN/SiGe/CMOS Chiplet）
3. **Make-Before-Break**（LEO 交接 <1 μs）→ 雙波束架構

### 測試方法
| 方式 | 距離 | AESA 診斷能力 | 用途 |
|------|------|---------------|------|
| 近場 (NF) | <10λ | 極高（單單元失效定位） | 研發診斷 |
| 遠場 (FF) | 公里級 | 低（僅整體） | 最終驗證 |
| **CATR** | 室內 | **最佳** | **衛星終端整機驗證** |

---

## PCB IPC 標準（擴充）

### 三層 IPC Class
| Class | 應用 | 容許度 |
|-------|------|--------|
| 1 Consumer | 消費 | 高 |
| 2 Industrial | 通訊/商務/儀器 | 中 |
| **3 High-Rel** | **衛星/航空/醫療** | **嚴格** |

### 完整 IPC 標準樹（新版展開）
- 設計：IPC-2221/2222/2152、IPC-7351、IPC-2581、IPC-2810
- 製造檢驗：IPC-A-600、IPC-6012
- 組裝：IPC-A-610、J-STD-001、J-STD-002、J-STD-609
- 清潔度：IPC-TM-650.2.3.25.1（離子汙染）

### PCB 設計流程 18 步
Start → Drawing Frame → Symbols → Components → Footprints → Schematic → Connect → Link to PCB → BOM → Mounting/Dimensions → Board Shape → Placement → Routing → Planes → **DRC/MRC** → Gerber/NC Drill → Correct Errors → Assembly Drawing.

### IR Drop 設計準則
- `V_drop = I × R`
- 陷阱：窄走線 / VIA 過孔不足 / 「瑞士起司」鋪銅破碎
- 實例：10 mil 走線餵 Power IC → 一段時間後異常

---

## Baseband / SDR（新架構揭露）

### Prometheus SoC（AMD/Xilinx 衛星專用）
- Cortex-A53 多核 + HWA + Mesh NoC + ACE 快取一致性
- 片內 30 Gbps 吞吐、支援 100 GbE OISL

### 80/20 異構分流法則
- **80% HWA 固化**：2048-pt FFT、LDPC 解碼（4 Gbps 並行）、<10 pJ/bit
- **20% DSP/CPU 彈性**：信道估計、AMC、多協議轉接（DVB-S2X / 3GPP NTN）、路由決策

### NoC vs 傳統 AXI Crossbar
- AXI 在 >數百個 IP 核時佈線指數爆炸
- NoC Mesh + GALS（局部時鐘域）是 Tbps 級 SoC 唯一解

### 專利 US 12,244,396 B1（2025-03, SpaceX）
- Configurable OFDM Multi-Layer Receiver for SAT/UT/SAG
- 防護範圍：PILOT 子帶 + DATA 線性插值、邊帶導頻 + 部署感知參數切換
- 迴避策略：ZC 序列替換、本地計算、環境基礎濾波器

### 衛星 SDR 平台三強
| 平台 | 特色 |
|------|------|
| Xilinx Zynq UltraScale+ RFSoC | 8×14-bit ADC/DAC @5 Gsps |
| ADI ADRV9009-ZU11EG / AD9361 | DC-6 GHz Transceiver + JESD204C |
| AMD Prometheus | 衛星專用，NoC + HWA + ACE |

---

## 新技術名詞（需注入 agent 知識庫）

| 術語 | 定義 | 所屬 agent |
|------|------|-----------|
| Gruhl Study | SE 投資減 1% → 成本 +10-20% | SE / QA / CEO |
| Normalization of Deviance | 偏差常態化 | QA / CEO |
| Heritage SW Fallacy | 遺產軟體未重驗證 | SE / QA / SW-FW |
| HITL | Hardware-in-the-Loop | SW-FW / QA |
| KDP | Key Decision Point | PM / CEO |
| Programmable Frailty | 軟體故障降級模式 | SW-FW |
| MBSE (Cameo/TLA+/QVscribe) | Model-Based SE 工具鏈 | SE |
| AESA / BFIC / TTD | 相控陣 + 波束 IC + 真實時延 | Comm-Payload |
| Beam Squint | 寬帶掃描偏斜 | Comm-Payload |
| AiP / Chiplet / TSV | 封裝內天線 + 異質整合 | Comm-Payload / Mech-Thermal |
| NoC / ACE / GALS | 片上網路 + 快取一致性 | SW-FW |
| 80/20 HWA/DSP | 硬體加速 vs 軟體彈性分流 | SW-FW |
| Prometheus SoC | 衛星專用 SoC | Comm-Payload / SW-FW |
| TMR + LCL + Careful COTS | NewSpace 可靠度三要素 | SW-FW / QA |
| Kessler 50,000 閾值 | 軌道永續性紅線 | AOCS / CEO |

---

## 影響的 agent / reference 盤點

| 檔案 | 變動類型 |
|------|---------|
| `references/comm-design.md` | 🔁 大幅改寫（新增 AESA、Fail Cases、80/20、Prometheus、數值更新） |
| `references/pdf-paths.md` | 🆕 新增 0418 條目，更新 agent 對應表 |
| `references/system-engineering.md` | 🆕 新增 Gruhl Study、5 大斷裂環節、KDP、MBSE 工具鏈 |
| `agents/comm-payload.md` | 🆕 新增 AESA、BFIC、TTD、Prometheus、±700 kHz Doppler |
| `agents/systems-engineer.md` | 🆕 新增 Heritage Fallacy、HITL、ICD 可執行驗證 |
| `agents/qa-test.md` | 🆕 新增 60% 設計失效、偏差常態化、獨立驗證原則 |
| `agents/ceo.md` | 🆕 新增 NewSpace 哲學、Gruhl 成本曲線、LEO 永續性三維 |
| `agents/sw-firmware.md` | 🆕 新增 Prometheus、NoC/ACE、80/20、TMR+LCL |
| `agents/mech-thermal.md` | 🆕 新增 AESA 熱管理（645W、微流體、T_j >150°C） |
