"""
Subscriber - Subscribe dữ liệu từ Mosquitto, lưu vào PostgreSQL và forward lên ThingsBoard

Luồng hoạt động:
1. Subscribe vào MQTT topic trên Mosquitto
2. Khi nhận được dữ liệu, lưu vào PostgreSQL
3. Đồng thời forward dữ liệu lên ThingsBoard
"""

import json
import paho.mqtt.client as mqtt
import psycopg2
from config import (
    MOSQUITTO_BROKER,
    MOSQUITTO_PORT,
    MOSQUITTO_TOPIC,
    PG_HOST,
    PG_PORT,
    PG_DATABASE,
    PG_USER,
    PG_PASSWORD,
    THINGSBOARD_HOST,
    THINGSBOARD_PORT,
    THINGSBOARD_ACCESS_TOKEN,
    THINGSBOARD_TOPIC,
)


def get_pg_connection():
    """
    Tạo kết nối đến PostgreSQL database
    
    Returns:
        psycopg2.connection: Kết nối đến database
    """
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )


def save_to_postgresql(data):
    """
    Lưu dữ liệu vào bảng weather_data trong PostgreSQL
    
    Args:
        data (dict): Dữ liệu cần lưu (từ MQTT message)
    """
    conn = None
    cur = None
    try:
        # Kết nối đến database
        conn = get_pg_connection()
        cur = conn.cursor()

        # Câu lệnh INSERT SQL
        sql = """
        INSERT INTO weather_data
        (device_id, city, temperature, humidity, pressure, wind_speed, weather, recorded_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Thực thi câu lệnh với dữ liệu
        cur.execute(sql, (
            data.get("device_id"),
            data.get("city"),
            data.get("temperature"),
            data.get("humidity"),
            data.get("pressure"),
            data.get("wind_speed"),
            data.get("weather"),
            data.get("recorded_at")
        ))

        # Commit thay đổi
        conn.commit()
        print("[SUBSCRIBER] ✓ Đã lưu vào PostgreSQL")

    except Exception as e:
        print(f"[SUBSCRIBER] ✗ Lỗi PostgreSQL: {e}")

    finally:
        # Đóng cursor và kết nối
        if cur:
            cur.close()
        if conn:
            conn.close()


def forward_to_thingsboard(data):
    """
    Gửi dữ liệu lên ThingsBoard qua MQTT
    
    Args:
        data (dict): Dữ liệu cần gửi
    """
    if not THINGSBOARD_ACCESS_TOKEN or THINGSBOARD_ACCESS_TOKEN == "YOUR_THINGSBOARD_ACCESS_TOKEN":
        print("[SUBSCRIBER] ⊘ Bỏ qua ThingsBoard (chưa cấu hình token)")
        return

    tb_client = None
    try:
        # Tạo MQTT client cho ThingsBoard
        tb_client = mqtt.Client()
        tb_client.username_pw_set(THINGSBOARD_ACCESS_TOKEN)
        tb_client.connect(THINGSBOARD_HOST, THINGSBOARD_PORT, 60)
        tb_client.loop_start()

        # Tạo telemetry data cho ThingsBoard
        telemetry = {
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "pressure": data.get("pressure"),
            "wind_speed": data.get("wind_speed"),
            "city": data.get("city"),
            "weather": data.get("weather")
        }

        # Publish lên ThingsBoard
        info = tb_client.publish(THINGSBOARD_TOPIC, json.dumps(telemetry), qos=1)
        info.wait_for_publish()

        # Dừng loop và disconnect
        tb_client.loop_stop()
        tb_client.disconnect()
        print("[SUBSCRIBER] ✓ Đã gửi lên ThingsBoard")

    except Exception as e:
        print(f"[SUBSCRIBER] ✗ Lỗi ThingsBoard: {e}")


def on_connect(client, userdata, flags, rc):
    """
    Callback khi kết nối thành công đến Mosquitto
    
    Args:
        client: MQTT client object
        userdata: User data
        flags: Connection flags
        rc: Result code
    """
    if rc == 0:
        print(f"[SUBSCRIBER] ✓ Kết nối đến Mosquitto thành công (rc={rc})")
        # Subscribe vào topic
        client.subscribe(MOSQUITTO_TOPIC)
        print(f"[SUBSCRIBER] ✓ Đã subscribe vào: {MOSQUITTO_TOPIC}")
    else:
        print(f"[SUBSCRIBER] ✗ Kết nối thất bại (rc={rc})")


def on_message(client, userdata, msg):
    """
    Callback khi nhận được message từ MQTT
    
    Args:
        client: MQTT client object
        userdata: User data
        msg: MQTT message object
    """
    try:
        # Decode message payload từ bytes sang string
        payload = msg.payload.decode("utf-8")
        print(f"[SUBSCRIBER] ← Nhận được: {payload}")

        # Parse JSON data
        data = json.loads(payload)

        # Lưu vào PostgreSQL
        save_to_postgresql(data)
        
        # Gửi lên ThingsBoard
        forward_to_thingsboard(data)

    except json.JSONDecodeError as e:
        print(f"[SUBSCRIBER] ✗ Lỗi parse JSON: {e}")
    except Exception as e:
        print(f"[SUBSCRIBER] ✗ Lỗi xử lý message: {e}")


def main():
    """
    Hàm main - khởi động subscriber
    """
    # Tạo MQTT client
    client = mqtt.Client()
    
    # Gán các callback function
    client.on_connect = on_connect
    client.on_message = on_message

    # Kết nối đến Mosquitto Broker
    client.connect(MOSQUITTO_BROKER, MOSQUITTO_PORT, 60)
    
    print(f"[SUBSCRIBER] Kết nối tới Mosquitto tại {MOSQUITTO_BROKER}:{MOSQUITTO_PORT}")
    print("[SUBSCRIBER] Đang lắng nghe MQTT messages...")
    
    # Bắt đầu loop để lắng nghe messages
    client.loop_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[SUBSCRIBER] Dừng chương trình!")
