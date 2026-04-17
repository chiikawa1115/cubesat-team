---
deliverable: B-011
sprint: 2
wave: 3
author: QA Agent（林宜靜）
date: 2026-05-09
status: draft
---

# B-011：P2P Review Report（Sprint 2，Wave 2 核心文件審查）

## 審查概況

| 交付物 | 作者 | 審查員 | 判定 | Critical Issues | Major Issues |
|--------|------|--------|------|:---------------:|:------------:|
| B-001 Link Budget v2 | Comm Agent（林志遠）| QA Agent（林宜靜）| **Conditional Approve** | 1 | 3 |
| B-006 ADCS Trade Study v1 | AOCS Agent（黃俊誠）| QA Agent（林宜靜）| **Approve** | 0 | 2 |
| B-007 OBC/FPGA Architecture v1 | SW/FW Agent（徐志豪）| QA Agent（林宜靜）| **Approve** | 0 | 2 |

---

## B-001 審查意見（Link Budget v2.0）

### 通過項目

1. **FSPL 公式正確**：使用 `FSPL = 20 log10(4 pi d f / c)` 標準公式，@1995 MHz, 2,126 km 計算得 165.0 dB，公式與數值均正確。
2. **C/N0 計算交叉驗證一致**：逐項加總法得 32.8 dB-Hz，EIRP+G/T 法亦得 32.8 dB-Hz，兩種方法吻合。
3. **End-to-end cascade C/N0 分析**：透明轉發器的 `(C/N0)_total^(-1) = (C/N0)_UL^(-1) + (C/N0)_DL^(-1)` 公式正確，數值計算無誤。
4. **Feeder Link Margin +59.8 dB 合理**：SAT EIRP +36.5 dBm（PA 1W）+ gNB 32.2 dBi 碟形天線 + 路徑距離短（1,000 km），Feeder Link 遠優於 Service Link 是 bent-pipe NTN 的典型特徵，數字合理。
5. **UL Margin +6.8 dB > 3 dB**：滿足最低裕度需求，PASS。
6. **Doppler 計算正確**：v_orbit = 7,612.5 m/s（500 km SSO 典型值），f_d = f x v/c = ±50.6 kHz（UL），計算正確。
7. **TCXO 選型合理**：±0.5~2.0 ppm 滿足 LO 穩定度 < 5 ppm 需求，功耗 < 50 mW，不需 OCXO。
8. **敏感度分析完整**：S1~S8 場景涵蓋 EIRP 退化、G/T 退化、暴雨、仰角降低及複合場景，方法論完整。
9. **天線選型評估**：含 4 個候選方案、評分矩陣，EnduroSat 首選合理（TRL 7-8、尺寸匹配 3U）。

### Critical Issues

**C-001：斜距 d = 2,126 km 作為 10 deg 仰角設計基準，但精確計算得 ~1,676~1,695 km，差異達 25%**

文件自身計算兩種方法均得到 ~1,676~1,695 km（Section 3.1），但以"與 Sprint 1 基線一致"為由沿用 2,126 km。問題在於：

- 2,126 km 對應的仰角約為 **5~6 deg**，不是 10 deg。文件自身 S6 場景計算 5 deg 仰角斜距為 3,040 km，而非 2,126 km，這暗示 2,126 km 實際對應的仰角在 5~10 deg 之間。
- **"保守"的說法有邏輯矛盾**：若真正 10 deg 仰角 FSPL 應低 ~3 dB（因距離短 25%），表示實際 10 deg Margin 應為 ~9.8 dB 而非 6.8 dB。這意味著文件低估了系統真實裕度，雖然保守不會導致設計失敗，但**會誤導敏感度分析**（例如 S8 場景"FAIL"結論可能不成立）。
- **Sprint 1 的 2,126 km 本身就可能是錯誤**，不應以"一致性"為由延續。

**要求**：Comm Agent 必須釐清 d = 2,126 km 對應的真正仰角，或使用正確的 10 deg 仰角斜距（~1,695 km）重新計算。兩個版本的 Link Budget 都應記錄，明確標示哪個是 nominal、哪個是 worst-case。此為 PDR 前必須修正的 Critical Issue。

