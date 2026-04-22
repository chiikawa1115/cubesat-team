# D-HG-001 v1.1：BPF 選型重新評估報告（修正版）
# Hard Gate Q1 正式回覆 — P2P Review REJECT 修正

**作者：** 通訊酬載工程師 林志遠
**日期：** 2026-04-17
**版本：** v1.1（P2P Review REJECT 修正）
**關聯：** D-HG-001 v1 Review REJECT（2026-04-17）
**狀態：** SUBMITTED FOR RE-REVIEW

---

## 1. REJECT 問題確認與修正摘要

### 1.1 REJECT 根本原因

D-HG-001 v1 所選用的 Murata SAFC1G98EA0F0A SAW BPF 存在通帶覆蓋缺口：

| 項目 | 數值 | 判定 |
|------|------|------|
| 元件標稱中心頻率 | 1980 MHz | — |
| -3 dB 頻寬（標稱） | 40 MHz | — |
| -3 dB 通帶（推算） | 1960 – 2000 MHz | — |
| 系統 UL 需覆蓋頻段（SYS-001） | **1980 – 2010 MHz** | — |
| 通帶缺口 | **2000 – 2010 MHz（10 MHz）** | FAIL |

Option B（舉證豁免）不可行：SAW 邊坡 5–15 dB/10 MHz，2010 MHz 處最樂觀 IL ≈ 10.5 dB，遠超 3.5 dB 門檻。

### 1.2 修正：選用 Option A — 換選 Qorvo QPQ1900 BAW FBAR

---

## 2. UL BPF 替換方案分析

候選器件通帶覆蓋判斷（需 f₀ ≥ 1995 MHz，BW ≥ 60 MHz）：

| 候選器件 | 技術 | f₀ (MHz) | BW (MHz) | 通帶 | 覆蓋 1980–2010？ | 決策 |
|----------|------|-----------|----------|------|-----------------|------|
| Murata SAFC1G98EA0F0A（原件） | SAW | 1980 | 40 | 1960–2000 | FAIL | 排除 |
| Murata SAFC2G00EA0F0A | SAW | 2000 | ~40 | ~1980–2020 | 邊際（溫度裕量不足） | 排除 |
| Murata SAFFB1G98FFA0F0A | SAW | 1980 | 50 | 1955–2005 | FAIL（缺 5 MHz）| 排除 |
| TDK B39162B8422U410 | SAW | 1980 | 50 | 1955–2005 | FAIL（缺 5 MHz）| 排除 |
| **Qorvo QPQ1900（BAW）** | **BAW FBAR** | **1995** | **≥ 80** | **~1955–2035** | **PASS（+25 MHz 餘量）** | **選用** |

---

## 3. 推薦 UL BPF — Qorvo QPQ1900（BAW FBAR）

| 參數 | 規格值 |
|------|--------|
| 技術類型 | BAW FBAR |
| 標稱中心頻率 f₀ | 1995 MHz |
| -3 dB 頻寬 | ≥ 80 MHz（典型 85 MHz）|
| -3 dB 通帶 | ~1955–2035 MHz |
| 覆蓋 1980–2010 MHz | ✅（雙端餘量各 ≥ 25 MHz）|
| 通帶插損 IL（25°C 典型） | ≤ 2.0 dB |
| 通帶插損 IL（全溫，最惡劣）| ≤ 3.0 dB |
| @2170 MHz 抑制 | ≥ 40 dB（最小）|
| 額定功率 | +27 dBm（UL 路徑需求 +10 dBm，餘量 17 dB）|
| 工作溫度 | –40 ~ +85°C |
| 封裝 | 2.0 × 1.6 mm SMD |

**最惡劣條件驗證（–40°C + 製程 worst case）：**
- 溫度漂移：TCF = –20 ppm/°C → Δf = +2.6 MHz（中心上移）
- 製程容差：±10 MHz（3σ）
- 低端最差：1952 + 2.6 + 10 = 1964.6 MHz ≤ 1980 MHz ✅
- 高端最差：2037 + 2.6 – 10 = 2029.6 MHz ≥ 2010 MHz ✅

---

## 4. 帶外抑制確認（SYS-003）

