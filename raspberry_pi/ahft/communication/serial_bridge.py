"""Transport-independent serial request/response bridge."""

from __future__ import annotations

from collections.abc import Callable
import itertools
import time
from typing import Any, Protocol

from .protocol import Message, ProtocolError, decode_message, encode_message


class LineTransport(Protocol):
    def open(self) -> None: ...
    def close(self) -> None: ...
    def write(self, data: bytes) -> None: ...
    def readline(self, timeout: float) -> bytes: ...


class PySerialTransport:
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 2.0) -> None:
        self.port, self.baudrate, self.timeout = port, baudrate, timeout
        self._serial: Any = None

    def open(self) -> None:
        try:
            import serial
        except ImportError as exc:
            raise RuntimeError("pyserial is required for hardware communication") from exc
        self._serial = serial.serial_for_url(self.port, baudrate=self.baudrate, timeout=self.timeout)

    def close(self) -> None:
        if self._serial is not None:
            self._serial.close()
            self._serial = None

    def write(self, data: bytes) -> None:
        if self._serial is None:
            raise ConnectionError("serial transport is not open")
        self._serial.write(data)

    def readline(self, timeout: float) -> bytes:
        if self._serial is None:
            raise ConnectionError("serial transport is not open")
        self._serial.timeout = timeout
        return bytes(self._serial.readline())


class SerialBridge:
    def __init__(self, transport: LineTransport, default_timeout: float = 2.0, id_factory: Callable[[], str] | None = None) -> None:
        self.transport = transport
        self.default_timeout = default_timeout
        self._ids = itertools.count(1)
        self._id_factory = id_factory or (lambda: f"host-{next(self._ids)}")

    def open(self) -> None:
        self.transport.open()

    def close(self) -> None:
        self.transport.close()

    def request(self, msg_type: str, payload: dict[str, Any] | None = None, timeout: float | None = None) -> Message:
        request_id = self._id_factory()
        request = Message(1, msg_type, request_id, payload)
        self.transport.write(encode_message(request))
        deadline = time.monotonic() + (self.default_timeout if timeout is None else timeout)
        while time.monotonic() < deadline:
            line = self.transport.readline(max(0.0, deadline - time.monotonic()))
            if not line:
                continue
            try:
                response = decode_message(line)
            except ProtocolError:
                continue
            if response.in_reply_to == request_id or response.id == request_id:
                if response.type == "error":
                    detail = (response.payload or {}).get("message", "device returned an error")
                    raise ProtocolError(str(detail))
                return response
        raise TimeoutError(f"timed out waiting for response to {request_id}")

