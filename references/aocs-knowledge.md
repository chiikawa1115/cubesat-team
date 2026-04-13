# AOCS/ADCS 知識庫

> 蒸餾自 TASA 課程教材（詹鎮宇研究員）- 第二講

## 目錄
1. [AOCS 基本定義](#1-aocs-基本定義)
2. [姿態感測器 (Attitude Sensors)](#2-姿態感測器)
3. [致動器 (Actuators)](#3-致動器)
4. [指向精度預算 (Pointing Budget)](#4-指向精度預算)
5. [GN&C 統計與模式](#5-gnc-統計與模式)
6. [典型故障案例](#6-典型故障案例)
7. [CubeSat ADCS 方案](#7-cubesat-adcs-方案)

---

## 1. AOCS 基本定義

- **AOCS (Attitude and Orbit Control System)：** 涵蓋姿態控制 + 軌道控制的完整系統
- **ADCS (Attitude Determination and Control System)：** 專指姿態的量測與控制
- **GN&C (Guidance, Navigation & Control)：** 導航、定位與控制的整體框架

### 三軸定義
| 軸 | 名稱 | 方向 |
|---|------|------|
| X | Roll | 飛行方向 |
| Y | Pitch | 翼展方向 |
| Z | Yaw | 地心/天頂方向 |

### 姿態表示法
- **歐拉角 (Euler Angles)：** 直覺但有 Gimbal Lock 問題
- **四元數 (Quaternions)：** 四參數表示，無奇異點，運算效率高
- **方向餘弦矩陣 (DCM)：** 3x3 旋轉矩陣，精確但冗餘

---

## 2. 姿態感測器

| 感測器 | 精度 | 原理 | 適用場景 |
|--------|------|------|--------|
| 太陽感測器 (Sun Sensor) | 0.01-1 deg | 光電效應量測太陽方向 | 粗定位、安全模式 |
| 地球感測器 (Earth Sensor) | 0.05-0.1 deg | 紅外線偵測地球邊緣 | 地球指向任務 |
| 星追蹤器 (Star Tracker) | 1-10 arcsec | CCD 拍攝星場比對星表 | 高精度姿態確定 |
| 磁力計 (Magnetometer) | 0.5-3 deg | 量測地磁場方向 | LEO 粗定位 |
| 陀螺儀 (Gyroscope) | 0.001-0.1 deg/hr | 量測角速率 | 高動態、快速機動 |
| GPS 接收機 | 10 m (位置) | 衛星導航定位 | 軌道確定 |

---

## 3. 致動器

| 致動器 | 扭矩範圍 | 原理 | 特點 |
|--------|----------|------|------|
| 反應輪 (Reaction Wheel) | 0.001-1 Nm | 角動量交換 | 高精度，但有飽和問題 |
| 動量輪 (Momentum Wheel) | 連續旋轉 | 維持陀螺穩定 | 適合自旋穩定 |
| 控制力矩陀螺 (CMG) | 10-1000 Nm | 改變陀螺進動方向 | 大型衛星、高敏捷 |
| 磁力矩器 (Magnetorquer) | 0.0001-0.01 Nm | 電磁線圈與地磁場交互 | 反應輪卸載、LEO 常用 |
| 推進器 (Thruster) | 0.001-10 N | 化學/電推進噴射 | 軌道機動、大角度調姿 |

### 反應輪 vs. 磁力矩器的搭配
- LEO CubeSat 典型配置：3-4 個反應輪 + 3 軸磁力矩器
- 磁力矩器負責週期性卸載反應輪累積的角動量
- 磁力矩器僅在 LEO 有效（需要地磁場）

---

## 4. 指向精度預算

### 誤差來源分類

| 類別 | 來源 | 典型量級 |
|------|------|--------|
| 感測器誤差 | Star tracker noise, alignment | 5-50 arcsec |
| 致動器誤差 | Reaction wheel jitter, friction | 1-20 arcsec |
| 結構彈性 | 太陽能板撓曲、熱變形 | 10-100 arcsec |
| 外部擾動 | 大氣阻力、太陽光壓、重力梯度 | 任務相關 |

### LEO 主要擾動力矩

| 擾動源 | 特性 | 量級 (3U CubeSat) |
|--------|------|------------------|
| 大氣阻力 (Aerodynamic) | 與高度、面積相關，< 600 km 顯著 | ~10^-7 Nm |
| 重力梯度 (Gravity Gradient) | 與慣量矩差異相關 | ~10^-7 Nm |
| 太陽光壓 (Solar Radiation) | 與面積和反射率相關 | ~10^-8 Nm |
| 殘磁 (Residual Magnetic) | 與衛星永久磁偶極相關 | ~10^-7 Nm |

---

## 5. GN&C 統計與模式

### 典型操作模式

| 模式 | 目的 | 感測器 | 致動器 | 精度 |
|------|------|--------|--------|------|
| 分離/去旋轉 (Detumbling) | 部署後穩定 | 磁力計 + 陀螺 | 磁力矩器 | -- |
| 安全模式 (Safe Mode) | 異常時最低功耗 | 太陽感測器 + 磁力計 | 磁力矩器 | ~5 deg |
| 粗指向 (Coarse Pointing) | 太陽追蹤/通訊 | 太陽感測器 + 磁力計 | RW + 磁力矩器 | ~1 deg |
| 精指向 (Fine Pointing) | 酬載觀測 | Star Tracker + 陀螺 | RW | < 0.1 deg |
| 軌道機動 (Orbit Maneuver) | 軌道維持/離軌 | GPS + 陀螺 | 推進器 | -- |

---

## 6. 典型故障案例

### 常見 ADCS 故障模式
1. **反應輪飽和 (Wheel Saturation)：** 外部擾動持續累積角動量，反應輪轉速達到極限
   - 預防：定期磁力矩器卸載 (momentum dumping)
2. **Star Tracker 遮蔽：** 太陽、月球或地球邊緣進入視野導致失盲
   - 預防：多 Star Tracker 配置、排除區設定
3. **磁力計校準偏差：** 衛星本體殘磁干擾導致量測偏差
   - 預防：在軌校準演算法
4. **陀螺漂移 (Gyro Drift)：** MEMS 陀螺長期偏差累積
   - 預防：與 Star Tracker 融合更新

---

## 7. CubeSat ADCS 方案

### 商用 COTS 方案比較

| 供應商 | 型號 | 適用尺寸 | 指向精度 | 包含元件 |
|--------|------|----------|--------|--------|
| Blue Canyon Tech | XACT | 3U+ | < 0.003 deg | Star Tracker + RW + Magnetorquer |
| CubeSpace | CubeADCS | 1U-12U | 0.1-0.01 deg | 模組化可選配 |
| NewSpace Systems | NFSS / NMHW | 各尺寸 | 元件級 | Star Tracker / Reaction Wheel 單賣 |
| AAC Clyde Space | iADCS | 3U-6U | < 0.1 deg | 整合式 ADCS 模組 |

### 設計考量要點
- **功耗預算：** ADCS 子系統通常佔衛星總功耗 15-30%
- **質量預算：** 3U CubeSat ADCS 質量約 200-500g
- **磁潔淨度：** 應要求所有子系統量測殘磁，避免干擾磁力計
- **冗餘設計：** 關鍵任務至少需 2 個 Star Tracker 視野不重疊