### Major Issues

**M-001：T_sys = 340 K 的 Friis cascade 計算不嚴謹**

文件承認精確 Friis cascade 給出 T_sys = 235 K（Section 3.4 備註），但以"與 Sprint 1 一致"為由採用 340 K。340 K 比精確值高 45%，相當於 G/T 差 ~1.6 dB。

- 問題不在於保守本身，而在於**兩個數字（235 K vs 340 K）都沒有明確標示哪個是 nominal、哪個是 worst-case**。PDR 審查時教授一定會追問"你的 T_sys 到底是多少？"
- **建議**：PDR 前應明確定義：nominal T_sys = 235 K（精確 Friis），worst-case T_sys = 340 K（含降額），並在 Link Budget 表中標示兩組數字。

**M-002：極化失配損耗 0.5 dB（統計平均）假設依據不足**

文件標記"UE 線極化 vs SAT RHCP，worst case ~3 dB，典型 ~0.5 dB（統計平均）"。但：

- 3 dB 是 LHCP vs RHCP 的 worst case（正交極化），不是線極化 vs 圓極化的 worst case。
- **線極化接收圓極化的固有損耗為 3 dB**（不是 worst case，而是精確值），因為線極化天線只能接收圓極化的一個分量。
- 0.5 dB "統計平均"需要引用具體文獻或模擬結果。若 UE 天線為完美線極化，理論損耗就是 3 dB。0.5 dB 可能假設了 UE 天線有部分圓極化分量或多路徑效應，但文件未說明。
- **影響**：若實際極化損耗為 3 dB，UL Margin 會從 6.8 dB 降至 4.3 dB（仍 PASS），但安全裕度大幅縮減。

**建議**：引用 3GPP TR 38.821 或 ITU-R 相關文件說明 NTN UE 極化損耗的統計模型。若無法找到文獻支持 0.5 dB，建議至少用 1.5 dB 作為設計值（多路徑統計中位數）。

**M-003：敏感度分析缺少 pointing loss 退化場景**

敏感度矩陣 S1~S8 未包含"ADCS 指向精度退化"的場景。例如若 ADCS 指向從 5 deg 退化至 15 deg，pointing loss 從 0.3 dB 增至 ~0.6 dB，margin 減少 0.3 dB。雖影響不大，但作為完整敏感度分析，應包含所有 Link Budget 中的變數。

**建議**：新增 S9 場景（ADCS 指向 15 deg，pointing loss +0.3 dB）。

### Minor Issues

1. Section 3.1 的兩種斜距計算方法排版略混亂，建議整理為"方法一 / 方法二 / 設計選定值"三欄對照表。
2. Section 7.2 Doppler 計算的推導可精簡，中間有重複解釋。
3. Section 8.2 天線廠商表格中 Anywaves 頻段 2025~2110 / 2200~2290 MHz，與需求 1980~2010 MHz 不完全覆蓋 UL 頻段，應明確標示此為不合格原因。

### 判定：Conditional Approve

B-001 Link Budget v2.0 的核心計算正確，UL Margin +6.8 dB 滿足 >= 3 dB 需求。但 **C-001（斜距矛盾）為 Critical Issue，必須在 PDR 前釐清修正**。M-001~M-003 列為 PDR Action Item。

條件：C-001 修正後自動升級為 Approve，不需重新 P2P Review。

---

## B-006 審查意見（ADCS Trade Study v1）

### 通過項目

