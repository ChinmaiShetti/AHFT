#pragma once

#include "driver/uart.h"

namespace ahft {

constexpr int kMaxLineBytes = 4096;

void serial_init();
void serial_poll();

}  // namespace ahft

