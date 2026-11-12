idf_component_register(
    SRCS "main.cpp" "communication/serial_handler.cpp"
    INCLUDE_DIRS "." "communication"
    REQUIRES driver json esp_hw_support
)

