# 低軌衛星通訊產業格局 知識庫

> 蒸餾自 TASA 課程教材（詹鎮宇研究員）- 2026/04/08 講次

## 目錄
1. [無線通訊演進 (1G-5G-LEO)](#1-無線通訊演進)
2. [GEO 到 LEO 的典範轉移](#2-geo-到-leo-的典範轉移)
3. [四大星座競爭力分析](#3-四大星座競爭力分析)
4. [頻段佈局策略](#4-頻段佈局策略)
5. [AESA 終端演進](#5-aesa-終端演進)
6. [RF vs. 光學星間鏈路 (ISLL)](#6-rf-vs-光學星間鏈路)
7. [商業模式比較](#7-商業模式比較)
8. [TASA B5G 計畫](#8-tasa-b5g-計畫)
9. [Starlink vs. Kuiper 終端對決](#9-starlink-vs-kuiper-終端對決)
10. [競合關係矩陣](#10-競合關係矩陣)
11. [次世代部署時程](#11-次世代部署時程)

---

## 1. 無線通訊演進

| 世代 | 年代 | 技術 | 速率 | 頻率 | 天線 |
|------|------|------|------|------|------|
| 1G | 1980s | AMPS | 2.4 kbps | 800-900 MHz | 全向天線 |
| 2G | 1990s | GSM/CDMA | 14.4k-64 kbps | 900/1800/1900 MHz | 扇形天線 |
| 3G | 2000s | UMTS/CDMA2000 | 384k-10 Mbps | 700-2600 MHz | 自適應天線 |
| 4G | 2010s | LTE | 100M-1 Gbps | 700-2600 MHz | MIMO |
| 5G NR | 2020s | OFDM | 10 Gbps | Sub-6G + mmWave (24-39 GHz) | Massive MIMO + Beamforming |

**關鍵轉折：** 5G 開始，地面網路與衛星網路走向融合 (NTN = Non-Terrestrial Network)。

---

## 2. GEO 到 LEO 的典範轉移

| 維度 | GEO (The Past) | LEO (The Future) |
|------|---------------|-----------------|
| 高度 | 36,000 km | ~500 km |
| 延遲 | 500 ms | 25-60 ms |
| 架構 | 透明轉發 (Bent-pipe) | 星上處理 (Regenerative SDR) |
| 波形 | 單載波 DVB-S2 | OFDM / 5G NTN |
| 衛星角色 | 廣播器 | 空中基地台 (gNB in the sky) |
| 速度 | 0 km/s (靜止) | 7.5 km/s |

### 系統三段架構
- **饋電終端 (Feeder Terminal, FT)：** 骨幹節點，大型碟型天線，連線至光纖骨幹或 AWS 雲端
- **空間段 (LEO Satellites)：** 星間雷射路由 (Regenerative/Bent-pipe)，高通量板載處理 (Up to 1 Tbps)
- **用戶終端 (User Terminal, UT)：** 邊緣節點，SWaP-C 成本導向，需具備 MBB 條件式換手能力

---

## 3. 四大星座競爭力分析

| 特性 | SpaceX Starlink | Amazon Kuiper | OneWeb | AST SpaceMobile |
|------|----------------|---------------|--------|-----------------|
| 衛星數量 (已部署/計劃) | >7,900 / ~12,000+ | 54 / 3,236 | >600 / ~700+ | 5 商用衛星 |
| 軌道高度 | ~340-570 km (多層) | 590-630 km | 1,200 km | ~700 km |
| ISLL 能力/速率 | 已大規模部署 / 100 Gbps | 核心架構 / 100 Gbps | 早期部署，能力有限 | 無 ISL |
| 宣稱下行速率 | ~200 Mbps (中位數) | 最高 400 Mbps (目標) | ~100 Mbps | 標準手機直連 |
| 核心差異化 | 垂直整合、快速迭代、發射成本優勢 | 與 AWS 深度整合、自研核心晶片 | 專注 B2B 市場、與 GEO 營運商合作 (Eutelsat) | 使用 MNO 已授權頻譜直連手機 |
| 載荷類型 | 再生式 SDR | 再生式 SDR | 彎管轉發 (Gen1) → 再生 (Gen2) | 超大相控陣天線 |
| 底層波形 | OFDM 架構 | 單載波/高頻寬密度 | DVB-S2x 單載波 | 3GPP LTE/NR |

---

## 4. 頻段佈局策略

### Spectrum Stratigraphy（頻段地層學）

| 頻段 | 頻率範圍 | 使用者 | 特性 |
|------|---------|--------|------|
| Sub-2 GHz | 700-2400 MHz | AST SpaceMobile | 完全依賴 MNO 行動頻譜，穿透力最強，直連標準手機 |
| Ku-band | 10.7-14.5 GHz | Starlink & OneWeb 用戶鏈路 | 雨衰適中，硬體工藝成熟 |
| Ka-band | 17.7-30.0 GHz | Kuiper 用戶/閘道鏈路, Starlink/OneWeb 閘道 | 可用頻寬極大，但雨衰嚴重 |
| E-band & Optical | 71-86 GHz & ~193 THz | Starlink V2 Mini 回程 & ISL, Kuiper ISL | 極高速骨幹網路通道 |

### 物理權衡結論
> AST 犧牲頻寬換取直連能力；Starlink 選擇 Ku 頻段以確保連線韌性；Kuiper 押注 Ka 頻段以追求極致容量密度。

---

## 5. AESA 終端演進

### 傳統企業級 vs. 新世代矽整合終端

| 特性 | 傳統企業級 (OneWeb/Hughes/Intellian) | 新世代矽整合 (Starlink Gen3/Kuiper Standard) |
|------|--------------------------------------|------------------------------------------|
| 天線類型 | 機械式輔助 / 大口徑 | 扁平式 AESA 電子相控陣 |
| 活動部件 | 有（馬達） | 無 |
| 換手方式 | 機械追蹤 | 瞬間電子換手 (Make-before-break) |
| 驅動架構 | 分離式 RF 元件 | 垂直整合 SoC/ASIC |
| 製造成本 | 高 | 極低 (< $400 目標) |
| 適用場景 | 海事與航空基建 | 消費級大規模部署 |

### 全球主流 LEO 用戶終端規格

| 終端 | DL / UL 速率 | 功耗 | 重量 |
|------|------------|------|------|
| Kuiper Leo Nano | 100 Mbps / 20 Mbps | 25-40 W (估) | 1.0 kg |
| Kuiper Leo Pro | 400 Mbps / 未公開 | ~90 W | 2.4 kg |
| Kuiper Leo Ultra | 1000 Mbps / 400 Mbps | >100 W | 19.5 kg |
| Starlink Mini | 100+ Mbps (DL) / 5-20 Mbps (UL) | 25-40 W | 1.1 kg |
| Starlink Standard (Gen3) | 25-220 Mbps (DL) / 5-20 Mbps (UL) | 75-100 W | 3.6 kg |
| OneWeb (Intellian OWT1FL) | 195 Mbps / 32 Mbps | 150-300 W | 20.5 kg |

---

## 6. RF vs. 光學星間鏈路

| 參數 | 射頻 (RF) 鏈路 | 光學 (雷射) 鏈路 (ISLL) |
|------|-------------|----------------------|
| 頻寬/數據速率 | 有限 (Mbps - 低 Gbps) | 極高 (數十至數百 Gbps，潛力達 Tbps) |
| 延遲 (長距離) | 較高 | 潛在更低（光在真空中比在光纖中快） |
| 安全性 (抗干擾/攔截) | 易受干擾和攔截 | 極高 (LPI/LPD) |
| 頻譜許可 | 需要，頻譜擁擠且昂貴 | 無需許可 |
| 尺寸/重量/功耗 (SWaP) | 較大、較重、功耗高 | 較小、較輕、功耗低 |
| 大氣影響 (星地鏈路) | 影響較小（可穿透雲層） | 影響極大（受天氣嚴重干擾） |

---

## 7. 商業模式比較

| 營運商 | 模式 | 目標客群 | 策略 |
|--------|------|--------|------|
| **Starlink** | 訂閱制 + 硬體銷售 | B2C 住宅 ($80-120/月), B2B 商業與軍工 | 透過 T-Mobile 合作推進 Direct-to-Cell |
| **AST SpaceMobile** | 純 B2B2C 收入分成 | 零硬體銷售，與 50+ MNOs (AT&T, Verizon) 簽約 | 觸達 30 億潛在標準手機用戶 |
| **Amazon Kuiper** | 訂閱制 + AWS 整合 | B2B 企業、政府與高階消費者 | 核心護城河：D2A (Direct-to-AWS)，企業流量繞過公網直達雲端 |
| **OneWeb** | 批發容量 / 合約制 | 純 B2B / B2G | 提供極高可靠度的 SLA 託管服務 |

### 四大範式矩陣
- **X 軸：** 依賴既有地面網路 ←→ 建立獨立封閉生態系
- **Y 軸：** B2B/基礎設施延伸 ←→ D2C 消費者/直連

| 象限 | 營運商 | 定位 |
|------|--------|------|
| 左下 (B2B + 既有網路) | OneWeb | 傳統彎管的極致，專注企業/政府 |
| 右下 (D2C + 既有網路) | AST SpaceMobile | 天空中的 5G 基地台，零地面設備 |
| 左上 (B2B + 獨立生態) | Amazon Kuiper | 軌道上的 AWS 邊緣節點 |
| 右上 (D2C + 獨立生態) | Starlink | 平行全球網路，垂直整合 |

---

## 8. TASA B5G 計畫

### 最新進展 (2025/03)
- TASA 擬投入新台幣 25 億元，攜手業界研製 4 顆低軌通訊衛星
- 最快 2029 年升空，逐步形成台灣「星網」
- CesiumAstro 與 TASA 簽約，提供 SDR 太空通訊酬載和地面用戶終端系統
- 採用 CesiumAstro **Vireo Ka** 太空酬載和 **Skylark** 用戶終端

### ITRI B5G 架構
- **頻段：** Ka-band (UL: 27.5-30 GHz, DL: 17.7-20.2 GHz)
- **頻寬：** 250 MHz，分 4 個 Component Carrier (CC)，每個 54 MHz
- **速率：** UL/DL 各 total average 600 Mbps, peak 800 Mbps
- **Feeder Link (1T1R)：** 新竹 Ka-FT 信關站 + SNOS
- **Access Link (1T1R)：** 台北 Ka-UT x4

---

## 9. Starlink vs. Kuiper 終端對決

| 比較維度 | SpaceX (UT3-V1) | Amazon (Kuiper Standard) |
|---------|-----------------|--------------------------|
| 目標頻譜 | Ku-band（抗雨衰強） | Ka-band（超高頻寬） |
| 孔徑尺寸 | 0.51 m | < 28 cm |
| 增益策略 | 依賴大物理面積增加訊號截獲 | 依賴超密集陣列與高發射功率 (EIRP) |
| 仰角遮蔽極限 | 25 度（擴大可用衛星數量） | 35 度（避開深層大氣與熱雜訊） |
| 系統大腦 | 離散式波束成形控制 | Prometheus 高度整合 SoC |
| 核心戰略優勢 | 惡劣天候下的連線強健性 | 極致的體積成本優勢與頻寬密度 |

### 工程物理權衡
> Starlink 選擇「低頻 + 大孔徑 = 高韌性」；Amazon 選擇「高頻 + 極小化 = 高容量密度」，並用超高 EIRP 暴力克服 Ka 頻段的天候劣勢。

---

## 10. 競合關係矩陣

### Musk 聯盟 vs. 反 Musk 聯盟
- **Musk 聯盟：** Starlink + T-Mobile (Direct-to-Cell, DTC)
- **反 Musk 聯盟：** AST SpaceMobile + AT&T + Verizon
- **弔詭：** SpaceX (Falcon 9) 同時為對手 AST (BB1-5) 甚至競爭者發射衛星

### 護城河比較
| 營運商 | 護城河 |
|--------|--------|
| Starlink | 以近萬顆衛星與成熟 ISL 形成規模壓制 |
| Kuiper | 憑藉 AWS 生態系防守企業 IT 整合市場 |
| OneWeb | 穩拿非美國/歐洲主權避險與純企業 B2B 市場 |
| AST | 零地面設備，直接使用 MNO 已授權頻譜提供手機直連 |

---

## 11. 次世代部署時程

| 營運商 | 時程 | 計畫 |
|--------|------|------|
| Starlink V3 | 2024-2029 | 規劃 1 Tbps 下行 / 200 Gbps 上行，依賴 Starship 發射 (每次 ~60 顆)，擴充 V-band 與 E-band |
| AST SpaceMobile Block 3 | 2025 商用 | 導入 AST5000 ASIC，擴展 1.4-2.4 GHz 中頻，目標 2026 全球覆蓋 |
| Amazon Kuiper | 2026/2029 FCC 死線 | 部署過半與全數入軌，已預購 92 次重型發射 (ULA, Ariane 6, New Glenn) |
| OneWeb Gen2 | 2027 完成 | 規劃 340 顆，由透明轉發轉向再生有效載荷，全面支援 3GPP 5G NTN 與 Beam-hopping |

### 三大巨頭架構總結

| 營運商 | 核心頻段 | 載荷架構 | 底層波形 | 戰略目標 |
|--------|--------|--------|--------|--------|
| Starlink | Ku-band | 星上處理 (Regenerative SDR) | OFDM 架構 | 消費級規模擴展 / 低終端成本 |
| Amazon Kuiper | Ka-band | 星上處理 (Regenerative SDR) | 單載波 / 高頻寬密度 | AWS 雲端生態系深度整合 |
| OneWeb | Ku / Ka-band | 彎管轉發 (Transparent Bent-pipe) | DVB-S2x 單載波 | 企業與政府級穩定傳輸 (CIR) |
