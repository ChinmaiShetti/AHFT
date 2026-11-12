"""AHFT v1 NDJSON framing and message validation."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping

PROTOCOL_VERSION = 1
MAX_MESSAGE_BYTES = 4096
SUPPORTED_TYPES = {"ping", "pong", "identify", "device_info", "error"}


class ProtocolError(ValueError):
    """Raised when a wire message violates the AHFT protocol."""


@dataclass(frozen=True)
class Message:
    protocol_version: int
    type: str
    id: str
    payload: dict[str, Any] | None = None
    in_reply_to: str | None = None

    def as_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "protocol_version": self.protocol_version,
            "type": self.type,
            "id": self.id,
        }
        if self.in_reply_to is not None:
            value["in_reply_to"] = self.in_reply_to
        if self.payload is not None:
            value["payload"] = self.payload
        return value


def validate_message(value: Mapping[str, Any]) -> Message:
    if not isinstance(value, Mapping):
        raise ProtocolError("message must be a JSON object")
    version = value.get("protocol_version")
    if version != PROTOCOL_VERSION:
        raise ProtocolError(f"unsupported protocol_version: {version!r}")
    msg_type = value.get("type")
    if not isinstance(msg_type, str) or msg_type not in SUPPORTED_TYPES:
        raise ProtocolError(f"unsupported message type: {msg_type!r}")
    msg_id = value.get("id")
    if not isinstance(msg_id, str) or not msg_id or len(msg_id) > 128:
        raise ProtocolError("id must be a non-empty string of at most 128 characters")
    payload = value.get("payload")
    if payload is not None and not isinstance(payload, dict):
        raise ProtocolError("payload must be an object")
    reply = value.get("in_reply_to")
    if reply is not None and (not isinstance(reply, str) or not reply):
        raise ProtocolError("in_reply_to must be a non-empty string")
    return Message(version, msg_type, msg_id, payload, reply)


def encode_message(message: Message | Mapping[str, Any]) -> bytes:
    value = message.as_dict() if isinstance(message, Message) else dict(message)
    validated = validate_message(value)
    raw = (json.dumps(validated.as_dict(), separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")
    if len(raw) > MAX_MESSAGE_BYTES:
        raise ProtocolError("encoded message exceeds maximum size")
    return raw


def decode_message(line: bytes | str) -> Message:
    raw = line.encode("utf-8") if isinstance(line, str) else line
    if len(raw) > MAX_MESSAGE_BYTES:
        raise ProtocolError("message exceeds maximum size")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProtocolError("invalid JSON message") from exc
    return validate_message(value)

