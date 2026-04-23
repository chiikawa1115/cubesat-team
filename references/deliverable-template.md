# 子系統交付物統一模板

> 本檔為 CubeSat 課程專題報告的**文件品質標準**。所有子系統 agent 在產出設計交付物時，必須套用此 6 節模板。每一節都是課程評分的得分點，缺一不可。

---

## 為什麼要統一模板

### 任務本質定位
本專題是**課程作業**，不是真的要發射衛星。評委（詹老師）看的是：
- ✅ **Spec 符合性**：選用元件的 datasheet 數值是否滿足系統需求
- ✅ **價格合理性**：BOM 項目有實際報價、總金額在合理區間
- ✅ **選型理由**：為何選這顆、不選那顆，trade-off 寫清楚
- ✅ **介面清楚**：I2C/SPI/UART 接線、暫存器設定、驅動流程寫得出來
- ❌ **不是要真的買到貨、不是要真的做 TVAC、不是要真的燒錄 FPGA**

只要 datasheet 規格滿足、價格有出處、介面邏輯正確，就是高分交付物。

---

## 標準模板（6 節）

```markdown
# [子系統名稱] 設計文件

## 1. Block Diagram
[功能方塊圖 — 用 ASCII art、Mermaid 或引用圖片]

範例（Mermaid）:
flowchart LR
  ANT[天線] --> LNA --> MIXER --> ADC --> FPGA --> OBC
  OBC -. SPI .-> FPGA

## 2. Interface Table
| Signal | 方向 | Protocol | Rate | Pin | 備註 |
|--------|------|----------|------|-----|------|
| CMD_BUS | OBC→SDR | SPI Mode 0 (CPOL=0 CPHA=0) | 20 MHz | MOSI/MISO/SCK/CS_N | 命令與狀態查詢 |
| TLM_I2C | Sensor→OBC | I2C Fast-mode | 400 kHz | SDA/SCL | 溫度/電壓遙測 |
| UART_DBG | 雙向 | UART 8N1 | 115200 | TX/RX | 地面除錯介面 |

## 3. Key Register Configuration
| Register | Addr | Config Value | 說明 |
|----------|------|--------------|------|
| MODE_SEL | 0x00 | 0x03 | 進入 Normal Operation Mode |
| MODCOD_SEL | 0x10 | 0x0A | DVB-S2X 8PSK 3/4 |
| AGC_GAIN | 0x14 | 0x7F | AGC 初始化中位值 |
| ... | ... | ... | ... |

> 只列 8-15 個最關鍵的 register，不必完整抄 datasheet。

## 4. Driver Sequence / State Machine
```c
// 偽碼或 C-like 描述，用意是展示初始化邏輯
void init_sdr() {
  spi_write(RESET_REG, 0x01);
  delay_ms(10);
  spi_write(MODE_SEL, 0x03);
  spi_write(MODCOD_SEL, 0x0A);
  spi_write(AGC_GAIN, 0x7F);

  if (wait_for_lock(timeout_ms=100)) {
    transition_to(STATE_READY);
  } else {
    transition_to(STATE_ERROR);
  }
}

// 或：狀態機
// INIT → CONFIG → LOCK_WAIT → READY → (RX | TX) → DONE → IDLE
//                    ↓
//                  ERROR → RESET
```

## 5. Spec vs Datasheet 比對
| 系統需求 | 需求值 | 所選元件 (datasheet) | Meet? | 備註 |
|---------|--------|---------------------|:----:|------|
| RX 靈敏度 | ≤ -110 dBm | AD9361: -112 dBm (typ) | ✅ | 2 dB margin |
| TX 功率 | ≥ 28 dBm | Qorvo GaN PA: 30 dBm (typ) | ✅ | 2 dB margin |
| 功耗 | ≤ 5 W | AD9361 + Zynq: 4.2 W | ✅ | 0.8 W margin |
| 尺寸 | ≤ 90×90 mm | PCB layout: 85×85 mm | ✅ | 合規 |

> 每條需求都要能回答「我怎麼知道它夠用」。

## 6. COTS 選型理由 + 價格 + 替代方案
### 主選方案
- **料號**：AD9361BBCZ (Analog Devices)
- **供應商**：DigiKey [連結 + 截圖]
- **單價**：NT$ 4,500
- **需求數量**：1 pcs + 1 備品
- **選用理由**：
  - 整合度高（RF transceiver + baseband filter）
  - DC-6 GHz 寬頻，涵蓋 S-band 上下行
  - 公開 datasheet + 活躍 community support
  - 有多個太空任務 heritage（CesiumAstro、YTTEK）

### 替代方案（至少 1 個）
| 替代料號 | 供應商 | 單價 | Pros | Cons | 為何不選 |
|---------|--------|------|------|------|---------|
| ADRV9009-ZU11EG | ADI + Xilinx | NT$ 32,000 | RF-SOM 整合度更高 | 成本 7 倍、PL 資源可能過剩 | 預算不允許 |
| MAX2769C | Maxim | NT$ 1,200 | 便宜 | 頻率範圍窄、僅支援 GNSS | spec 不滿足 S-band |

### Trade-off 決策
**結論：AD9361 為最佳 cost/performance 平衡**
- 理由：單價 NT$ 4,500 比 ADRV9009-ZU11EG 省 NT$ 27,500，spec 滿足 + heritage 充分
- 風險：ADI 長單交期 12 週 → 報告中註明「採購風險 — 低」（專題不實際採購）
```

