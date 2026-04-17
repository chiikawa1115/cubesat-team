import numpy as np
import json

# Parameters - Revised for Worst-Case Scenarios based on P2P Review
num_simulations = 10000

# PA Output Power
tx_power_dbw = np.random.normal(10.2, 0.3, num_simulations) 

# SE Review: Edge of Coverage (EOC) Antenna Gain 
# Instead of fixed 6.0 dBi, model varying elevation angles from 10 deg (EOC) to 90 deg (Nadir)
# Nadir = 6.0 dBi, EOC = 3.5 dBi. Modeled as a uniform distribution of passes.
tx_gain_dbi = np.random.uniform(3.5, 6.0, num_simulations)

# AOCS Review: Worst-Case Transient Pointing Errors
# Adding a bi-modal distribution to simulate nominal vs eclipse transition spikes
is_transient = np.random.choice([0, 1], size=num_simulations, p=[0.9, 0.1])
nominal_pointing = np.random.rayleigh(1.0, num_simulations)
transient_pointing = np.random.normal(4.0, 1.0, num_simulations) # Mean 4 deg error during transients
pointing_error_deg = np.where(is_transient == 1, transient_pointing, nominal_pointing)

# Pointing Loss Calculation (Approximation for half-power beamwidth ~ 30 deg)
pointing_loss_db = 12 * (pointing_error_deg / 30)**2 

# Path Loss & Ground Station
fspl_db = 152.5 
rx_g_t_db_k = 5.0 

# Atmosphere
atm_fade_db = np.random.lognormal(mean=0.5, sigma=0.8, size=num_simulations)

# Constants
k_dbw = -228.6
bandwidth_hz = 10e6
bandwidth_dbhz = 10 * np.log10(bandwidth_hz)

# CNR Calculation
eirp_dbw = tx_power_dbw + tx_gain_dbi
cnr_db = eirp_dbw - fspl_db - pointing_loss_db - atm_fade_db + rx_g_t_db_k - k_dbw - bandwidth_dbhz

# Required CNR for DVB-S2X (QPSK 1/2 as baseline)
required_cnr = 1.0 
margins = cnr_db - required_cnr

# Statistics
mean_margin = np.mean(margins)
p99_margin = np.percentile(margins, 1) 
p95_margin = np.percentile(margins, 5)

result = {
    'mean_margin_db': round(float(np.mean(margins)), 2),
    'p95_margin_db': round(float(np.percentile(margins, 5)), 2),
    'p99_margin_db': round(float(np.percentile(margins, 1)), 2),
    'success_rate_pct': round(float(np.sum(margins > 0) / num_simulations * 100), 2)
}

print(json.dumps(result))
