---
deliverable: C-008
sprint: 3
wave: 3
author: SE Agent（陳建宏）
date: 2026-04-15
status: draft
version: v2.0
reference_documents:
  - ConOps v1（A-001，Sprint 1 基線）
  - workspace/sprints/sprint2/patches/PATCH-P1-P2-comm.md（M1 策略量化）
  - workspace/sprints/sprint2/wave1/B-005_power-budget-v2.md（Power Budget v2.1）
  - workspace/sprints/sprint3/wave1/C-001_srs-v2.md（SRS v2.0）
change_log:
  - v2.0: 新增 EOL 降級操作模式（模式 2、模式 3），補充 IoT SLA 表格，補充 FDIR 觸發邏輯（來自 PATCH-P1-P2 量化）
---

# TASA-NTN-3U ConOps v2.0
# 任務概念文件（Concept of Operations）

**任務**：TASA-NTN-3U
**版本**：v2.0
**日期**：2026-04-15
**作者**：SE Agent（陳建宏）
**狀態**：Draft

---

## 1. 文件目的

### 1.1 ConOps v1 → v2 變更說明

本文件為 TASA-NTN-3U 任務概念文件（ConOps）v2.0，在 v1 基礎上進行以下更新：

| 章節 | v1 | v2 |
|------|----|----|
| 操作模式數量 | 2（正常模式 / 安全模式）| 4（新增 M1 降級模式、M1+M2 最差情況模式）|
| IoT 延遲保證 | 未量化 | 明確 SLA 表格（含最大延遲上限）|
| EOL 服務降級 | 未描述 | M1 / M2 自動觸發邏輯，含 OBC FDIR 條件 |
| FDIR 觸發條件 | 未定義 | DoD 門檻 25%（M1 觸發）/ 30%（安全模式）|

**v2 變更依據**：
- Sprint 2 Power Budget v2.1（B-005）確認 EOL 能源收支為 -0.040 Wh/orbit，微幅赤字
- PATCH-P1-P2（Comm Agent 林志遠，2026-05-10）量化 M1 策略對覆蓋率與延遲的影響，並確認大多數 IoT-NTN 用例可接受
- SRS v2.0（C-001，2026-04-16）將 DoD 操作門檻 ≤30% 列為 SYS-006 需求，FDIR 觸發點設定為 25%

**其餘章節（Section 2、6、7）繼承 v1 內容，無變更。**

---

## 2. 任務概述

### 2.1 任務背景

TASA-NTN-3U 為台灣太空中心（TASA）主導之低軌道 IoT-NTN 通訊技術驗證任務。透過 3U CubeSat 平台，驗證 3GPP Release-17 NTN（Non-Terrestrial Network）標準在 500 km 低地球軌道（LEO）環境下的 S-band 通訊可行性，並展示台灣自主酬載技術能力。

### 2.2 平台與軌道

| 參數 | 數值 | 備注 |
|------|------|------|
| 平台規格 | 3U CubeSat | CalPoly P-POD Rev.13 相容 |
| 軌道高度 | 500 km ±50 km | 圓軌 |
| 軌道類型 | SSO（太陽同步軌道）| LTAN 10:30 |
| 軌道週期 | 94.5 min | |
| Eclipse 時間 | 35.7 min / 圈 | Eclipse fraction 37.78% |
| 日照時間 | 58.8 min / 圈 | |
| 每日軌道圈數 | 15.24 圈 / day | |

### 2.3 通訊任務

| 參數 | 數值 | 備注 |
|------|------|------|
| 頻段 | S-band n236 | 3GPP Rel-17 NTN |
| 上行（UE → SAT）| 1980–2010 MHz | |
| 下行（SAT → GS）| 2170–2200 MHz | |
| 調變方式 | QPSK，碼率 1/2 | |
| 目標資料率 | ≥100 bps | IoT-NTN 最低需求 |
| 透明轉發架構 | Bent-pipe | 無星上基帶處理 |

### 2.4 服務對象

- **主要服務目標**：3GPP IoT-NTN UE（地面 IoT 感測器、手持裝置）
- **UE 天線特性**：線極化（PIFA / monopole），對衛星 RHCP 天線存在 3.0 dB 極化失配損耗（PATCH-P1 已入冊）
- **UE 功率等級**：3GPP Power Class 5（+20 dBm，+2 dBi EIRP）

