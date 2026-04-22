# Distillation A: 第 1-30 頁

> 來源：`20260422 低軌衛星通訊設計概論_0418.pdf` (TASA 詹鎮宇研究員)
> 主題：LEO 現況、物理環境、失敗案例、Gruhl Study、系統工程斷裂環節

---

## 逐頁摘要

### p.1 封面
- 標題：低軌衛星通訊設計概論
- 日期：2026/04/22
- 副標：LEO Satellite Communications: The Space-to-Silicon Blueprint

### p.2 LEO 衛星現況（2026 年 4 月數據）
- 總追蹤物體：~33,074 個（活躍 + 失聯 + 火箭殘骸 + 大型碎片）
- 活躍衛星：~15,295 顆（較 2023 年成長約兩倍）
- Starlink 活躍衛星：10,166 顆（佔全球活躍 LEO 約 66%）
- OneWeb：~650 顆；Amazon Kuiper：~180 顆
- **容納能力三維限制**：
  1. **物理碰撞風險**：軌道大型物體 (>10 cm) >50,000 時觸發凱斯勒現象臨界
  2. **電磁波頻譜限制**（ITU）：LEO 頻譜分配已趨近飽和
  3. **軌道槽位**：各國向 ITU 遞交申請已超過 100,000 顆

### p.3 物理環境限制與宏觀系統參數
- LEO 速度：7.5 km/s
- **多普勒頻移**：28 GHz 頻段 **±700 kHz**（舊版 ±480 kHz，此為重大數值更新）
- 大氣路徑對比：天頂 680 km vs. 低仰角 25° 1,350 km
- **極端雨衰**：K/Ka 頻段 50 mm/h 低仰角可達 **-22.0 dB**
- 吞吐量目標：18/28 GHz 頻段 1 GHz 頻寬、單波束支援 20 使用者、每人 200 Mbps

### p.4 Outline
1. Fail Cases Study & Amendments
2. From Link Budget Analysis to Design Specification
3. Phased Array Antenna (AESA) Fundamentals
4. Introduction on PCB Implementation
5. COTS Parts Selection
6. Baseband Modem Architecture & Implementation (SDR)

### p.5 通訊理論關鍵公式與實例
- **Shannon Capacity**：`C = B · log₂(1 + S/N)`
- **頻譜效率**：`η = C/B = log₂(1 + SNR)` (bps/Hz)
- 範例：WiFi 7 (802.11be)，6 GHz 頻段 / 320 MHz / SNR >35 dB / 4096-QAM → η >12 bps/Hz, >10 Gbps

### p.6-7 Link Budget 對設計的影響（雙頁）
- 天線：Omni vs Directional 取捨
- Tx Power vs 電力預算；Rx 靈敏度 vs NF
- 覆蓋面積與 handover
- 頻率選擇：高頻 FSPL 大但 BW 多
- 可靠性 vs 效能：老化、不確定性、coding (LDPC/BCH/Convolutional)
- 環境：大氣損耗、多路徑、介質損耗
- 法規：EMC、健康共存

### p.8 LEO Link Budget — 極端情境對比（核心表）

| 情境 | 最佳 (18 GHz DL, 90°, 晴空) | 極限 (28 GHz UL, 25°, 暴雨) |
|------|--------------------------|---------------------------|
| EIRP | +50.5 dBW | +50.0 dBW |
| FSPL | -174.2 dB | -184.0 dB |
| 大氣/雨衰 | -0.3 dB | **-22.0 dB** |
| G/T | +15.8 dB/K | +11.5 dB/K |
| **Final C/N** | **29.9 dB** | **-26.9 dB** |
| 支援模式 | DVB-S2X 256APSK, 5.2 Gbps | 必須 Spread Spectrum 或縮至 10 MHz 窄頻 |

**關鍵結論**：系統必須在 **>50 dB 動態範圍** 內維持穩定基頻處理。

### p.9 SQNR 與 ENOB 定量推導
- **SNR = 6.02N + 1.76 dB**（N = ENOB）
- 目標 SNR 40 dB → ENOB ≥ 8.5 bits
- **Dynamic Headroom 需求**：
  1. 64APSK PAPR → 7-9 dB 峰值動態
  2. AGC 動態餘裕
  3. Pilot 與非線性 Headroom (-12 dB)
- **結論**：必須選 **12-bit (Q1.10) 1.25 Gsps ADC/DAC**

