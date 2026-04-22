# D-007 整合測試計畫 v1（Integration Test Plan）

**作者：** QA Agent 林宜靜
**日期：** 2026-04-17
**任務：** TASA-NTN-3U CubeSat，S-band NTN 透明轉發，50 kbps @ ≥60°
**狀態：** v1 — Wave 2 交付

---

## 1. 測試策略

### 1.1 測試哲學
- **HIL 優先（Hardware-in-the-Loop）**：所有測試使用真實元件，不以模擬器替代關鍵硬體
- **V-Model 對應**：UT（元件驗證）→ ST（子系統驗證）→ SIT（整合驗證）→ ET（環境資格）
- **量化合格準則**：所有測試項目必須有數值門檻，禁止「功能正常」等模糊描述

### 1.2 缺陷管理
| 等級 | 定義 | 處置 |
|------|------|------|
| P1 | 飛行阻擋：影響任務存活或關鍵功能 | 立即停測，升報 CEO，修正後重測全項 |
| P2 | 條件接受：性能降級但不影響任務存活 | PM + QA 聯合評估，記錄接受條件 |
| P3 | 次要：文件問題、輕微偏差 | 記錄後繼續，下次迭代修正 |

### 1.3 測試層次與時序
```
Sprint 4 W2         → UT（單元測試）
Sprint 4 W2         → ST（子系統測試）
Sprint 4 W2-W3      → SIT（系統整合）
Post-TRR（ET GO）   → ET（環境資格）
```

---

## 2. 單元測試（Unit Test，UT）

### UT-001：OBC 開機序列

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-009（FSW 初始化）|
| 測試對象 | Zynq-7020 PS + FSW |
| 方法 | 上電後監控 UART log |
| 合格準則 | ① Boot 完成時間 ≤ 30 s；② WDT 啟動確認；③ Heater State Restore（AC-010）執行，加熱片狀態 = ON（若 NTC < 5°C）|
| 測試設備 | 電源供應器、邏輯分析儀、UART 終端 |

### UT-002：ADF4351 PLL Lock

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-010（LO 190 MHz）|
| 測試對象 | ADF4351 PLL 子模塊 |
| 方法 | OBC SPI 初始化序列 → 頻率計量測輸出，Lock Detect 引腳邏輯分析 |
| 合格準則 | ① f_OUT = 190 MHz ± 100 Hz；② Lock Detect 高電位時間 ≤ 200 μs；③ SSB Phase Noise @ 10 kHz ≤ -85 dBc/Hz |
| 測試設備 | 頻率計（分辨率 1 Hz）、邏輯分析儀、示波器 |

### UT-003：QPQ1900 UL BPF S21 量測

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-003（帶外抑制 ≥ 40 dB）、SYS-002（UL 通帶覆蓋）|
| 測試對象 | Qorvo QPQ1900 BAW FBAR（UL BPF） |
| 方法 | VNA S21 掃描（1.8–2.4 GHz，SOLT 校準）|
| 合格準則 | ① IL @1980–2010 MHz：每個頻點 ≤ 3.0 dB；② IL @2170 MHz ≥ 40 dB；③ IL @2200 MHz ≥ 45 dB |
| 測試設備 | VNA（如 Keysight E5063A），SOLT 校準件 |

### UT-004：ADL5523 LNA 增益/雜訊

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-002（UL 系統 NF ≤ 2.5 dB）|
| 測試對象 | ADL5523 LNA |
| 方法 | Y-factor 法（ENR 已知雜訊源 + 頻譜分析儀）|
| 合格準則 | ① 增益 G ≥ 15 dB @ 1995 MHz；② NF ≤ 1.0 dB @ 1995 MHz；③ P1dB ≥ +20 dBm |
| 測試設備 | 雜訊源（ENR 標定）、頻譜分析儀、偏壓電路 |

