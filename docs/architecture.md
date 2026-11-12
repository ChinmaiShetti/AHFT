# AHFT Milestone 0 architecture

The Raspberry Pi host owns orchestration and persistence. The ESP32 is the device under test and independently validates commands. The current seam is deliberately small: a transport-independent Python bridge speaks versioned NDJSON to a native ESP-IDF UART receiver.

The host protocol module is deterministic and testable without hardware. `SerialBridge` handles framing, correlation IDs, malformed-line tolerance, timeouts, and device error responses. `ConnectionManager` owns lifecycle state and exposes only the current smoke-test operations. Future experiment and safety layers should call the bridge only after host-side validation.

The firmware responds only to `ping` and `identify` in Milestone 0. It does not execute experiments or claim timing/resource results. This keeps the first hardware boundary auditable before adding FreeRTOS workload generation.

