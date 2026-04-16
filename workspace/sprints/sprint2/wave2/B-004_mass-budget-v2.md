# B-004：Mass Budget v2（3U，目標 ≤4.0 kg）

**文件版本**：v2.1
**負責人**：吳建宇（Mech/Thermal Agent）
**日期**：2026-05-07
**Cross-reading 來源**：B-005 Power Budget v2、B-006 AOCS Trade Study、B-007 OBC Architecture、B-001 Link Budget v2

---

## 元件質量清單

| 子系統 | 元件 | 質量 (g) | 備注 |
|--------|------|----------|------|
| 結構框架 | ISIS 3U Aluminium Frame (Al 6061-T6) | 350 | 不含面板，100×100×340 mm |
| 太陽能板 | 展開式 3U Solar Panels ×2 | 200 | 含展開機構 hinge，4 panel，6.5W BOL（DCN-001） |
| EPS | GomSpace P31u + Li-ion 15 Wh | 500 | 含連接器 harness；DCN-002 電池升級 +250g |
| OBC | Zynq-7020 class（Xiphos Q7s） | 150 | 含 PCB stack，Wave 2 B-007 確認選型 |
| ADCS | MTQ×3 + CubeWheel Nano + 感測器 | 232 | 含 mounting，Wave 2 B-006 確認選型 |
| S-band 酬載 | RF chain PCB（LNA+BPF+Mixer+PA） | 100 | 含 shield |
| S-band 天線 | EnduroSat S-band Patch Array | 120 | 含 connector |
| TT&C radio | GomSpace AX100 UHF radio | 200 | |
| TT&C 天線 | ISIS UHF 折疊偶極天線 | 100 | 含展開機構 |
| 熱控 | 加熱器 ×2 + MLI 薄膜 + 熱傳導墊 | 80 | 估值，見 B-008 熱控分析 |
| 線材/連接器 harness | 衛星內部接線 | 150 | 約佔乾重 10% |
| 雜項/緊固件 | 螺絲、墊片、misc | 50 | |
| **合計** | | **2,232 g** | 未含 contingency |
| **10% contingency** | | **223 g** | 標準設計餘裕 |
| **總質量（含 contingency）** | | **2,455 g** | |
| **與上限比較** | | **≤4,000 g（限值）** | Margin: 1,545 g（38.6%） |

---

## 質量分佈圖

```
結構框架     ████████████████████  350g (15.7%)
EPS          ████████████████████████████  500g (22.4%)
ADCS         █████████████        232g (11.7%)
太陽能板     ███████████          200g (10.1%)
TT&C radio   ███████████          200g (10.1%)
OBC          ████████             150g  (7.6%)
Harness      ████████             150g  (7.6%)
S-band 天線  ██████               120g  (6.1%)
S-band 酬載  █████                100g  (5.0%)
TT&C 天線    █████                100g  (5.0%)
熱控         ████                  80g  (4.0%)
雜項         ██                    50g  (2.5%)
```

---

## 結論

1. **質量餘裕充足**：全星總質量（含 10% contingency）為 2,455g，距離 4,000g 限值尚有 1,545g（38.6%）餘裕。DCN-002 電池升級後餘裕仍充足，符合 3U CubeSat 發射需求。

2. **Top-3 最重元件及可優化方向**：
   - **結構框架（350g）**：目前採用標準 ISIS 3U 框架，若需減重可考慮碳纖維複合材料（CFRP）骨架，預估可減至 ~250g，但成本增加約 3 倍。以目前餘裕而言不需要。
   - **EPS（500g）**：DCN-002 核准後電池升級至 15 Wh（+250g），質量已調整至 500g。後續如需減重，可評估降至 12 Wh 方案，但需重新驗證 Eclipse 能量平衡（參考 B-005）。
   - **ADCS（232g）**：CubeWheel Nano 是此等級中最輕的反應輪方案，MTQ 亦為標準元件，優化空間有限。

3. **波 2 Cross-reading 一致性確認**：
   - ADCS 232g 與 B-006 Trade Study 結果一致
   - OBC 150g 與 B-007 Xiphos Q7s 規格一致
   - TT&C 300g（radio + antenna）與 B-001 Link Budget 選用的 GomSpace AX100 + ISIS UHF 一致

---

## 設計變更記錄（DCN Log）

| DCN 編號 | 變更內容 | 質量影響 | 核准日期 | 核准人 |
|----------|----------|----------|----------|--------|
| DCN-001 | 太陽能板升級展開式 4 panel，6.5W BOL | +50g（估） | 2026-04-01 | PM |
| DCN-002 | 電池容量升級 10→15 Wh，EPS 質量 250g→500g | +250g | 2026-04-15 | CEO |
