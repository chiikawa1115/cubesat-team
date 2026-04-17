# D-GEM-002: BOM Supply Chain & Risk Assessment v1

## 1. Executive Summary
To ensure manufacturability for the Phase D integration, PM Agent has validated the critical RF and FPGA components against current market availability and lead times. Real-world component shortages pose a higher risk to Phase D than design flaws.

## 2. Critical Components Assessment

### 2.1 OBC & SDR Brain: Xilinx Zynq UltraScale+ (XCZU3EG-1SFVC784I)
- **Current Status**: High Risk
- **Lead Time**: > 40 weeks (Allocated)
- **Mitigation**: 
  1. We must secure stock immediately through secondary distributors or Avnet.
  2. Backup option: Down-grade to Zynq-7000 series if Rel-17 processing can be offloaded, but this requires major FW rework. Not recommended.

### 2.2 S-band Power Amplifier: Qorvo/Analog Devices GaN PA (10W+)
- **Current Status**: Medium Risk
- **Lead Time**: 12-16 weeks
- **Mitigation**: GaN components are subject to export controls (EAR). End-user certificates must be prepared immediately by the procurement team.

### 2.3 ADCS Reaction Wheels & Sensors
- **Current Status**: Low Risk
- **Lead Time**: 8-10 weeks (COTS from GomSpace/CubeSpace)
- **Mitigation**: Place order upon Phase D kickoff.

## 3. Action Items
- [ ] **CEO/Procurement**: Sign off on immediate purchase of Xilinx MPSoC to mitigate the 40-week lead time.
- [ ] **Legal**: Begin EAR compliance paperwork for the GaN PA.
