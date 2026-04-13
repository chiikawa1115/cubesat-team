# CubeSat 元件規格參考

> 以規格需求為導向，不綁定特定料號

## OBC（On-Board Computer）
| 規格項目 | 需求 | 參考等級 | 概估價 |
|---------|------|---------|--------|
| 處理器 | ARM Cortex-A9+ 或同等 | Zynq-7000 class | ~$150 |
| FPGA | ≥50K LUT, 內建 DSP | Artix/Zynq class | included |
| 溫度範圍 | -40°C ~ 85°C (工業級) | | |
| 介面 | SPI, CAN, UART, SpaceWire | | |
| 功耗 | <5W | | |

## 通訊子系統
### TT&C
| 規格項目 | 需求 | 參考等級 | 概估價 |
|---------|------|---------|--------|
| 頻段 | UHF 435 MHz | ISIS class | ~$5,000 |
| 資料率 | ≥9600 bps | | |
| 發射功率 | ≥1W | | |
| 協定 | AX.25 or CCSDS | | |

### SDR 酬載
| 規格項目 | 需求 | 參考等級 | 概估價 |
|---------|------|---------|--------|
| 頻段 | Ka-band (27.5-30 GHz UL / 17.7-20.2 GHz DL) | CesiumAstro Vireo class | ~$50,000+ |
| 頻寬 | ≥250 MHz | | |
| ADC | ≥14-bit, ≥5 Gs/s | RFSoC class | ~$3,000 |
| DAC | ≥14-bit, ≥10 Gs/s | | included |
| 調變 | DVB-S2X (up to 256-APSK) | | |
| SD-FEC | 內建 LDPC+BCH | | |

## ADCS
| 規格項目 | 需求 | 參考等級 | 概估價 |
|---------|------|---------|--------|
| 控制模式 | 3-axis stabilized | CubeSpace class | ~$15,000 |
| 指向精度 | ≤±0.5° | | |
| 感測器 | 星追蹤器 + 太陽感測器 + 磁力計 + 陀螺儀 | | |
| 致動器 | 反應輪 (3+1) + 磁扭器 (3) | | |

## EPS（電力子系統）
| 規格項目 | 需求 | 參考等級 | 概估價 |
|---------|------|---------|--------|
| 太陽能板 | ≥7W BOL per panel (3U body-mounted) | Endurosat class | ~$2,000/panel |
| 電池 | Li-ion, ≥20Wh | 18650 cells | ~$500 |
| MPPT | ≥90% efficiency | SPV1040 class | ~$100 |
| 匯流排電壓 | 3.3V / 5V / 12V regulated | | |
| 總功率需求 | ≥30W (peak), ≥15W (average) | | |

## 結構
| 規格項目 | 需求 | 參考等級 | 概估價 |
|---------|------|---------|--------|
| 構型 | 3U (10x10x30 cm) | ISIS/Pumpkin class | ~$3,000 |
| 質量上限 | 4.0 kg | | |
| 材料 | Al 7075-T6 or 6061-T6 | | |
| 展開機構 | 太陽能板 x2 (deployable) | | ~$1,500 |

## 感測器（獨立採購）
| 規格項目 | 需求 | 參考等級 | 概估價 |
|---------|------|---------|--------|
| 磁力計 | 3-axis, ±8 Gauss | HMC5883L class | ~$3 |
| IMU | 6-DOF, gyro ≤0.01°/hr | BMX160 class | ~$3 |
| GPS 接收器 | LEO compatible, ≤10m accuracy | | ~$500 |
| 溫度感測 | x8 points, ±0.5°C | PT100/thermistor | ~$50 |

## 估價注意事項
- 以上為概估價，實際採購需查 DigiKey 或專業 CubeSat 供應商
- 專業 CubeSat 模組（ADCS、EPS、TT&C）通常不在 DigiKey，需直接聯繫廠商
- 規格為最低需求，選型時考慮 margin
- 教育/研究折扣可能適用
