# CubeSat 元件規格參考（TASA-NTN-3U，S-band NTN Rel-17）

> 以規格需求為導向，附 DigiKey/Mouser 實際報價（2026/04 查詢）
> 注意：太空級子系統（OBC/EPS/ADCS）需直接向廠商詢價，無公開標價

---

## S-band NTN 酬載 RF 鏈路（可在 DigiKey 購買）

### 透明轉發 RF 鏈路架構
```
UE → [UL 1980-2010 MHz]
     ↓
  Rx Patch 天線 (+8 dBi)
     ↓
  LNA（低雜訊放大）
     ↓
  BPF（UL 帶通濾波）
     ↓
  Mixer（頻率搬移 UL→DL）
     ↓
  BPF（DL 帶通濾波）
     ↓
  PA（功率放大 ~1W）
     ↓
  Tx Patch 天線
     ↓
→ [DL 2170-2200 MHz] → gNB
```

| 元件 | 型號 | 規格 | DigiKey 單價（USD）| 連結 | 備注 |
|------|------|------|------------------|------|------|
| **LNA（首選）** | Analog Devices ADL5523ACPZ-R7 | 0.4–4 GHz, NF ~1 dB @2GHz, Gain 15 dB | **$4.38** | [DigiKey](https://www.digikey.com/en/products/detail/analog-devices-inc/ADL5523ACPZ-R7/2261199) | SMD LFCSP，現貨充足 |
| **LNA（模組型，測試用）** | Mini-Circuits ZX60-242GLN-S+ | 1.71–2.4 GHz, NF 0.9 dB, Gain 28 dB | ~$52–$89 | [DigiKey](https://www.digikey.com/en/products/detail/mini-circuits/ZX60-242GLN-S/16682732) | SMA 接頭，原型驗證佳 |
| **PA 1W** | Mini-Circuits PMA3-43-1W+ | 10–4000 MHz, Psat +32.6 dBm, Gain 21 dB | 詢價（上架中） | [DigiKey](https://www.digikey.com/en/products/detail/mini-circuits/PMA3-43-1W/27669457) | QFN 3×3 mm, +12V 供電 |
| **BPF（SMD）** | Mini-Circuits SYBP-2250+ | 2250 MHz 中心, BW 740 MHz | **$24.58** | [DigiKey](https://www.digikey.com/en/products/detail/mini-circuits/SYBP-2250/25963491) | 覆蓋 S-band n236 |
| **BPF（測試用，SMA）** | Mini-Circuits ZX75BP-2250-S+ | 2000–2500 MHz, IL 1.5 dB | 詢價 | [DigiKey](https://www.digikey.com/en/products/detail/mini-circuits/ZX75BP-2250-S/20526674) | 原型驗證，同日出貨 |
| **Mixer** | Analog Devices LT5512EUF#PBF | 1 kHz–3 GHz, 主動雙平衡 | **$11.14** | [DigiKey](https://www.digikey.com/en/products/detail/linear-technology-analog-devices/LT5512EUF-PBF/889631) | 高線性度，整合 LO buffer |

**RF 鏈路元件小計（DigiKey 可採購部分）：~$50–$150**
（含 LNA×2、BPF×2、Mixer×1、備用元件，不含 PA 詢價及 PCB 製作）

---

## TT&C（UHF 遙傳追蹤）

| 規格項目 | 需求 | 參考廠商/型號 | 概估價（USD）| 備注 |
|---------|------|------------|------------|------|
| 頻段 | UHF 435–438 MHz | ISIS UHF/VHF Radio | ~$3,000–$5,000 | 需直接詢價 |
| 資料率 | ≥9,600 bps 下行 | GomSpace AX100 | | 飛行驗證 |
| 發射功率 | ≥1 W | | | |
| 協定 | AX.25 or CCSDS | | | |
| 天線 | 折疊式偶極，展開後 | ISIS UHF Antenna | ~$1,000–$2,000 | |

---

## S-band 天線（酬載用）

| 規格項目 | 需求 | 參考廠商/型號 | 概估價（USD）| 備注 |
|---------|------|------------|------------|------|
| 頻段 | S-band n236，1980–2200 MHz | EnduroSat S-Band Patch | ~$2,000–$5,000 | 需詢價 |
| 增益 | ≥8 dBi | ISISPACE S-Band Patch | | 飛行驗證 |
| 極化 | RHCP（右旋圓極化）| | | 減少 Faraday rotation 損耗 |
| HPBW | ≥±30°（S-band 寬波束） | | | 指向需求寬鬆 ✅ |

---

## OBC（On-Board Computer）

| 規格項目 | 需求 | 參考廠商/型號 | 概估價（USD）| 備注 |
|---------|------|------------|------------|------|
| 處理器 | ARM Cortex-A9+ 或 Zynq class | GomSpace NanoMind A3200 | ~$3,000–$10,000 | 需詢價 |
| FPGA | ≥50K LUT（SDR 基帶用）| ISIS OBC | | Zynq 整合 ARM+FPGA 最佳 |
| 溫度範圍 | -40°C ~ +85°C（工業級） | | | |
| 介面 | SPI, CAN, UART, I²C | | | |
| 功耗 | ≤2 W（待機），≤5 W（操作） | | | |
| SEU 防護 | TMR 或 Configuration Scrubbing | | | 由 FPGA RTL 實作（Rudy 主場） |

---

## ADCS（姿態控制，S-band 用寬波束天線，指向需求寬鬆）

| 規格項目 | 需求 | 參考廠商/型號 | 概估價（USD）| 備注 |
|---------|------|------------|------------|------|
| 指向精度 | **≤±3°**（S-band HPBW ±30°，大餘裕）| CubeSpace ADCS-3 | ~$5,000–$15,000 | Ka-band 才需要 ±0.5° |
| 控制模式 | 3-axis stabilized | MAI-400 ADACS | ~$20,000–$40,000（過規格）| 不需要這麼貴 |
| 感測器 | 磁力計 + 太陽感測器 + IMU | 磁力矩器 + IMU 組合 | ~$3,000–$8,000 | 無需星追蹤器 |
| 致動器 | 磁力矩器 (3) + 小型反應輪 (可選) | | | |
| 功耗 | ≤0.6 W（操作）| | | |

> **注意：** 因選 S-band（HPBW ±30–45°），ADCS 指向需求從 ±0.5° 大幅放寬至 ±3°，
> 可省下 $10,000–$30,000 選用較便宜的 ADCS 方案。

---

## EPS（電力子系統，3U 實際規格）

| 規格項目 | 需求 | 參考廠商/型號 | 概估價（USD）| 備注 |
|---------|------|------------|------------|------|
| 太陽能板 | **≥3 W avg（含 eclipse）**，BOL ~5 W | Clyde Space 3U Panel | ~$1,500–$3,000/panel | ~~「≥30W」是舊 Ka-band 資料，已更正~~ |
| 電池 | Li-ion, **≥10 Wh**（支援 4 min 接觸窗口）| GomSpace P31u 內建 | ~$500 | 每圈放電 ~2.4% DoD ✅ |
| MPPT | ≥90% 效率 | GomSpace NanoPower P31u | ~$3,000–$7,000（整套）| 含電池管理 |
| 匯流排電壓 | 3.3 V / 5 V / 12 V regulated | | | |
| **Peak 功耗** | **≤5 W**（S-band 酬載接觸窗口）| | | 電池補足差額 |

---

## 結構框架

| 規格項目 | 需求 | 參考廠商/型號 | 概估價（USD）| 備注 |
|---------|------|------------|------------|------|
| 構型 | 3U（100×100×340 mm）| ISIS 3U Frame | ~$2,000–$4,000 | Al 6061-T6 |
| 質量上限 | **≤4.0 kg 含所有元件** | Pumpkin 3U kit | | |
| 展開機構 | 太陽能板展開 ×2 | NanoAvionics class | ~$1,000–$1,500 | |
| P-POD 相容 | CalPoly Rev.13 標準 | | | 發射商要求 |

---

## 感測器（獨立採購，DigiKey 有貨）

| 元件 | 型號 | 規格 | DigiKey 價格（USD）|
|------|------|------|------------------|
| 磁力計 | Honeywell HMC5883L | 3-axis, ±8 Gauss | ~$5 |
| IMU | Bosch BMX160 | 6-DOF | ~$4 |
| 溫度感測器 | PT100 thermistor ×8 | ±0.5°C | ~$2 each |
| GPS 接收器 | u-blox LEA-M8S | LEO compatible | ~$60–$100 |

---

## BOM 硬體費用彙整

| 類別 | 項目 | 估算（USD）| 採購方式 |
|------|------|----------|---------|
| RF 鏈路元件 | LNA, PA, BPF, Mixer, PCB | ~$500–$1,500 | DigiKey / Mouser |
| S-band 天線 | 酬載用 patch array | ~$3,000–$5,000 | EnduroSat / ISISPACE |
| TT&C 收發器 + 天線 | UHF radio + 折疊天線 | ~$4,000–$7,000 | ISIS / GomSpace |
| OBC（含 FPGA）| Zynq class | ~$5,000–$10,000 | GomSpace / ISIS |
| EPS（含電池）| 3U, ≥10 Wh | ~$4,000–$8,000 | GomSpace / Clyde Space |
| ADCS | 磁力矩器 + IMU（±3° 需求）| ~$5,000–$12,000 | CubeSpace / ISIS |
| 結構框架 + 展開機構 | 3U aluminum kit | ~$3,000–$5,500 | ISIS / Pumpkin |
| 感測器雜項 | GPS + IMU + 溫度 | ~$200–$500 | DigiKey |
| PCB 打樣（RF 板 ×2）| 4 層 PCB, 小批量 | ~$500–$1,000 | JLCPCB / PCBWay |
| 備品 + 耗材 | 10% buffer | ~$2,500–$5,000 | |
| **合計** | | **~$27,700–$55,500** | |
| **NTD 換算（×32）** | | **~NT$885,000–$1,776,000** | |

> **對比原 PM 估算 NT$1,700,000** — 硬體部分與估算範圍吻合（上限約 NT$1.8M）。
> 課程報告可用「硬體預算 NT$120 萬（USD 37,500）」作為中位數基準。

---

## 採購注意事項

1. **DigiKey 直接採購**：RF 鏈路元件（LNA, BPF, Mixer）— 價格透明，可附單據
2. **廠商詢價（無公開標價）**：OBC, EPS, ADCS, 天線 — 報告中標注「廠商報價，見附件」
3. **教育折扣**：GomSpace、ISIS、EnduroSat 對學術機構有 10–30% 折扣，需提供大學信件
4. **JLCPCB 打樣**：RF PCB 建議 4 層板，阻抗控制 50Ω，可附報價單作為成本佐證
