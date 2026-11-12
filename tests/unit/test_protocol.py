import pytest

from ahft.communication.protocol import Message, ProtocolError, decode_message, encode_message


def test_round_trip_message():
    original = Message(1, "ping", "abc", {"sent": True})
    assert decode_message(encode_message(original)) == original


@pytest.mark.parametrize("raw", [b"not-json\n", b'{"type":"ping","id":"x"}\n', b'{"protocol_version":1,"type":"wat","id":"x"}\n'])
def test_invalid_messages_are_rejected(raw):
    with pytest.raises(ProtocolError):
        decode_message(raw)


def test_oversized_message_is_rejected():
    with pytest.raises(ProtocolError):
        encode_message(Message(1, "ping", "x", {"data": "a" * 5000}))

