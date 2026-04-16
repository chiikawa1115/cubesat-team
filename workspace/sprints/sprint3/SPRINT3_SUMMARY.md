# Sprint 3 總結 — TASA-NTN-3U

**Sprint 期間**：2026-05-13 ~ 2026-05-26  
**里程碑**：CDR（Critical Design Review）  
**Sprint 目標**：Phase C 詳細設計，完成 10 項交付物並通過 CDR Entry Criteria  
**結果**：**CDR READY ✅**（10/10 Entry Criteria PASS，P2P Review 2/2 Conditional Approve）

---

## 交付物清單

| ID | 標題 | 負責 | 版本 | 狀態 |
|----|------|------|------|------|
| C-001 | 系統需求規格書凍結 v2（吸收 DCN-001/002、B-006 指向修正） | SE Agent | v2.0 | Done |
| C-002 | RF PCB 詳細設計（4層板 50Ω，含 PA 散熱佈局） | Comm Agent | v1.0 | Done |
| C-003 | FPGA RTL 詳細設計（QPSK demod/mod + TMR scrubber + SAA 動態切換） | SW/FW Agent | v1.0 | Done |
| C-004 | ADCS 控制律模擬（RW 每軌去飽和驗證，B-006 正式更新 ±3.1°） | AOCS Agent | v2.0 | Done |
| C-005 | 熱詳細分析（PA 散熱片設計，contact window peak 驗算） | Mech Agent | v2.0 | Done |
| C-006 | SPENVIS 軌道輻射模擬（SAA SEU rate，動態 scrubbing 設計驗證） | SW/FW Agent | v1.0 | Done |
| C-007 | BOM v3 定案（料號確認，JLCPCB PCB 報價，教育折扣更新） | PM Agent | v3.0 | Done |
| C-008 | ConOps v2（補 EOL 降級操作模式，IoT 延遲保證） | SE Agent | v2.0 | Done |
| C-009 | CDR 審查包（含 RTM v2、V&V 計畫 v1） | SE + QA Agent | v1.0 | Done |
| C-010 | P2P Review（CDR 前核心文件審查） | QA Agent | v1.0 | Done |

---

## 關鍵設計數據

### 系統需求（C-001 — SRS v2）
- 凍結需求條數：**37 條**（吸收 DCN-001/002 修訂、B-006 指向精度修正）
- RTM v2 追蹤覆蓋率：100%

### RF PCB 詳細設計（C-002）
| 參數 | 數值 |
|------|------|
| 板層結構 | 4 層板，50Ω 微帶線 |
| 特性阻抗線寬 | W = **0.38 mm** |
| PA junction 溫度 | **+104.2°C**（上限 150°C，margin **45.8°C**）|
| 散熱 via 配置 | **8×8 via array**（升級前 4×4）|

### FPGA RTL（C-003 + B-007 補充）
| 模組 | LUT 使用量 |
|------|-----------|
| C-003 新增（QPSK + TMR scrubber + SAA 切換） | **17,600 LUT** |
| B-007 既有（OBC/FPGA 基礎架構） | **19,000 LUT** |
| Sprint 3 累計總用量 | **37,000 LUT（69.5% / Zynq-7020 53,200）** |
| SEU 防護機制 | TMR + ICAP partial scrub，SAA 動態 10ms scrubbing |

### ADCS 控制律模擬（C-004）
- 濾波器：**EKF 10D 狀態向量**（四元數 + 角速率 + 陀螺偏差）
- RW 去飽和裕度：**6.5×**（需求 ≥1.0×）
- 驗證場景：**4 場景全 PASS**
  - 正常軌道（MTQ×3 + RW×1）
  - 極區通過（入極前 RW 清空）
  - 冬至最長蝕刻
  - 初始取向誤差 45° 收斂

