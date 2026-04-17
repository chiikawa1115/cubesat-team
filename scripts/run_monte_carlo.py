import numpy as np
import json

num_simulations = 10000
tx_power_dbw = np.random.normal(10.2, 0.3, num_simulations)
tx_gain_dbi = 6.0
pointing_error_deg = np.random.rayleigh(1.5, num_simulations)
pointing_loss_db = 12 * (pointing_error_deg / 30)**2
fspl_db = 152.5
rx_g_t_db_k = 5.0
atm_fade_db = np.random.lognormal(mean=0.5, sigma=0.8, size=num_simulations)
k_dbw = -228.6
bandwidth_hz = 10e6
bandwidth_dbhz = 10 * np.log10(bandwidth_hz)

eirp_dbw = tx_power_dbw + tx_gain_dbi
cnr_db = eirp_dbw - fspl_db - pointing_loss_db - atm_fade_db + rx_g_t_db_k - k_dbw - bandwidth_dbhz

required_cnr = 1.0 
margins = cnr_db - required_cnr

result = {
    'mean_margin_db': round(float(np.mean(margins)), 2),
    'p95_margin_db': round(float(np.percentile(margins, 5)), 2),
    'p99_margin_db': round(float(np.percentile(margins, 1)), 2),
    'success_rate_pct': round(float(np.sum(margins > 0) / num_simulations * 100), 2)
}
print(json.dumps(result))
