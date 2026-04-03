"""
Test ThingsBoard API gửi dữ liệu trực tiếp

Script này để test gửi dữ liệu trực tiếp lên ThingsBoard qua MQTT.
Chạy trước để đảm bảo ThingsBoard host và Access Token đúng.

Cách chạy:
    python test_thingsboard.py
"""

import json
import time
import paho.mqtt.client as mqtt
from config import (
    THINGSBOARD_HOST,
    THINGSBOARD_PORT,
    THINGSBOARD_ACCESS_TOKEN,
    THINGSBOARD_TOPIC,
)


def test_thingsboard():
    """Test gửi dữ liệu trực tiếp lên ThingsBoard"""
    
    print(f"=== TEST THINGSBOARD ===")
    print(f"Host: {THINGSBOARD_HOST}")
    print(f"Port: {THINGSBOARD_PORT}")
    print(f"Topic: {THINGSBOARD_TOPIC}")
    print(f"Token: {THINGSBOARD_ACCESS_TOKEN[:20]}..." if len(THINGSBOARD_ACCESS_TOKEN) > 20 else f"Token: {THINGSBOARD_ACCESS_TOKEN}")
    print()

    if THINGSBOARD_ACCESS_TOKEN == "YOUR_THINGSBOARD_ACCESS_TOKEN":
        print("✗ Lỗi! Chưa cấu hình Access Token")
        print("   Hãy cập nhật THINGSBOARD_ACCESS_TOKEN trong config.py")
        return

    try:
        # Tạo MQTT client
        client = mqtt.Client()
        
        # Cấu hình username/password (dùng token làm username, password trống)
        client.username_pw_set(THINGSBOARD_ACCESS_TOKEN)
        
        print("Đang kết nối đến ThingsBoard...")
        client.connect(THINGSBOARD_HOST, THINGSBOARD_PORT, 60)
        client.loop_start()
        time.sleep(2)

        # Tạo telemetry data
        payload = {
            "temperature": 28.5,
            "humidity": 80,
            "pressure": 1008,
            "wind_speed": 3.1,
            "city": "Hanoi",
            "weather": "test-direct"
        }

        message = json.dumps(payload)
        print(f"✓ Kết nối thành công!")
        print()
        print(f"Đang gửi dữ liệu: {message}")

        # Publish dữ liệu
        info = client.publish(THINGSBOARD_TOPIC, message, qos=1)
        info.wait_for_publish()

        print(f"✓ Dữ liệu đã được gửi!")
        print()
        print("Hãy kiểm tra ThingsBoard:")
        print(f"  1. Vào Devices")
        print(f"  2. Chọn thiết bị của bạn")
        print(f"  3. Vào tab 'Latest telemetry'")
        print(f"  4. Nếu thấy các dữ liệu dưới đây thì thành công:")
        print(f"     - temperature: 28.5")
        print(f"     - humidity: 80")
        print(f"     - pressure: 1008")
        print(f"     - wind_speed: 3.1")
        print(f"     - city: Hanoi")
        print(f"     - weather: test-direct")

        time.sleep(2)
        client.loop_stop()
        client.disconnect()

    except Exception as e:
        print(f"✗ Lỗi: {e}")
        print()
        print("Gợi ý khắc phục:")
        print("  1. Kiểm tra THINGSBOARD_HOST có đúng không (ví dụ: demo.thingsboard.io)")
        print("  2. Kiểm tra THINGSBOARD_ACCESS_TOKEN có đúng không")
        print("  3. Kiểm tra internet connection")
        print("  4. Kiểm tra ThingsBoard server có bật không")


if __name__ == "__main__":
    print()
    test_thingsboard()
    print()
