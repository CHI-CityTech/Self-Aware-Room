/*
 * SAR Environmental Node - BME680 wired baseline
 *
 * Project:    Self-Aware Room (SAR), Center for Holistic Integration (CHI),
 *             New York City College of Technology
 * Author:     Jabber Bin Kibria
 * Supervisor: Professor David B. Smith
 *
 * Hardware:   ESP32-WROOM-32 dev board + Adafruit BME680 breakout (I2C)
 * Wiring:     BME680 VIN -> 3V3, GND -> GND, SCK (SCL) -> IO22, SDI (SDA) -> IO21
 * Libraries:  Adafruit BME680 Library, Adafruit Unified Sensor
 * Language:   C++
 *
 * Output:     One JSON object per line on USB serial (115200 baud). Each line
 *             is an L0 frame following the SAR Shared Streaming Contract
 *             (D01.02) and the Environmental Streaming Profile (D01.02.06).
 *             The node is an event-based source: a frame is an event, and
 *             "payload" holds the measurements taken at that event.
 *             Lines starting with '#' are human-readable status messages and
 *             are not frames; the receiver skips them.
 *
 * Receiver:   env_node_receiver.py reads these lines, adds a
 *             timestamp, and saves them on the computer the node is plugged into.
 *
 * Events:     The sensor is sampled every SAMPLE_INTERVAL_MS. A frame is sent
 *             only for an event: "startup" (first reading), "change" (a value
 *             moved past its threshold since the last sent frame), or
 *             "heartbeat" (HEARTBEAT_INTERVAL_MS passed with no change).
 */

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>

// ---------------------------------------------------------------- Identity
// Placeholder IDs until the SAR sensor ID scheme (issue #22) is settled.
const char* const SOURCE_NODE_ID   = "esp32_env_01";
const char* const SOURCE_ID        = "bme680_01";
const char* const MODALITY         = "environmental";
const char* const SENSOR_MODEL     = "BME680";
const char* const FIRMWARE_VERSION = "sar_env_node_bme680/1.2.0";

// ---------------------------------------------------------------- Hardware
const uint8_t  I2C_SDA_PIN     = 21;
const uint8_t  I2C_SCL_PIN     = 22;
const uint8_t  BME680_I2C_ADDR = 0x77;   // 0x76 if SDO is tied to GND
const uint32_t SERIAL_BAUD     = 115200;

// ------------------------------------------------------- Sensor settings
const uint16_t GAS_HEATER_TEMP_C      = 320;
const uint16_t GAS_HEATER_DURATION_MS = 150;

// ------------------------------------------------------------------ Events
const uint32_t SAMPLE_INTERVAL_MS    = 2000;
const uint32_t HEARTBEAT_INTERVAL_MS = 60000;
const uint32_t SENSOR_RETRY_MS       = 2000;

const float THRESHOLD_TEMPERATURE_C         = 0.5f;
const float THRESHOLD_RELATIVE_HUMIDITY_PCT = 1.0f;
const float THRESHOLD_PRESSURE_HPA          = 0.5f;
const float THRESHOLD_GAS_RESISTANCE_OHM    = 5000.0f;

// ------------------------------------------------------------------- State
struct Reading {
  float temperatureC;
  float relativeHumidityPct;
  float pressureHpa;
  float gasResistanceOhm;
  bool  gasHeaterStable;
};

Adafruit_BME680 bme;

Reading  lastEmitted   = {0, 0, 0, 0, false};
bool     hasEmitted    = false;
uint32_t lastEmitMs    = 0;
uint32_t lastSampleMs  = 0;
uint32_t frameIndex    = 0;
uint32_t sessionId     = 0;

// ----------------------------------------------------------------- Helpers

// Returns the event this reading represents, or nullptr if there is no event to send.
const char* eventTypeFor(const Reading& r, uint32_t nowMs) {
  if (!hasEmitted) {
    return "startup";
  }
  if (fabsf(r.temperatureC - lastEmitted.temperatureC) >= THRESHOLD_TEMPERATURE_C ||
      fabsf(r.relativeHumidityPct - lastEmitted.relativeHumidityPct) >= THRESHOLD_RELATIVE_HUMIDITY_PCT ||
      fabsf(r.pressureHpa - lastEmitted.pressureHpa) >= THRESHOLD_PRESSURE_HPA ||
      fabsf(r.gasResistanceOhm - lastEmitted.gasResistanceOhm) >= THRESHOLD_GAS_RESISTANCE_OHM) {
    return "change";
  }
  if (nowMs - lastEmitMs >= HEARTBEAT_INTERVAL_MS) {
    return "heartbeat";
  }
  return nullptr;
}