### UT-005：PMA3-43-1W+ PA 功率特性

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-004（衛星 EIRP +31.3 dBm）|
| 測試對象 | Mini-Circuits PMA3-43-1W+ |
| 方法 | 功率掃描，測量 P1dB 及 3 dB backoff 輸出功率 |
| 合格準則 | ① P1dB ≥ +30 dBm @ 2185 MHz；② P_out @ -3 dBBO = +29.6 ± 0.5 dBm；③ Gain = 17 ± 1 dB |
| 測試設備 | 訊號產生器、功率計、定向耦合器 |

### UT-006：Reactel 4C5-2185 DL BPF S21 量測

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-003（DL 帶外抑制）、SYS-010（DL 頻段 2170-2200 MHz）|
| 測試對象 | Reactel 4C5-2185 陶瓷同軸 BPF（DL BPF） |
| 方法 | VNA S21 掃描 |
| 合格準則 | ① IL @2170–2200 MHz ≤ 1.5 dB（每點）；② IL @1980 MHz ≥ 40 dB；③ IL @2010 MHz ≥ 45 dB |
| 測試設備 | VNA，SOLT 校準件 |

### UT-007：TSS-53LNB+ Driver Amp

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-004（PA 驅動，DL EIRP）|
| 測試對象 | Mini-Circuits TSS-53LNB+ |
| 方法 | 訊號注入，量測增益與線性度 |
| 合格準則 | ① G = 27 ± 1.5 dB @ 2185 MHz；② P1dB ≥ +20 dBm；③ 輸出功率 +13.5 ± 0.5 dBm（PA 驅動點）|
| 測試設備 | 訊號產生器、功率計 |

### UT-008：EPS 充放電與 BMS 保護

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-006（DoD ≤ 30%）|
| 測試對象 | Samsung INR18650-35E 2S2P + BMS |
| 方法 | 恒流充電至 100%，恒流放電至 DoD = 35%（刻意超限測試） |
| 合格準則 | ① BMS 在 DoD = 30% 時發出警告；② BMS 在 DoD = 35% 時切斷放電（切斷時間 ≤ 100 ms）；③ 充電效率 ≥ 92% @ C/2 rate |
| 測試設備 | 電子負載、充放電測試儀、溫度計 |

### UT-009：NTC 熱敏電阻 + 加熱片控制

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-012（電池 T ≥ -20°C），AC-009（NTC Failsafe）|
| 測試對象 | NTC ×2 + 電池加熱片 0.75W |
| 方法 | 在環境腔中緩慢降溫，觀察加熱片 ON/OFF 邏輯；另進行斷線故障注入 |
| 合格準則 | ① 加熱片 ON 時機：T ≤ 5°C（允許 ±0.5°C）；② 加熱片 OFF 時機：T ≥ 15°C；③ Failsafe（NTC 斷路模擬）：系統切換至備用 NTC 或預設加熱 50% ON；④ 雙 NTC 溫差 < 2°C（確認貼附良好）|
| 測試設備 | 環境腔（桌上型）、電阻箱（模擬斷路）、電源量測模組 |

### UT-010：反應飛輪（RW）轉速控制

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-010（RW 額定角動量 ≤ 0.25 mNms）|
| 測試對象 | CubeWheel Nano ×3（3 軸）|
| 方法 | OBC 指令轉速，光電編碼器量測 |
| 合格準則 | ① 指令 500 rpm，穩態轉速 500 ± 25 rpm；② 制動至 0 rpm 時間 ≤ 30 s；③ 額定角動量 ≤ 0.25 mNms（@額定轉速）|
| 測試設備 | 電流計、轉速計（光電 or 霍爾元件）|

### UT-011：磁力計讀值精度

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-008（ADCS 指向 ≤ 5°），EKF 量測雜訊模型 |
| 測試對象 | 磁力計（三軸） |
| 方法 | Helmholtz 線圈模擬已知地磁場，比對量測值 |
| 合格準則 | ① 量測誤差 ≤ 100 nT（每軸）；② 線性度：R² ≥ 0.999（50–60,000 nT 範圍）|
| 測試設備 | Helmholtz 線圈組（三軸）、電流精密電源、參考磁力計 |

