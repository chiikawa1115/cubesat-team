# cubesat-team Skill Pivot 效能評估報告（Reporting-First 轉向）

> 評估日期：2026-04-23
> Pivot 緣由：任務本質從「CubeSat 產品開發模擬」轉為「課程專題紙上設計」
> 比較方式：2 eval × 新 pivot 版本（讀取 pivot 後的 agents + deliverable-template.md）

---

## TL;DR

**Pivot 完全成功。兩個 eval 都自然產出紙上專題所需的結構化交付物，無需額外微調。**

- Eval A (Comm-Payload SDR 設計文件)：6/6 節模板全數套用，分數區間 **18-20/20**
- Eval B (PM BOM 表 + Gantt)：BOM/預算/trade-off/Gantt 全員到齊，分數區間 **18-20/20**

兩份 output 都主動引用：
- `deliverable-template.md` 的 6 節格式
- `course-rubric.md` 的紙上專題評分要點
- **明確聲明「紙上專題，不實際採購」**

→ 這代表 pivot 後的 agent 正確內化了新的任務本質。

---

## Eval A 評分：Comm-Payload 產出 S-band SDR 設計文件

### 6 節模板完整度

| 節 | 檢查項目 | 結果 |
|---|---------|:----:|
| 1. Block Diagram | Mermaid 流程圖 + 完整 RF 鏈路 | ✅ |
| 2. Interface Table | 9 個 signals（SPI/LVDS/I2C/GPIO/UART/PPS），含 Protocol/Rate/Pin/備註 | ✅ |
| 3. Register Config | 12 個關鍵 register + Address + Config Value + 說明 | ✅ |
| 4. Driver Sequence | `comm_payload_init()` + `rx_loop()` + 錯誤路徑 + 狀態機圖 | ✅ |
| 5. Spec vs Datasheet | 9 條系統需求對應、全部 Margin 標示、全 Meet | ✅ |
| 6. COTS 選型 | 主選 + 3 替代 + trade-off 表 + Cost/Perf/Heritage 三維決策 | ✅ |

### 加分項（pivot 內化證據）

- ✅ 明確聲明「本專題為**紙上設計不實際採購**，採購風險標記 Low / N/A」
- ✅ 主動引用「deliverable-template.md §常見誤區」
- ✅ 跨章節呼應：引用 0418 PDF p.8-12（Link Budget 極端情境）+ p.91-109（Prometheus 80/20）
- ✅ 技術深度（非敷衍）：AMC 用 2nd-order PI loop、熱保護 T_j > 95°C throttle PA、AD9361 飛行 heritage >50 次
- ✅ Doppler NCO FTW 特地保留 ±700 kHz 範圍（Ka 未來擴展），呼應 0418 更新值

### 預估評分對應（課程 rubric）

| 評分項 | 權重 | 預估 | 命中點 |
|-------|:---:|:---:|------|
| HW/SW 功能定義 | 20% | **18-20** | ICD 深度到 Register Config + Driver State Machine + Pin |
| COTS 酬載 | 10% | **9-10** | 主選 + 3 替代 + trade-off 數據化 |

---

## Eval B 評分：PM 產出 BOM 表 + 總預算 + Gantt

### 完整度

| 項目 | 檢查內容 | 結果 |
|------|---------|:----:|
| A. BOM 表 | 12 項元件、含料號/供應商/單價 TWD/數量/小計/報價來源 | ✅ |
| B. 總預算表 | 8 大類 + 18% Contingency、合計 NT$ 13,532,382 | ✅ |
| C. 替代方案 | 2 組（FPGA + Reaction Wheel）× 3 個選項 + trade-off | ✅ |
| D. Mermaid Gantt | 16 條 task、5 個 milestones、Critical Path 標示 | ✅ |
| E. 自檢 | 對照 course-rubric.md 評分項 5 自檢表 | ✅ |

### 加分項

- ✅ 明確寫「性質：**課程紙上專題**，所有報價僅為規劃參考，不執行實際採購」
- ✅ 幣別 + 匯率 + 報價凍結日期（USD/TWD 32.5, 2026-04-23）
- ✅ 提供雙版本預算：含發射 NT$ 13.5M / 不含發射 NT$ 2.8M（學術情境）
- ✅ Critical Path 紅色 crit tag 標示
- ✅ Heritage 數據（Sinclair RW-0.06 > 30 顆 LEO 飛行）作為選型理由

