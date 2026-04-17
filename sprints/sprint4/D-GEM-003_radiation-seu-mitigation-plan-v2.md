# D-GEM-003: Integrated Radiation & SEU Mitigation Plan v2 (Post-Professor Review)

## 1. Overview
In LEO (500 km SSO), the CubeSat will encounter trapped protons and galactic cosmic rays. This v2 document outlines the hardened mitigation strategy, specifically addressing secondary bremsstrahlung radiation, I/O state control during resets, and external supervisor architectures.

## 2. Hardened Radiation Environment Analysis
- **TID & Bremsstrahlung (Secondary X-rays)**: While 2mm Al shielding stops primary protons, it generates secondary X-rays. To mitigate this, a **Z-graded shielding approach** will be used: a 0.5mm Tantalum (Ta) foil will be applied to the inner chassis directly above the MPSoC and critical memory to absorb secondary X-rays.
- **SEL (Single Event Latch-up)**: The Xilinx 16nm process has an SEL LET threshold of ~60 MeV-cm2/mg. Latch-up protection relies on the external supervisor (see below).

## 3. Hardened Mitigation Architecture

### 3.1 Hardware Level: External Supervisor (Ultimate Watchdog)
- Relying solely on the MPSoC's internal PL Watchdog or SEM IP is insufficient due to single-point-of-failure routing risks.
- **Design Addition**: A high-heritage, external rad-tolerant MCU (TI MSP430-EP) will act as the System Supervisor. 
- **Mechanism**: The MPSoC must send a toggling "heartbeat" GPIO signal to the MSP430 every 500ms. If the MSP430 misses two heartbeats, it will physically actuate the Power MOSFET to hard-power-cycle the MPSoC, clearing any latch-ups or uncorrectable SEM IP failures.

### 3.2 System Level: Preventing the "Death Spin"
- During an SEU-induced reboot or reconfiguration, the MPSoC I/O pins default to a High-Impedance (High-Z) floating state.
- **Design Addition**: To prevent floating pins from randomly activating the ADCS motor drivers (causing a spin out of control), strict hardware **4.7kΩ pull-down resistors** will be placed on all PWM and Enable traces connecting the OBC to the Magnetorquers and Reaction Wheels. The default state is strictly OFF until software asserts control.

### 3.3 Firmware Level (FPGA Fabric)
- **SEM IP**: Continues to be used for background CRAM scrubbing and single-bit ECC correction.
- **TMR**: Local TMR applied to the heartbeat generator logic to ensure the external watchdog is only fed if the core logic is truly healthy.

## 4. Conclusion
By integrating Z-graded shielding, a physical external MCU watchdog, and hardware pull-downs, the DVB-S2X payload is secured against both soft errors and hard latch-ups.
