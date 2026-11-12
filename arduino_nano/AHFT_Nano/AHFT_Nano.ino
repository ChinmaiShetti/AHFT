/* AHFT Milestone 0 firmware for the classic Arduino Nano (ATmega328P). */
#include <Arduino.h>

static const size_t MAX_LINE_BYTES = 240;
static const char FIRMWARE_VERSION[] = "0.1.0-nano";
char lineBuffer[MAX_LINE_BYTES + 1];
size_t lineLength = 0;

bool findStringField(const char *json, const char *field, char *out, size_t outSize) {
  char key[48];
  snprintf(key, sizeof(key), "\"%s\"", field);
  const char *keyStart = strstr(json, key);
  if (keyStart == NULL) return false;
  const char *colon = strchr(keyStart + strlen(key), ':');
  if (colon == NULL) return false;
  const char *quoteStart = strchr(colon + 1, '"');
  if (quoteStart == NULL) return false;
  const char *quoteEnd = strchr(quoteStart + 1, '"');
  if (quoteEnd == NULL) return false;
  size_t length = (size_t)(quoteEnd - quoteStart - 1);
  if (length == 0 || length >= outSize) return false;
  memcpy(out, quoteStart + 1, length);
  out[length] = '\0';
  return true;
}

bool hasProtocolVersion(const char *json) {
  const char *key = strstr(json, "\"protocol_version\"");
  if (key == NULL) return false;
  const char *colon = strchr(key, ':');
  if (colon == NULL) return false;
  while (*(colon + 1) == ' ' || *(colon + 1) == '\t') colon++;
  return strncmp(colon + 1, "1", 1) == 0;
}

void sendError(const char *id, const char *message) {
  const char *safeId = (id != NULL && id[0] != '\0') ? id : "nano-error";
  Serial.print(F("{\"protocol_version\":1,\"type\":\"error\",\"id\":\""));
  Serial.print(safeId);
  Serial.print(F("\",\"in_reply_to\":\""));
  Serial.print(safeId);
  Serial.print(F("\",\"payload\":{\"message\":\""));
  Serial.print(message);
  Serial.println(F("\"}}"));
}

void sendPong(const char *id) {
  Serial.print(F("{\"protocol_version\":1,\"type\":\"pong\",\"id\":\""));
  Serial.print(id);
  Serial.print(F("\",\"in_reply_to\":\""));
  Serial.print(id);
  Serial.println(F("\"}"));
}

void sendDeviceInfo(const char *id) {
  Serial.print(F("{\"protocol_version\":1,\"type\":\"device_info\",\"id\":\""));
  Serial.print(id);
  Serial.print(F("\",\"in_reply_to\":\""));
  Serial.print(id);
  Serial.print(F("\",\"payload\":{\"firmware_version\":\""));
  Serial.print(FIRMWARE_VERSION);
  Serial.print(F("\",\"protocol_version\":1,\"board\":\"Arduino Nano ATmega328P\",\"cpu\":\"ATmega328P\",\"clock_hz\":16000000,\"reset_reason\":\"not_available_on_classic_nano\"}}"));
  Serial.println();
}

void handleLine() {
  lineBuffer[lineLength] = '\0';
  char id[64] = {0};
  const bool hasId = findStringField(lineBuffer, "id", id, sizeof(id));
  if (!hasProtocolVersion(lineBuffer) || !hasId) {
    sendError(hasId ? id : "", "invalid protocol fields");
  } else {
    char type[32] = {0};
    if (!findStringField(lineBuffer, "type", type, sizeof(type))) sendError(id, "missing message type");
    else if (strcmp(type, "ping") == 0) sendPong(id);
    else if (strcmp(type, "identify") == 0) sendDeviceInfo(id);
    else sendError(id, "unsupported message type");
  }
  lineLength = 0;
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  while (Serial.available() > 0) {
    const char incoming = (char)Serial.read();
    if (incoming == '\n') handleLine();
    else if (incoming != '\r') {
      if (lineLength >= MAX_LINE_BYTES) {
        lineLength = 0;
        sendError("", "message too large for Nano input buffer");
      } else lineBuffer[lineLength++] = incoming;
    }
  }
}

