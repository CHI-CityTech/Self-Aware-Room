# SAR Environmental Node: Stage C Custom Breakout BOM

**Project:** Self-Aware Room (SAR)  
**Center:** Center for Holistic Integration (CHI), New York City College of Technology  
**Modality:** Environmental Sensing  
**Target Node:** ESP32 + Bosch BME680 (bare chip, in-house assembled breakout)  
**Stage:** Stage C — Custom Breakout Fabrication (Bill of Materials)  
**Author:** Jabber Bin Kibria  
**Supervisor:** Professor David B. Smith  
**Date:** November 2, 2026  

---

## 1. Objective
Utilize the lab's existing stock of bare Bosch BME680 sensor chips by fabricating custom breakout boards based on Adafruit's open-source BME680 breakout design, and assembling them in-house using hot air reflow. Each finished board is intended to be a drop-in replacement for the commercial Adafruit BME680 breakout validated in Stage B, so the existing firmware and wiring can be reused without changes.

## 2. Design Source
The PCB design is Adafruit's open-source BME680 breakout (the same board used in Stage B), released under **Creative Commons Attribution/Share-Alike (CC BY-SA)**. Attribution to Adafruit Industries must be kept in this repository, and any modified version of the design must be shared under the same license.

* **Design files (EagleCAD .brd / .sch):** [adafruit/Adafruit-BME680-PCB](https://github.com/adafruit/Adafruit-BME680-PCB)
* **Product page (reference board):** [Adafruit BME680 — Product 3660](https://www.adafruit.com/product/3660)
* **Pinouts and schematic guide:** [Adafruit BME680 Learn Guide](https://learn.adafruit.com/adafruit-bme680-humidity-temperature-barometic-pressure-voc-gas)

The repository contains two board versions:
* `Adafruit BME680.brd` / `.sch` — current version (expected to be the STEMMA QT revision)
* `Adafruit BME680 Original.brd` / `.sch` — earlier version

**Selected:** `Adafruit BME680.brd` (STEMMA QT revision). Confirm in the board viewer that the layout includes the two JST SH 4-pin connectors before ordering.

**Note on power:** The design includes a 3.3 V regulator and level shifting for 5 V compatibility. These are not required for the ESP32 but are kept to use the proven design unmodified. The Stage B board is this same design and runs correctly from the ESP32's 3V3 pin.

**Previous Stage References:**
* [SAR_BOM_Environmental_Node_Stage_A_Breadboard_V1_2026-10-08.md](https://github.com/JabberBinKibria/Self-Aware-Room/blob/main/docs/sensors/SAR_BOM_Environmental_Node_Stage_A_Breadboard_V1_2026-10-08.md)
* [SAR_Environmental_Node_Wired_Baseline_V1_2026-11-01.md](https://github.com/JabberBinKibria/Self-Aware-Room/blob/main/docs/sensors/Sar_Environmental_Node_Wired_Baseline_Validation.md)

## 3. Bill of Materials

**N** = number of breakout boards to assemble (one per bare BME680 chip). Order passives with extra quantity, since 0603 parts are easily lost during hand assembly.

### 3.1 Items Already On Hand

| Item | Description | Qty | Status |
|---|---|---|---|
| Bosch BME680 (bare chip) | 8-pin metal-lid LGA, 3.0 × 3.0 mm, U1 on the breakout | N | On hand (lab stock) |
| Hot air rework station | Reflow of the BME680 and small SMD parts | 1 | On hand |
| Soldering iron | Passives, connectors, header pins, touch-up | 1 | On hand |
| Inland ESP32-WROOM-32 | Test host for validating each assembled board | 1+ | On hand (Stage B) |
| Adafruit BME680 breakout (commercial) | Reference board for side-by-side validation | 1 | On hand (Stage B) |

### 3.2 PCB Fabrication

| Item | Description | Qty | Est. Cost | Vendor Options |
|---|---|---|---|---|
| Bare PCB, Adafruit BME680 design | Fabricated from `Adafruit BME680.brd` | N + 2 spares | $2–10 + shipping | [JLCPCB](https://jlcpcb.com) (requires Gerber export), [OSH Park](https://oshpark.com) (accepts Eagle .brd directly) |
| SMT solder paste stencil | Matches the top paste layer of the board; required for even solder height under the LGA chip | 1 | $7–15 | Order with the PCBs (JLCPCB) or separately (OSH Stencils for OSH Park) |

**Gerber export (for JLCPCB):** Open the Eagle files in [KiCad](https://www.kicad.org) (File → Import → EAGLE Project), then plot Gerbers and drill files. The 2 spare boards are reserved for hot air practice before using real chips.

### 3.3 Board Components (per breakout)

Parts and quantities below were read from Adafruit's *Schematic & Fabrication Print - STEMMA QT Version* (BME680 rev D) in the Adafruit Learn Guide. Capacitor values were read from the schematic. Individual resistor values are not fully legible at the published resolution (most appear to be 10 kΩ); they are covered by the 0603 resistor kit and will be verified from the full-resolution schematic or the Eagle files during assembly.

| Ref | Item | Schematic Section | Qty / board | Part | Est. Cost |
|---|---|---|---|---|---|
| U1 | Bosch BME680 | Sensor | 1 | On hand | — |
| U2 | 3.3 V LDO voltage regulator, SOT-23-5 | Power supply | 1 | AP2112K-3.3 | ~$0.50 |
| C1–C3 | Capacitors (regulator input/output) | Power supply | 3 | 10 µF (×2), 0.1 µF (×1); 0603 capacitor kit | Kit ~$10 |
| LED1 | Green indicator LED, SMD | ON LED | 1 | Package to be read from the .brd file | ~$0.10 |
| R | Resistor (LED current limit) | ON LED | 1 | Value from schematic; 0603 resistor kit | Kit ~$10 |
| Q1–Q2 | N-channel MOSFET, SOT-23 (level shifting on SCK and SDI) | I2C Pullups & Shift | 2 | BSS138 | ~$0.20 each |
| R | Resistors (level shifter, 2 to VIN side, 2 to 3.3 V side) | I2C Pullups & Shift | 4 | Values from schematic; 0603 resistor kit | (same kit) |
| R | Resistors (CS and SDO pull-ups) | I2C Pullups | 2 | Values from schematic; 0603 resistor kit | (same kit) |
| D1 | Small-signal diode on CS line | I2C Pullups | 1 | 1N4148-type; package to be read from the .brd file | ~$0.10 |
| JP | Address solder jumper (SDO to GND) | I2C Pullups | — | PCB feature, no part to buy | — |
| J1–J2 | JST SH 4-pin SMD right-angle connector (STEMMA QT / Qwiic) | STEMMA/I2C Headers | 2 | JST SM04B-SRSS-TB | ~$0.50 each |
| JP1 | 7-pin 0.1" (2.54 mm) male header | Header | 1 | Break from header strip | ~$1/strip |

**Per-board totals:** 7 resistors, 3 capacitors, 2 MOSFETs, 1 diode, 1 LED, 1 regulator, 2 JST connectors, 1 header, 1 BME680.

**Optional simplification:** The ON LED and its resistor can be left unpopulated without affecting the sensor.

### 3.4 Assembly Consumables (required)

| Item | Purpose | Qty | Est. Cost |
|---|---|---|---|
| Lead-free no-clean solder paste, Type 4 (e.g., SAC305) | Stencil-applied paste for hot air reflow. Type 4 suits the 0.4 × 0.4 mm BME680 pads. Store refrigerated. | 1 syringe/jar | $15–30 |
| Polyimide (Kapton-type) tape, silicone-free adhesive if available | Covering the BME680 vent hole during soldering (Bosch requirement) | 1 roll | ~$10 |
| Nitrile gloves | Silicone-free handling of sensors (Bosch requirement) | 1 box | ~$10 |
| No-clean flux | Rework and touch-up | 1 pen/syringe | ~$10 |
| Digital hygrometer | Confirming humidity during post-reflow reconditioning | 1 | $10–15 |

### 3.5 Connection to ESP32

| Item | Purpose | Qty | Est. Cost |
|---|---|---|---|
| STEMMA QT / Qwiic JST SH 4-pin to male header cable | Connecting each breakout to the ESP32 on a breadboard | N | ~$1 each |

### 3.6 Estimated Total (excluding on-hand items)

| Category | Est. Cost |
|---|---|
| PCBs + stencil | $10–25 + shipping |
| Board components (kits + ICs + connectors for N boards) | $25–40 |
| Assembly consumables | $55–75 |
| Cables | ~$1 × N |
| **Total** | **≈ $90–140 + shipping** |

## 4. Bosch Handling and Soldering Requirements
Summarized from the official Bosch document *BME680: Handling, Soldering and Mounting Instructions* (BST-BME680-HS000): [PDF](https://www.mouser.lt/pdfDocs/bst-bme680-hs000.pdf)

* **Reflow limits:** Peak temperature up to 260 °C for 20–40 seconds. Maximum of 3 reflow cycles per chip (every rework counts).
* **No baking before soldering:** The BME680 is moisture sensitivity level 1 and must not be dry-baked before soldering.
* **Vent hole:** Cover with a silicone-free protective layer during soldering and any cleaning.
* **Handling:** ESD precautions and silicone-free (nitrile) gloves. Keep away from adhesives, lacquers, sprays, and hand lotion.
* **No liquids:** Do not wash boards or soak/splash the sensor (no IPA bath, no ultrasonic cleaning). Use no-clean paste and flux.
* **Post-reflow reconditioning (mandatory for humidity accuracy):** Either dry-bake at 125 °C / <5% RH for 6 h followed by re-hydration at 25 °C / 80% RH for 24 h, **or** (no-bake alternative) store at 25 °C and >50% RH for more than 5 days. The no-bake alternative will be used, verified with the hygrometer.
* **Storage:** Original packaging, 10–50 °C and 20–60% RH.
* **Engineering samples:** Chips marked with `*`, `E`, or `e` may not meet production specifications.

## 5. Planned Assembly and Validation Workflow
1. Inspect chip markings and record the lot code for traceability.
2. Practice paste application and hot air reflow on the 2 spare PCBs.
3. Apply paste with the stencil, place passives and the BME680, cover the vent hole with polyimide tape.
4. Reflow with hot air (low airflow, gradual preheat, stop once the paste flows and the chip self-aligns). Let the board cool naturally.
5. Solder connectors and header pins with the iron.
6. Check for shorts between VIN, GND, SCK, and SDI with a multimeter.
7. Run an I2C scan on the ESP32 and confirm the sensor at address `0x77`.
8. Recondition for >5 days at >50% RH.
9. Validate each board side by side with the commercial Adafruit reference board using the Stage B firmware, and record the results in a Stage C validation document.

## 6. Open Items
* Confirm the number of bare BME680 chips on hand (sets **N**).
* Verify the individual resistor values, and the LED and diode packages, from the full-resolution schematic or Eagle files (covered by kits for purchasing).
* Confirm the selected `.brd` file is the STEMMA QT revision (rev D).
* Check chip markings for engineering samples.

---

*PCB design by Limor Fried/Ladyada for Adafruit Industries, licensed under Creative Commons Attribution/Share-Alike. Source: [github.com/adafruit/Adafruit-BME680-PCB](https://github.com/adafruit/Adafruit-BME680-PCB).*
