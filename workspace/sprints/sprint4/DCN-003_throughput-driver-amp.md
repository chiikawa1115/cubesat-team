# DCN-003：設計變更通知 — 資料速率降至 50 kbps + 驅動放大器
**類型：** Design Change Notice
**作者：** SE Agent 陳明哲
**日期：** 2026-05-28
**CEO 批准：** ✅ Rudy Hsieh（口頭核准，2026-05-28）
**影響等級：** Medium（性能降低，但仍符合任務目標）

---

## 變更摘要

| 項目 | 變更前 | 變更後 |
|-----|--------|--------|
| UL/DL 資料速率 | 200 kbps | **50 kbps** |
| Symbol Rate | 200 ksps（QPSK + R=1/2）| **50 ksps** |
| 衛星 TX Driver Amp | 無 | **新增 Mini-Circuits TSS-53LNB+ (G=27 dB)** |
| 衛星 PA 工作點 | 深線性（+16.5 dBm, -16 dB backoff）| **近 P3dBBO（+29.6 dBm, -3 dB backoff）** |
| 最低服務仰角 | 5°（原設計目標）| **45°（Link Budget 更新後）** |
| BOM 增加 | — | +$18.50（Driver Amp + 元件）|

---

## 變更原因

D-003 Link Budget v3 詳細計算後發現：
1. Bent-Pipe 在 500 km S-band 200 kbps 的系統雜訊/路徑損耗，使 Eb/N₀ 在 5° 仰角時為負值
2. 衛星 TX 鏈路 DAC→Mixer(-13.5 dBm) 遠低於 PA P1dB 輸入需求（+13 dBm），PA 效率極低
3. CEO 批准方案 F：降速 + Driver Amp，以最小成本改善雙鏈路裕量

**任務可行性維持：**
- 50 kbps 仍符合 NTN IoT 典型應用（NB-IoT NTN 3GPP Rel-17 定義 ≤ 127 kbps）
- 最低仰角 45° 代表每次過境可服務窗口 ~10-15 分鐘，每天 5-7 次過境，累積服務時間 50-105 分鐘/天

---

## 影響的需求（SRS v2 修訂）

| 需求 ID | 原需求 | 修訂後 |
|--------|--------|--------|
| SYS-003 | 資料速率 ≥ 200 kbps | **≥ 50 kbps（NTN IoT 應用）** |
| SYS-002 | 最低服務仰角 5° | **最低服務仰角 45°** |
| SYS-004 | Link Margin ≥ 3 dB | 維持 ≥ 3 dB（仰角 ≥ 60° 時滿足）|

**Action：** SE 陳明哲於 Sprint 4 W1 更新 SRS v2 → v3（需求修訂版本）

---

## BOM 影響

| 料號 | 描述 | 數量 | 單價 | 小計 |
|-----|------|-----|------|------|
| TSS-53LNB+ | Mini-Circuits Driver Amp, G=27 dB, P1dB=+20 dBm out | 1 | $16.50 | $16.50 |
| 被動元件（匹配網路 × 4）| | 4 | $0.05 | $0.20 |
| 偏置電感 × 2 | | 2 | $0.90 | $1.80 |
| **合計** | | | | **+$18.50** |

**TX 鏈路修訂（Driver Amp 插入位置）：**
```
DAC(-5 dBm) → Mixer (IL 7dB) → BPF(-13.5 dBm)
  → Driver Amp TSS-53LNB+ (G=+27 dB) → +13.5 dBm
  → PA PMA3-43-1W+ (G=+17 dB, P3dBBO 輸入 ~+12.6 dBm)
  → PA 輸出 ~+29.6 dBm（3 dB backoff）
  → Feeder(-0.3 dB) → Antenna(+2 dBi)
  → Satellite EIRP = +31.3 dBm
```

---

*DCN-003 | SE Agent 陳明哲 | 2026-05-28*
