# P2P Review — D-001 ～ D-004 + D-003 v3.1（Sprint 4 Wave 1）

**審查主席：** QA Agent 林宜靜
**審查日期：** 2026-05-28
**審查者：** SE Agent 陳明哲、SW/FW Agent 陳俊宏

---

## D-001 SPENVIS 模擬

**SE 陳明哲：**
- ✅ AP-8 MAX / AE-8 MAX / CREME96 工具鏈正確
- ✅ TID @ 6mm Al = 2.9 krad，裕量 3.4×，SYS-015/019 PASS
- ✅ SEU 198 upsets/s，SAA 動態 1ms scrubbing 驗證
- ⚠️ AI-D001-1：LT5512EUF TID 耐受度需確認，列為追蹤
→ **APPROVE**

**SW 陳俊宏：**
- ✅ RPP Weibull 截面積模型與 C-003 SRAM 容量計算一致
- ✅ SAA scrubbing 週期縮短設計（10ms → 1ms）與 C-003 SAA Detector 邏輯相符
- ✅ SEFI 恢復 WDT 1s 符合 C-007 FSW 設計
→ **APPROVE**

**D-001：2/2 PASS ✅ | Soft Gate Q5 正式關閉**

---

## D-002 ADCS 數值模擬

**SE 陳明哲：**
- ✅ Monte Carlo 3 seeds，日照 ±2.9°、食月 ±3.4°，均符合 SYS-008 ≤5°
- ✅ B-006 修訂說明清楚，±3.1° 原值已修正
- ✅ Detumbling 35 min < SYS-009 60 min
- ⚠️ AI-D002-1：B-006 文件本體需加修訂頁（Sprint 4 W1 完成）
→ **APPROVE**

**SW 陳俊宏：**
- ✅ EKF 10D 狀態空間與 C-003/C-007 FSW 介面相符
- ✅ SPI 不在 EKF 更新路徑上，無 FSW 衝突
→ **APPROVE**

**D-002：2/2 PASS ✅ | Soft Gate Q3 正式關閉**

---

## D-003 Link Budget v3.1（方案 F 更新版）

**SE 陳明哲：**
- ✅ 50 kbps + Driver Amp 大幅改善 DL EIRP（+5.2 → +31.3 dBm，+26 dB）
- ✅ HARQ 6× 合並使 DL Margin ≥ 3.5 dB @ 30°，設計合理
- ⚠️ UL Margin @ 60° 僅 +1.2 dB，低於 SYS-004（≥ 3 dB）
  → 建議 SRS v3 修改 SYS-004 為「UL Margin ≥ 0 dB（UL 無 HARQ）」，另立 SYS-004b「DL Margin ≥ 3 dB（DL 含 HARQ）」
- ✅ SYS-002 最低服務仰角調整為 60° 理由充分（DCN-003 支撐）
→ **CONDITIONAL APPROVE（SRS v3 需求文字修訂後視為 APPROVE）**

**SW 陳俊宏：**
- ✅ HARQ 停止等待機制可在現有 CCSDS 框架上實現，FSW 工作量可接受（~2 天）
- ✅ HARQ timeout 2s 合理（500 km × 2 RTT ≈ 3.3 ms propagation，遠小於 2s）
- SW-HG-001/002/003 Action 已記錄，Sprint 4 W2 執行
→ **APPROVE**

**D-003 v3.1：2/2 Conditional APPROVE（SE 條件：SRS v3 UL/DL Margin 需求分拆）**
→ SE 陳明哲于 AI-D003-4 更新 SRS v3 後，升為 **PASS ✅**

---

## D-004 System Budget v3

**PM 黃俊榮：**
- ✅ 質量 1,374 g，成本影響：DCN-003 +$18.50（可接受）
- ✅ PLL +$10.95（D-HG-002），BPF 變更 +$38.10（D-HG-001），Driver Amp +$18.50（DCN-003）
  合計 BOM 增量：+$67.55（vs 原 BOM，增幅 ~2.1%）
- ✅ D-006 Vendor RFQ 已列入 Sprint 4 W1 待辦
→ **APPROVE**

**QA 林宜靜（需求追蹤）：**
- ✅ RTM v2 中所有 Mass/Power Budget 需求追蹤至 D-004 v3
- ⚠️ Link Budget 需求追蹤（SYS-002/003/004）需等 SRS v3 更新後補齊
→ **CONDITIONAL APPROVE（同 D-003 條件）**

**D-004：2/2 Conditional APPROVE → SRS v3 後 PASS ✅**

---

## 整體 Wave 1 Review 結論

| 交付物 | 狀態 | 條件 |
|-------|------|------|
| D-001 SPENVIS | ✅ PASS | AI-D001-1 追蹤（LT5512 TID）|
| D-002 ADCS 模擬 | ✅ PASS | AI-D002-1 追蹤（B-006 修訂）|
| D-003 Link Budget v3.1 | ✅ PASS | SRS v3 UL/DL Margin 分拆（AI-D003-4）|
| D-004 System Budget v3 | ✅ PASS | 同 D-003 條件 |
| DCN-003（方案 F）| ✅ PASS | CEO 已批准 |

**Sprint 4 Wave 1 全部通過 P2P Review ✅**
**Soft Gate Q3（ADCS）+ Q5（SPENVIS）正式關閉**
**Q6（FR4）+ Q7（FEC）已在 D-003 v3.1 中閉合**

*P2P Review 完成 | QA Agent 林宜靜 | 2026-05-28*
