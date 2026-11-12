# AHFT

Adaptive Hardware Fuzzing Testbench: a safety-constrained framework for discovering and characterizing embedded runtime failures.

## Current status

Milestone 0 is implemented:

- Versioned NDJSON protocol with strict framing and validation.
- Host serial bridge with request timeouts and device reset/disconnect handling.
- Native Arduino Nano firmware foundation for `ping` and `identify`.
- Mock-transport unit and integration tests.
- No hardware experiment execution, adaptive ML, dashboard, or peripheral diagnostics yet.

Actual Nano upload and hardware serial validation remain pending until a board and USB cable are available.

## Hardware target and plug-and-play connection

The current target is the classic Arduino Nano using the ATmega328P, normally a 5 V / 16 MHz board. This is not the Nano Every or Nano 33 series.

For Milestone 0, the hardware engineer needs only:

| Item | Connection |
|---|---|
| Arduino Nano | Connect directly to the development computer with a data-capable USB cable |
| External wiring | None |
| Sensors/peripherals | None |
| Power | USB supplies the board |
| Serial pins | No jumper wiring; the USB-serial adapter exposes the Nano `Serial` port |

Do not connect external voltages, motors, sensors, or experimental wiring for this smoke test. Do not power the board from USB and an external supply at the same time. Close Arduino Serial Monitor before running the Python host because only one program can own the serial port.

### Arduino IDE upload settings

1. Install Arduino IDE 2.x.
2. Open `arduino_nano/AHFT_Nano/AHFT_Nano.ino`.
3. Select `Tools > Board > Arduino AVR Boards > Arduino Nano`.
4. Select `Tools > Processor > ATmega328P`.
5. If upload fails on a common clone, retry with `ATmega328P (Old Bootloader)`.
6. Select the COM port shown when the Nano is connected.
7. Upload the sketch.

No Arduino library is required beyond the standard Arduino core. A clone with a CH340 USB-serial chip may require its matching driver. Use a USB data cable, not a charge-only cable.

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

## Nano smoke test

```powershell
cd C:\Users\chinm\Desktop\AHFT
\.venv\Scripts\Activate.ps1
python raspberry_pi/main.py --port COM5
```

Replace `COM5` with the port assigned to the Nano. On Raspberry Pi, use `/dev/ttyUSB0` or `/dev/ttyACM0`. Expected output contains a `pong` response followed by `device_info` identifying the Arduino Nano ATmega328P.

The firmware uses 115200 baud, 8 data bits, no parity, and 1 stop bit. It accepts one JSON message per line. The Nano input buffer is intentionally limited to 240 bytes because the ATmega328P has only 2 KB SRAM.

## Repository layout

- `raspberry_pi/ahft/communication/`: host protocol and serial lifecycle.
- `arduino_nano/AHFT_Nano/`: Arduino Nano command receiver and responses.
- `protocol/`: wire-level specification and schema.
- `tests/`: host-only tests that do not claim hardware validation.
- `docs/`: architecture and milestone notes.

