# 低軌衛星通訊設計概論 知識庫

> 蒸餾自 TASA 課程教材（詹鎮宇研究員）- 2026/04/01 講次

## 目錄
1. [課程總覽與 LEO 基本前提](#1-課程總覽與-leo-基本前提)
2. [GEO vs. LEO 架構典範轉移](#2-geo-vs-leo-架構典範轉移)
3. [DVB-S2X 與 5G NTN 波形比較](#3-dvb-s2x-與-5g-ntn-波形比較)
4. [Link Budget 概念](#4-link-budget-概念)
5. [SDR 軟體定義無線電](#5-sdr-軟體定義無線電)
6. [FPGA/RFSoC 硬體平台](#6-fpgarfsoc-硬體平台)
7. [SEU 防護策略](#7-seu-防護策略)
8. [PCB IPC 標準與製造](#8-pcb-ipc-標準與製造)
9. [星載介面協定](#9-星載介面協定)
10. [頻段取捨：Ku vs. Ka](#10-頻段取捨ku-vs-ka)
11. [環境挑戰應對](#11-環境挑戰應對)
12. [UAV 通訊延伸](#12-uav-通訊延伸)

---

## 1. 課程總覽與 LEO 基本前提

### 課程主題架構
- **System Engineering：** Life Cycle, V-model, SCRUM, SDR 實作
- **Environment in Space：** 溫度、輻射
- **Communication System：** Link Budget, Fading, Protocol, Signal Processing
- **Design & Implementation：** RF & Antenna, Baseband DSP & SDR, PCB IPC, Parts Selection, Testing
- **Case Study：** 失敗案例分析、B5G 發展

### LEO 衛星基本限制
- **軌道週期：** ~96.7 min (500 km SSO)
- **地面站接觸時間：** 每次約 2-4 min
- **不是每圈都過：** 取決於地面站緯度與軌道傾角
- **Eclipse 影響：** 進入地影時無太陽能供電

---

## 2. GEO vs. LEO 架構典範轉移

| 特性 | 傳統 GEO | LEO 星座 |
|------|---------|---------|
| 高度 | 36,000 km | ~500 km |
| 延遲 | ~500 ms (RTT) | 25-60 ms (RTT) |
| 架構 | 透明轉發 (Bent-pipe) | 星上處理 (Regenerative SDR) |
| 覆蓋 | 單顆覆蓋 1/3 地球 | 需星座 (數百~數千顆) |
| 波形 | 單載波 DVB-S2 | OFDM / 5G NTN |
| 概念 | 靜止廣播器 | 空中基地台 (gNB in the sky) |
| 速度 | 靜止 | 7.5 km/s |

### RTT 延遲比較
| 軌道 | 單程距離 | RTT |
|------|---------|-----|
| LEO | ~500 km | 30-50 ms |
| MEO | ~8,000 km | 125-250 ms |
| GEO | ~36,000 km | 600-800 ms |

---

## 3. DVB-S2X 與 5G NTN 波形比較

### DVB-S2X
- 單載波傳輸，依賴 PL-Pilots 進行相位恢復
- 適合彎管轉發架構 (Bent-pipe)
- ModCod 自適應：QPSK → 16APSK → 64APSK
- 同步：固定間隔實體層引導符號 (PL-Pilots)

### 3GPP 5G NTN (Rel-17/18/19)
- OFDM 多載波架構，引入 PTRS 動態可調相位跟蹤
- 支援 Massive MIMO 與 Beam-hopping
- **Rel-17/18 (透明轉發)：** gNB 在地面站，LEO RTT 8-26 ms，彎管式轉裝
- **Rel-19 (再生轉發)：** gNB 在衛星上，RTT ~4-13 ms，支援 ISL (Xn Interface)

### 終端連線生命週期 (7 階段)
1. **目標偵測 (Target Detection & Doppler)：** UE 偵測 SSB，GNSS 預補償 ±48 kHz 都卜勒偏移
2. **初始交握 (Handshake & Sync)：** Timing Advance 補償衛星與地面間的電磁傳播延遲
3. **路由決策 (Payload Routing)：** 星上或地面決定資料路由
4. **數據交換 (Data & HARQ)：** 利用 AMC 自適應調變與編碼
5. **波束追蹤 (Mobility & Beam)：** Massive MIMO 動態波束追蹤
6. **邊緣衰減 (Edge Degradation)：** 低仰角時路徑損耗劇增
7. **條件換手 (Conditional Handover, CHO)：** R17 引入基於時間/位置的 CHO

---

## 4. Link Budget 概念

### 核心公式
```
Received Power (dBW) = EIRP - FSPL + G/T - L_atm - L_rain - L_misc
```

### 自由空間路徑損耗 (FSPL)
```
FSPL (dB) = 20*log10(d) + 20*log10(f) + 32.44
```
其中 d 為距離 (km)，f 為頻率 (MHz)

### LEO 通訊特殊考量
- 極端路徑損耗波動 > 20 dB（仰角變化）
- 都卜勒頻移：Ka 頻段可高達 ±480 kHz
- 需即時 CQI 反饋與 AMC (自適應調變與編碼) 機制

---

## 5. SDR 軟體定義無線電

### 核心概念
- 將傳統硬體射頻處理改為軟體/韌體實現
- 可通過軟體升級改變波形、協定、調變方式
- 太空 SDR 需考慮輻射防護與功耗限制

### 商用 SDR 參考
| 產品 | 製造商 | 特點 |
|------|--------|------|
| SDR-1001 | CesiumAstro | 4Rx/4Tx，信用卡大小，搭載 FPGA |
| ADRV9009-ZU11EG | ADI + Xilinx | RF-SOM，寬頻收發器 |
| AD9361/AD9364 | Analog Devices | SDR 界「瑞士刀」，Silvus/YTTEK 等模組核心 |
| ADRV9002 | Analog Devices | 新一代低功耗、高抗擾方案 |

---

## 6. FPGA/RFSoC 硬體平台

### Xilinx/AMD Defense-Grade SoC 比較

| 特性 | XQ Zynq-7000 | XQ Zynq US+ EG | XQ Zynq US+ EV | XQ Zynq US+ RFSoC |
|------|-------------|----------------|----------------|-------------------|
| Application CPU | Dual Cortex-A9 800MHz | Quad Cortex-A53 1.33GHz | Quad Cortex-A53 1.33GHz | Quad Cortex-A53 1.33GHz |
| Real-Time CPU | -- | Dual Cortex-R5F 533MHz | Dual Cortex-R5F 533MHz | Dual Cortex-R5F 533MHz |
| High-Speed Analog | -- | -- | -- | 14-bit DAC 10 Gs/s, 14-bit ADC 5 Gs/s |
| Logic Cells | 85K-444K | 154K-1,143K | 256K-504K | 930K |
| DSP Slices | 220-2,020 | 360-3,528 | 1,248-1,728 | 4,272 |
| 溫度範圍 | -40 to +125C | -55 to +125C | -55 to +125C | -55 to +125C |
| 特殊功能 | PCIe Gen2 | ECC on all memories, 256-bit PUF | GPU (Mali-400 MP2) | SD-FEC, RF-ADC/DAC |

### RFSoC 架構亮點
- 將 ADC/DAC 直接整合進晶片，實現「直接射頻取樣 (Direct RF Sampling)」
- Processing System (PS) + Programmable Logic (PL) 雙核架構
- 內建 SD-FEC (Soft-Decision Forward Error Correction)
- 支援 GigE, CAN, SPI, UART, PCIe 等衛星常用介面

---

## 7. SEU 防護策略

### 三層防護架構

| 層級 | 方法 | 說明 |
|------|------|------|
| **HW** | Selective TMR/SDR | 硬體三模冗餘 (Triple Modular Redundancy)，關鍵路徑投票表決 |
| **FW** | 2 Updating Images + 1 Golden Image | Golden Image 含系統診斷，確保永遠可回復啟動 |
| **SW** | N-version Programming | 多版本軟體同時執行，共識機制輸出結果 |

### COTS 策略（CubeSat 適用）
1. COTS 元件 -- 更便宜且選擇多
2. 不做硬體冗餘 -- 降成本
3. 2X interconnection with no single point failure
4. 最高效能 + built-in fail-safe（full-set 與 reduced function 模式）
5. 目標：3 年任務壽命可接受 SEU 效應

---

## 8. PCB IPC 標準與製造

### IPC Class 等級

| Class | 用途 | 可靠度要求 |
|-------|------|---------|
| Class 1 | 一般電子產品 | 低 |
| Class 2 | 專用服務電子 | 中（工業/通訊設備） |
| Class 3 | 高可靠度電子 | 高（太空、軍用、醫療） |

### 關鍵 IPC 標準
| 標準 | 用途 |
|------|------|
| IPC-2221 | PCB 設計通用標準 |
| IPC-A-600 | 裸板驗收標準 |
| IPC-A-610 | 電子組裝驗收標準 |
| IPC-6012 | 剛性 PCB 性能規格 |
| IPC J-STD-001 | 焊接要求 |

---

## 9. 星載介面協定

### SPI vs. CAN Bus 比較

| 特性 | SPI | CAN Bus |
|------|-----|---------|
| 拓撲 | 主從式 (Master-Slave) | 匯流排式 (Multi-master) |
| 功能 | 同步串列通訊 | 非同步訊息式協定 |
| 速率 | ~1 Mbps | ~1 Mbps |
| 線纜長度 | < 10 m | ~10 m |
| 錯誤校正 | 無 | 有 (內建 CRC) |
| 延遲 | 低 | 中 |
| 應用 | 週邊控制 (sensor, memory) | 汽車/航太/醫療 |

### SpaceWire (SpW)
- 基於 IEEE-1355 + LVDS
- 資料率高達 200 Mbps
- 典型線纜長度 ~1 m
- 支援 Logical Addressing 與 Router 網路拓撲
- 太空級標準，廣泛用於衛星子系統間高速資料傳輸

---

## 10. 頻段取捨：Ku vs. Ka

| 特性 | Ku-band (SpaceX 主力) | Ka-band (Amazon 主力) |
|------|---------------------|---------------------|
| 頻率範圍 | 10.7-14.5 GHz | 17.7-30.0 GHz |
| 波長特性 | 較大，平穩穿透雨滴 | 極短，劇烈大氣散射與雨衰 |
| 天候容忍度 | 高 | 低（需高 EIRP 補償） |
| 可用頻寬 | 較小 | 超高頻寬密度 |
| 元件製程 | 成熟 | 需緊密排列，散熱困難 |

### Starlink UT3-V1 (Ku-band)
- 孔徑：0.51 公尺
- TX Gain：36.4 dBi
- 仰角極限：25 度
- 核心哲學：**Robustness via Aperture**（大面積容錯）

### Amazon Kuiper Standard (Ka-band)
- 孔徑：< 28 cm (11 吋)
- Max EIRP：45.8 dBW
- 仰角極限：35 度
- 核心大腦：Prometheus SoC（5G 級數位訊號處理）
- 核心哲學：**Capacity via Integration**（晶片算力突破物理限制）

---

## 11. 環境挑戰應對

### 克服極端路徑損耗
- 仰角從 90 度到 25 度，路徑損耗波動 > 20 dB
- 透過 CQI 反饋 + AMC 自適應切換：高仰角用 64APSK（高吞吐），低仰角用 QPSK（強健）

### 征服都卜勒頻移
- LEO 速度 7.5 km/s，Ka 頻段都卜勒偏移可達 ±480 kHz
- **DVB-S2x 策略：** PL-Pilots 固定間隔相位恢復
- **5G-NTN 策略：** PTRS 動態可調相位跟蹤參考訊號

---

## 12. UAV 通訊延伸

### 下一代 UAV 通訊架構三大支柱
1. **AI-Native SDR：** 認知無線電，動態適應電磁環境，自主規避干擾
2. **MIMO 陣列天線與波束成形：** 提升鏈路預算與指向性
3. **先進抗干擾波形與編碼：** FHSS + OFDM + LDPC 強韌編碼

### KPI 指標（軍規等級）
| 指標 | 目標值 |
|------|--------|
| BER | < 10^-7 @ SNR 10 dB |
| Jamming Margin (J/S) | > 15 dB |
| Hopping Rate | 1000 hops/sec |
| Data Rate | > 10 Mbps |
| MTBF | > 8,000 hrs |
| Sync Accuracy | < 100 ns |

### 台灣 UAV SDR 產業鏈
- **上游：** 聯發科 (SoC), 全訊科技 (GaN SSPA), 耀登/鐳洋 (mmWave 天線)
- **中游：** 円通科技/YTTEK (SDRone), 創未來科技 (AESA 雷達/干擾器)
- **下游：** 雷虎科技 (Thunder Tiger), 中光電智能機器人 (CIRC)
- **國際：** AMD-Xilinx (FPGA), ADI (RF Transceiver), Silvus (MN-MIMO), Doodle Labs (Mesh Rider)