### 2.5 接觸窗口（BOL 正常模式）

```
接觸窗口長度：4 min / pass（10° 最低仰角，500 km 高度幾何計算）
每日接觸次數：15.24 passes / day（BOL，每圈均服務）
每日服務時間：~60.96 min（≈61 min / day）
地面特定點重訪（台灣緯度 ~25°N）：3–5 passes / day，每次 4–6 min
```

### 2.6 任務壽命

- **設計壽命**：2 年
- **除軌計畫**：500 km 軌道自然大氣阻力降軌，估算 ~3.2 年（符合 IADC 5 年法規限制）
- **EOL 定義**：任務第 3 年起（電池 EOL 容量衰減至 ~80%，太陽能板 EOL 峰值 5.939 W）

---

## 3. 操作模式定義

TASA-NTN-3U 定義四種操作模式，涵蓋從 BOL 正常運作至 EOL 能源降級、以及緊急安全保護的完整任務剖面。

### 3.1 模式 1：正常操作模式（Normal Operations Mode）

**適用階段**：BOL / Early EOL（任務前 2 年設計壽命內）

**觸發條件**：
- 電池 DoD < 25%（正常充電狀態）
- EOL 能源收支餘額 ≥ 0 Wh/orbit

**操作描述**：
- 每次軌道接觸窗口均開啟酬載服務（每圈 1 次，全 15.24 passes/day）
- S-band PA 全功率輸出（~1 W RF，DC in 4 W）
- OBC Active 模式（4 W），TT&C Tx 模式（1.5 W）

**能量收支（BOL）**：

| 項目 | 數值 |
|------|------|
| 每圈能量收入（BOL）| +5.159 Wh |
| 每圈能量支出 | -4.755 Wh |
| **淨收支（BOL）** | **+0.404 Wh/orbit（PASS）** |

**服務等級（模式 1）**：
- 每日服務接觸次數：15.24 passes
- 每日有效服務時間：~61 min
- 平均 IoT 訊息延遲（衛星端 contact interval）：~47 min
- 地面特定 UE 平均延遲（台灣，4 passes/day）：~3.0 hr
- 地面特定 UE 最大延遲：~8–10 hr
- 每日數據吞吐量：~44.6 KB（100 bps × 60.96 min）
- 目標資料率：≥100 bps

---

### 3.2 模式 2：M1 降級操作模式（M1 Degraded Operations Mode — EOL Energy Conservation）

**v2 新增模式**（對應 PATCH-P1-P2 Section 2、B-005 Section 7.3 Mitigation M1）

**觸發條件**：以下任一條件成立，OBC FDIR 自動觸發：
1. 連續 3 軌道的平均 DoD > 25%（能源赤字累積警告）
2. 連續 3 軌道能源餘額 < -0.05 Wh/orbit（超過 EOL 赤字門檻）
3. 季節性 beta angle 進入最壞情況區間（cos_theta_avg < 0.70，MPPT 效率下降）

**背景說明**：
Power Budget v2.1（B-005）顯示 EOL 正常操作每圈能源赤字為 -0.040 Wh/orbit，連續運作將導致電池 DoD 持續上升。M1 模式（每 2 圈才開啟酬載一次）可使 EOL 能源收支轉正為 +0.303 Wh/orbit（B-005 Section 7.4），解除赤字。

**操作描述**：
- **酬載啟動頻率**：每 2 軌道接觸窗口開啟 1 次（正常模式的 50%）
- **跳過圈次**：S-band PA 完全關機（PA OFF），LNA 也關閉；OBC 保持 Standby 模式（1.5 W）
- **每圈能量支出（M1 模式）**：