1. **Trade Study 方法論完整**：評估矩陣含 8 項（指向精度、polar zone、功耗、質量、成本、TRL、壽命風險、體積），方法論嚴謹。
2. **CubeWheel Nano 0.42W 在 Power Budget 0.5W 限值內**：MTQ 0.30W + RW avg 0.12W = 0.42W，margin 16%，驗算正確，通過。
3. **指向精度 ±2°（穩態）有合理依據**：PD controller + 磁力計/IMU 三軸姿態確定，±2° 在 MTQ+RW 系統中為典型可達值（CubeSat 文獻支持）。
4. **Polar dead zone 分析邏輯正確**：|lat| > 80° 地磁場近垂直，MTQ yaw 力矩趨零，需 RW 補償。7.1 min/orbit 的 yaw 失控時間推導合理（SSO 500 km 過極區時間約 7~8 min）。
5. **CubeWheel Nano 選型數據一致**：角動量 0.25 mNms vs polar zone yaw 干擾 0.01~0.05 mNms，餘裕 5~25 倍，足夠。
6. **控制律設計完整**：B-dot 消旋 → PD 穩態 → Polar zone RW assist → Desaturation，模式切換邏輯清晰。
7. **感測器功耗分類正確**：感測器 0.29W 歸入 OBC/Sensor 預算，不計入 ADCS 致動器 0.5W，與 B-005 分類一致。
8. **與 B-001 cross-reading 一致**：確認 pointing loss 0.05 dB（±2° 指向）遠小於 1 dB 預算。

### Critical Issues

無。

### Major Issues

**M-004：±2°（穩態）和 ±3°（polar zone）的數值來源缺乏模擬支持**

文件聲稱穩態 ±2°、polar zone ±3°，但未提供：
- PD 控制器增益（Kp, Kd）的設定值
- 任何模擬/數值分析結果（例如 MATLAB/Simulink 姿態模擬）
- 干擾力矩模型（氣動力矩、重力梯度力矩、太陽輻射壓力矩）的量化值

±2° 在 MTQ+RW 3U CubeSat 中是可達的（文獻有先例），但 B-006 作為 PDR 文件，應至少附上簡易的 pointing error budget（各項干擾力矩 vs 控制力矩餘量），而非僅聲明數字。

**建議**：在 PDR 前補充 pointing error budget 表（各項干擾力矩量化 + 控制力矩餘量分析），或至少引用 1~2 篇 CubeSat ADCS 文獻支持 ±2° 的可達性。

**M-005：RW desaturation 策略缺乏量化分析**

Section 5.3 提到"在非 polar zone 時由 MTQ 對 RW 進行 momentum dumping"，但未分析：
- RW 在 polar zone 累積的角動量有多少（7.1 min x yaw torque = ? mNms）
- 非 polar zone MTQ desaturation 所需時間
- 若連續多圈 RW 角動量累積，是否會在數十圈後飽和

CubeWheel Nano 角動量容量為 0.25 mNms，若每圈 polar zone 累積 0.05 mNms，5 圈就飽和。雖然非 polar zone 有時間 desaturate，但應有量化計算證明不會飽和。

**建議**：補充 RW 角動量 budget（每圈累積 vs 每圈 desaturation 量），確認穩態不飽和。

### Minor Issues

1. Section 6 感測器表格中 HMC5883L 磁力計已停產（Honeywell 已將產線轉給 QST），建議確認替代料號（如 QMC5883L）或標示供應風險。
2. "概估單價 $3,000~$4,000 USD（教育/研究折扣後約 $2,500）"— 研究折扣金額應在 cost estimate 中明確標示為"不確定"，PDR 成本應取 $3,500（中位數，不含折扣）。
3. Section 4 CubeWheel Nano 規格表中"TRL: 7（多個 3U/6U CubeSat 任務飛行驗證）"— 既然有多個飛行驗證，TRL 應為 8 或至少 7-8。建議確認 CubeSpace 官方 TRL 聲明。

### 判定：Approve

B-006 ADCS Trade Study 方法論完整，方案選定合理，功耗與質量在預算內。Major Issues (M-004, M-005) 不影響方案選定結論，但應作為 PDR Action Item 在後續 Sprint 補充量化數據。

---

## B-007 審查意見（OBC/FPGA Architecture v1）

### 通過項目

