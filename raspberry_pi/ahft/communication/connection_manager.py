"""Connection lifecycle and device smoke-test operations."""

from __future__ import annotations

from enum import Enum
from .serial_bridge import SerialBridge


class ConnectionState(str, Enum):
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    FAULTED = "faulted"


class ConnectionManager:
    def __init__(self, bridge: SerialBridge) -> None:
        self.bridge = bridge
        self.state = ConnectionState.DISCONNECTED

    def connect(self) -> None:
        try:
            self.bridge.open()
        except Exception:
            self.state = ConnectionState.FAULTED
            raise
        self.state = ConnectionState.CONNECTED

    def close(self) -> None:
        self.bridge.close()
        self.state = ConnectionState.DISCONNECTED

    def ping(self):
        return self.bridge.request("ping")

    def identify(self):
        return self.bridge.request("identify")