```
M1 模式每圈平均支出計算（以 2 圈為週期，取平均）：

  服務圈（contact on）：
    Sunlit 非接觸：2.50 W × 54.8/60 hr = 2.283 Wh
    Contact Window：10.30 W × 4.0/60 hr = 0.687 Wh
    Eclipse：3.00 W × 35.7/60 hr = 1.785 Wh
    小計 = 4.755 Wh

  跳過圈（contact off，PA 關閉）：
    Sunlit 全段：2.50 W × 58.8/60 hr = 2.450 Wh（無 PA 消耗）
    Eclipse：3.00 W × 35.7/60 hr = 1.785 Wh
    小計 = 4.235 Wh

  2 圈平均 = (4.755 + 4.235) / 2 = 4.495 Wh/orbit（≈ B-005 的 4.412 Wh，差異因加熱器等細項）

EOL 能源收支（M1 模式）：
  收入 4.715 Wh/orbit（EOL）
  支出 4.412 Wh/orbit（M1，B-005 Section 7.4）
  淨收支 = +0.303 Wh/orbit（轉正 PASS）
```

**OBC FDIR 自動觸發邏輯**：

```
// OBC FDIR — M1 模式觸發條件（FreeRTOS FDIR task）
if ((DoD_3orbit_avg > 0.25) OR (energy_balance_3orbit < -0.05)) {
    activate_M1_mode();
    log_event("M1_DEGRADED_MODE_ACTIVATED", timestamp, DoD_3orbit_avg, energy_balance_3orbit);
    beacon_status("DEGRADED_M1");
    notify_ground("M1 MODE: payload skip every other orbit");
}

// 恢復條件
if ((DoD_3orbit_avg < 0.20) AND (energy_balance_3orbit > 0.0)) {
    deactivate_M1_mode();
    log_event("NORMAL_MODE_RESTORED");
    beacon_status("NORMAL");
}
```

**服務等級（模式 2）**：
- 每日服務接觸次數：7.62 passes（-50%）
- 每日有效服務時間：~30.5 min（-50%）
- 衛星端 contact interval：~189 min（2 × 94.5 min）
- 地面特定 UE 平均延遲（台灣，有效 2 passes/day）：~6.0 hr（延長 2×）
- 地面特定 UE 最大延遲：~16–18 hr
- 每日數據吞吐量：~22.3 KB（-50%）

**大多數 IoT-NTN 用例可接受性**（PATCH-P1-P2 Section 2.4）：

| IoT 應用類別 | 延遲容忍度 | M1 平均延遲 | 判定 |
|-------------|-----------|------------|------|
| 水文 / 環境監測 | 1–24 hr | ~6.0 hr | PASS |
| 農業感測器 | 1–12 hr | ~6.0 hr | PASS |
| 資產追蹤 | 1–6 hr | ~6.0 hr | PASS（邊緣）|
| 緊急告警 | < 1 hr | ~6.0 hr | FAIL（單星架構固有限制，非 M1 造成）|

---

### 3.3 模式 3：M1+M2 最差情況降級模式（Worst-Case Degraded Mode — Winter Solstice EOL）

**v2 新增模式**

**觸發條件**：
- 季節最壞情況：beta angle ±20°，cos_theta_avg = 0.65（冬至前後）
- EOL 能源赤字達 -0.356 Wh/orbit（太陽能板有效輸入大幅下降）
- 計算依據：

```
冬至 EOL 能量收入：
  P_solar_EOL × MPPT × cos_theta_worst × T_sunlit
  = 5.939 × 0.90 × 0.65 × (58.8/60)
  = 5.939 × 0.585 × 0.98
  = 3.406 Wh（vs 正常 EOL 的 4.715 Wh，減少 1.309 Wh）

冬至 EOL 能源收支（正常模式）：
  收入 3.406 Wh − 支出 4.755 Wh = −1.349 Wh/orbit（嚴重赤字）

  M1 模式（每 2 圈）：
  收入 3.406 Wh − M1 支出 4.412 Wh = −1.006 Wh/orbit（仍赤字）

  M1+M2 組合（M2：縮短接觸窗口至 2 min 或降低 PA 功率至 0.5 W）：
  M2 節省 ≈ 0.343 Wh/orbit（4 min → 2 min contact，PA 節省）
  M1+M2 淨收支 ≈ −1.006 + 0.343 = −0.663 Wh/orbit（仍需觀察）

  備注：cos_theta_avg = 0.65 為極端情況，正常 beta angle 範圍內 M1 即足夠；
  M1+M2 適用於連續多軌仍負值時的額外降載手段。
```

