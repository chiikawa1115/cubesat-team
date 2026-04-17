# P2P Review — D-HG-001 + D-HG-002（Hard Gate Q1/Q2）

**審查主席：** QA Agent 林宜靜
**審查日期：** 2026-05-27
**審查對象：** D-HG-001（BPF 重新選型）+ D-HG-002（LO PLL 方案）
**作者：** Comm Agent 林志遠

---

## 審查者 1：SE Agent 陳明哲（系統整合視角）

### D-HG-001 審查

**需求符合性：**
- ✅ UL BPF 帶外抑制 @2170 MHz：45 dB（≥ 40 dB 門檻通過）
- ✅ DL BPF 帶外抑制 @2010 MHz：≥ 50 dB（≥ 40 dB 門檻通過）
- ✅ Link Margin 修訂後 +5.3 dB（≥ SYS-002 要求 3 dB）
- ⚠️ **追蹤事項：** SAFC1G98EA0F0A 中心 1980 MHz，通帶右緣覆蓋至 ~2000 MHz，1980-2010 MHz 完整覆蓋需確認 — 建議 D-003 Link Budget 時補上 SAW 在 2005-2010 MHz 的 IL 量測值

**ICD 影響：**
- BPF 更換後，RF 鏈路 IL 變化：UL +1.0 dB（SAW 3dB vs SYBP 2dB, 1dB 差）
- D-004 System Budget 需同步更新 RF 子系統欄位
- PCB 面積影響：SAW (1.1×0.9 mm) 替換 SYBP (3.0×1.5 mm)，面積反而減少 ✅

**裁決：APPROVE（含追蹤事項）**

### D-HG-002 審查

**需求符合性：**
- ✅ ADF4351 INT mode：VCO 3040 MHz ÷ 16 = 190 MHz，計算正確
- ✅ Phase noise @ LO 190 MHz：-114.6 dBc/Hz @10 kHz（遠優於 -85 dBc/Hz 目標）
- ✅ 上混頻後 2185 MHz 載波：-93.4 dBc/Hz，Costas loop 相位誤差 0.055° — 可忽略
- ✅ 功耗：ADF4351 典型 ICC ~34 mA @ 3.3V = **112 mW**，需加入 D-004 Power Budget

**ICD 影響：**
- D-004 Power Budget 需新增 PLL 子系統：~120 mW（TCXO 6.6 mW + ADF4351 112 mW + loop filter ~1 mW）
- 目前 Sprint 2 Power Budget（B-005）是否有預留 RF 輔助功耗的裕量，需確認

**裁決：APPROVE（含功耗追蹤）**

---

## 審查者 2：SW/FW Agent 陳俊宏（FPGA 介面視角）

### D-HG-001 審查

**FPGA 介面影響評估：**
- BPF 更換為純被動元件，不影響 FPGA RTL 設計（C-003）
- ADC 輸入訊號 SNR 可能因 BPF 選擇性更好而改善（噪聲帶寬收窄）→ 正面影響
- ✅ 無 RTL 修改需求

**裁決：APPROVE**

### D-HG-002 審查

**ADF4351 SPI 介面評估：**
- ADF4351 使用 SPI（3-wire serial）配置寄存器，需 Zynq-7020 PS 端提供 SPI master
- ✅ Zynq-7020 PS 有 2 組 SPI（SPI0/SPI1），可直接使用
- 初始化時序：SPI 配置 6 個寄存器（R0～R5），約 200 μs 可完成 lock → 在 FSW startup 序列中加入 PLL init 步驟

**FSW 修改需求（minor）：**
- startup.py（C-007 FSW）中加入 `pll_init()` 函式調用（10 行程式碼）
- 監控 ADF4351 LD（Lock Detect）腳位：接 Zynq GPIO，若 unlock 觸發重新初始化
- D-007 整合測試計畫需加入 PLL lock 測試案例

**裁決：APPROVE（FSW 追蹤事項：pll_init + LD 監控）**

---

## QA 主席總結

| 交付物 | 審查者 1 | 審查者 2 | 結果 |
|-------|---------|---------|------|
| D-HG-001（BPF）| ✅ APPROVE | ✅ APPROVE | **2/2 PASS** |
| D-HG-002（LO PLL）| ✅ APPROVE | ✅ APPROVE | **2/2 PASS** |

**追蹤事項（非阻塞）：**
1. D-003 Link Budget：補 SAW @ 2005-2010 MHz IL 量測值
2. D-004 Power Budget：新增 PLL 120 mW
3. FSW（C-007 更新版）：加入 pll_init() + LD 監控
4. D-007 整合測試計畫：加入 PLL lock 測試案例

**Hard Gate Q1/Q2 正式關閉：** ✅ CDR Conditional Pass → **CDR PASS 確認**

*P2P Review 完成 | QA Agent 林宜靜 | 2026-05-27*
