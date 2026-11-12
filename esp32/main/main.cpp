#include "communication/serial_handler.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

extern "C" void app_main() {
    ahft::serial_init();
    while (true) {
        ahft::serial_poll();
        vTaskDelay(pdMS_TO_TICKS(1));
    }
}