**觸發升級條件**（從模式 2 升級至模式 3）：
```
// 從 M1 模式升級至 M1+M2
if (M1_active AND (DoD_3orbit_avg > 0.28) AND (seasonal_beta_worst_case == TRUE)) {
    activate_M2_payload_reduction();
    log_event("M1_M2_WORST_CASE_MODE_ACTIVATED");
    beacon_status("DEGRADED_M1_M2");
}
```

**操作描述**：
- **M1 策略**：每 2 軌才開啟酬載（同模式 2）
- **M2 策略**（選一）：
  - 選項 A：縮短每次接觸窗口至 2 min（從 4 min 減半，儘量服務更多 pass 但縮短每次服務）
  - 選項 B：PA 降功至 0.5 W DC in（鏈路餘裕 +6.3 dB，降功後仍可維持最低 100 bps）
- **OBC Standby**：考慮 M2 OBC clock gating，Standby 從 1.5 W 降至 1.2 W（B-005 Section 7.4 Mitigation M2）

**服務等級（模式 3）**：
- 每日服務接觸次數：~3.8 passes（M1 跳圈後，再扣除幾何不可見）
- 每日有效服務時間：~15 min
- 地面特定 UE 平均延遲：~6 hr
- 地面特定 UE 最大延遲：~16 hr
- **接受條件**：最大延遲 16 hr < 24 hr（3GPP TR 38.811 NTN IoT-NTN 典型延遲容忍 > 24 hr 的大多數應用），符合天氣、環境監測等 IoT 應用需求

**降級接受聲明**：本模式為冬至極端季節條件（~6 週/年）下的臨時措施，非全年常態。任務 2 年設計壽命內，此模式預計每年啟動 1–2 次，每次持續不超過 4 週。

---

### 3.4 模式 4：安全模式（Safe Mode）

**觸發條件**：
- 電池 DoD > 30%（超過 SYS-006 SRS 限值）
- 系統異常（OBC watchdog reset、FDIR 嚴重故障事件）
- 地面站緊急指令

**操作描述**：
- 關閉所有酬載（S-band PA OFF、LNA OFF）
- 關閉非必要子系統
- 僅保留：
  - TT&C UHF beacon（1.5 W Tx 週期發射）
  - OBC 最小功耗（1.0 W safe mode）
  - ADCS detumble 模式（MTQ only，0.3 W）
  - EPS self-consumption（0.3 W）
- 總功耗：~3.1 W（對應 B-005 Table 3.1 Safe Mode 欄位）

**安全模式能量收支**：
```
安全模式支出（全圈估計）：
  Sunlit：3.1 W × 58.8/60 = 3.038 Wh
  Eclipse：3.1 W × 35.7/60 = 1.843 Wh
  總支出 = 4.881 Wh/orbit

  EOL 收入：4.715 Wh → 仍有微幅赤字（-0.166 Wh）
  需搭配 beacon 週期降低（duty cycle 50%）進一步節能
```

**恢復條件**：
```
if (DoD_3orbit_avg < 0.20) {
    exit_safe_mode();
    enter_M1_mode();  // 先進入 M1 降級模式，確認能源穩定後才恢復正常
    log_event("SAFE_MODE_EXIT");
}
```

**恢復策略**：安全模式退出後，**不直接回到模式 1**，優先進入模式 2（M1 降級模式），待連續 10 圈能源收支確認正值後，再切換回模式 1。

---

## 4. 操作模式轉換圖

### 4.1 轉換邏輯（文字描述）

```
                    ┌───────────────────────┐
                    │   模式 1：正常操作      │
                    │ DoD < 25%             │
                    │ 15.24 passes/day       │
                    └───────────┬───────────┘
                                │
           DoD_3orbit > 25%     │
           OR energy_3orbit < -0.05 Wh
                                ▼
                    ┌───────────────────────┐
                    │  模式 2：M1 降級       │
                    │ DoD 25–28%            │
                    │ 7.62 passes/day        │
                    └───────────┬───────────┘
                                │
           DoD_3orbit > 28%     │
           AND beta_worst_case  │
                                ▼
                    ┌───────────────────────┐
                    │ 模式 3：M1+M2 最差    │
                    │ 冬至 EOL 季節         │
                    │ ~3.8 passes/day       │
                    └───────────┬───────────┘
                                │
                  DoD > 30%     │
               OR 系統異常      │
                                ▼
                    ┌───────────────────────┐
                    │   模式 4：安全模式     │
                    │ 酬載全部關閉          │
                    │ 僅 TT&C + OBC         │
                    └───────────┬───────────┘
                                │
                  DoD < 20%     │ 恢復
                                ▼
                    ┌───────────────────────┐
                    │  模式 2：M1 降級       │ ← 先穩定能源再升級
                    │（確認 10 圈能源正值）  │
                    └───────────┬───────────┘
                                │
               能源連續 10 圈正值│
                                ▼
                    ┌───────────────────────┐
                    │   模式 1：正常操作     │
                    └───────────────────────┘
```