### 預估評分對應

| 評分項 | 權重 | 預估 | 命中點 |
|-------|:---:|:---:|------|
| 時程經費 | 20% | **18-20** | WBS + Gantt + BOM 合計 + Contingency |
| COTS 酬載 | 10% | **9-10** | 每項附報價來源 + trade-off |

---

## Pivot 前後對比（概念）

| 面向 | Pivot 前 | Pivot 後 | 差異 |
|------|---------|----------|------|
| Agent 回答導向 | 真的規劃實體採購、真的預約測試設施 | 紙上 BOM、計畫書式測試方案 | 不再卡在「採購沒下單」的焦慮 |
| 交付物格式 | 分散、各 agent 各自格式 | 統一 6 節模板 | D-019 簡報能直接組裝 |
| COTS 選型深度 | 只提需求規格 | 主選 + 替代 + trade-off + 報價來源 | 直接對應課程評分 10% |
| ICD 深度 | 模糊 | Physical/Protocol/Register/Timing/Sequence 五層 | 直接對應 HW/SW 20% 拿高分 |
| 風險表述 | 「已向 Avnet 下訂」 | 「採購交期風險：40 週（monitor）」 | 符合紙上專題精神 |
| 評分自檢 | 無 | 每 agent 產出都自檢 course-rubric.md | 自動化品質守門 |

---

## 新框架結構總覽

```
cubesat-team/
├── SKILL.md                                  ← Reporting-First 原則 + 12 條升級後原則
├── agents/
│   ├── ceo.md                                ← 25 頁報告 focus + Q&A 彈藥庫
│   ├── pm.md                                 ← 紙上 BOM + Mermaid Gantt + 評分追蹤
│   ├── systems-engineer.md                   ← ICD 五層深度（Physical→Sequence）
│   ├── qa-test.md                            ← 紙上 V&V 計畫書 + 6 節檢查表
│   ├── comm-payload.md                       ← 6 節模板 + AESA + Prometheus
│   ├── aocs.md                               ← 6 節模板（sensor/wheel/torquer）
│   ├── sw-firmware.md                        ← 6 節模板 + FDIR 四層 + 80/20 分流
│   ├── mech-thermal.md                       ← 6 節模板 + 紙上熱分析 + AESA 熱管理
│   ├── professor-challenger.md               ← 保留（Q&A 壓測用）
│   └── ...
├── references/
│   ├── deliverable-template.md               ⭐ 新建：6 節統一模板
│   ├── course-rubric.md                      ⭐ 新增紙上專題得分要點
│   ├── comm-design.md                        ← 0418 蒸餾成果（§13-17）
│   ├── pdf-paths.md                          ← 0418 主戰場
│   └── ...
└── evals/
    ├── REPORT_0418.md                        ← 前次 eval（知識更新）
    └── REPORT_PIVOT_0423.md                  ← 本次 eval（任務本質 pivot）⭐
```

---

## 總結 + 後續建議

### 現況
- 8 個 agent 全部 pivot 完成、2 個 eval 驗證通過
- 新定位：**CubeSat 課程專題報告設計團隊（非實體開發）**
- 統一模板可直接拼裝進 D-019 25 頁簡報與 D-020 50 頁計畫書

### 預期分數影響
- Pre-pivot 預估：73-80 分（詳見 REPORT_0418.md）
- Post-pivot 執行完 Sprint 5：**85-92 分**（穩定進入 A 等）
- 如加上口頭簡報 run-through × 2：**88-93 分**

### 立即可做
1. 把 Eval A 的輸出當作 comm-payload 章節 template，其他子系統照搬
2. 把 Eval B 的 BOM + Gantt 嵌入 D-019 簡報 p.17-22
3. `/challenge` 壓測 Eval A 輸出，看詹老師視角還有哪裡會被電

### 風險與限制
- Eval 只跑 2 個樣本（comm-payload + PM），AOCS/Mech-Thermal/SW-FW 還沒驗證（但模板是統一的，理論上一致）
- 若真的要做 10+ 個 trigger eval 與 assertion scoring，可後續跑 full skill-creator loop
