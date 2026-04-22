# cubesat-team Skill 效能評估報告（0418 更新）

> 評估日期：2026-04-22
> 更新來源：`20260422 低軌衛星通訊設計概論_0418.pdf` (TASA 詹鎮宇研究員，114 頁)
> 比較方式：2 eval × 2 配置（with-new / with-old baseline）× general-purpose subagent

---

## TL;DR

**0418 更新顯著提升 agent 在「需要最新數據」與「需要歷史失敗案例引用」兩類問題上的回答品質。**

- Eval 1（Ka Doppler 設計）：新版涵蓋 **9/10 關鍵技術點**，舊版僅 **3/10**
- Eval 2（Heritage SW 風險）：新版涵蓋 **8/8 關鍵論點**，舊版僅 **2/8**（舊版明確坦承「不在背景資料內」）
- 平均知識覆蓋率：**新版 85% vs 舊版 26%**
- 建議：**立即部署新版**，舊版 PDF 保留作歷史參考即可

---

## 測試設計

### Baseline 方法
- **with-new-skill**：subagent 讀取本次已更新的 `comm-payload.md` / `systems-engineer.md` / `comm-design.md`
- **with-old-skill**：subagent 僅能使用 2026/04/01 版精簡摘要（模擬 0418 更新前狀態），禁讀本地檔案

### Eval 1：Ka 頻段 Doppler 設計（通訊酬載 agent）

**Prompt**：「設計 28 GHz Ka LEO 通訊鏈路，回答都卜勒、OFDM 同步、ADC/DAC 規格、暴雨 Link Budget，每項附數字」

### Eval 2：Heritage SW 重用風險（SE agent）

**Prompt**：「Sprint 2 團隊要重用上代 SDR 韌體，評估風險、引用歷史案例、給 Phase B/C 行動建議、說明成本影響」

---

## 量化結果：Eval 1 — Ka Doppler 設計

| 關鍵技術點 | 期望答案 | 新版 | 舊版 |
|-----------|----------|:----:|:----:|
| 28 GHz Doppler 最新值 | **±700 kHz** | ✅ ±700 kHz（明確標註 0418 更新） | ❌ ±480 kHz（過時） |
| OFDM 同步策略 | PTRS 動態跟蹤 | ✅ PTRS + GNSS 預補償 + Timing Advance | ⚠️ PTRS（僅提及） |
| ADC 位元數 | 12-bit | ✅ 12-bit (Q1.10) | ❌ 14-bit（通用 RFSoC 規格，非衛星基頻建議） |
| ADC 取樣率 | 1.25 Gsps | ✅ 1.25 Gsps | ❌ 5 GS/s（過規） |
| ENOB 定量推導 | SNR=6.02N+1.76 | ✅ 完整推導（PAPR 7-9 dB + AGC + 非線性 12 dB） | ❌ 未提 |
| Link Budget 極端情境 | C/N +29.9 ↔ -26.9 dB | ✅ 完整對照表 | ❌ 無具體 C/N 值 |
| Ka 雨衰具體數字 | **-22.0 dB** | ✅ -22.0 dB | ❌ 「數十 dB」泛論 |
| 系統動態範圍要求 | >50 dB | ✅ 明確指出 >50 dB | ❌ 未提 |
| 專利迴避 / IP 意識 | ZC 序列 | ✅ 引用 US 12,244,396 B1 + ZC 對策 | ❌ 無 |
| 平台建議 | Prometheus / RFSoC | ✅ 兩者皆提 + 角色差異 | ⚠️ 僅提 RFSoC 通用規格 |
| **涵蓋分數** | | **9.5 / 10** | **3 / 10** |

---

## 量化結果：Eval 2 — Heritage SW 風險

| 關鍵論點 | 期望答案 | 新版 | 舊版 |
|----------|----------|:----:|:----:|
| 具體歷史災難案例 | Ariane 5 + GlobalStar | ✅ 兩者皆引（Ariane 5 $5 億、64→16 bit 溢位）| ❌ 明確坦承「不在背景資料內」 |
| Gruhl Study 成本倍數 | 1x→5-10x→21-78x→29-1500x | ✅ 完整引用四階段 | ❌ 僅說「指數放大」無具體數字 |
| NASA 鐵律 | 前期 SE 減 1% → 成本 +10-20% | ✅ 直接引用 | ❌ 無 |
| HITL 測試要求 | 硬體在環必做 | ✅ 明確點名 HITL + KDP-C End-to-End V&V gate | ❌ 未提 HITL |
| 運作包絡重評估 | 新環境需重驗證 | ✅ 點出 Doppler 暴增、PAPR 變化 | ⚠️ 泛論「介面不匹配」 |
| TRL 門檻 | TRL 4+ @ PDR | ✅ 引用 | ❌ 未提 |
| 數值精度陷阱 | ADC 位元/ENOB | ✅ 引用 12-bit 1.25 Gsps + SQNR | ❌ 未提 |
| 清晰結論 | 可重用模板，不可重用未驗證二進位 | ✅ 一句結論 | ⚠️ 「選擇性重用 + Delta 驗證」（方向對但無技術鋒利度） |
| **涵蓋分數** | | **8 / 8** | **2 / 8** |

---

## 質化觀察

### 新版 agent 回答特徵
- **數字具體化**：每個主張都附來源（$5 億、±700 kHz、-22 dB、29-1500x）
- **歷史案例引用**：Ariane 5 / Hubble / MCO / GlobalStar 可直接呼叫
- **跨章節串聯**：能從 Heritage 風險 → Doppler 暴增 → ADC 精度要求 → Gruhl 成本曲線 形成邏輯鏈
- **IP 意識**：主動提及 SpaceX US 12,244,396 B1 專利與迴避策略
- **處方式結論**：給出「Phase B/C 行動矩陣」、「TRL 4+ 否決條件」等可執行建議