1. **Zynq-7020 選型合理**：53K LUT 滿足 TMR 後 37,000 LUT（69.5%），ARM Cortex-A9 運行 FreeRTOS，PS/PL 分工明確。
2. **TMR LUT 計算正確**：原始 critical logic 11,500 LUT x 3 = 34,500 LUT（加上 voter 約 0.5%），加上 non-TMR 2,500 LUT，總計 37,000 LUT。69.5% utilization 在 < 80% 設計上限內。各模組 LUT 估算合理（QPSK demod 3,500 LUT 為典型值）。
3. **SEU rate 計算支持 100ms scrubbing 週期**：1.08 upset/day = 每 86,400 秒 1 次 SEU，100ms 週期意味 SEU 影響時間窗極小（最遲 100ms 內修正）。在 4 min contact window 內同時有 2 個 SEU 影響同一 TMR module 的概率 ~10^-7，可忽略。計算方法與數字正確。
4. **OBC active 4.0W 與 B-005 Power Budget v2 一致**：PS 1.5W + PL 2.2W + I/O 0.3W = 4.0W，與 B-005 OBC Active envelope 吻合。各模式功耗拆解合理。
5. **三級 Watchdog + Safe Mode 設計完整**：SW (2s) -> HW (5s) -> EPS (30s) 逐級升級，最終 fallback 為 EPS power cycle，safe mode 功耗 2.4~2.9W，邏輯嚴謹。
6. **Boot sequence 完整**：5 步驟、~5 sec total，含 CRC 校驗 + 備份 image 切換，冗餘設計合理。
7. **NOR Flash 分區規劃合理**：256 Mbit (32 MB) 分配 Golden + Backup FSW/Bitstream + Config + TM Log，空間充裕。
8. **介面實作對照 ICD 完整**：IF-01~IF-09 全部有對應實作方式、驅動端、速率，與 B-002 ICD 一致。
9. **Xiphos Q7s 選型比較**：3 個候選方案比較表完整，排除 Unibap（功耗超標）和 NanoAvionics（Flash 偏小）的理由合理。

### Critical Issues

無。

### Major Issues

**M-006：原始邏輯 11,500 LUT 的估算依據未說明**

各模組 LUT 數字（QPSK Demod 3,500、QPSK Mod 2,500、Doppler NCO 1,500、FSW SM 1,000、AXI Bus 3,000）雖在 CubeSat SDR 文獻中屬合理範圍，但文件未引用任何來源：
- 是否來自 Xilinx IP 估算工具（Vivado resource estimation）？
- 是否參考已有的 SDR 設計（如 GNU Radio on FPGA 或 MATLAB HDL Coder output）？
- AXI Bus Controller 3,000 LUT 特別值得質疑 — Xilinx AXI Interconnect IP 的 LUT 用量高度取決於配置（master/slave 數量、FIFO 深度），3,000 是什麼配置？

**建議**：在 PDR 前至少標註各模組 LUT 估算的來源（IP catalog / 文獻引用 / 合成結果），並對 AXI Bus Controller 說明配置假設。

**M-007：Xiphos Q7s $25,000 成本與替代方案降低成本的可能性**

文件列出 Xiphos Q7s ~$25,000、NanoAvionics ~$18,000、Unibap ~$45,000。Xiphos 選型合理但價格偏高（佔 3U CubeSat 總預算比例大），且排除 NanoAvionics 的唯一理由是"128 Mbit NOR Flash 偏小"。

- 128 Mbit = 16 MB，Golden Bitstream (4.5 MB) + Backup (4.5 MB) + FSW A (2 MB) + FSW B (2 MB) = 13 MB，實際上勉強可放。剩餘 3 MB 可用於 Config/TM。
- 若 NanoAvionics 支持外接 SD 卡（8 GB），TM log 可移至 SD 卡，NOR Flash 僅放 boot-critical images。
- 價差 $7,000 對教育/研究衛星非小數目。

**建議**：在 PDR 中補充 NanoAvionics 的 NOR Flash 分區可行性分析。若 16 MB 確實不夠（例如需要更大 TM log in NOR），則維持 Xiphos；若可行，則標記為 cost reduction opportunity。

### Minor Issues

