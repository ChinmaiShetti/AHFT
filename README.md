# AHFT

Adaptive Hardware Fuzzing Testbench: a safety-constrained framework for discovering and characterizing embedded runtime failures.

## Current status

Milestone 0 is implemented:

- Versioned NDJSON protocol with strict framing and validation.
- Host serial bridge with request timeouts and device reset/disconnect handling.
- Native ESP-IDF firmware foundation for `ping` and `identify`.
- Mock-transport unit and integration tests.
- No hardware experiment execution, adaptive ML, dashboard, or peripheral diagnostics yet.

Actual ESP32 flashing and hardware serial validation remain pending until ESP-IDF and a board are available.

## Host setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
python -m pytest
```

Run a hardware smoke test after connecting the board:

```powershell
python raspberry_pi/main.py --port COM5
```

On Raspberry Pi, use the corresponding device path, for example `/dev/ttyUSB0`.

## ESP32 setup

Install ESP-IDF using Espressif's supported installer, then open an ESP-IDF terminal:

```powershell
cd esp32
idf.py set-target esp32
idf.py build
idf.py -p COM5 flash monitor
```

The firmware uses UART0 at 115200 baud and accepts one JSON message per line. Confirm the board's USB/UART arrangement before flashing. Do not connect or test unknown electrical wiring through this project.

## Repository layout

- `raspberry_pi/ahft/communication/`: host protocol and serial lifecycle.
- `esp32/main/`: minimal ESP-IDF command receiver and responses.
- `protocol/`: wire-level specification and schema.
- `tests/`: host-only tests that do not claim hardware validation.
- `docs/`: architecture and milestone notes.

