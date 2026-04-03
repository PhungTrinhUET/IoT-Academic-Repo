# ========================================
# Cấu hình cho IoT Demo Project
# ========================================

# ========================================
# OpenWeather API
# ========================================
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
CITY = "Hanoi"

# ========================================
# Mosquitto MQTT Broker
# ========================================
MOSQUITTO_BROKER = "localhost"
MOSQUITTO_PORT = 1883
MOSQUITTO_TOPIC = "iot/weather/hanoi"

# ========================================
# PostgreSQL Database
# ========================================
PG_HOST = "localhost"
PG_PORT = 5432
PG_DATABASE = "iot_demo"
PG_USER = "postgres"
PG_PASSWORD = "YOUR_POSTGRES_PASSWORD"

# ========================================
# ThingsBoard Configuration
# ========================================
THINGSBOARD_HOST = "demo.thingsboard.io"
THINGSBOARD_PORT = 1883
THINGSBOARD_ACCESS_TOKEN = "YOUR_THINGSBOARD_ACCESS_TOKEN"
THINGSBOARD_TOPIC = "v1/devices/me/telemetry"
