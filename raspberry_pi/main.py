"""AHFT host smoke-test CLI for Milestone 0."""

from __future__ import annotations

import argparse
import logging

from ahft.communication.connection_manager import ConnectionManager
from ahft.communication.serial_bridge import PySerialTransport, SerialBridge


def main() -> int:
    parser = argparse.ArgumentParser(description="AHFT ESP32 communication smoke test")
    parser.add_argument("--port", required=True, help="Serial port, e.g. COM5 or /dev/ttyUSB0")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    transport = PySerialTransport(args.port, args.baud, args.timeout)
    manager = ConnectionManager(SerialBridge(transport, default_timeout=args.timeout))
    try:
        manager.connect()
        print(manager.ping())
        print(manager.identify())
    finally:
        manager.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

