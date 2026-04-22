# 低軌衛星通訊設計概論 知識庫

> 蒸餾自 TASA 課程教材（詹鎮宇研究員）
> 整合版本：2026/04/01（基礎理論）+ **2026/04/18（最新重大改版，新增失敗案例、AESA、Prometheus SoC）**
> 最後更新：2026-04-22

## 目錄

**基礎理論（0401 版）**
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

**0418 新增章節**
13. [2026/04 LEO 現況與軌道永續性](#13-202604-leo-現況與軌道永續性)
14. [失敗案例庫 + Gruhl Study](#14-失敗案例庫--gruhl-study)
15. [Link Budget 極端情境對比與 Tranzeo 範例](#15-link-budget-極端情境對比與-tranzeo-範例)
16. [AESA 相控陣天線深度](#16-aesa-相控陣天線深度)
17. [Prometheus SoC 與 80/20 SDR 分流](#17-prometheus-soc-與-8020-sdr-分流)

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
- **都卜勒頻移：28 GHz (Ka) 可達 ±700 kHz**（0418 更新，舊版數值為 ±480 kHz，已失效）
- 需即時 CQI 反饋與 AMC (自適應調變與編碼) 機制
- 50 mm/h 亞熱帶雨 + 25° 低仰角 → 雨衰可達 **-22.0 dB**（0418 新增具體數值）

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
- LEO 速度 7.5 km/s
- **Ka 頻段 (28 GHz) 都卜勒偏移可達 ±700 kHz**（0418 更新值，此為最新與最嚴苛的規格基準）
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

---

## 13. 2026/04 LEO 現況與軌道永續性

> 來源：0418 版 p.2（封面後首頁）

### LEO 群星統計（2026 年 4 月）

| 類別 | 數量 | 備註 |
|------|------|------|
| 總追蹤物體 | ~33,074 | 含活躍 + 失聯衛星 + 火箭殘骸 + 大型碎片 |
| 活躍衛星 | ~15,295 | 較 2023 年成長約兩倍 |
| Starlink | **10,166** | 佔全球活躍 LEO 約 66% |
| OneWeb | ~650 | |
| Amazon Kuiper | ~180 | |

### LEO 容納能力三維動態平衡

1. **物理碰撞風險（Kessler 閾值）**
   - 當軌道上大型物體（>10 cm）數量超過 **50,000** 時，凱斯勒連鎖碰撞風險達臨界點
   - 來源：2026《Frontiers in Space Technologies》

2. **電磁波頻譜限制（ITU）**
   - 真正的限制往往不是空間，而是訊號干擾
   - LEO 頻譜分配已趨近飽和

3. **軌道槽位分配（Orbital Shells）**
   - 各國向 ITU 遞交申請總數 **>100,000 顆**
   - 「計畫容納量」與「安全承載量」之間存在顯著落差

### 物理環境宏觀參數

| 參數 | 數值 | 說明 |
|------|------|------|
| 衛星相對速度 | 7.5 km/s | 相對地表 |
| 大氣路徑（天頂 90°） | 680 km | 短路徑 |
| 大氣路徑（25° 低仰角） | 1,350 km | 增加表減區 |
| 28 GHz Doppler | **±700 kHz** | 威脅 OFDM 正交性 |
| Ka 50 mm/h 低仰角雨衰 | **-22.0 dB** | 亞熱帶 0.1% 降雨時間 |
| 單波束吞吐目標 | 20 使用者 × 200 Mbps | 18/28 GHz 1 GHz 頻寬 |

---

## 14. 失敗案例庫 + Gruhl Study

> 來源：0418 版 p.13-30（課程核心新增章節）

### NASA Gruhl Study：成本隨發現時機指數爆炸

| 成本倍數 | 發現階段 | 狀態 |
|---------|---------|------|
| **1x** | Phase A 設計 | Go-Flight Green（基線成本） |
| **5-10x** | Phase B/C 設計與製造 | Early Amber（影響相依設計） |
| **21-78x** | Phase D 整合與測試（I&T） | Alert Amber（跨子系介面翻修） |
| **29-1,500x** | Phase E 在軌運作 | **Critical Red（高代價且可能無法修正）** |

**NASA 鐵律**：前期 SE 投資每減少 1%，計畫總成本增加 10-20%。

**The Agile Fallacy**：「快速失敗」在純軟體可行，但太空硬體系統後期發現的架構錯誤 → 指數級財務與時間災難。

### 10 大歷史失敗案例

| 案例 | 年代 | 斷裂環節 | 根本原因 | 損失 |
|------|------|---------|---------|------|
| IRIDIUM | 1990s | 需求工程 | 12 年超長設計致 2.4 kbps 過時、市場脫節 | 上線 9 月破產 |
| GLOBALSTAR | 2000s | 架構設計 | SAA/TID 環境預估不足、SSPA 過早退化 | 頻率容量耗盡 |
| STARLINK | 2020s | 架構設計 | 脫軌性質 + 電力可靠性；2022 40 顆群墜 | 2025 全球 150 分鐘斷訊 |
| 千帆星座 (QIANFAN) | 2024 | 需求工程 | 初期缺乏 ISL、高度依賴地面、首輪彈射出現 Tumbling 翻轉 | 軌道失效 |
| Mars Climate Orbiter | 1999 | 介面管理 | 公制/英制單位混用、ICD 未強制數值驗證 | $1.25 億 |
| Ariane 5 Flight 501 | 1996 | V&V 不足 | Ariane 4 Heritage SW 直接沿用、64→16 bit 整數溢位、缺 HITL | $5 億 |
| Hubble Telescope | 1990 | V&V 單一源盲點 | 完全依賴單一 RNC 測量基準、忽視矛盾證據（確認偏誤） | $8,600 萬修復 |
| NASA DART | - | 高風險低預算妥協 | 排程壓力致晚期變更未測試、系統整合防護被繞過 | 任務全失 |
| Challenger | 1986 | 風險文化 | O 環 -28°F 喪失彈性；已知異常被視為「可接受」 | 7 命 |
| Columbia | 2003 | 風險文化 | 泡棉撞擊早有警訊，降級為「非飛安問題」（偏差常態化） | 7 命 |

**INCOSE/NASA AIAA 2024 結論**：分析 50 個歷史太空系統失效案例 → **60% 源自設計錯誤與系統性缺陷**，而非單一硬體製造不良。

### 5 大系統工程斷裂環節（防衛策略）

| # | SE 環節 | 典型案例 | 防衛策略 |
|---|---------|---------|----------|
| 1 | 需求工程 | Iridium | 可驗證需求（Functional Baseline）+ 市場驗證循環 |
| 2 | 架構設計 | Ariane 5 / GlobalStar | 完整 V&V + HITL 測試 + 運作包絡重評估 |
| 3 | V&V 驗證確認 | Hubble / MPL | 獨立驗證工具（獨立驗證你的驗證者）+ 多測量基準 + 邊界條件測試 |
| 4 | 介面管理 | MCO | 可執行 ICD（Executable Verification）+ 自動化單位轉換 |
| 5 | 風險與文化 | Challenger / Columbia | 獨立技術權威；決策權與排程壓力脫鉤；無情盤查微小異常 |

### NASA 生命週期 KDP（Key Decision Points）

| 階段 | 名稱 | 關鍵關卡 |
|------|------|---------|
| Pre-Phase A / A | Concept & Technology | MCR, SRR |
| Phase B | Preliminary Design | MDR/SDR |
| **Phase C** | **Final Design & Fabrication** | **PDR, CDR（⚠️ Ariane 5 End-to-End V&V gate）** |
| Phase D | Assembly Integration Test | SIR, ORR, ERR/MRR |
| **Phase E** | **Operations** | ⚠️ Challenger 低溫發射約束應在此關 |
| Phase F | Closeout | - |

**設計熱度門檻**：
- Functional Baseline (MDR/SDR)：架構可滿足頂層需求
- Allocated Baseline (PDR)：**設計熱度達 10-20% 且風險可控**
- Product Baseline (CDR)：**設計熱度必須 >90% 方可開始硬體製造**

### 規格一致性現代工具鏈（MBSE）

| 層次 | 工具 | 用途 |
|------|------|------|
| 架構級 | Cameo / System Composer / Gaphor | MBSE 跨組件跨文件一致性 |
| 文字規格級 | QVscribe / IBM RQA | AI/NLP 自動檢查模糊語義（符合 INCOSE 撰寫準則） |
| 通訊協議級 | TLA+ | 狀態機與訊息協議的形式化數學證明 |

---

## 15. Link Budget 極端情境對比與 Tranzeo 範例

> 來源：0418 版 p.8-12, p.31-36

### LEO Link Budget 極端情境（核心對比表，必背）

| 參數 | 最佳（18 GHz DL, 90°, 晴空） | 極限（28 GHz UL, 25°, 暴雨） |
|------|------------------------------|-------------------------------|
| EIRP | +50.5 dBW | +50.0 dBW |
| FSPL | -174.2 dB | -184.0 dB |
| 大氣/雨衰 | -0.3 dB | **-22.0 dB** |
| G/T | +15.8 dB/K | +11.5 dB/K |
| **Final C/N** | **29.9 dB** | **-26.9 dB** |
| 支援模式 | DVB-S2X 256APSK, 5.2 Gbps | 必須 Spread Spectrum 或縮至 10 MHz 窄頻 |

**關鍵結論**：系統必須在 **>50 dB 動態範圍**內維持穩定基頻處理；RF 端物理餘裕不足 → 由基頻 DSP 精度、面積、功耗償還。

### FSPL 公式（多單位版本）

- 公制 (d=m, f=Hz)：`FSPL[dB] = 20·log₁₀(d) + 20·log₁₀(f) - 147.55`
- 常用 (d=km, f=MHz)：`FSPL[dB] = 20·log₁₀(d) + 20·log₁₀(f) + 32.45`
- 英制 (d=mile, f=MHz)：`FSPL[dB] = 20·log₁₀(d) + 20·log₁₀(f) + 36.58`

### FSPL 速查表

| 距離 | 900 MHz | 2.4 GHz | 5.8 GHz |
|------|---------|---------|---------|
| 1 km | 91.53 | 100.05 | 107.72 |
| 5 km | 105.51 | 114.03 | 121.70 |
| 10 km | 111.53 | 120.05 | 127.72 |
| 50 km | 125.51 | 134.03 | 141.70 |

### Tranzeo P2P 設計範例（5 km @ 5.8 GHz, 2×TR-Splus-24）

| 參數 | 數值 |
|------|------|
| Tx Power | +23 dBm |
| Tx Antenna Gain | +24 dBi |
| **Tx EIRP** | **+47 dBm** |
| FSPL | 121.70 dB |
| Polarization Loss | 3 dB |
| Rx Antenna Gain | +24 dBi |
| Received Isotropic Power | -160.55 dBm |
| Channel Noise | -75.70 dBm |
| **CNR** | **~25 dB** |
| Required SNR (54 Mbps) | -75 dB |
| **Link Margin** | **21.30 dB** |

### Modulation vs. SNR 速查

| 調變 | 資料速率 | 最小 SNR |
|------|---------|----------|
| BPSK 1/2 | 6 Mbps | 8 dB |
| QPSK 1/2 | 12 Mbps | 11 dB |
| QPSK 3/4 | 18 Mbps | 13 dB |
| 16-QAM 1/2 | 24 Mbps | 16 dB |
| 16-QAM 3/4 | 36 Mbps | 20 dB |
| 64-QAM 2/3 | 48 Mbps | 24 dB |
| 64-QAM 3/4 | 54 Mbps | 25 dB |

### SQNR 與 ENOB 定量推導

- **公式**：SNR = 6.02·N + 1.76 dB（N = ENOB）
- 目標 SNR 40 dB → ENOB ≥ 8.5 bits
- Dynamic Headroom：64APSK PAPR 7-9 dB + AGC 餘裕 + Pilot/非線性 -12 dB
- **結論**：LEO 基頻必須選 **12-bit (Q1.10) 1.25 Gsps ADC/DAC**

### 效能參數總整

| 指標 | 目標值 | 意義 |
|------|--------|------|
| EVM | **< 3% (-30.5 dB)** | 64/256APSK 對抗相位噪聲 |
| PER/CRC | **< 10⁻⁵** | QoS 保證 |
| LDPC Coding Gain | **8-10 dB** | SNR 0.9 dB 邊緣救命線 |

---

## 16. AESA 相控陣天線深度

> 來源：0418 版 p.44-60（17 頁完整新章節）

### 為何 LEO 需要 AESA
- LEO 速度 7.8 km/s，仰角窗口僅 5-10 分鐘
- 傳統機械天線（Gimbal）無法追蹤
- AESA 透過相位偏移 Δφ 達成**毫秒（ms）級無機械波束轉向**

### Beamforming 架構對比

| 特性 | Analog BF | **Hybrid BF** | Digital BF |
|------|-----------|---------------|------------|
| ADC/DAC | 共享單一 | 子陣列級結合 | 每單元獨立 |
| 耗電 | 極低 | 中等 | 極高（1024 單元需 8 Tbps 數據處理） |
| 多波束 | 單 | 有限多波束 | 無限獨立 |
| 成本 | 低 | 最佳平衡 | 極高 |
| 應用 | 固定回傳 | **LEO 商用終端主流** | 高階星上鏈級 |

### 掃描損耗曲線

- 法線 (Boresight 0°)：**35.8 dBi**
- 60° 最大掃描：**31.5 dBi**（降 4.3 dB）
- 規律：有效孔徑 ∝ cos θ

### Starlink 終端演進

| 代次 | 架構 | 特徵 |
|------|------|------|
| Gen 1 (V1) | 純數位 | 79 DBF + 8 FEM，極高成本 |
| Gen 2/3 (V2/V3) | 轉向混合 | 縮小化 Hybrid BF |
| Gen 4 (V4) | 高度整合 | 6 顆 DBF 晶片驅動 **1536 個天線單元**，量產降本 |

### BFIC 四大廠商對標

| 廠商 | 代表產品 | 核心優勢 | 最佳場景 |
|------|---------|---------|----------|
| **Anokiwave (Qorvo)** | AWMF-0221 Gen-4 | CMOS 高集成 | 大規模平價終端 |
| **Renesas** | F6122 / F6522 | SiGe 雙波束、**<100 ns 切換** | 高機動/雙星追蹤 |
| **Analog Devices** | ADAR3000 | **TTD 整合、4 波束、CSH/CSL 太空認證** | 寬頻多波束中星 |
| **SatixFy / Launchip** | Prime 2.0 / TBF0828A | 全數位 DBF ASIC / 低成本抗輻射 CMOS | 新一代數位酬載 / 本土供應鏈 |

### AESA 三大挑戰

1. **Beam Squint（寬帶掃描偏斜）**
   - 原因：Phase Shifter 頻率相關折射
   - 症狀：>100 MHz 寬帶下 0.5°-2.0° 偏斜
   - 解方：**True Time Delay (TTD) 補償**（<8.1° 對準精度）

2. **熱管理挑戰**
   - PA 效率僅 15-25%，75-85% 變廢熱
   - 大型終端如 Skylark 達 **645W**
   - Ka-band 單元間距 λ/2 ≈ **5 mm**，熱極度集中
   - **BFIC T_junction > 150°C [CRITICAL]**
   - 解方：微流體冷卻通道 + 銅心 PCB + 異質 3D 整合（GaN Tx / SiGe Rx / CMOS DBF Chiplet）

3. **Make-Before-Break（LEO 交接）**
   - 切換需求 **<1 μs**
   - Renesas 雙波束 <100 ns 完美對應

### 測試方法對比

| 方法 | 距離 | AESA 診斷 | 用途 |
|------|------|-----------|------|
| Near-Field (NF) | <10λ | 極高（單單元失效定位） | 研發診斷、孔徑分析 |
| Far-Field (FF) | 公里級 | 低（僅整體波束） | 最終驗證 |
| **CATR** | 室內暗室 | **最佳（兼顧校準與高精測）** | **衛星終端整機驗證** |

---

## 17. Prometheus SoC 與 80/20 SDR 分流

> 來源：0418 版 p.91-109

### Prometheus SoC 架構（AMD/Xilinx 衛星專用）

- Cortex-A53 多核 CPU + 硬體加速器（HWA） + DSP 向量陣列
- **Mesh NoC + ACE 快取一致性**（30 Gbps 內部吞吐）
- 100 GbE / SerDes 支援 OISL 光學星間鏈路
- 整合 1.25 Gsps ADC/DAC 數位前端

### 80/20 異構負載分流法則

**80% 硬體加速路徑（HWA）**：
- 2048-pt FFT / IFFT
- LDPC 解碼（4 Gbps 並行）
- 脈衝成形、匹配濾波器、相位旋轉
- 能效目標：**<10 pJ/bit**

**20% 軟體彈性路徑（DSP + CPU）**：
- 信道估計與等化
- AMC 自適應調變編碼選擇
- 多協議轉接（DVB-S2X ⇄ 3GPP NR NTN）
- 衛星間路由決策

### 匯流排協調三機制

1. **DMA (Direct Memory Access)**：DFE 樣本直接推入共享 SRAM，繞過 CPU
2. **ACE Snooping**：硬體快取一致性，避免軟體鎖定開銷
3. **CPU Bypass**：Zero-copy，運算延遲 ms → μs 級

### NoC vs AXI Crossbar（為何傳統匯流排不行）

- 傳統 AXI Crossbar 在 >數百 IP 核時佈線指數爆炸
- NoC Mesh + GALS（Globally Asynchronous Locally Synchronous）允許局部休眠省電
- Flits 微封包交換 + 虛擬通道多工

### 衛星 SDR 平台三強

| 平台 | 特色 | 應用 |
|------|------|------|
| **Xilinx Zynq UltraScale+ RFSoC** | 8 通道 14-bit ADC/DAC @5 Gsps | 前端數位化 + 可程式邏輯 |
| **ADI ADRV9009-ZU11EG / AD9361** | DC-6 GHz Transceiver + JESD204C | RF 前端整合、多通道相控陣驅動 |
| **AMD Prometheus** | NoC + HWA + ACE + 100 GbE | 衛星 Payload 數據機、多協議 |

### US Patent 12,244,396 B1（SpaceX, 2025-03）

**標題**：Configurable OFDM Multi-Layer Receiver for Satellite to Gateway Uplink and Downlink

**IP 防護範圍**：
- Claim 1：PILOT 子帶 + DATA 子塊線性插值、邊帶導頻路徑
- Claim 17：部署感知參數切換（SAT/UT/SAG 角色 + DC Null + LO 涵蓋）

**迴避策略**：
1. 導頻框架替換：改用 Zadoff-Chu (ZC) 序列（LTE/5G 標準）
2. 同步機制：本地計算（Local Calculation）取代專用 ASIC 解碼
3. 環境濾波器：採用開源 OFDM 模組

### NewSpace 可靠度公式

**Careful COTS + Lot-by-lot NDT & Proton + TMR + LCL = NewSpace Reliability**

- **Careful COTS**：精挑細選商用晶片（非太空級）
- **Lot-by-lot NDT**：批次非破壞性測試 + 質子輻射
- **TMR**：三模冗餘 + Majority Voter
- **LCL (Latch-up Current Limiter)**：<1 ms 內切斷過流，防 SEL 熱損傷
- **設計哲學**：「系統級容錯」取代「件級絕對保證」，成本效益才是巨型星座制勝之道

### 衛星作為雲原生軌道節點

Prometheus 不只是 Modem，而是**太空邊緣運算節點**：
- 在軌流量快取、路由
- AWS Ground Station 整合
- 99.9999% 可用度（TMR + 異構加速）
- 未來通訊競爭 = 矽片微觀架構競爭