### UT-012：FPGA QPSK BER 測試

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-011（資料率 50 kbps，BER ≤ 1E-6）|
| 測試對象 | Zynq-7020 PL RTL（QPSK 調變/解調）|
| 方法 | FPGA loopback（Tx→加雜訊通道模型→Rx），掃描 Eb/N0 |
| 合格準則 | ① BER ≤ 1E-6 @ coded Eb/N0 = 5.5 dB（Rate 1/2 Viterbi）；② BER ≤ 1E-4 @ coded Eb/N0 = 4.0 dB（HARQ 門檻）|
| 測試設備 | FPGA 開發板（Zynq-7020）、AWGN 通道模型（軟體/硬體模擬）|

---

## 3. 子系統測試（Subsystem Test，ST）

### ST-001：RF 子系統端對端量測

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-002, SYS-003, SYS-004 |
| 方法 | 訊號產生器注入 1995 MHz UL → 完整 RF 鏈路 → 頻譜分析儀量測；溫度：-40°C / +25°C / +85°C |
| 合格準則 | ① 系統 NF ≤ 2.2 dB（worst case, QPQ1900 IL 3.0 dB）；② DL EIRP = +31.3 ± 1 dBm；③ UL/DL 頻道隔離 ≥ 40 dB；④ 全溫度範圍內 Δ(EIRP) ≤ 2 dB |
| 測試設備 | VNA、訊號產生器（Keysight E8267D 等）、頻譜分析儀、溫度腔 |

### ST-002：ADCS 子系統（Helmholtz 線圈）

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-008, SYS-009 |
| 方法 | Helmholtz 線圈模擬地磁場，模擬 5 軌，驗證 B-dot 去滾動 + Nadir Pointing |
| 合格準則 | ① Detumbling：從 ω = 5°/s 收斂至 ≤ 0.1°/s，時間 ≤ 60 min；② MTQ 最大電流 ≤ 50 mA/軸；③ RW 去飽和週期約 2.1 軌（允許 ±0.5 軌）|
| 測試設備 | Helmholtz 線圈（三軸，±60,000 nT）、電流計 |

### ST-003：EPS 子系統（太陽模擬器）

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-006, SYS-007 |
| 方法 | 太陽模擬器（AM0，1361 W/m² 等效）照射太陽能板，電池充放電 30 次循環 |
| 合格準則 | ① 充電效率 ≥ 85%（30 次平均）；② DoD 每軌 ≤ 8.3%（DL 接觸 8 min/軌）；③ 30 次循環後電池容量 ≥ 97%（容量損耗 ≤ 3%）|
| 測試設備 | 太陽模擬器、電子負載、電容量分析儀 |

### ST-004：OBC + FSW（HARQ 與 Scrubbing）

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-011（HARQ），輻射緩減（Scrubbing）|
| 方法 | FSW 功能測試：HARQ 停止等待、Scrubbing 週期切換、WDT 重置 |
| 合格準則 | ① HARQ：6 次重傳後 ACK，BER ≤ 1E-4；NACK timeout = 2 s ± 0.1 s；② Scrubbing：正常 10 ms，SAA Detector 觸發後切換至 1 ms（≤ 100 ms 切換時間）；③ WDT 超時 1 s → 重置 → 恢復時間 ≤ 2 s |
| 測試設備 | FPGA 開發板、邏輯分析儀、bit-flip 注入工具 |

### ST-005：熱控子系統

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-012（電池 T ≥ -20°C）|
| 方法 | 環境腔中模擬食月熱功率（Q_internal = 3.18 W），觀察加熱片控制行為 |
| 合格準則 | ① 電池節點溫度 ≥ -15°C（MLI + 0.75W 加熱片，留 5°C 裕量）；② 加熱片 ON/OFF 週期正確；③ 備用 NTC 切換功能正常（主 NTC 人工斷路後 ≤ 1 s 切換）|
| 測試設備 | 環境腔、熱電偶、電功率量測 |

