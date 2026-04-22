"""
TASA-NTN-3U CubeSat — Link Budget Monte Carlo Simulation
Claude Team v1 (2026-04-21)

適配我們的系統參數：
- DL: 50 kbps, QPSK R=1/2, HARQ 6x Chase Combining
- 衛星 EIRP: +31.3 dBm (Driver Amp + PA PMA3-43-1W+)
- 地面站: 1.8m dish (+30.1 dBi), T_sys = 135 K
- QPQ1900 UL BPF IL 變異
- ADCS 指向誤差雙峰模型（日照/食月過渡）
- 最低服務仰角: 60°（UL 主瓶頸）
"""

import numpy as np
import json

np.random.seed(42)
NUM_SIM = 10000

# ────────────────────────────────────────────
# 1. 幾何：仰角 → 斜距 → FSPL
# ────────────────────────────────────────────
# 服務窗口內仰角分布（60°~85°，假設均勻）
elevation_deg = np.random.uniform(60, 85, NUM_SIM)
elevation_rad = np.radians(elevation_deg)
slant_range_km = 500.0 / np.sin(elevation_rad)

F_DL = 2185e6  # Hz
F_UL = 1995e6
C = 3e8

def fspl(d_km, f_hz):
    return 20 * np.log10(4 * np.pi * d_km * 1e3 * f_hz / C)

fspl_dl = fspl(slant_range_km, F_DL)
fspl_ul = fspl(slant_range_km, F_UL)

# ────────────────────────────────────────────
# 2. ADCS 指向誤差雙峰模型
# ────────────────────────────────────────────
# 90% 日照段：Rayleigh(σ=0.97°)，3σ ≈ 2.9°（D-002 日照段）
# 10% 食月過渡瞬態：Normal(μ=3.4°, σ=0.5°)（D-002 食月段最大值）
is_eclipse_transient = np.random.choice([0, 1], size=NUM_SIM, p=[0.90, 0.10])
sunlit_error  = np.random.rayleigh(scale=0.97, size=NUM_SIM)
eclipse_error = np.random.normal(loc=3.4, scale=0.5, size=NUM_SIM)
pointing_error_deg = np.where(is_eclipse_transient, eclipse_error, sunlit_error)

# Patch 天線 3dB beamwidth ≈ 60°（±30°）
# 指向損耗：近似 Gaussian beam L = 12 × (θ/θ_3dB)²
BEAMWIDTH_3DB = 60.0  # degrees
pointing_loss_db = 12.0 * (pointing_error_deg / BEAMWIDTH_3DB) ** 2

# ────────────────────────────────────────────
# 3. 大氣衰減（S-band，仰角依賴）
# ────────────────────────────────────────────
# 中位衰減：ITU-R P.676，仰角 60° ≈ 0.2 dB，85° ≈ 0.1 dB
# 以 LogNormal 模型表示不確定性
atm_mean = 0.2 / np.sin(elevation_rad)  # 仰角越低衰減越大
atm_fade_db = np.random.lognormal(
    mean=np.log(atm_mean) - 0.1**2 / 2,
    sigma=0.1,
    size=NUM_SIM
)

# ────────────────────────────────────────────
# 4. DL Link Budget（衛星 → 地面站）
# ────────────────────────────────────────────
# 衛星 TX 功率不確定性（PA P3dBBO + Driver Amp chain）
p_tx_dl_dbm  = np.random.normal(loc=31.3, scale=0.5, size=NUM_SIM)  # dBm
p_tx_dl_dbw  = p_tx_dl_dbm - 30.0

G_ant_sat_dl = 2.0   # dBi，patch 天線
L_feeder_sat = 0.3   # dB

# 地面站接收
G_ant_gnd    = 30.1  # dBi，1.8m dish @ 2185 MHz
L_feeder_gnd = 1.0   # dB
T_sys_gnd    = 135.0 # K
N0_gnd_dbw   = 10 * np.log10(1.38065e-23 * T_sys_gnd)  # dBW/Hz ≈ -177.3

