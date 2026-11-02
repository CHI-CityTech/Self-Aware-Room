# SAR Environmental Node: Wired Baseline Validation

**Project:** Self-Aware Room (SAR)  
**Center:** Center for Holistic Integration (CHI), New York City College of Technology  
**Modality:** Environmental Sensing  
**Target Node:** ESP32 + Bosch BME680 Proof of Concept  
**Stage:** Stage B — Wired Baseline Validation  
**Author:** Jabber Bin Kibria  
**Supervisor:** Professor David B. Smith  
**Date:** November 1, 2026  

---

## 1. Objective
Validate the baseline physical data ingestion pipeline for the Self-Aware Room (SAR) project by establishing a stable, wired serial connection between the Adafruit BME680 environmental sensor and the Inland ESP32-WROOM-32 microcontroller.

## 2. Hardware Preparation
The BME680 breakout board was prepared by soldering the bottom header pins to allow flush mounting on a standard breadboard.

![BME680 Front](IMG_6058.jpeg)
![BME680 Back Pins](IMG_6057.jpeg)

## 3. Wiring and Pinout Architecture
The BME680 supports both I2C and SPI. For this architecture, I2C was selected. 

**Reference Documentation:**
* [Adafruit BME680 Pinouts](https://learn.adafruit.com/adafruit-bme680-humidity-temperature-barometic-pressure-voc-gas/pinouts)
* [ESP32 Pinout Reference](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/hw-reference/esp32/get-started-devkitc.html#pin-layout)
* Previous Stage Reference: [SAR_BOM_Environmental_Node_Stage_A_Breadboard_V1_2026-10-08.md](https://github.com/JabberBinKibria/Self-Aware-Room/blob/main/docs/sensors/SAR_BOM_Environmental_Node_Stage_A_Breadboard_V1_2026-10-08.md)

Initial wiring attempts incorrectly bridged the I2C data lines to the breadboard's power rails. This was corrected to a direct point-to-point architecture bypassing the unpowered side rails:
* **VIN** (BME680) -> **3V3** (ESP32)
* **GND** (BME680) -> **GND** (ESP32)
* **SCK** (BME680 SCL) -> **IO22** (ESP32)
* **SDI** (BME680 SDA) -> **IO21** (ESP32)

![ESP32 Pinout Back](IMG_6059.jpeg)
![Breadboard Top Down](IMG_6063.jpeg)
![Breadboard Angled](IMG_6067.jpeg)

## 4. Workstation Configuration & Driver Troubleshooting
Upon connecting the ESP32 via USB, the Arduino IDE failed to recognize the COM port.
* **Diagnosis:** Windows Device Manager threw an error for the CP2102 USB to UART Bridge Controller due to missing drivers.
* **Resolution:** Installed the CP210x Universal Windows Driver (v11.6.0). The ESP32 successfully enumerated as `COM11` and the profile was set to **ESP32 Dev Module**.

## 5. Firmware Implementation
To prevent log flooding, the C++ firmware was engineered with a threshold-based reporting mechanism. The script only transmits data over the serial interface when environmental changes exceed defined deltas (0.5 °C for temperature, 1.0% for humidity, 0.5 hPa for pressure, and 5.0 KOhms for gas resistance).

![Arduino IDE Firmware Script](IMG_6068.jpeg)
