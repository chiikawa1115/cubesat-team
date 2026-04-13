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
| `20260401 低軌衛星通訊設計概論0401.pdf` | B5G LEO 通訊設計主教材：DVB-S2X、NTN 架構、SDR/FPGA 酬載、Link Budget | 通訊酬載設計、DVB-S2X 調變選擇、FPGA 架構 |
| `20260408 低軌衛星通訊設計概論 (1).pdf` | Starlink/Kuiper/OneWeb 星座分析、AESA 終端設計、TASA B5G 計畫 | 產業分析、競爭對手研究、終端設計參考 |

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
| CEO | 00..pdf (評分標準)、所有 PDF (統籌) |
| PM | 00..pdf (時程/評分)、01. (1).pdf (任務階段) |
| 系統工程師 | 01. (1).pdf (V-model/系統工程) |
| 通訊酬載工程師 | 20260401...pdf (通訊主教材)、20260408...pdf (產業分析) |
| AOCS 工程師 | 02..pdf (AOCS)、03..pdf (軌道模擬) |
| 軟韌體工程師 | 20260401...pdf (FPGA/SDR 架構) |
| 機構熱控工程師 | 01. (1).pdf (系統 budget)、02..pdf (元件規格) |
| QA 測試工程師 | 01. (1).pdf (審查準則)、00..pdf (評分標準) |
