# D-GEM-003: Integrated Radiation & SEU Mitigation Plan v1

## 1. Overview
In LEO (500 km SSO), the CubeSat will encounter trapped protons (South Atlantic Anomaly) and galactic cosmic rays. Given the reliance on a complex Xilinx Zynq UltraScale+ MPSoC for the DVB-S2X SDR payload, Single Event Upsets (SEU) in the SRAM-based FPGA and processors are a primary mission risk. This document outlines the integrated SE/AOCS/FW mitigation strategy.

## 2. Radiation Environment Analysis (SPENVIS Baseline)
- **Orbit**: 500 km, 97.4° inclination.
- **TID (Total Ionizing Dose)**: Expected to be < 5 krad(Si) over a 2-year mission with 2mm Al shielding. The Xilinx MPSoC and commercial ADCS components are generally resilient up to 10-20 krad. **TID is a Low Risk.**
- **SEE (Single Event Effects)**: High probability of SEUs in configuration memory (CRAM) and Block RAM (BRAM). **SEU is a High Risk.**

## 3. Mitigation Architecture

### 3.1 Firmware/Hardware Level (FPGA Fabric)
- **SEM IP (Soft Error Mitigation)**: We will implement the Xilinx SEM IP core to continuously scan the FPGA Configuration RAM.
  - **Correction**: Automatic correction of single-bit errors via ECC.
  - **Detection**: Flagging of multi-bit errors requiring partial reconfiguration or subsystem reset.
- **TMR (Triple Modular Redundancy)**: Critical control paths (e.g., interfaces to the ADCS and watchdog timers) will be instantiated using Local TMR within the FPGA fabric.

### 3.2 Software Level (Processing System - ARM Cortex)
- **Watchdog Timers (WDT)**: Dual-layer WDTs. A software WDT running on the RTOS, monitored by a hardware WDT in the PL (Programmable Logic).
- **Memory ECC**: L1/L2 caches and external DDR4 memory must have ECC enabled.
- **Golden Image Fallback**: The persistent memory (eMMC/NOR Flash) will store three bitstreams:
  1. Boot.bin (Active)
  2. Boot_Backup_1.bin
  3. Golden_Boot.bin (Read-only, bare-minimum recovery firmware)

### 3.3 System Level (AOCS & Power)
- **Latch-up Protection**: Rad-hard LDOs and power switches with over-current protection (auto-trip and power cycle) to prevent Single Event Latch-up (SEL) from permanently damaging the RF PA or MPSoC.
- **ADCS Safe Mode**: If the OBC reboots due to an SEU, the ADCS will autonomously enter "Sun-Pointing Safe Mode" using analog sun sensors and magnetorquers, ensuring positive power generation while the main SDR recovers.

## 4. Testing & Validation Plan
- **Fault Injection**: Prior to launch, the Software team will use the Xilinx Fault Injection tool to simulate CRAM bit flips and verify the SEM IP and Watchdog recovery times.
- **Requirement**: System recovery from a multi-bit SEU must take < 30 seconds to minimize data loss during a 10-minute ground station pass.