### p.10 Compute Load — 基頻 DSP 負載
- 資料流：ADC → Filter → FFT/IFFT → Demod → Channel Coding → Sink
- 1 GHz BW / 2048-pt FFT → 單通道 6.7×10⁸ CMAC/sec
- 16 通道 DBF → **Tbps 級算力**
- FFT 固定點 14-16 bits（14 total, 3 integer）維持 BER

### p.11 效能參數總整理
| 指標 | 目標值 | 意義 |
|------|--------|------|
| EVM | < 3% (-30.5 dB) | 64/256APSK 對抗相位噪聲 + 非線性 |
| PER/CRC | < 10⁻⁵ | QoS 保證 |
| Coding Gain (LDPC) | 8-10 dB | SNR 0.9 dB 邊緣場景救命線 |

### p.12 Link Budget 三大構件
- 公式：`P_r = P_t + G_t + G_r - L_fs - L_other`
- 三層堆疊：
  1. **天線陣列**：EIRP 50.5 dBW / 波束成形 39 dBi
  2. **混合訊號**：AD/DA SQNR (12-bit / 1.25 Gsps)
  3. **基頻算力**：Doppler/LLR/FFT，Tbps 級 DSP
- **核心理念**：RF 端物理餘裕不足 → 由基頻 DSP 精度、面積、功耗償還

### p.13 LEO 設計失敗全解析
- 三框架：失敗案例比較 / 成本模型 / 工程師工具箱
- 案例概覽：IRIDIUM / GLOBALSTAR / STARLINK / 千帆星座
- TRL (1-9)、RIDM vs CRM 整合框架
- TRL 6 是技術進入系統整合的最低門檻（相關環境原型驗證）

### p.14 成本曲線與 Gruhl Study（核心 insight）
**NASA Gruhl Study**：前期 SE 投資每減少 1%，計畫總成本增加 10-20%

| 成本倍數 | 發現階段 | 狀態 |
|---------|---------|------|
| 1x | 設計階段 | Go-Flight Green |
| 5-10x | 設計/製造 | Early Amber |
| 21-78x | 整合測試 (I&T) | Alert Amber |
| **29-1,500x** | **在軌運作 (Phase E)** | **Critical Red** |

**The Agile Fallacy**：敏捷「快速失敗」在純軟體可行，但太空硬體系統後期發現的架構錯誤 = 指數級災難。

### p.15 系統工程斷裂點（5 大類，分析 50 案例 → 60% 源自設計錯誤）

| # | SE 環節 | 典型案例 | 根本缺陷 |
|---|---------|---------|---------|
| 1 | 需求工程 | Iridium | 系統架構與市場脫節 |
| 2 | 架構設計 | Ariane 5 | 繼承軟體未在新運作包絡下驗證 |
| 3 | V&V 驗證確認 | Hubble & MPL | 獨立驗證缺失與單一測量基準 |
| 4 | 介面管理 | MCO | ICD 執行失效與單位制混用 |
| 5 | 風險與文化 | Challenger & Columbia | 偏差常態化與技術警告壓制 |

### p.16 太空災難案例矩陣

| 案例 | 損失 | 斷裂環節 | 核心病灶 |
|------|------|---------|---------|
| Mars Climate Orbiter | $1.25 億 | 介面管理失效 | 公/英制單位未強制數值驗證 |
| Ariane 5 Flight 501 | $5 億 | 軟體 V&V 不足 | Heritage Code 未在新包絡驗證，缺 HITL |
| Hubble Telescope | $8,600 萬修復 | 單一驗證源盲點 | 依賴單一 RNC 基準，忽視矛盾證據（確認偏誤） |
| NASA DART | 任務全失 | 高風險低預算妥協 | 排程壓力致晚期變更未測試，整合防護被繞過 |

**Synthesis**：INCOSE/NASA AIAA 2024 結論 — **60% 太空載具失效源自設計與溝通的系統性缺陷**，非單一技術無能。

### p.17 Iridium (1990s) 深度剖析
- 12 年超長設計 → 1998 上線時 2.4 kbps 已過時
- 根因：需求與市場脫節；衛星設計節奏 ≠ 地面網路演進
- 結果：上線 9 個月破產，66 顆衛星才服務首位客戶
- 教訓：「舊的能用」≠「新環境能用」，必須重走完整設計 + 驗證包絡

### p.18 Ariane 5 (1996) Heritage 災難
- T+40s 爆炸
- 根因：Ariane 4 SRI 軟體直接繼承，未評估新火箭更高加速度對運作包絡的影響
- 技術原因：64-bit float 轉 16-bit signed integer 時溢位（horizontal velocity 值超出範圍）
- 雙重冗餘無效：兩台電腦執行同一 SW → 同時崩潰（共模失效）
- 教訓：Heritage SW 必須經歷完整系統層級 V&V，不能僅組件層測試

