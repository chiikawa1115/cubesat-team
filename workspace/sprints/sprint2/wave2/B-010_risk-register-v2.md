---
deliverable: B-010
sprint: 2
wave: 3
author: PM Agent（詹雅婷）
date: 2026-05-07
status: draft
reference_documents:
  - workspace/sprints/sprint2/wave1/B-005_power-budget-v2.md
  - workspace/sprints/sprint2/wave2/B-001_link-budget-v2.md
  - workspace/sprints/sprint2/wave2/B-006_aocs-trade-study-v1.md
  - workspace/sprints/sprint2/wave2/B-007_obc-fpga-architecture-v1.md
  - workspace/sprints/sprint2/wave2/B-009_bom-v2.md
  - workspace/discussions.json（THR-002 PA 散熱、Wave 2 各 Agent 交付紀錄）
---

# B-010：Risk Register v2（Sprint 2 更新）

## 1. 風險評估矩陣說明

- **可能性（L）**：1=極低, 2=低, 3=中, 4=高, 5=極高
- **衝擊（I）**：1=可忽略, 2=低, 4=中, 8=高, 16=關鍵
- **RPN = L x I**（Risk Priority Number）

RPN 分級：

| RPN 範圍 | 等級 | 處置 |
|:--------:|------|------|
| 1–4 | Low | 接受，定期監控 |
| 5–12 | Medium | 需有緩解策略，每 sprint 追蹤 |
| 13–32 | High | 需主動緩解，每 wave 追蹤 |
| 33–80 | Critical | 需立即行動，blocker 級 |

---

## 2. 風險清單

| ID | 類別 | 描述 | L | I | RPN | 狀態 | 緩解策略 |
|----|------|------|:-:|:-:|:---:|------|---------|
| RISK-001 | 頻率協調 | S-band n236 商業頻段 ITU 協調困難，可能在課程期限內無法完成 | 4 | 8 | **32** | Open | Path A: ITU RR No.4.4 non-interference basis 先行申報 + Path B: NCC 學術實驗執照（詳見 freq-coordination-v1.1）。Sprint 3 需確認 NCC 回覆時程。 |
| RISK-002 | 能源預算 | EOL 能量收支 -0.040 Wh/orbit（微幅赤字），需採取 M1/M2 緩解措施 | 3 | 4 | **12** | Mitigated | M1: 降低 contact duty cycle 至每 2 圈接觸 1 次（EOL 收支轉正 +0.303 Wh）。M2: OBC clock gating 降 standby 至 1.2W（+0.428 Wh）。DCN-001 後 BOL 已翻正 +0.404 Wh，EOL 赤字極小。（B-005 v2 Section 7.3） |
| RISK-003 | OBC 成本 | Xiphos Q7s 單價 ~$25,000，使 OBC 子系統成本高於 Sprint 1 預估（$5,000–$10,000），硬體 BOM 增量超 50% | 3 | 4 | **12** | Open | 替代方案：自研 Zynq-7020 PCB（~$3,000 PCB cost），但 TRL 低、開發週期長（>12 週），不符 8 週課程時程。建議申請教育折扣（Xiphos 10-20% off），可降至 $20,000–$22,500。（B-009 教育折扣章節） |
| RISK-004 | ADCS RW 壽命 | CubeWheel Nano bearing 機械磨耗，3 年任務期間 MTTF 需確認 | 2 | 4 | **8** | Watch | 向 CubeSpace 索取 MTTF 數據，確保 > 3 yr @ 95% 信賴度。若不足，可增備品 RW 或設計 graceful degradation 至 MTQ-only 模式（精度降為 ±8°，Polar zone 受影響但不致任務失敗）。（B-006 Section 3） |
| RISK-005 | PA 散熱 | S-band PA 4W DC input / ~1W RF output / ~3W 熱耗散，Contact Window 期間（4 min）散熱需求集中在小面積 PA 模組 | 2 | 4 | **8** | Open | Wave 3 熱控分析（B-008）需評估：(1) PA 至結構面板導熱路徑（thermal pad + copper spreader），(2) 輻射散熱面積是否足夠，(3) 接觸窗口 4 min 溫升是否 < Tj max 125°C。B-007 已提出 OBC Zynq die 10x10mm 散熱亦需規劃。 |
| RISK-006 | SEU/FPGA 失效 | 500 km SSO 輻射環境，Zynq-7020 configuration SRAM 預估 ~1 SEU/day（CREME96 模型） | 3 | 4 | **12** | Mitigated | TMR（Triple Modular Redundancy）+ Configuration Scrubbing 週期 100 ms，可將 MTBF 從 ~1 day 提升至 >1 year。PS 端 ARM dual-core lockstep 偵錯。FDIR 偵測到 MBU 時自動 reconfigure PL。（B-007 Section SEU 緩減策略） |
| RISK-007 | 質量超標 | 若所有子系統質量取上限值，全星可能超過 4.0 kg（3U 標準上限） | 1 | 8 | **8** | Low | B-006 ADCS 質量 182g（含 RW），B-007 OBC ~200g，結構 ~1.5 kg，太陽能板 ~300g。初估全星 ~2.2 kg，3U 上限 4.0 kg 餘裕 45.5%。除非增加大型元件，否則質量超標風險極低。 |

