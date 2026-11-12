# Milestone status

## Milestone 0 — complete in software, hardware pending

- Host protocol encoding/decoding and validation: implemented.
- Host serial transport and request correlation: implemented.
- Arduino Nano ATmega328P ping/identify receiver: implemented.
- Mock transport tests: implemented.
- Physical upload/serial test: pending Arduino IDE installation and Nano availability.

## Next: Milestone 1

Add a bounded baseline experiment for the ATmega328P: explicit configuration validation, timer-based periodic execution, raw timing samples, SRAM observations, reset/recovery metadata where available, and telemetry batches. The host must parse and recompute metrics before any adaptive layer is introduced.