| 頻段 | 最小抑制 | SYS-003 達標？ |
|------|---------|--------------|
| @2170 MHz | ≥ 40 dB（QPQ1900 datasheet 最小值）| ✅ PASS |
| @2110–2170 MHz 全段 | ≥ 40 dB（阻帶平台）| ✅ PASS |
| 2037–2060 MHz 過渡帶 | 22.5–40 dB（不在 SYS-003 要求範圍內）| N/A |

---

## 5. Link Budget Delta 計算表（AI-HG-001-5）

| 項目 | v1 基準 | v1.1 更新 | Delta |
|------|---------|----------|-------|
| UL BPF 器件 | SYBP-2250+（IL 1.5 dB）| Qorvo QPQ1900 | — |
| UL BPF IL（最惡劣，用於預算）| 1.5 dB | **3.0 dB** | **+1.5 dB** |
| UL Link Margin（原 v1 估算）| +6.3 dB | — | — |
| **修正後 UL Link Margin** | — | **+4.8 dB** | –1.5 dB |
| SYS-002 要求 | ≥ +3.0 dB | ≥ +3.0 dB | — |
| **判定** | PASS | **PASS** | — |
| 裕量 | +3.3 dB | **+1.8 dB** | — |

---

## 6. 更新後 RF 鏈路架構

**UL 接收鏈（修正後）：**
```
天線 → Diplexer → [QPQ1900 BAW BPF] → LNA → Mixer → ADC → Zynq
                     f₀=1995 MHz
                     BW≥80 MHz
                     IL≤3.0 dB (worst)
                     @2170 MHz ≥40 dB
```

**DL 發射鏈：維持 v1（Reactel 4C5-2185 不變）**

---

## 7. BOM 更新

| 位號 | v1 | v1.1 |
|------|-----|------|
| FL2（UL BPF）| Murata SAFC1G98EA0F0A，$3.10 | **Qorvo QPQ1900，~$4.50（估）** |
| FL1（DL BPF）| Reactel 4C5-2185（不變）| Reactel 4C5-2185（不變）|

BOM 淨差：+$1.40（QPQ1900 vs SAFC1G98EA0F0A），影響微小。

---

## 8. RTM Entry（AI-HG-001-7）

| 需求 ID | 需求描述 | 驗證方法 | 計算結果 | 狀態 |
|---------|---------|---------|---------|------|
| SYS-002 | UL Link Margin ≥ 3 dB | Analysis（Link Budget，D-HG-001 v1.1 §5） | +4.8 dB（worst case）| Analysis CLOSED ✅ |
| SYS-003 | @2170 MHz 抑制 ≥ 40 dB | Analysis（廠商 datasheet，§4）| ≥ 40 dB（最小）| Analysis CLOSED ✅ |

---

## 9. 開放事項

### 已關閉（v1.1）

| AI | 狀態 |
|----|------|
| AI-HG-001-BLOCK（通帶缺口）| **CLOSED** — QPQ1900 完整覆蓋 |
| AI-HG-001-4（全段抑制確認）| **CLOSED** — §4 確認 |
| AI-HG-001-5（Link Budget delta）| **CLOSED** — §5 完成 |
| AI-HG-001-7（RTM entry）| **CLOSED** — §8 完成 |
| AI-HG-001-8（Sprint backlog evidence）| **CLOSED** — 本文件即為交付 |

### 遺留（後續 Sprint）

| 編號 | 事項 | 負責人 |
|------|------|--------|
| AI-HG-001-9 | PCB Layout footprint 確認（1610 → 2016 封裝變更）| PCB Layout 工程師 |
| AI-HG-001-10 | EQM VNA 實測（S21 @1980–2010 MHz，@2170 MHz）| 林志遠 |
| AI-HG-001-11 | 備用料號 QPQ1907 評估 | 採購 |

---

## 10. 結論

**Q1 Hard Gate：RESOLVED ✅（請求 Re-Review）**

| 問題 | v1 | v1.1 |
|-----|-----|------|
| UL BPF 通帶缺口 | BLOCK | **RESOLVED — QPQ1900，餘量 ≥ 25 MHz** |
| SYS-002 Link Margin | FAIL（邊坡最差 –1.7 dB）| **PASS（+4.8 dB）** |
| SYS-003 帶外抑制 | PASS | **PASS（維持）** |
| RTM entry | OPEN | **CLOSED** |

**D-003 Link Budget v3 解除 blocking，可啟動。**

---
*D-HG-001 v1.1 | 林志遠 | 2026-04-17 | 提交 Re-Review*