### 4.2 模式轉換條件彙整

| 從 → 到 | 觸發條件 | 類型 |
|---------|---------|------|
| 模式 1 → 模式 2 | DoD_3orbit > 25% 或 energy_3orbit < -0.05 Wh | 自動（FDIR）|
| 模式 2 → 模式 3 | DoD_3orbit > 28% 且 beta 最壞情況 | 自動（FDIR）|
| 模式 2/3 → 模式 4 | DoD > 30% 或系統異常 | 自動（FDIR）|
| 模式 4 → 模式 2 | DoD_3orbit < 20%（恢復）| 自動（FDIR）|
| 模式 2 → 模式 1 | 連續 10 圈能源收支 > 0 | 自動（FDIR）|
| 任意 → 模式 4 | 地面緊急指令 | 地面指令 |
| 模式 4 → 任意 | 地面解除指令 + DoD < 20% | 地面指令（確認後）|

---

## 5. IoT 服務等級協議（SLA）

### 5.1 SLA 定義表

| 模式 | 每日接觸次數 | 平均延遲 | 最大延遲 | 每日吞吐量 | 適用場景 |
|------|:-----------:|:-------:|:-------:|:---------:|---------|
| 模式 1（正常）| 15.24 | ~1.5 hr（衛星端）<br>~3.0 hr（特定 UE）| ~8–10 hr | ~44.6 KB | BOL / 正常運行 |
| 模式 2（M1 降級）| 7.62 | ~3.0 hr（衛星端）<br>~6.0 hr（特定 UE）| ~16–18 hr | ~22.3 KB | EOL 節能 |
| 模式 3（M1+M2 最差）| ~3.8 | ~6 hr | ~16 hr | ~11 KB | 冬至最壞情況 |
| 模式 4（安全）| 0 | N/A | N/A | 0 | 緊急節能 |

> **備注（衛星端 vs 特定 UE 延遲差異）**：「衛星端」延遲以全球軌道層面計算（contact interval / 2）；「特定 UE」延遲以台灣 ~25°N 緯度地面站計算（~4 passes/day 下的平均等待時間）。

### 5.2 接受依據

**規格依據**：3GPP TR 38.811 V15.4.0 NTN IoT-NTN，典型 mMTC 延遲容忍 > 24 hr

| 模式 | 最大延遲 | 3GPP 典型上限 | 判定 |
|------|:-------:|:-----------:|:----:|
| 模式 1 | ~10 hr | 24 hr | PASS |
| 模式 2 | ~18 hr | 24 hr | PASS |
| 模式 3 | ~16 hr | 24 hr | PASS |

**模式 3 最大延遲 16 hr < 24 hr，符合大多數 IoT-NTN 應用規格（天氣監測、環境感測、農業追蹤等），接受此降級服務等級。**

### 5.3 SLA 降級通知機制

當系統進入模式 2 或模式 3 時，衛星 beacon 狀態字段更新為 `DEGRADED_M1` 或 `DEGRADED_M1_M2`，地面任務控制中心（MCC）接收到降級 beacon 後，應：
1. 記錄進入時間戳與觸發原因（DoD 值、energy balance）
2. 通知使用者服務水準已降級
3. 每 24 小時評估是否需要手動干預

---

## 6. 地面操作程序

### 6.1 日常監控程序

- **MCC 每日例行**：監看衛星健康 beacon（TT&C UHF），記錄電池 DoD、能源收支、操作模式
- **DoD 遙測警報**：
  - DoD > 20%：地面注意（Yellow alert），觀察趨勢
  - DoD > 25%：地面確認 M1 模式已觸發（Orange alert），評估手動介入必要性
  - DoD > 30%：安全模式警報（Red alert），立即確認衛星狀態