### ST-006：SEU 緩減驗證（Ground 模擬）

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-013, SYS-016, SYS-017 |
| 方法 | 軟體 bit-flip 注入工具，模擬正常（198/s）和 SAA 峰值（951/s）兩種 SEU 率 |
| 合格準則 | ① 正常 SEU 率（198/s，10 ms scrubbing）：累積錯誤 ≤ 1 bit/scrub 週期（Poisson 期望值 1.98，TMR 有效）；② SAA 峰值（951/s，1 ms scrubbing）：累積錯誤 ≤ 0.95 bit/scrub；③ 1 小時注入測試無不可恢復錯誤（SEFI 需 WDT 恢復） |
| 測試設備 | FPGA bit-flip 注入工具、邏輯分析儀 |

---

## 4. 系統整合測試（System Integration Test，SIT）

### SIT-001：機電整合

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-020（質量 ≤ 4000 g）、SYS-021（CG < 20 mm）|
| 方法 | 全部子系統安裝至 3U 結構，電子秤量測，CG 測量台量測 |
| 合格準則 | ① 整機質量 ≤ 4000 g（目標 1374 g + 裕量）；② CG 偏移 < 20 mm（三軸各測）；③ 外形尺寸符合 CubeSat 標準（100×100×340.5 mm ± 0.1 mm）|
| 測試設備 | 精密電子秤（精度 0.1 g）、CG 測量台 |

### SIT-002：整機上電與初始化

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-009（FSW 初始化）|
| 方法 | 整機上電，監控所有子系統 Health Check 訊號 |
| 合格準則 | ① Boot 完成時間 ≤ 30 s；② 所有子系統回報 Nominal（ADCS、EPS、RF、熱控）；③ Heater State Restore 自動執行；④ HARQ + WDT + SAA Detector 自動初始化 |
| 測試設備 | 電源供應器、UART 終端、示波器 |

### SIT-003：RF Bent-Pipe 端對端回路

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-002, SYS-004, SYS-011 |
| 方法 | 地面站模擬器（訊號產生器 @ 1995 MHz）→ 衛星 UL → 衛星 DL（@ 2185 MHz）→ 頻譜分析儀接收 + HARQ 功能測試 |
| 合格準則 | ① 衛星 EIRP = +31.3 ± 1 dBm；② 50 kbps QPSK，BER ≤ 1E-4（HARQ 6× 後）；③ HARQ 6 次重傳後 ACK 確認，buffer 清空；④ UL/DL 頻道隔離 ≥ 40 dB |
| 測試設備 | 訊號產生器、頻譜分析儀、功率計、50 dB 衰減器（模擬路徑損耗）|

### SIT-004：ADCS 閉迴路（Air Bearing Table）

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-008（指向 ≤ 5°），SYS-009（Detumbling ≤ 60 min）|
| 方法 | Air Bearing Table 無摩擦旋轉平台，注入初始翻滾 ω = 5°/s，EKF + B-dot 控制 |
| 合格準則 | ① Detumbling：ω 收斂至 ≤ 0.1°/s，時間 ≤ 60 min；② Nadir Pointing 穩態指向誤差 ≤ 5°（3σ，持續 ≥ 10 min）；③ RW 角動量峰值 ≤ 0.25 mNms |
| 測試設備 | Air Bearing Table、外部動作捕捉系統、角速度計 |

### SIT-005：TVAC 前整機功能驗證（Ambient）

| 項目 | 內容 |
|------|------|
| 對應需求 | 全系統功能完整性確認 |
| 方法 | 模擬一個完整軌道（96 min）：日照段（Science Mode, 7.16 W）→ 食月段（SafeMode, 3.18 W）→ DL 接觸（DL Mode, 11.25 W，8 min）|
| 合格準則 | ① DoD/軌 ≤ 8.3%；② 接觸窗口期間 EIRP 穩定（≤ ±0.5 dBm 漂移）；③ 食月段切換 SafeMode 時間 ≤ 5 s；④ 整機功耗符合 Power Budget（±5%）|
| 測試設備 | 電源量測模組、UART 遙測記錄、功率計 |