### p.19 Phase C/D 首區：介面管理與 V&V 單點失效
- **MCO**：ICD 紙本約定不可取代硬體層執行驗證（Executable Verification）
- **Hubble**：依賴單一 RNC 基準；兩個獨立眼鏡誤差測試被視為「設備錯誤」而否決
- 防衛：任何系統中的唯一驗證工具，必須**首先**被獨立驗證

### p.20 Phase E 首區：偏差常態化與組織沈默
- **Challenger**：O 環 -28°F 喪失彈性；低溫警告被壓制
- **Columbia**：泡棉撞擊已在先前任務觀察到，降級為「非飛安問題」
- **防衛法則**：當安全數據不完整時，**預設決策是「不飛」**。舉證責任在於證明安全，非證明危險。

### p.21 NASA SE 引擎：技術與管理雙螺旋
- Formulation：Stakeholder 期望 → Tech Req → 分解 → 設計方案
- Implementation：設計 → 實施 → 整合 → V&V → 移交
- 雙迴圈閉合：技術管理流程統御整個週期（防 MCO 斷層）

### p.22 生命週期與 KDP（Key Decision Points）
- Pre-Phase A / Phase A (Concept) → KDP-A (MCR, SRR)
- Phase B (Prelim Design) → KDP-B (SRR, MDR/SDR)
- **Phase C (Final Design) → KDP-C**（**警示：Ariane 5 End-to-End V&V gate 應在此關**）
- Phase D (System AI&T) → KDP-D (CDR, SIR, ORR, ERR/MRR)
- **Phase E (Ops)**（**警示：Challenger 低溫發射約束應在此關**）
- Phase F (Closeout) → KDP-F

### p.23 決策分析：規避設計慢性病
- 決策流程：定義標準 → 識別替代 → 評估方法 → 執行 → 選擇
- **Ariane 5 Heritage Fallacy**：重新評估運作包絡，量化不確定性
- **Hubble Confirmation Bias**：獨立測試矛盾 = 系統性問題強烈信號，**不可任意捨棄異常數據**

### p.24 故障管理 (FM) 由上而下設計
- 三層防衛：System → Subsystem → Component
- **同質冗餘 vs 功能多樣性**：
  - Ariane 5 陷阱：兩台相同電腦 + 相同 Bug = 零保護（共模失效）
  - 真正縱深防衛：使用**截然不同的機制**達成相同安全目標
- Mars Observer 教訓：「Test as you fly」所有 FM SW 必須在真實飛行載具上驗證

### p.25 實戰手冊：規避常見缺陷
- **需求與介面**：強制可驗證 ICD（規避 MCO）；支援軟體更新失敗的降級模式（Programmable Frailty）
- **V&V**：邊界條件測試（閾秒/低溫/部署衝擊，規避 MPL）；獨立驗證驗證工具（規避 Hubble）
- **組織與文化**：獨立技術權威，決策權與排程壓力脫鉤（規避 Columbia）；無情追蹤微小異常（規避 Challenger）

### p.26 解決方案矩陣：規格一致性現代工具鏈

| 層次 | 工具 | 用途 |
|------|------|------|
| 架構級 | MBSE (Cameo / System Composer) | 跨組件跨文件一致性 |
| 文字規格級 | AI/NLP (QVscribe / IBM RQA) | 自動檢查模糊語義（INCOSE 撰寫準則） |
| 通訊協議級 | Formal Verification (TLA+) | 狀態機與訊息協議數學證明 |

### p.27-30 Gaphor + Outline
- **Gaphor**：開源 SysML/UML 建模工具，支援 UML 2 全規範
- 重複課程大綱提醒

---

## 核心技術點萃取

### 失敗案例完整矩陣