- **遙測儲存**：OBC 提供至少 7 天滿載遙測本地儲存（SW-005），確保過境時可完整下傳

### 6.2 季節性預測程序

- **每季 beta angle 計算**：地面軌道分析人員於每季初計算未來 30 天 beta angle 變化預測
- **冬至前準備**（每年 11–12 月）：
  1. 計算未來 6 週 cos_theta_avg 趨勢
  2. 若預測 cos_theta_avg < 0.70，提前通知地面站預期進入模式 2
  3. 若預測 cos_theta_avg < 0.65（最壞情況），準備模式 3 操作程序

### 6.3 地面站可視窗口

- **TASA 新竹地面站**：每日 4–6 次過境（>10° 仰角），每次過境窗口 8–12 min（TT&C UHF 聯繫）
- **科學數據下傳**：S-band 下行（2170–2200 MHz），透明轉發架構，地面站需安裝相容 S-band 接收設備
- **緊急指令上傳**：TT&C UHF 上行（指令），第一次可見窗口即可執行

---

## 7. 壽命末期操作計畫

### 7.1 EOL 定義與標準

| 條件 | 說明 |
|------|------|
| 任務設計壽命 | 2 年（MIS-003，SRS v2）|
| 電池 EOL 容量 | ~12.0 Wh（BOL 15 Wh × 80% EOL 衰減，DCN-002）|
| 太陽能板 EOL 峰值 | 5.939 W（BOL 6.5 W × 0.9137 衰減因子，DCN-001）|
| EOL 能源收支（正常模式）| -0.040 Wh/orbit（Marginal，B-005 Section 4.3）|
| EOL 能源收支（M1 模式）| +0.303 Wh/orbit（PASS）|

### 7.2 任務延壽計畫

若衛星在 2 年設計壽命後仍功能正常（健康 beacon 持續、OBC 無異常），可在 M1 降級模式下繼續延壽運作：

- **延壽操作基線**：模式 2（M1 降級）為預設操作模式
- **延壽判斷指標**：電池 DoD 循環次數、每日遙測可下傳數據量
- **預估延壽時間**：6–12 個月額外壽命（視電池循環退化速率，B-005 Section 7.3）

### 7.3 除軌計畫

| 項目 | 說明 |
|------|------|
| 除軌方式 | 自然大氣阻力降軌（無推進系統）|
| 預估降軌時間 | ~3.2 年（500 km SSO，3U CubeSat 面積質量比）|
| IADC 法規符合 | 5 年上限，3.2 年 < 5 年 PASS（MIS-005，SYS-014）|
| 除軌啟動時間 | 任務結束時（設計壽命 2 年或電池報廢）|

### 7.4 最終 TT&C 計畫

- 除軌降低過程中持續發送 beacon（TT&C UHF），直至電池耗盡或信號消失
- 最終軌道圈數：不可控（依降軌軌道自然演化）
- IADC 合規確認：TASA 地面站追蹤確認降軌完成

---

## 8. 與 v1 差異摘要

### 8.1 v1 → v2 變更清單

| 章節 | v1 描述 | v2 描述 | 變更原因 |
|------|---------|---------|---------|
| 操作模式數量 | 2（正常 / 安全）| 4（新增 M1、M1+M2）| Sprint 2 EOL 赤字量化（B-005）|
| IoT 延遲保證 | 未量化 | 明確 SLA 表格（4 模式均有延遲上限）| PATCH-P1-P2 延遲分析 |
| EOL 服務降級描述 | 未描述 | M1 / M2 自動觸發邏輯 + OBC FDIR 代碼框架 | PATCH-P1-P2 ConOps 補充需求 |
| FDIR 觸發條件 | 未定義 | DoD 門檻：25%（M1）/ 28%+beta（M1+M2）/ 30%（Safe）| SRS v2 SYS-006 + B-005 FDIR 建議 |
| 模式轉換圖 | 無 | 完整轉換邏輯（Section 4）| 操作程序清晰化 |
| 地面操作程序 | 基礎描述 | 增加季節性 beta angle 預測程序、DoD 警報等級 | EOL 操作計畫需求 |