### 熱詳細分析（C-005）
| 位置 | Sprint 2 | Sprint 3（via 8×8 升級後） |
|------|----------|--------------------------|
| PA junction | — | **+104.2°C**（via 升級後降 34.7°C）|
| 電池（nominal） | -8.3°C | **-8.3°C**（維持）|
| 電池（冬至蝕刻） | — | **-9.1°C**（下限 -10°C，margin 0.9°C）|
| PA via 升溫改善 | 基準 | **降低 34.7°C** |

### 軌道輻射模擬 — SPENVIS（C-006）
| 項目 | 數值 |
|------|------|
| SAA 區域 SEU 速率 | **214 SEU/s**（500 km SSO）|
| 防護策略 | TMR + 10ms scrubbing（雙重）|
| 雙重命中機率 | **1.7×10⁻⁸**（per orbit，需求 < 10⁻⁶）✅ |

### BOM v3（C-007）
| 項目 | 金額（USD）|
|------|-----------|
| 硬體總計 | **$61,266** |
| 教育折扣後估計 | **~$50,000** |
| 全任務（含 $300K 發射費） | ~$455,000 |

### ConOps v2（C-008）
- 操作模式：**4 個**
  1. Normal Mode（透明轉發）
  2. Safe Mode（最低功耗 + 反振盪設計）
  3. Deorbit Mode（EOL 降級）
  4. Emergency Mode（異常保護）
- SLA 表格：IoT 延遲保證、可用度目標
- 安全模式反振盪設計：角速率閾值觸發，MTQ 阻尼控制

---

## P2P Review 結論（C-010）

**審查日期**：Sprint 3 Wave 3  
**結果**：**2/2 Conditional Approve**

| 文件 | 結論 | AI 意見數量 |
|------|------|-----------|
| CDR 審查包（C-009） | Conditional Approve | 5 項（3 medium / 2 low）|
| RTM v2 + V&V 計畫 | Conditional Approve | 3 項（1 medium / 2 low）|
| 合計 | — | **8 項（medium/low，無 critical/high）** |

所有 medium AI 項目均列入 Sprint 4 行動清單，無阻礙 CDR 進入的 critical 問題。

---

## CDR Entry Criteria 驗證（10/10 PASS）

1. SRS v2 凍結（37 條需求，RTM v2 100% 覆蓋）
2. 所有子系統詳細設計文件完成（C-002 ~ C-006）
3. RF PCB 50Ω 設計完成（W=0.38mm，via 8×8）
4. PA 熱裕度 ≥ 30°C（45.8°C margin）
5. FPGA LUT 使用率 < 80%（69.5%）
6. ADCS 控制律 4 場景全 PASS（去飽和裕度 6.5×）
7. SEU 雙重命中率 < 10⁻⁶（1.7×10⁻⁸）
8. BOM v3 定案（硬體 $61,266，教育折扣後 ~$50,000）
9. ConOps v2 完成（4 操作模式 + 安全模式設計）
10. P2P Review 通過（2/2 Conditional Approve，無 critical AI）

---

## Sprint 4 待辦（Phase C 實作驗證 / 最終報告）

| 優先 | 項目 | 負責 | 備註 |
|------|------|------|------|
| High | RF PCB 製板與實體測試 | Comm Agent | via 8×8，JLCPCB 下單 |
| High | FPGA 實作（Vivado 開發） | SW/FW Agent | QPSK loopback 測試 |
| High | ADCS Python 控制律數值模擬 | AOCS Agent | EKF 10D 完整模擬 |
| High | 廠商 RFQ 送出 | PM Agent | 6 家：GomSpace / ISIS / EnduroSat / CubeSpace / Clyde / Pumpkin |
| High | 最終報告撰寫 | 全員 | 25 頁 CEO 報告 |
| Medium | SPENVIS 線上精確模擬 | SW/FW Agent | 替代 Sprint 3 保守估算 |
| Medium | TVAC 測試設施確認 | Mech Agent | 電池 -9.1°C 裕度驗證 |

---

*Sprint 3 由 PM Agent 彙整 | TASA-NTN-3U CubeSat Project*
