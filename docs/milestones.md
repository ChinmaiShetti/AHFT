# Milestone status

## Milestone 0 — complete in software, hardware pending

- Host protocol encoding/decoding and validation: implemented.
- Host serial transport and request correlation: implemented.
- ESP-IDF ping/identify receiver: implemented.
- Mock transport tests: implemented.
- Physical flash/serial test: pending ESP-IDF installation and ESP32 availability.

## Next: Milestone 1

Add a bounded baseline experiment on the ESP32: explicit configuration validation, absolute periodic task releases, raw timing samples, heap/stack observations, reset metadata, and telemetry batches. The host must parse and recompute metrics before any adaptive layer is introduced.

