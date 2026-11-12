# AHFT Milestone 0 architecture

The Raspberry Pi host owns orchestration and persistence. The Arduino Nano is the device under test and independently validates commands. The current seam is deliberately small: a transport-independent Python bridge speaks versioned NDJSON to an Arduino sketch over the Nano's USB-serial adapter.

The host protocol module is deterministic and testable without hardware. `SerialBridge` handles framing, correlation IDs, malformed-line tolerance, timeouts, and device error responses. `ConnectionManager` owns lifecycle state and exposes only the current smoke-test operations. Future experiment and safety layers should call the bridge only after host-side validation.

The firmware responds only to `ping` and `identify` in Milestone 0. It does not execute experiments or claim timing/resource results. The classic Nano has no FreeRTOS and only 2 KB SRAM, so Milestone 1 must use timer-based execution and bounded fixed buffers rather than ESP32/FreeRTOS assumptions.

