# 系統工程 (System Engineering) 知識庫

> 蒸餾自 TASA 課程教材（詹鎮宇研究員）- 第一講

## 目錄
1. [NASA 任務生命週期 (Life-Cycle Phases)](#1-nasa-任務生命週期)
2. [V-Model 架構](#2-v-model-架構)
3. [技術審查閘門 (Review Gates)](#3-技術審查閘門)
4. [技術成熟度等級 (TRL)](#4-技術成熟度等級-trl)
5. [需求追溯矩陣 (RTM)](#5-需求追溯矩陣-rtm)
6. [驗證方法 (Verification Methods)](#6-驗證方法)
7. [TASA 交付文件清單 (CDRL)](#7-tasa-交付文件清單)
8. [SDR 審查實務準則](#8-sdr-審查實務準則)
9. [SRB 評估矩陣](#9-srb-評估矩陣)
10. [參考文獻](#10-參考文獻)

---

## 1. NASA 任務生命週期

| Phase | 名稱 | 核心活動 | 關鍵產出 |
|-------|------|--------|--------|
| Pre-A | Concept Studies | 任務概念探索、可行性分析 | Mission Concept Review (MCR) |
| A | Concept & Technology Development | 需求定義、技術成熟化 | SRR (系統需求審查) |
| B | Preliminary Design & Technology Completion | 初步設計、介面定義 | PDR (初步設計審查) |
| C | Final Design & Fabrication | 詳細設計、製造、編碼 | CDR (關鍵設計審查) |
| D | System Assembly, Integration & Test (AIT) | 整合測試、環境驗證 | SIR / ORR |
| E | Operations & Sustainment | 任務操作、科學資料回收 | PFAR (飛行後評估審查) |
| F | Closeout / Disposal | 除役、安全處置 | DR / DRR |

---

## 2. V-Model 架構

左半邊（分解）：定義需求 → 分解架構 → 系統開發
右半邊（驗證）：逐層驗證 → 系統驗證

**理論 vs. 實務的差異：**
- 理論承諾：按部就班定義需求、分解架構、逐層驗證，系統就能完美運作
- 實務挑戰：子系統達標卻在系統整合時崩潰；為降低風險反而導致成本失控；專案依然可能在發射台前失敗

**關鍵洞察：** 物理世界與人性充滿變數，標準流程是「必要條件」而非「充分條件」。

---

## 3. 技術審查閘門

### 3.1 SRR (系統需求審查) | Phase A
- **核心目的：** 凍結專案需求，確保系統規格完全滿足任務目標
- **進入準則：** 已定義功能與效能需求；專案初步計畫已就緒
- **成功準則：** 成功凍結專案與系統需求；確認概念可進入後續系統定義

### 3.2 MDR/SDR (系統定義審查) | Phase A 尾聲
- **核心目的：** 確立系統架構，建立 Functional Baseline
- **進入準則：** 系統架構提案已完成；需求已向下分配至各子系統層級
- **成功準則：** 架構能有效回應功能與效能需求；Functional Baseline 正式確立

### 3.3 PDR (初步設計審查) | Phase B
- **核心目的：** 確立 Allocated Baseline，確認初步設計能以可接受風險進入細部設計
- **進入準則：** 初步設計已完成；技術介面已充分定義
- **成功準則：** 設計成熟度達 10%-20%；授權專案進入 Implementation Phase
- **確立基準：** Allocated Baseline

### 3.4 CDR (關鍵設計審查) | Phase C
- **核心目的：** 確立 Product Baseline，確保設計成熟至可進行全規模製造
- **進入準則：** 最終設計文件已備齊；系統成熟度足以支撐製造計畫
- **成功準則：** 核准進入硬體製造與軟體 Coding 階段
- **確立基準：** Product Baseline

### 3.5 PRR (量產準備審查) | Phase C
- **核心目的：** 確認開發者具備高效量產的準備度（適用於數量 > 3 的專案如低軌衛星星系）
- **進入準則：** 生產計畫已完成；製造、組裝、測試設備與人員已就位
- **成功準則：** Build-to Baseline 獲批准；正式圖面釋出，授權啟動規模化生產

### 3.6 SIR (系統整合審查) | Phase D
- **核心目的：** 確保所有子系統、軟硬體均已準備妥當，可依計畫進行系統級整合
- **進入準則：** 各區段、元件與子系統依進度交付；整合設施與程序書已就緒
- **成功準則：** 整合計畫與程序獲批准；技術與時程風險可控

### 3.7 ORR (營運準備審查) | Phase D/E
- **核心目的：** 檢驗實際系統特性與操作程序，確保軟硬體與人員反映部署後的真實狀態
- **進入準則：** 飛行與地面支援硬體、軟體已就位；使用者文件與操作手冊已完備
- **成功準則：** 系統可移交至指定營運單位或發射場；人員培訓完成，應急計畫就緒

### 3.8 PFAR / DR / DRR | Phase E/F
- **PFAR (飛行後評估審查)：** 評估飛行後狀態，識別異常，制定未來航班的緩解對策
- **DR (除役審查) & DRR (處置準備審查)：** 確認終止任務的決策，確保資產最終處置安全且符合規範

---

## 4. 技術成熟度等級 (TRL)

| TRL | 定義 | 說明 |
|-----|------|------|
| 1 | Basic Principles Observed | 基本原理被觀察與報告 |
| 2 | Technology Concept Formulated | 技術概念或應用已規劃 |
| 3 | Analytical/Experimental Proof-of-Concept | 關鍵功能的分析與實驗原理驗證 |
| 4 | Component Validation in Lab | 元件/麵包板在實驗室環境中驗證 |
| 5 | Component Validation in Relevant Environment | 元件/麵包板在相關環境中驗證 |
| 6 | System/Subsystem Prototype Demo | 系統/子系統模型在相關環境中展示（地面或太空） |
| 7 | System Prototype Demo in Space | 系統原型在太空環境中展示 |
| 8 | Actual System Completed & Qualified | 實際系統完成並通過飛行測試 |
| 9 | Flight Proven | 實際系統通過成功任務操作驗證 |

**實務重點：** PDR 時子系統 TRL 應達 4-5，CDR 時應達 6 以上。

---

## 5. 需求追溯矩陣 (RTM)

- **雙向追溯 (Bidirectional Traceability)：** 確保每條需求都能對應到功能單元，沒有孤兒需求
- 上行追溯：功能 → 需求（為何做？）
- 下行追溯：需求 → 設計/測試（如何做？如何驗？）

---

## 6. 驗證方法

| 方法 | 英文 | 說明 | 適用場景 |
|------|------|------|--------|
| 測試 | Test | 實際操作元件/系統並量測結果 | 效能參數、環境耐受 |
| 分析 | Analysis | 數學模型、模擬計算 | 結構應力、熱分析 |
| 檢查 | Inspection | 目視或量測尺寸確認 | 外觀、製造品質 |
| 展示 | Demonstration | 在實際或模擬環境中操作 | 操作程序、功能驗證 |

---

## 7. TASA 交付文件清單

| 編號 | 審查階段 | 文件名稱 |
|------|----------|--------|
| XX-CDRL-001 | KO | Project Management Report |
| XX-CDRL-002 | PDR+CDR+ITR+SRR | Spacecraft Design Report |
| XX-CDRL-003 | PDR+CDR+ITR+SRR | Satellite Systems Specification |
| XX-CDRL-004 | PDR | Orbit Simulation Report |
| XX-CDRL-005 | CDR | Spacecraft Structure Design and Analysis |
| XX-CDRL-006 | CDR | Spacecraft Thermal Analysis |
| XX-CDRL-007 | CDR | Spacecraft Firmware/Software Design Document |
| XX-CDRL-008 | CDR | Command & Telemetry Allocation Document |
| XX-CDRL-009 | CDR | Spacecraft ADCS Design Report |
| XX-CDRL-010 | CDR | Mechanical and Electrical Interface Control Document |
| XX-CDRL-011 | ITR | Integration and Test Implementation Plan |
| XX-CDRL-012 | ITR | Functional Test Procedure |
| XX-CDRL-016 | SRR | Satellite Registration and Frequency Coordination Report |
| XX-CDRL-017 | SRR | Satellite to Launcher Interface Control Document |
| XX-CDRL-019 | PLR | Ground Station Operation Manual |
| XX-CDRL-021 | FR | Early Orbit Operation Report |

---

## 8. SDR 審查實務準則

### 必須做 (DO THIS)
1. **建立雙向追溯 (Bidirectional Traceability)：** 確保每條需求都能對應到功能單元
2. **定義清晰介面 (Define Interfaces)：** 及早劃定內部與外部的系統邊界
3. **誠實面對風險 (Transparent Risk Management)：** 詳實記錄風險並提出 CRM 緩解計畫
4. **擁抱 SRB 意見 (Embrace Independent Assessment)：** 將 SRB 視為專案的防護網

### 絕對不要做 (DON'T DO THIS)
1. **過早進入細部設計 (Jumping to Detailed Design)：** SDR 關注架構與功能，零件是 PDR/CDR 的工作
2. **隱藏技術瑕疵 (Hiding Technical Flaws)：** 絕不可將未決的 Trade Studies 掃入地毯下
3. **需求與架構脫鉤 (Orphaned Requirements)：** 避免架構設計超出需求範圍
4. **忽視測試與驗證計畫 (Ignoring Verification)：** 不要等到 CDR 才開始思考測試

---

## 9. SRB 評估矩陣

**紅黃綠燈判定：**
- **綠燈 (Successful)：** 符合預期，基準穩固
- **黃燈 (Partially Successful)：** 存在缺陷但具備可行的 Mitigation Plan
- **紅燈 (Unsuccessful)：** 重大缺陷，需暫停或重做

**SRB 審查 6 大維度：**
1. 策略目標契合度 (Strategic Alignment)
2. 管理架構 (Management Approach)
3. 技術方法 (Technical Approach)
4. 成本與時程 (Cost & Schedule)
5. 資源可用性 (Resource Availability)
6. 風險管理 (Risk Management)

---

## 10. 參考文獻

| 文件 | 說明 |
|------|------|
| NPR 7123.1C | NASA Systems Engineering Processes and Requirements（核心強制性標準與 Appendix G 檢查清單） |
| NASA/SP-2016-6105 Rev 2 | NASA Systems Engineering Handbook（實作手冊與 Phase A/B 轉換細節） |
| NASA SRB Handbook | Standing Review Board 運作指引與 RFA 實務操作 |

---

## 課程評分標準（期末）

| 項目 | 權重 |
|------|------|
| CubeSat 酬載任務設定，使用 COTS 元件 | 10% |
| 硬體與軟體功能定義 | 20% |
| 驗測方法設計（功能與環規測試） | 20% |
| 計畫成員（5人：系統工程/硬體&軟體設計/驗測/機構散熱/品管） | 20% |
| 計畫時程與經費規畫 | 20% |
| 簡報：每組 25 min（20 min 簡報 + 5 min Q&A），不少於 25 頁 | -- |