---

## 各子系統應套用的要點

### Comm-Payload（通訊酬載）
- Block Diagram：RF 鏈路（天線 → LNA/PA → Mixer → ADC/DAC → FPGA → OBC）
- Interface：SPI (FPGA↔ADC/DAC)、JESD204C（高速）、GPIO/I2C（控制）
- Register：MODCOD、AGC、Doppler 補償、PLL 頻率字
- Driver：init 序列 + AMC 自適應切換邏輯

### AOCS（姿態軌道控制）
- Block Diagram：Sun sensor / IMU / Magnetometer → OBC → Reaction Wheels / Magnetorquers
- Interface：I2C (sensors)、CAN (wheels)
- Register：sensor sampling rate、wheel torque setpoint、PID 增益
- Driver：控制迴路偽碼（detumble、sun-pointing、nadir-pointing）

### SW-Firmware
- Block Diagram：FSW 層級（App → Middleware → HAL → Drivers）
- Interface：OBC 周邊（UART/SPI/I2C/CAN）匯總
- Register：關鍵 peripheral 的 init register
- Driver：bootloader + FDIR 狀態機 + FSW 任務調度

### Mech-Thermal
- Block Diagram：熱流路徑（發熱源 → 傳導 → MLI/散熱片 → 輻射外太空）
- Interface：溫度感測器 I2C 位址表、加熱器 GPIO 控制
- Register：溫度感測器配置、PID threshold
- Driver：熱管理控制迴路偽碼（heater on/off hysteresis）

### CEO / PM / SE / QA（系統層）
不需套用本模板；他們的交付物是**其他格式**：
- CEO：25 頁簡報 + Executive Summary
- PM：WBS + Gantt + BOM 表（有自己的模板）
- SE：ICD 系統級 + RTM + Budget 表
- QA：V&V matrix + 審查報告

---

## 品質檢查清單（P2P Review 時用）

套用此模板的 deliverable 在 Peer Review 時，審查者須逐項確認：

- [ ] **節 1 Block Diagram**：清楚標示信號走向、介面標註齊全
- [ ] **節 2 Interface Table**：所有外部信號列入、protocol/rate/pin 完整
- [ ] **節 3 Register Config**：至少 8 個關鍵 register、有 config value + 說明
- [ ] **節 4 Driver Sequence**：包含 init + 正常運作 + 錯誤處理三路徑
- [ ] **節 5 Spec 比對**：每條 SYS-level 需求對應一行、Margin 標示、Meet 判定清楚
- [ ] **節 6 COTS**：DigiKey/Avnet 連結、單價有出處、至少 1 個替代方案 + trade-off

任何一節缺失 → **Reject**，退回 backlog rework。

---

## 常見誤區（避免）

| ❌ 不要做 | ✅ 應該做 |
|----------|----------|
| 寫「預計 TVAC 在 4/28 執行」 | 寫「TVAC 測試計畫書：溫度範圍 -40~+85°C、循環 8 次、熱平衡停留 2h」 |
| 寫「已向 Avnet 下單」 | 寫「DigiKey 報價 NT$ 4,500 / pcs（截圖附錄）」 |
| 長篇大論 RF 理論推導 | 用一句話帶過 + 引用 Link Budget 表 |
| 抄整份 datasheet | 只摘錄最關鍵的 8-15 個 register 與 2-3 項 spec |
| 把所有 40-pin connector 列出來 | 只列功能性的 interface（I2C 主 bus、SPI 命令 bus 等） |