---

## 5. 環境測試（Environmental Test，ET）

### ET-001：熱真空測試（TVAC）

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-012（電池 T ≥ -20°C，結構 T -20°C~+60°C）、ENV-002（TVAC 條件）|
| 方法 | 真空度 ≤ 0.01 Pa，溫度 -20°C ~ +60°C，4 次循環，各段保溫 ≥ 60 min |
| 合格準則 | ① 全程電池節點溫度 ≥ -20°C（MLI + 加熱片有效）；② 各溫度端點全功能測試 PASS（RF + ADCS + EPS）；③ 每次循環後電池容量 ≥ 97% |
| 測試設備 | 熱真空腔（NSPO 或 國研院），熱電偶 8 點（電池、PA、FPGA、結構） |
| 前置條件 | **Q4 MLI 安裝 + AC-009 + AC-010 關閉後方可執行** |

### ET-002：振動測試

| 項目 | 內容 |
|------|------|
| 對應需求 | ENV-001（發射振動環境）|
| 方法 | 依 NASA-STD-7003A，X/Y/Z 三軸各一次 Random Vibration（14.1 Grms）|
| 合格準則 | ① 振動後外形目視無裂縫/鬆動；② 振動後 SIT-003 RF 回路測試 PASS（EIRP ± 2 dBm）；③ 振動後 ADCS 陀螺偏差漂移 ≤ 0.1°/s |
| 測試設備 | 振動台（三軸）、加速規感測器（4 點）|

### ET-003：EMC/EMI 測試

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-003（UL/DL 隔離）、EMC 法規合規 |
| 方法 | DL 發射開啟時，量測 UL 接收端雜訊基底，確認自我干擾 |
| 合格準則 | ① UL/DL 頻道隔離 ≥ 40 dB（DL @2185 MHz 對 UL @1995 MHz 接收機靈敏度影響 ≤ 0.5 dB）；② 30 MHz~1 GHz 傳導雜訊符合 CISPR 22 Class B |
| 測試設備 | 屏蔽腔、頻譜分析儀、雜訊源 |

### ET-004：天線場型量測

| 項目 | 內容 |
|------|------|
| 對應需求 | SYS-002（衛星接收天線 ≥ 2 dBi）、SYS-004（DL 發射天線增益）|
| 方法 | 無反射電波暗室（Anechoic Chamber），3D 場型掃描 @ 1995 MHz + 2185 MHz |
| 合格準則 | ① UL Patch 天線增益 ≥ 2 dBi 在 ±60° 半角內（仰角 ≥ 60° 對應衛星視角）；② DL Patch 天線增益 ≥ 2 dBi 在 ±60° 內；③ 圓極化軸比 ≤ 3 dB |
| 測試設備 | 無反射電波暗室、天線架（三軸旋轉）、標準增益天線 |

---

## 6. V&V 矩陣（SYS-001 ~ SYS-021）

