# Bill of Materials (BOM): Stage A Breadboard Prototype

**Project:** Self-Aware Room (SAR)  
**Center:** Center for Holistic Integration (CHI), New York City College of Technology  
**Modality:** Environmental Sensing  
**Target Node:** ESP32 + Bosch BME680 Proof of Concept  
**Stage:** Stage A — Breadboard Proof of Concept  
**Author:** Jabber Bin Kibria  
**Supervisor:** Professor David B. Smith  
**Date:** October 8, 2026  

---

## 1. Overview and Purpose

This Bill of Materials (BOM) specifies the hardware, wiring, and interface components required to construct the initial **Stage A — Breadboard Proof of Concept** for the SAR Environmental Sensor Node. 

The objective of this stage is to verify baseline hardware acquisition, establish electrical continuity over I2C, and provide an initial test platform for the SAR Shared Streaming Contract without permanent soldering or custom enclosure fabrication.

---

## 2. Component Breakdown

| Item | Component | Specification / Model | Qty | Estimated Unit Cost | Source / Vendor | Purpose / Function |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| **1** | Environmental Sensor Breakout | Bosch Sensortec BME680 | 1 | ~$19.00 | Adafruit / SparkFun | Samples ambient temperature, relative humidity, barometric pressure, and VOC gas resistance. |
| **2** | Microcontroller Dev Board | ESP32-WROOM-32 (30-pin DevKit) | 1 | ~$6.00 | Espressif / Lab Stock | L0 edge acquisition controller and serial transport interface. |
| **3** | Solderless Breadboard | Full-Size (830 tie-points) | 1 | ~$5.00 | Lab Stock | Prototyping bus for power distribution and I2C lines. |
| **4** | Jumper Wires | Premium Dupont (Male-to-Male) | 6–10 | ~$2.00 | Lab Stock | Direct connections for 3V3, GND, SDA, and SCL lines. |
| **5** | USB Interface Cable | USB-A to Micro-USB (or USB-C) | 1 | ~$4.00 | Lab Stock | Provides 5V logic power and handles 115200-baud UART data transmission. |
| **6** | Power Supply | 5V 2A Regulated USB Adapter / Battery | 1 | ~$8.00 | Lab Stock | Regulated DC power source for standalone bench testing. |

**Total Estimated Prototype Cost:** ~$44.00

---

## 3. Hardware Interconnect and Pinout Reference

The BME680 communicates with the ESP32 microcontroller using hardware I2C over GPIO 21 and GPIO 22.

| BME680 Sensor Pin | ESP32 Dev Board Pin | Description / Electrical Constraints |
| :--- | :--- | :--- |
| **VIN / VCC** | **3V3** | 3.3V Logic Supply (Do not connect to 5V/VIN) |
| **GND** | **GND** | Common Ground Reference |
| **SCL / SCK** | **GPIO 22** | Hardware I2C Serial Clock Line |
| **SDA / SDI** | **GPIO 21** | Hardware I2C Serial Data Line |
| **CS** | *Floating / Unconnected* | Chip Select pulled high internally for I2C mode |
| **SDO / ADDR** | *Floating or GND* | Sets default I2C address (0x77 default; 0x76 if tied to GND) |

---

## 4. Hardware Verification and Acceptance Criteria

Before advancing to Stage B (Characterized Prototype), the Stage A assembly must satisfy the following checks:

1. **Power Verification:** Multi-meter check confirms stable 3.3V at the BME680 `VIN` pin relative to `GND`.
2. **I2C Bus Detection:** Microcontroller scan successfully acknowledges the sensor at address `0x77` (or `0x76`).
3. **Data Link Continuity:** Firmware performs a successful register read across all four environmental modalities without bus stalls or I2C timeouts.