---

## 3. 高 RPN 風險摘要（RPN >= 20）

### RISK-001：頻率協調（RPN = 32）-- 最高優先

**現狀**：
- S-band n236（2200-2290 MHz）為 3GPP NTN 商業頻段，ITU 協調需經由 NCC → ITU Filing，一般流程 6-18 個月
- 課程僅 8 週（Sprint 1-5），無法在課程內完成 ITU 協調
- 已識別兩條執行路徑，但均依賴外部機構回覆

**Sprint 3 行動項目**：
1. 確認 NCC 學術實驗執照申請時程（目標：CDR 前取得臨時許可）
2. 準備 ITU RR No.4.4 non-interference basis 申報文件
3. 備案：若 NCC 審核延遲，評估改用 ISM band 2.4 GHz（影響 link budget，需重新計算）

---

## 4. Sprint 2 新增 vs Sprint 1

| 項目 | Sprint 1 | Sprint 2 | 變化說明 |
|------|---------|---------|---------|
| RISK-001（頻率協調）| RPN = 96（L=6, I=16）| RPN = 32（L=4, I=8）| 已有具體執行路徑（Path A + Path B），L 降低；重新校正 I 至合理量表範圍 |
| RISK-002（能源預算）| RPN = 48（嚴重赤字）| RPN = 12（Mitigated）| DCN-001 太陽能板升級後 BOL 翻正，EOL 赤字從 -1.56 降至 -0.040 Wh/orbit |
| RISK-003（OBC 成本）| -- | RPN = 12（新增）| Sprint 2 確認 OBC 選用 Xiphos Q7s 後識別 |
| RISK-004（ADCS RW 壽命）| -- | RPN = 8（新增）| Sprint 2 B-006 trade study 選定方案 A 後識別 |
| RISK-005（PA 散熱）| -- | RPN = 8（新增）| Wave 2 B-007 提出 PA 3W 熱耗散 + OBC 4W active 散熱需求 |
| RISK-006（SEU/FPGA 失效）| -- | RPN = 12（新增，已緩解）| B-007 設計即包含 TMR + Scrubbing，識別時已同步緩解 |
| RISK-007（質量超標）| -- | RPN = 8（新增）| 初估餘裕 45.5%，低風險但需持續追蹤 |

**Sprint 1 → Sprint 2 整體趨勢**：

- Sprint 1 最高 RPN = 96（頻率協調），Sprint 2 降至 32 -- **改善 67%**
- Sprint 1 能源預算為 blocker 級風險，Sprint 2 經 DCN-001 後降為 Medium -- **已解除 blocker**
- Sprint 2 新增 5 項風險（RISK-003~007），均為 Medium 或 Low 等級，無新增 Critical 風險

---

## 5. 風險趨勢圖（文字版）

```
RPN
 96 |  X (RISK-001 Sprint 1)
    |
 48 |  X (RISK-002 Sprint 1)
    |
 32 |                           O (RISK-001 Sprint 2)
    |
 12 |                           O (RISK-002, 003, 006 Sprint 2)
    |
  8 |                           O (RISK-004, 005, 007 Sprint 2)
    |
  0 +------+-------------------+---->
      Sprint 1              Sprint 2

  X = Sprint 1 風險點    O = Sprint 2 風險點
  趨勢：整體 RPN 總和從 144 降至 92（-36%）
```

---

## 6. 結論

1. **最高風險仍為 RISK-001 頻率協調**（RPN=32），為唯一 High 等級風險。需在 Sprint 3 確認 NCC 學術執照申請回覆時程。

2. **RISK-002 能源預算已有效緩解**：DCN-001 使 BOL 能量收支翻正，EOL 赤字極小（-0.040 Wh/orbit），搭配 M1（降低 contact duty cycle）即可消除。此風險已從 blocker 降為可管理的 Medium 等級。

3. **Sprint 2 新增風險均在 Medium/Low 範圍**：OBC 成本（RISK-003）可透過教育折扣部分緩解；PA 散熱（RISK-005）待 Wave 3 B-008 熱控分析確認；SEU 防護（RISK-006）已在 B-007 設計中同步處理。

4. **建議 Sprint 3 優先追蹤**：
   - RISK-001：NCC 回覆追蹤
   - RISK-005：B-008 熱控分析結果
   - RISK-003：教育折扣 RFQ 回覆

5. **PDR 審查包（B-003）應涵蓋本 Risk Register 所有 7 項風險**，特別需在 PDR 會議中討論 RISK-001 的 Path A/B 進展。