# C/N0 計算
p_rx_dl_dbw = (p_tx_dl_dbw
               + G_ant_sat_dl
               - L_feeder_sat
               - fspl_dl
               - atm_fade_db
               - pointing_loss_db
               + G_ant_gnd
               - L_feeder_gnd)

cn0_dl = p_rx_dl_dbw - N0_gnd_dbw  # dBHz

# 所需 C/N0（50 kbps info rate，coded Eb/N0 = 5.5 dB）
RB_INFO = 50e3          # info bit rate
CN0_REQ = 5.5 + 10 * np.log10(RB_INFO)  # = 5.5 + 47.0 = 52.5 dBHz

# 無 HARQ margin
margin_dl_raw = cn0_dl - CN0_REQ

# 含 HARQ 6× Chase Combining 等效增益（保守取 7.0 dB）
HARQ_GAIN_DB = 7.0
margin_dl_harq = margin_dl_raw + HARQ_GAIN_DB

# ────────────────────────────────────────────
# 5. UL Link Budget（地面站 → 衛星）
# ────────────────────────────────────────────
# 地面站 TX（4W + 1.8m dish）
P_TX_UL_DBM  = np.random.normal(loc=36.0, scale=0.3, size=NUM_SIM)
P_TX_UL_DBW  = P_TX_UL_DBM - 30.0
G_ANT_GND_UL = 30.1   # dBi
L_FEED_GND   = 1.0

# 衛星接收
G_ant_sat_ul  = 2.0   # dBi
L_feeder_ul   = 0.3   # dB
BPF_IL_QPQ    = np.random.normal(loc=2.0, scale=0.5, size=NUM_SIM).clip(min=0.5, max=4.0)

# 系統雜訊（QPQ1900 BPF IL 變異影響 NF）
# NF_system ≈ 2.09 + 0.1*(BPF_IL - 2.5)/0.5 ≈ 近似線性
NF_sys_db = 2.09 + 0.10 * (BPF_IL_QPQ - 2.5) / 0.5
T_rx  = 290.0 * (10**(NF_sys_db / 10) - 1.0)
T_ant = 290.0
T_sys_sat = T_ant + T_rx
N0_sat_dbw = 10 * np.log10(1.38065e-23 * T_sys_sat)

p_rx_ul_dbw = (P_TX_UL_DBW
               + G_ANT_GND_UL
               - L_FEED_GND
               - fspl_ul
               - atm_fade_db
               - pointing_loss_db
               + G_ant_sat_ul
               - L_feeder_ul)

cn0_ul = p_rx_ul_dbw - N0_sat_dbw
margin_ul = cn0_ul - CN0_REQ

# ────────────────────────────────────────────
# 6. 統計輸出
# ────────────────────────────────────────────
def stats(arr, label):
    return {
        "link": label,
        "mean_margin_db":   round(float(np.mean(arr)), 2),
        "p95_margin_db":    round(float(np.percentile(arr, 5)), 2),
        "p99_margin_db":    round(float(np.percentile(arr, 1)), 2),
        "p999_margin_db":   round(float(np.percentile(arr, 0.1)), 2),
        "success_rate_pct": round(float(np.sum(arr > 0) / NUM_SIM * 100), 4),
        "margin_3db_pct":   round(float(np.sum(arr > 3) / NUM_SIM * 100), 4),
    }

results = {
    "system": "TASA-NTN-3U Claude Team",
    "data_rate_kbps": 50,
    "min_elevation_deg": 60,
    "num_simulations": NUM_SIM,
    "DL_no_HARQ": stats(margin_dl_raw,  "DL (no HARQ)"),
    "DL_HARQ_6x": stats(margin_dl_harq, "DL (HARQ 6x)"),
    "UL":         stats(margin_ul,       "UL"),
    "pointing_stats": {
        "eclipse_transient_fraction": float(np.mean(is_eclipse_transient)),
        "mean_pointing_error_deg": round(float(np.mean(pointing_error_deg)), 3),
        "p99_pointing_error_deg":  round(float(np.percentile(pointing_error_deg, 99)), 3),
    }
}

print(json.dumps(results, indent=2))