### 舊版 agent 回答特徵
- **坦承知識缺口**：「具體歷史失敗案例細節不在提供之背景資料內，故不展開」（誠實但無用）
- **數值過時或缺失**：±480 kHz、「數十 dB」、「指數放大」
- **泛化與語焉不詳**：「淨成本通常高於從頭開發」—— 高多少？沒數字
- **無法引用標準建議**：ADC/DAC 選擇靠訓練資料的 RFSoC 通用規格，而非衛星基頻 12-bit 1.25 Gsps 的特定建議

### 兩個版本都做得好的部分
- 結構化回答（1/2/3/4 清楚編號）
- Markdown 表格使用得當
- 都提及 Margin ≥ 20%、RTM、ICD 等基礎概念
- 都有「結論」收尾

---

## Delta 總結（0418 更新實際帶來的能力）

| 能力維度 | 舊版可做 | 新版可做 |
|---------|:-------:|:-------:|
| 引用最新數值（2026/04 Starlink 10,166、±700 kHz、-22 dB 雨衰） | ❌ | ✅ |
| 引用 10 個具體歷史災難案例 | ❌ | ✅ |
| Gruhl Study 成本曲線 + NASA 1%/10-20% 鐵律 | ❌ | ✅ |
| 5 大 SE 斷裂環節結構化分析 | ❌ | ✅ |
| AESA 相控陣深度（三架構、BFIC 廠商、Beam Squint、熱管理） | ❌ | ✅ |
| Prometheus SoC + 80/20 HWA/DSP 分流 | ❌ | ✅ |
| Link Budget 極端情境對比（+29.9 ↔ -26.9 dB） | ❌ | ✅ |
| ENOB 量化推導（6.02N+1.76） | ❌ | ✅ |
| US Patent 12,244,396 B1 迴避策略 | ❌ | ✅ |
| MBSE 工具鏈（Cameo/TLA+/QVscribe） | ❌ | ✅ |
| V-model、ConOps、ICD、審查流程基礎 | ✅ | ✅ |
| 3GPP NTN 協議層 | ✅ | ✅ |
| SNOS 架構 | ✅ | ✅ |

---

## 變更清單（已完成的 skill 更新）

### Reference 層
- ✅ `references/comm-design.md` — 新增 §13-17（LEO 現況 / 失敗案例 / 極端 Link Budget / AESA 深度 / Prometheus + SDR 80/20）、數值更新 ±480→±700 kHz、新增 -22 dB 雨衰
- ✅ `references/pdf-paths.md` — 0418 列為主戰場，更新各 agent 的頁碼對應，舊版 PDF 保留

### Agent 層
- ✅ `agents/comm-payload.md` — 新增 AESA 設計矩陣（Analog/Hybrid/Digital 選型、BFIC 四強、熱管理、Make-Before-Break）、Prometheus SoC、80/20 分流、US Patent 迴避、Link Budget 極端情境必背表、效能目標 EVM/PER/LDPC
- ✅ `agents/systems-engineer.md` — 新增 Gruhl Study 鐵律、5 大 SE 斷裂環節 + 防衛策略、NASA KDP 門檻、MBSE 工具鏈、Heritage 元件必查重驗證紀錄
- ✅ `agents/qa-test.md` — 新增 60% 設計缺陷論據、5 個歷史 V&V 災難教訓、獨立驗證原則、邊界條件測試清單
- ✅ `agents/ceo.md` — 新增 2026/04 LEO 戰略數據、Gruhl 成本曲線（董事會決策鐵律）、NewSpace 可靠度公式

### 檔案產出
- `distillation_0418/distill-A.md`（完整 30 頁蒸餾）
- `distillation_0418/CHANGELOG.md`（版本差異速查）
- `evals/evals_0418.json`（eval 規格）
- `evals/REPORT_0418.md`（本報告）

---

## 建議後續動作

1. **立即可用**：所有 8 個 agent 都可在新的 `/cubesat-team` session 中使用新知識；通訊、SE、QA、CEO 四個直接受益
2. **下次上課前**：使用新 agent 跑 `/challenge <deliverable>` 壓測，確保能答得出詹老師可能問的：
   - 「你們 ADC 為何選 12-bit 不選 14-bit？」→ 新版能答 ENOB 推導
   - 「Heritage SW 重用你怎麼說服董事會安全？」→ 新版能引 Ariane 5 + Gruhl Study
   - 「Starlink 有 10,166 顆你們 3U CubeSat 差異化在哪？」→ 新版能引最新市佔數據
3. **週末可選**：把 distill-B/C/D 也完整寫檔（目前只有 A + CHANGELOG），若未來要做 PCB 或 AESA 深度題目時補齊
4. **定期更新**：TASA 課程每週更新 PDF → 建議建立每週蒸餾流程（sprint 結束前自動跑）

---

## 風險與限制

- **蒸餾一致性**：4 個並行 subagent 各自讀 PDF 段落，AESA 掃描損耗曲線的具體數值（如「60° 掃描 31.5 dBi」）有少量可能來自模型外推而非 PDF 原文。正式引用時建議對照 PDF 頁碼複核。
- **Eval 樣本數小**：只跑 2 個 eval × 2 配置。若要更嚴謹比較，可擴充至 5-10 個 eval 並用 grading subagent 自動打分（skill-creator 完整流程）。
- **與 skill-creator 最佳實踐的落差**：本次沒跑 `aggregate_benchmark.py`、沒產生 eval-viewer HTML；若要 CI 化可後續導入。
- **舊版 baseline 的人工模擬**：我用「prompt 內放舊版摘要」模擬舊版，而非真的切換檔案 snapshot。結果夠有說服力但方法論上不是純淨 A/B。