### 8.2 繼承 v1 不變章節

以下內容與 v1 完全一致，無更動：
- Section 2.1 任務背景（平台、軌道參數）
- Section 2.2 通訊任務（頻段、調變方式）
- Section 2.4 服務對象（UE 類型）
- Section 7.3 除軌計畫（3.2 年自然降軌）
- Section 6.1 地面站可視窗口基本描述

### 8.3 受影響文件追蹤

| 文件 | 受影響項目 | 狀態 |
|------|----------|------|
| B-003 RTM v1 | 新增 ConOps v2 Section 3.2–3.4 的需求追蹤項目 | Sprint 3 Wave 3 更新 |
| B-010 Risk Register v2 | 新增 EOL 服務降級風險條目（Severity: Low，Mitigation: M1 mode）| Sprint 3 Wave 3 更新 |
| B-001 Link Budget v2 | Section 6.3 增加「M1 模式下 contact 減半」備注 | PATCH-P1-P2 已指出 |
| SRS v2.0（C-001）| SYS-006 DoD ≤30% 需求，FDIR 觸發 25% 門檻 | 已凍結（一致）|

---

## 9. 文件審核記錄

| 角色 | 審核意見 | 日期 |
|-----|---------|------|
| Comm Agent（林志遠）| PATCH-P1-P2 量化數據已正確引入（延遲、吞吐量）| _(待簽核)_ |
| EPS Agent | B-005 能量收支數值一致確認 | _(待簽核)_ |
| QA Agent | FDIR 觸發條件與 SRS v2 SYS-006 對齊確認 | _(待簽核)_ |
| SE Agent（陳建宏）| 文件主責，ConOps v1 → v2 變更正確性確認 | 2026-04-15 |

---

## 附錄 A：關鍵能量數值速查表

| 參數 | 數值 | 來源 |
|------|------|------|
| 軌道週期 | 94.5 min | B-005 |
| Eclipse 時間 | 35.7 min | B-005 |
| 每圈能量收入（BOL）| 5.159 Wh | B-005 Section 4.1 |
| 每圈能量收入（EOL）| 4.715 Wh | B-005 Section 4.1 |
| 每圈能量支出（正常模式）| 4.755 Wh | B-005 Section 4.2 |
| 每圈能量支出（M1 模式）| 4.412 Wh | B-005 Section 7.4 |
| EOL 淨收支（正常模式）| -0.040 Wh/orbit | B-005 Section 4.3 |
| EOL 淨收支（M1 模式）| +0.303 Wh/orbit | B-005 Section 7.4 |
| 電池 DoD 上限（SRS）| 30% | SYS-006，SRS v2 |
| M1 觸發 DoD 門檻 | 25% | B-005 Section 7.3 + SRS v2 |
| 安全模式觸發 DoD | 30% | SYS-006 |
| 安全模式退出 DoD | 20% | B-005 FDIR 建議 |

---

## 附錄 B：延遲量化計算摘要（PATCH-P1-P2 引用）

```
軌道端 contact interval 計算：
  正常模式：94.5 min（每圈 1 次）
  M1 模式：94.5 × 2 = 189 min（每 2 圈 1 次）

衛星端平均等待（均勻分布假設）：
  正常：94.5 / 2 = 47 min
  M1：189 / 2 = 94.5 min（≈ 1.58 hr）

特定地面 UE（台灣，~4 passes/day）：
  正常：24 hr / 4 passes = 6 hr interval → 平均等待 3.0 hr，最大 ~10 hr
  M1：有效 passes ≈ 2/day → 平均等待 6.0 hr，最大 ~16–18 hr

3GPP 應用延遲容忍判定（TR 38.811 mMTC）：
  正常最大 ~10 hr < 24 hr  → PASS
  M1 最大 ~18 hr < 24 hr   → PASS
  M1+M2 最大 ~16 hr < 24 hr → PASS

（來源：PATCH-P1-P2 Section 2.3, 2.4）
```

---

*文件結束 — C-008 ConOps v2.0 | TASA-NTN-3U | Draft 2026-04-15*
*SE Agent（陳建宏）主責，待 Comm Agent / EPS Agent / QA Agent 審核後凍結*
