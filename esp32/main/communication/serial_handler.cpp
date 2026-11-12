#include "serial_handler.h"

#include <cstring>

#include "cJSON.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_timer.h"

namespace ahft {
namespace {
constexpr uart_port_t kUart = UART_NUM_0;
constexpr int kBaud = 115200;
constexpr char kTag[] = "ahft_serial";
char line[kMaxLineBytes + 1];
int line_len = 0;

void send_message(const char* type, const char* id, const char* reply, cJSON* payload) {
    cJSON* root = cJSON_CreateObject();
    cJSON_AddNumberToObject(root, "protocol_version", 1);
    cJSON_AddStringToObject(root, "type", type);
    cJSON_AddStringToObject(root, "id", id && id[0] ? id : "device-0");
    if (reply) cJSON_AddStringToObject(root, "in_reply_to", reply);
    if (payload) cJSON_AddItemToObject(root, "payload", payload);
    char* encoded = cJSON_PrintUnformatted(root);
    if (encoded) {
        uart_write_bytes(kUart, encoded, strlen(encoded));
        uart_write_bytes(kUart, "\n", 1);
        cJSON_free(encoded);
    }
    cJSON_Delete(root);
}

void send_error(const char* id, const char* message) {
    cJSON* payload = cJSON_CreateObject();
    cJSON_AddStringToObject(payload, "message", message);
    send_message("error", id, id, payload);
}

void handle_line() {
    line[line_len] = '\0';
    cJSON* root = cJSON_Parse(line);
    if (!root) {
        ESP_LOGW(kTag, "malformed JSON command");
        line_len = 0;
        return;
    }
    cJSON* version = cJSON_GetObjectItem(root, "protocol_version");
    cJSON* type = cJSON_GetObjectItem(root, "type");
    cJSON* id = cJSON_GetObjectItem(root, "id");
    const char* id_text = cJSON_IsString(id) ? id->valuestring : "";
    if (!cJSON_IsNumber(version) || version->valueint != 1 || !cJSON_IsString(type) || !cJSON_IsString(id) || !id_text[0]) {
        send_error(id_text, "invalid protocol fields");
    } else if (strcmp(type->valuestring, "ping") == 0) {
        send_message("pong", id_text, id_text, nullptr);
    } else if (strcmp(type->valuestring, "identify") == 0) {
        cJSON* payload = cJSON_CreateObject();
        cJSON_AddStringToObject(payload, "firmware_version", "0.1.0");
        cJSON_AddNumberToObject(payload, "protocol_version", 1);
        cJSON_AddStringToObject(payload, "chip", "ESP32");
        cJSON_AddStringToObject(payload, "idf_version", esp_get_idf_version());
        cJSON_AddNumberToObject(payload, "reset_reason", static_cast<int>(esp_reset_reason()));
        send_message("device_info", id_text, id_text, payload);
    } else {
        send_error(id_text, "unsupported message type");
    }
    cJSON_Delete(root);
    line_len = 0;
}
}  // namespace

void serial_init() {
    uart_config_t config{};
    config.baud_rate = kBaud;
    config.data_bits = UART_DATA_8_BITS;
    config.parity = UART_PARITY_DISABLE;
    config.stop_bits = UART_STOP_BITS_1;
    config.flow_ctrl = UART_HW_FLOWCTRL_DISABLE;
    ESP_ERROR_CHECK(uart_driver_install(kUart, 2048, 0, 0, nullptr, 0));
    ESP_ERROR_CHECK(uart_param_config(kUart, &config));
    ESP_ERROR_CHECK(uart_set_pin(kUart, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
}

void serial_poll() {
    uint8_t byte = 0;
    while (uart_read_bytes(kUart, &byte, 1, 0) == 1) {
        if (byte == '\n') {
            handle_line();
        } else if (byte != '\r') {
            if (line_len >= kMaxLineBytes) {
                line_len = 0;
                ESP_LOGW(kTag, "oversized command dropped");
            } else {
                line[line_len++] = static_cast<char>(byte);
            }
        }
    }
}
}  // namespace ahft

