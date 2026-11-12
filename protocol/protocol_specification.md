# AHFT Protocol v1

AHFT uses newline-delimited JSON (NDJSON) over a byte stream. Each message is one UTF-8 JSON object followed by `\n`. The maximum encoded line size is 4096 bytes. The initial baud rate is 115200, 8 data bits, no parity, 1 stop bit.

Required common fields:

```json
{"protocol_version":1,"type":"ping","id":"request-id"}
```

`protocol_version` is the integer protocol version. `type` is a supported message type. `id` is a non-empty request or correlation identifier and must be unique for an active request.

Milestone 0 message types:

- `ping` → `pong`
- `identify` → `device_info`
- `error` for malformed, unsupported, or invalid requests

`ping` and `identify` may include a JSON object `payload`. Responses preserve the request `id` and include `in_reply_to` where applicable. The firmware must never report an experiment success because of a communication error.

Example:

```json
{"protocol_version":1,"type":"identify","id":"abc-2"}
{"protocol_version":1,"type":"device_info","id":"abc-2","in_reply_to":"abc-2","payload":{"firmware_version":"0.1.0","protocol_version":1,"chip":"ESP32","idf_version":"...","reset_reason":"power_on"}}
```

Malformed JSON, missing fields, unsupported protocol versions, oversized lines, and unsupported message types produce an `error` response when a correlation id can be recovered; otherwise the device logs and drops the line.

