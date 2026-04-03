"""
Publisher - Lấy dữ liệu từ OpenWeather API và publish lên Mosquitto MQTT Broker

Luồng hoạt động:
1. Kết nối đến Mosquitto MQTT Broker
2. Gọi OpenWeather API để lấy dữ liệu thời tiết
3. Đóng gói dữ liệu thành JSON
4. Publish dữ liệu lên MQTT topic
5. Chờ 30 giây rồi lặp lại
"""

import json
import time
import requests
import paho.mqtt.client as mqtt
from config import (
    OPENWEATHER_API_KEY,
    CITY,
    MOSQUITTO_BROKER,
    MOSQUITTO_PORT,
    MOSQUITTO_TOPIC,
)


def get_weather_data():
    """
    Lấy dữ liệu thời tiết từ OpenWeather API
    
    Returns:
        dict: Payload chứa dữ liệu thời tiết
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": CITY,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # Lấy dữ liệu theo độ C
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()  # Kiểm tra lỗi HTTP
    data = response.json()

    # Đóng gói dữ liệu thành payload
    payload = {
        "device_id": "openweather-simulator-01",
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "weather": data["weather"][0]["description"],
        "recorded_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return payload


def main():
    """
    Hàm main - kết nối MQTT và publish dữ liệu liên tục
    """
    # Tạo MQTT client
    client = mqtt.Client()
    
    # Kết nối đến Mosquitto Broker
    client.connect(MOSQUITTO_BROKER, MOSQUITTO_PORT, 60)
    
    print(f"[PUBLISHER] Đã kết nối đến Mosquitto tại {MOSQUITTO_BROKER}:{MOSQUITTO_PORT}")
    print(f"[PUBLISHER] Sẽ publish lên topic: {MOSQUITTO_TOPIC}")
    print(f"[PUBLISHER] Thành phố: {CITY}")
    print("[PUBLISHER] Bắt đầu publish dữ liệu...")

    while True:
        try:
            # Lấy dữ liệu từ OpenWeather API
            payload = get_weather_data()
            
            # Chuyển dữ liệu thành JSON string
            message = json.dumps(payload, ensure_ascii=False)
            
            # Publish lên MQTT topic
            client.publish(MOSQUITTO_TOPIC, message)
            
            # In ra thông báo
            print(f"[PUBLISHER] ✓ Published: {message}")
            
        except requests.exceptions.RequestException as e:
            print(f"[PUBLISHER] ✗ Lỗi kết nối API: {e}")
        except Exception as e:
            print(f"[PUBLISHER] ✗ Lỗi: {e}")

        # Chờ 30 giây trước khi publish lần tiếp theo
        time.sleep(30)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[PUBLISHER] Dừng chương trình!")