| 案例 | 年代 | 斷裂環節 | 根因 | 損失 |
|------|------|---------|------|------|
| IRIDIUM | 1990s | 需求工程 | 12 年設計週期致 2.4 kbps 過時；市場脫節 | 破產；66 顆才首客戶 |
| GLOBALSTAR | 2000s | 架構設計 | SAA/TID 適應不足、頻率容量耗盡 | 軌道收斂失效 |
| STARLINK | 2020s | 架構設計 | 脫軌性質與電力可靠性 | 2025 全球 150 分鐘斷訊；2022 40 顆群墜 |
| 千帆星座 | 2024 | 需求工程 | 擾旋異倫複雜性 | 軌道失效 |
| MCO | 1999 | 介面管理 | 公/英制混用 | $1.25 億 |
| Ariane 5 | 1996 | 軟體 V&V | Heritage Code + 16-bit 溢位 | $5 億 |
| Hubble | 1990 | V&V 單源 | 單一 RNC + 確認偏誤 | $8,600 萬修復 |
| NASA DART | - | 高風險妥協 | 晚期變更未測試 | 任務全失 |
| Challenger | 1986 | 風險文化 | O 環低溫 + 技術警告壓制 | 7 命 |
| Columbia | 2003 | 風險文化 | 泡棉撞擊 + 偏差常態化 | 7 命 |

### Gruhl Study 成本曲線（記憶背誦）
- **1x** → **5-10x** → **21-78x** → **29-1,500x**
- 對應：Phase A → B/C → D (I&T) → E (Operations)

### 5 大 SE 斷裂環節
1. 需求工程 (Iridium)
2. 架構設計 (Ariane 5 / GlobalStar / Starlink)
3. V&V (Hubble / MPL)
4. 介面管理 (MCO)
5. 風險文化 (Challenger / Columbia)

---

## 與舊版 (2026/04/01) 的差異

| 項目 | 舊版 | 新版 0418 | 變動 |
|------|------|-----------|------|
| 28 GHz Doppler | ±480 kHz | **±700 kHz** | 🔴 **數值上修** |
| LEO 衛星數 | 未提 | 15,295 顆 / Starlink 10,166 | 🆕 2026/04 數據 |
| 雨衰（Ka 50 mm/h） | 未細化 | **-22.0 dB** | 🆕 具體數字 |
| 失敗案例章節 | 無 | 10 個完整案例 + Gruhl Study | 🆕 新章節 |
| 系統工程斷裂環節 | 無 | 5 大類結構化分析 | 🆕 新章節 |
| Link Budget 極端情境 | 概念 | 18 GHz DL +29.9 dB vs 28 GHz UL -26.9 dB | 🆕 完整數值對比 |
| ADC/DAC 推導 | 概念 | 12-bit 1.25 Gsps + ENOB 推導 | 🆕 定量化 |
| MBSE 工具鏈 | 無 | Cameo / QVscribe / TLA+ / Gaphor | 🆕 新章節 |

---

## 關鍵名詞表

| 術語 | 中文 | 定義 |
|------|------|------|
| Gruhl Study | NASA 成本曲線研究 | 前期 SE 1% 投資減少 → 總成本 +10-20% |
| Heritage SW | 遺產軟體 | 來自前代任務的軟體重用（Ariane 5 陷阱來源） |
| Normalization of Deviance | 偏差常態化 | Challenger/Columbia 文化病源 |
| Programmable Frailty | 程序化脆弱性 | 軟體故障時降級而非崩潰的能力 |
| Confirmation Bias | 確認偏誤 | Hubble 忽視矛盾數據的認知陷阱 |
| KDP | Key Decision Point | NASA 生命週期閘檔 |
| HITL | Hardware-in-the-Loop | 硬體在環測試 |
| TRL | Technology Readiness Level | 1-9 技術成熟度 |
| RIDM / CRM | Risk-Informed Decision / Continuous Risk | 風險管理雙框架 |
| ICD | Interface Control Document | 介面控制文件 |
| MBSE | Model-Based SE | SysML/UML 規範設計 |
| EIRP | Equivalent Isotropic Radiated Power | 等效全向輻射功率 |
| FSPL | Free Space Path Loss | 自由空間路徑損耗 |
| G/T | Gain-to-Temperature | 接收天線品質因子 |
| SQNR | Signal-to-Quantization Noise Ratio | 量化雜訊比 |
| ENOB | Effective Number of Bits | 有效位元數 |
| PAPR | Peak-to-Average Power Ratio | 峰均功率比（OFDM/APSK 痛點） |
| AGC | Automatic Gain Control | 自動增益控制 |
| DBF | Digital Beam Forming | 數位波束成形 |
| EVM | Error Vector Magnitude | 誤差向量幅度 |
| PER | Packet Error Rate | 封包錯誤率 |
| LDPC | Low-Density Parity-Check | 低密度奇偶檢查碼 |
| SAA | South Atlantic Anomaly | 南大西洋異常輻射區 |
| TID | Total Ionizing Dose | 總離子劑量 |