void emitFrame(const Reading& r, const char* eventType, uint32_t nowMs, uint32_t latencyMs) {
  // Base contract fields (D01.02)
  Serial.printf("{\"source_node_id\":\"%s\",\"source_id\":\"%s\",\"modality\":\"%s\","
                "\"frame_index\":%lu,\"source_latency_ms\":%lu,",
                SOURCE_NODE_ID, SOURCE_ID, MODALITY,
                (unsigned long)frameIndex, (unsigned long)latencyMs);

  // Environmental profile fields (D01.02.06): what happened and the reporting rules in force
  Serial.printf("\"sensor_model\":\"%s\",\"event_type\":\"%s\",\"sample_interval_ms\":%lu,"
                "\"heartbeat_interval_ms\":%lu,",
                SENSOR_MODEL, eventType, (unsigned long)SAMPLE_INTERVAL_MS,
                (unsigned long)HEARTBEAT_INTERVAL_MS);
  Serial.printf("\"threshold_temperature_c\":%.2f,\"threshold_relative_humidity_pct\":%.2f,"
                "\"threshold_pressure_hpa\":%.2f,\"threshold_gas_resistance_ohm\":%.0f,",
                THRESHOLD_TEMPERATURE_C, THRESHOLD_RELATIVE_HUMIDITY_PCT,
                THRESHOLD_PRESSURE_HPA, THRESHOLD_GAS_RESISTANCE_OHM);
  Serial.printf("\"source_session_id\":\"%08lx\",\"source_uptime_ms\":%lu,\"firmware_version\":\"%s\",",
                (unsigned long)sessionId, (unsigned long)nowMs, FIRMWARE_VERSION);

  // Sensor configuration is static, so it is sent on startup events only
  if (strcmp(eventType, "startup") == 0) {
    Serial.printf("\"sensor_config\":{\"oversampling_temperature\":8,\"oversampling_humidity\":2,"
                  "\"oversampling_pressure\":4,\"iir_filter_size\":3,"
                  "\"gas_heater_temp_c\":%u,\"gas_heater_duration_ms\":%u},",
                  GAS_HEATER_TEMP_C, GAS_HEATER_DURATION_MS);
  }

  // Payload: the measurements themselves, raw, with no calibration applied
  Serial.printf("\"payload\":{\"temperature_c\":%.2f,\"relative_humidity_pct\":%.2f,"
                "\"pressure_hpa\":%.2f,\"gas_resistance_ohm\":%.0f,\"gas_heater_stable\":%s}}\n",
                r.temperatureC, r.relativeHumidityPct, r.pressureHpa,
                r.gasResistanceOhm, r.gasHeaterStable ? "true" : "false");
}

void configureSensor() {
  // Keep these in step with the oversampling/filter values sent in emitFrame().
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(GAS_HEATER_TEMP_C, GAS_HEATER_DURATION_MS);
}

// -------------------------------------------------------------------- Main

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(200);
  Serial.println();
  Serial.printf("# %s starting, node=%s\n", FIRMWARE_VERSION, SOURCE_NODE_ID);

  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);

  // Keep retrying instead of halting, so a loose wire can be fixed without a reset.
  while (!bme.begin(BME680_I2C_ADDR)) {
    Serial.printf("# ERROR BME680 not found at 0x%02X, check wiring; retrying\n", BME680_I2C_ADDR);
    delay(SENSOR_RETRY_MS);
  }
  configureSensor();

  sessionId = esp_random();
  lastSampleMs = millis() - SAMPLE_INTERVAL_MS;   // take the first sample right away
  Serial.println("# BME680 ready");
}

void loop() {
  const uint32_t nowMs = millis();
  if (nowMs - lastSampleMs < SAMPLE_INTERVAL_MS) {
    return;
  }
  lastSampleMs = nowMs;

  if (!bme.performReading()) {
    Serial.println("# WARN BME680 reading failed");
    return;
  }
  const uint32_t latencyMs = millis() - nowMs;

  Reading r;
  r.temperatureC        = bme.temperature;
  r.relativeHumidityPct = bme.humidity;
  r.pressureHpa         = bme.pressure / 100.0f;
  r.gasResistanceOhm    = (float)bme.gas_resistance;
  r.gasHeaterStable     = bme.gas_resistance > 0;   // library reports 0 when the gas reading is invalid

  const char* eventType = eventTypeFor(r, nowMs);
  if (eventType == nullptr) {
    return;   // nothing changed and no heartbeat is due
  }

  emitFrame(r, eventType, nowMs, latencyMs);
  lastEmitted = r;
  lastEmitMs  = nowMs;
  hasEmitted  = true;
  frameIndex++;
}
