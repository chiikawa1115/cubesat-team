# PDF 教材路徑索引

所有原始教材 PDF 位於：`C:\Users\rudy.hsieh\Desktop\satelite pdf\`

使用 Read 工具讀取 PDF 時，須指定 `pages` 參數（每次最多 20 頁）。
若 Read 失敗，使用 Poppler 工具作為備用方案（見 MEMORY.md Poppler 段落）。

---

## PDF 清單

| 檔案名稱 | 內容概要 | 建議查閱場景 |
|----------|---------|------------|
| `00..pdf` | 課程介紹、教學大綱、評分標準、分組規則 | 專案規劃、評分標準確認、報告格式要求 |
| `01. (1).pdf` | 衛星系統概論、系統工程 V-model、NASA 任務階段、設計審查節點 (SRR/PDR/CDR/TRR) | 系統工程流程、審查準則、V-model 對應 |
| `02..pdf` | AOCS 姿態軌道控制子系統、感測器與致動器、控制演算法 | AOCS 設計、姿態需求分析、元件選型 |
| `03..pdf` | 任務模擬 (GMAT/STK)、頻率協調 (ITU)、除軌法規 (25 年規則) | 軌道模擬設定、頻率申請、法規合規性 |
| `20260401 低軌衛星通訊設計概論0401.pdf` | B5G LEO 通訊設計主教材（第 1 版）：DVB-S2X、NTN 架構、SDR/FPGA 酬載、Link Budget | 歷史參考、基礎理論回顧 |
| `20260408 低軌衛星通訊設計概論 (1).pdf` | Starlink/Kuiper/OneWeb 星座分析、AESA 終端設計、TASA B5G 計畫 | 產業分析、競爭對手研究 |
| `20260415 低軌衛星通訊設計概論_0410 (1).pdf` | 0410 講次（過渡版本） | 歷史參考 |
| **`20260422 低軌衛星通訊設計概論_0418.pdf`** ⭐ **最新** | **4/22 重大改版（114 頁）**：新增 10 個失敗案例 + Gruhl Study + AESA 17 頁專章 + Prometheus SoC + 80/20 SDR + US Patent 12,244,396 B1 迴避策略。**數值更新：28 GHz Doppler ±700 kHz（舊 ±480）、Ka 50 mm/h 雨衰 -22 dB、Starlink 10,166 顆** | **所有通訊酬載設計優先查此版**；失敗案例 / 系統工程斷裂環節；AESA 熱管理；基頻 SoC 架構 |

---

## 使用方式

### 直接讀取
```
Read tool: file_path = "C:/Users/rudy.hsieh/Desktop/satelite pdf/01. (1).pdf", pages = "1-20"
```

### Poppler 備用（文字萃取）
```bash
"C:/Users/rudy.hsieh/poppler/poppler-24.08.0/Library/bin/pdftotext.exe" "C:/Users/rudy.hsieh/Desktop/satelite pdf/01. (1).pdf" -f 1 -l 20 -
```

### Poppler 備用（轉圖片後讀取）
```bash
"C:/Users/rudy.hsieh/poppler/poppler-24.08.0/Library/bin/pdftoppm.exe" -png -f 5 -l 5 "C:/Users/rudy.hsieh/Desktop/satelite pdf/02..pdf" /tmp/aocs_page
```
然後用 Read 工具讀取產出的 PNG。

---

## 各 Agent 對應 PDF

| Agent | 主要參考 PDF |
|-------|------------|
| CEO | **0418.pdf p.13-16** (失敗案例全景、Gruhl Study)、00..pdf (評分)、所有 PDF (統籌) |
| PM | **0418.pdf p.14 (成本曲線)、p.22 (KDP)**、00..pdf、01..pdf |
| 系統工程師 | **0418.pdf p.15-26** (5 大斷裂環節、NASA SE 引擎、MBSE 工具鏈)、01..pdf |
| 通訊酬載工程師 | **0418.pdf p.3, p.8-12 (Link Budget), p.44-60 (AESA), p.91-109 (Prometheus/SDR)** ⭐ 主戰場；20260408.pdf (產業) |
| AOCS 工程師 | 02..pdf (AOCS)、03..pdf (軌道)、**0418.pdf p.2 (軌道永續性三維限制、Kessler 50k 閾值)** |
| 軟韌體工程師 | **0418.pdf p.91-109** (NoC、ACE、80/20 HWA/DSP、Prometheus SoC)、20260401...pdf (基礎) |
| 機構熱控工程師 | 01..pdf、02..pdf、**0418.pdf p.57-58 (AESA 熱管理：645W、λ/2 5mm、T_j >150°C、微流體冷卻、異質 3D 整合)** |
| QA 測試工程師 | **0418.pdf p.13-20 (失敗案例 V&V 教訓)、p.25 (實戰手冊)**、01..pdf、00..pdf |