1. Section 3.2 TMR 功耗影響："TMR 三重化邏輯增加約 2x 動態功耗（第三份 + voter 額外切換）"— 嚴格來說 TMR 增加 ~2x 面積但動態功耗增加取決於 switching activity，2x 是概估，建議標示為 "estimated ~2x"。
2. Section 7.1 功耗表中 "Peak 4.3W, Budget 5.0W" — B-005 Power Budget v2 的 Peak envelope 為 5.0W 的引用應附上具體 section。
3. Config Scrubber "hardened-by-design" 的具體手法（手動佈局、分散式 coding）未展開，PDR 時可能被追問。建議在 Wave 3 SDR 詳細設計中補充。

### 判定：Approve

B-007 OBC/FPGA 架構設計完整，SEU 防護三層架構嚴謹，LUT utilization 與功耗均在預算內。Major Issues (M-006, M-007) 不影響架構選定結論，列為 PDR Action Item。

---

## 整體 Sprint 2 Wave 2 結論

### P2P Gate 判定

| 文件 | 判定 | Gate 通過 |
|------|------|:---------:|
| B-001 Link Budget v2 | Conditional Approve | 通過（附條件：C-001 修正後生效）|
| B-006 ADCS Trade Study v1 | Approve | 通過 |
| B-007 OBC/FPGA Architecture v1 | Approve | 通過 |

### 整體結論

Wave 2 三份核心文件**全部通過 P2P Gate**（B-001 附條件）。文件品質整體良好，計算嚴謹度達到 PDR 水準。主要問題集中在：

1. **B-001 斜距矛盾**（Critical）— 必須在 PDR 前釐清
2. **各文件缺乏模擬/量化支持**（Major）— 可作為 PDR action item，不阻擋 PDR 包製作

**PDR 審查包（B-003）可以繼續製作**，前提是 Comm Agent 在 B-003 完成前修正 B-001 C-001。

### 文件間一致性驗證

| 交叉項目 | B-001 值 | B-006 值 | B-007 值 | 一致性 |
|---------|----------|----------|----------|:------:|
| 天線 HPBW | 70 deg | 引用 70 deg | -- | OK |
| Pointing Loss | 1.0 dB | 指向 ±2° -> 0.05 dB（遠小於 1.0 dB）| -- | OK |
| ADCS 功耗 | -- | 0.42W | B-005 ref 0.5W | OK |
| OBC Active 功耗 | -- | -- | 4.0W = B-005 envelope | OK |
| S-band SPI 10 MHz | B-002 IF-04 | -- | PL 驅動 IF-04 | OK |
| SAT PA 1.0W RF | 30 dBm | -- | -- | OK |

---

## PDR Action Items（來自 Major Issues）

| ID | 文件 | 問題 | 負責人 | 完成期限 |
|----|------|------|--------|---------|
| **C-001** | B-001 | **斜距 d = 2,126 km vs 精確計算 ~1,695 km 矛盾，需釐清真正仰角並修正 Link Budget**（CRITICAL）| Comm Agent（林志遠）| PDR 前（Sprint 3 Wave 1）|
| M-001 | B-001 | T_sys 定義不明確（235K nominal vs 340K worst-case），需在 Link Budget 中明確標示 | Comm Agent（林志遠）| PDR 前 |
| M-002 | B-001 | 極化失配損耗 0.5 dB 需引用文獻支持，或提高至 1.5 dB | Comm Agent（林志遠）| PDR 前 |
| M-003 | B-001 | 敏感度分析補充 ADCS 指向退化場景 | Comm Agent（林志遠）| PDR |
| M-004 | B-006 | 補充 pointing error budget（干擾力矩量化 + 控制力矩餘量）| AOCS Agent（黃俊誠）| PDR |
| M-005 | B-006 | 補充 RW 角動量 budget（每圈累積 vs desaturation 分析）| AOCS Agent（黃俊誠）| PDR |
| M-006 | B-007 | 各模組 LUT 估算來源標註（IP catalog / 文獻 / 合成結果）| SW/FW Agent（徐志豪）| PDR |
| M-007 | B-007 | NanoAvionics OBC NOR Flash 分區可行性分析（cost reduction opportunity）| SW/FW Agent（徐志豪）| PDR |

---

*P2P Review Report generated by QA Agent（林宜靜）— Sprint 2 Wave 3, 2026-05-09*
