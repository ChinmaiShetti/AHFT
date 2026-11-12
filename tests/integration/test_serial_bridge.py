from collections import deque

import pytest

from ahft.communication.protocol import Message, encode_message
from ahft.communication.connection_manager import ConnectionManager, ConnectionState
from ahft.communication.serial_bridge import SerialBridge


class MockTransport:
    def __init__(self, responses=()):
        self.responses = deque(responses)
        self.writes = []
        self.opened = False

    def open(self):
        self.opened = True

    def close(self):
        self.opened = False

    def write(self, data):
        self.writes.append(data)

    def readline(self, timeout):
        return self.responses.popleft() if self.responses else b""


class FailingTransport(MockTransport):
    def open(self):
        raise OSError("device unavailable")


def test_request_matches_correlated_response():
    transport = MockTransport([encode_message(Message(1, "pong", "device-response", in_reply_to="host-1"))])
    bridge = SerialBridge(transport, default_timeout=0.01, id_factory=lambda: "host-1")
    response = bridge.request("ping")
    assert response.type == "pong"
    assert b'"type":"ping"' in transport.writes[0]


def test_timeout_is_not_success():
    with pytest.raises(TimeoutError):
        SerialBridge(MockTransport(), default_timeout=0.001).request("ping")


def test_device_error_is_raised():
    response = encode_message(Message(1, "error", "device-response", {"message": "bad request"}, "host-1"))
    with pytest.raises(ValueError, match="bad request"):
        SerialBridge(MockTransport([response]), id_factory=lambda: "host-1").request("ping")


def test_connection_failure_is_visible():
    manager = ConnectionManager(SerialBridge(FailingTransport()))
    with pytest.raises(OSError, match="device unavailable"):
        manager.connect()
    assert manager.state is ConnectionState.FAULTED