| 需求 ID | 需求描述 | 驗證方法 | 對應測試 ID | 狀態 |
|---------|---------|---------|-----------|------|
| SYS-001 | 軌道 500 km SSO | A, S（GMAT）| — | TBV（發射後）|
| SYS-002 | 最低服務仰角 ≥ 60° | A（D-003 v3.2）, T | UT-003, ST-001, SIT-003, ET-004 | Analysis VER |
| SYS-003 | 帶外抑制 ≥ 40 dB @2170 MHz | A + T（VNA）| UT-003, UT-006, ST-001, ET-003 | Partial VER（T 待執行）|
| SYS-004 | DL Link Margin ≥ 3 dB（HARQ 6×）| A + T | UT-005, UT-007, ST-001, SIT-003 | Analysis VER |
| SYS-005 | 系統峰值功耗 ≤ 10.3 W | A（D-004 v3）| SIT-005 | Analysis VER |
| SYS-006 | 電池 DoD ≤ 30% | A + T | UT-008, ST-003, SIT-005 | Analysis VER |
| SYS-007 | 太陽能板發電 ≥ 6.5 W BOL | A + T | ST-003 | Analysis VER |
| SYS-008 | 指向精度 ≤ 5°（3σ）| S（D-002）+ T | ST-002, SIT-004 | Analysis VER（⚠️ Q3 OPEN）|
| SYS-009 | Detumbling ≤ 60 min | S + T | UT-001, ST-002, SIT-004 | Analysis VER |
| SYS-010 | S-band n236（UL/DL 頻段）| I + T | UT-002, UT-003, UT-006, ST-001 | VER |
| SYS-011 | 資料率 ≥ 100 bps（50 kbps 實際）| A + T | UT-012, ST-004, SIT-003 | Analysis VER |
| SYS-012 | 電池操作溫度 ≥ -20°C | A（D-005）+ T | UT-009, ST-005, ET-001 | Partial VER（⚠️ Q4 TVAC 待執行）|
| SYS-013 | TID 防護 + SEU TMR/Scrubbing | A + S | ST-006 | Analysis VER |
| SYS-014 | 除軌 ≤ 5 年（IADC）| A（軌道衰減）| — | VER（Analysis）|
| SYS-015 | TID ≤ 10 krad / 2yr | A, S（SPENVIS）| — | VER（D-001 Analysis）|
| SYS-016 | SEU ≤ 500/s（軌道平均）| A, S | ST-006 | VER |
| SYS-017 | SEU ≤ 2000/s（SAA 峰值）| A, S | ST-006 | VER |
| SYS-018 | SEL 免疫（LET ≥ 40 MeV·cm²/mg）| A（推論）+ T（待 ADI）| — | Partial VER（⚠️ Q5 LT5512 OPEN）|
| SYS-019 | 任務壽命 2 年（TID 裕量 ≥ 2×）| A（D-001，裕量 3.4×）| — | VER |
| SYS-020 | 質量 ≤ 4000 g | A + T | SIT-001 | VER（1374 g）|
| SYS-021 | CG 偏移 < 20 mm | A（估算）+ T | SIT-001 | Partial VER（待 CAD + 實測）|

---

## 7. Soft Gate 依賴項

下列測試項目需等特定 Soft Gate 關閉後才能執行或更新驗收準則：

| Soft Gate | 狀態 | 影響的測試 | 說明 |
|-----------|------|-----------|------|
| Q3（ADCS ±3.4° 修正）| 🟡 OPEN | SIT-004 | 食月段指向驗收準則（±3.4° 或 ±3.5°）待 AI-D002-SW-03 確認後更新 |
| Q4（電池熱控 MLI）| 🟡 進行中 | ST-005, SIT-005, ET-001 | MLI 安裝後方可執行環境測試電池溫度驗收；AC-009/010 關閉後方可執行 |
| Q5（LT5512 TID 確認）| 🟡 OPEN | ET-001 | LT5512 TID 確認前，TVAC 後 RF 功能驗收含不確定性（若 TID 不足需加屏蔽）|

**ET GO 條件（環境測試啟動）：**
Q3 AI-D002-SW-03 ✅ + Q4 AC-009 ✅ + Q4 AC-010 ✅ + Q5 AI-D001-1 ✅ + HARQ SW-HG-001/002/003 ✅

---

## 8. 測試時程（預計）

| 階段 | 任務 | 預計完成 |
|------|------|---------|
| UT | UT-001 ~ UT-012 | Sprint 4 W2 |
| ST | ST-001 ~ ST-006 | Sprint 4 W2-W3 |
| SIT | SIT-001 ~ SIT-005 | Sprint 4 W3 |
| ET | ET-001 ~ ET-004 | Post-TRR（ET GO 條件滿足後）|

---

*D-007 v1 | QA Agent 林宜靜 | 2026-04-17*
*P2P Review：SE 陳明哲（需求覆蓋性）+ SW 陳俊宏（FSW 測試可行性）*
