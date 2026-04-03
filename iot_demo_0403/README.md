# IoT Demo hoàn chỉnh: OpenWeather → Mosquitto → PostgreSQL → ThingsBoard

## 1. Giới thiệu

Đây là project demo IoT hoàn chỉnh dành cho sinh viên mới bắt đầu học IoT.  
Project này mô phỏng một hệ thống IoT end-to-end với đầy đủ các thành phần quan trọng:

- một **nguồn dữ liệu đầu vào**
- một **MQTT Broker**
- một **subscriber xử lý dữ liệu**
- một **cơ sở dữ liệu lưu trữ**
- một **nền tảng IoT để giám sát trực quan**

Trong project này, thay vì dùng cảm biến thật như ESP32 hoặc DHT11, dữ liệu đầu vào sẽ được lấy từ **OpenWeather API**. Có thể xem đây là một **cảm biến ảo** để giúp sinh viên tập trung vào việc hiểu kiến trúc IoT mà không bị phụ thuộc vào phần cứng ngay từ đầu.

---

## 2. Mục tiêu học tập

Sau khi hoàn thành bài thực hành này, sinh viên có thể hiểu được:

- cách lấy dữ liệu từ API bên ngoài
- cách tổ chức một pipeline IoT cơ bản
- cách dùng giao thức **MQTT**
- vai trò của **Mosquitto** trong hệ thống
- cách viết chương trình **publisher**
- cách viết chương trình **subscriber**
- cách lưu dữ liệu vào **PostgreSQL**
- cách dùng **ThingsBoard** để xem telemetry
- cách kiểm tra và debug từng thành phần trong hệ thống

---

## 3. Luồng hoạt động của hệ thống

Hệ thống hoạt động theo luồng sau:

**OpenWeather API**  
→ `publisher.py` lấy dữ liệu thời tiết  
→ publish dữ liệu lên **Mosquitto** thông qua MQTT  
→ `subscriber.py` subscribe dữ liệu từ topic MQTT  
→ lưu dữ liệu vào **PostgreSQL**  
→ đồng thời forward dữ liệu lên **ThingsBoard**  
→ hiển thị telemetry trong ThingsBoard

Có thể tóm tắt bằng sơ đồ chữ như sau:

```text
OpenWeather API
      ↓
publisher.py
      ↓ MQTT publish
Mosquitto Broker
      ↓ MQTT subscribe
subscriber.py
   ↙          ↘
PostgreSQL   ThingsBoard
```

---

## 4. Cấu trúc thư mục project

Thư mục project ví dụ:

```text
iot_demo_0403/
│
├─ config.py
├─ publisher.py
├─ subscriber.py
├─ test_openweather.py
├─ test_thingsboard.py
└─ README.md
```

Ý nghĩa các file:

* `config.py`: chứa toàn bộ thông tin cấu hình
* `publisher.py`: lấy dữ liệu từ OpenWeather và publish lên Mosquitto
* `subscriber.py`: nhận dữ liệu từ Mosquitto, lưu vào PostgreSQL và gửi lên ThingsBoard
* `test_openweather.py`: test API OpenWeather
* `test_thingsboard.py`: test gửi dữ liệu trực tiếp lên ThingsBoard
* `README.md`: tài liệu hướng dẫn thực hiện project

---

## 5. Công nghệ sử dụng

Project sử dụng các công nghệ sau:

* **Python 3**
* **OpenWeather API**
* **Mosquitto MQTT Broker**
* **PostgreSQL**
* **pgAdmin 4**
* **ThingsBoard**
* Thư viện Python:

  * `requests`
  * `paho-mqtt`
  * `psycopg2-binary`

---

# 6. Chuẩn bị môi trường

## 6.1. Cài Python

### Bước 1: Tải Python

Tải Python 3.11 hoặc phiên bản gần tương đương.

### Bước 2: Cài Python

Trong quá trình cài đặt, cần tick vào mục:

```text
Add Python to PATH
```

### Bước 3: Kiểm tra

Mở PowerShell hoặc Command Prompt và chạy:

```bash
python --version
```

hoặc:

```bash
py --version
```

Nếu thấy hiện phiên bản Python thì đã cài thành công.

---

## 6.2. Cài Mosquitto

### Bước 1: Tải Mosquitto

Tải Mosquitto cho Windows.

### Bước 2: Cài đặt

Chạy file cài đặt `.exe` và giữ nguyên các tùy chọn mặc định.

### Bước 3: Xác định thư mục cài

Ví dụ, trên máy có thể cài ở:

```text
D:\Mosquitto
```

hoặc thư mục mặc định khác.

### Bước 4: Chạy Mosquitto broker

Mở PowerShell và chạy:

```powershell
cd "D:\Mosquitto"
.\mosquitto.exe -v
```

Nếu broker chạy thành công, cửa sổ sẽ hiển thị log lắng nghe cổng mặc định `1883`.

### Bước 5: Test publish/subscribe

Mở thêm một cửa sổ PowerShell:

```powershell
cd "D:\Mosquitto"
.\mosquitto_sub.exe -h localhost -t test/topic -v
```

Mở thêm một cửa sổ khác:

```powershell
cd "D:\Mosquitto"
.\mosquitto_pub.exe -h localhost -t test/topic -m "hello mqtt"
```

Nếu cửa sổ `mosquitto_sub` hiện ra nội dung `hello mqtt` thì Mosquitto đã hoạt động đúng.

---

## 6.3. Cài PostgreSQL và pgAdmin

### Bước 1: Tải PostgreSQL

Tải bản PostgreSQL cho Windows x64.

### Bước 2: Chạy cài đặt

Trong quá trình cài, nên giữ cấu hình như sau:

* chọn **PostgreSQL Server**
* chọn **pgAdmin 4**
* chọn **Command Line Tools**
* port: `5432`
* locale: mặc định
* ghi nhớ mật khẩu của user `postgres`

### Bước 3: Mở pgAdmin

Sau khi cài xong, mở **pgAdmin 4** và kết nối vào PostgreSQL bằng mật khẩu đã đặt.

---

# 7. Tạo database và bảng

## 7.1. Tạo database `iot_demo`

Trong pgAdmin:

* chuột phải vào **Databases**
* chọn **Create**
* chọn **Database...**
* nhập tên database:

```text
iot_demo
```

* nhấn **Save**

---

## 7.2. Tạo bảng `weather_data`

Mở **Query Tool** của database `iot_demo` và chạy câu lệnh sau:

```sql
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(100),
    city VARCHAR(100),
    temperature REAL,
    humidity REAL,
    pressure REAL,
    wind_speed REAL,
    recorded_at TIMESTAMP,
    weather VARCHAR(200)
);
```

### Kiểm tra bảng

Chạy tiếp:

```sql
SELECT * FROM weather_data;
```

Nếu không báo lỗi thì bảng đã được tạo thành công.

---

# 8. Tạo thiết bị trên ThingsBoard

## 8.1. Đăng nhập ThingsBoard

Đăng nhập vào ThingsBoard mà bạn sử dụng.

## 8.2. Tạo thiết bị mới

Trong menu **Devices**:

* chọn **Add new device**
* nhập tên thiết bị, ví dụ:

```text
iot_demo_K68
```

* bấm **Add**

## 8.3. Lấy Access Token

Mở thiết bị vừa tạo và tìm phần **Credentials**.

Sao chép:

* **Access Token**

Lưu ý rất quan trọng:

* khi gửi dữ liệu lên ThingsBoard bằng MQTT, phải dùng **Access Token**
* **không dùng Device ID**

---

# 9. Tạo file cấu hình `config.py`

Tạo file `config.py` trong thư mục project với nội dung như sau:

```python
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
CITY = "Hanoi"

MOSQUITTO_BROKER = "localhost"
MOSQUITTO_PORT = 1883
MOSQUITTO_TOPIC = "iot/weather/hanoi"

PG_HOST = "localhost"
PG_PORT = 5432
PG_DATABASE = "iot_demo"
PG_USER = "postgres"
PG_PASSWORD = "YOUR_POSTGRES_PASSWORD"

THINGSBOARD_HOST = "demo.thingsboard.io"
THINGSBOARD_PORT = 1883
THINGSBOARD_ACCESS_TOKEN = "YOUR_THINGSBOARD_ACCESS_TOKEN"
THINGSBOARD_TOPIC = "v1/devices/me/telemetry"
```

### Giải thích

* `OPENWEATHER_API_KEY`: API key lấy từ OpenWeather
* `CITY`: thành phố cần lấy dữ liệu
* `MOSQUITTO_*`: cấu hình broker MQTT
* `PG_*`: cấu hình PostgreSQL
* `THINGSBOARD_*`: cấu hình kết nối ThingsBoard

---

# 10. Cài thư viện Python

Mở terminal tại thư mục project và chạy:

```bash
pip install requests paho-mqtt psycopg2-binary
```

---

# 11. Test OpenWeather API

Tạo file `test_openweather.py` với nội dung:

```python
import requests

API_KEY = "YOUR_OPENWEATHER_API_KEY"
CITY = "Hanoi"

url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": CITY,
    "appid": API_KEY,
    "units": "metric"
}

response = requests.get(url, params=params, timeout=10)
print("Status code:", response.status_code)
print(response.text)
```

Chạy:

```bash
python test_openweather.py
```

Nếu kết quả là `Status code: 200` thì API hoạt động đúng.

---

# 12. File `publisher.py`

File này có nhiệm vụ:

* gọi OpenWeather API
* lấy dữ liệu thời tiết
* publish dữ liệu lên Mosquitto

```python
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
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": CITY,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

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
    client = mqtt.Client()
    client.connect(MOSQUITTO_BROKER, MOSQUITTO_PORT, 60)

    while True:
        try:
            payload = get_weather_data()
            message = json.dumps(payload, ensure_ascii=False)
            client.publish(MOSQUITTO_TOPIC, message)
            print(f"[PUBLISHER] Published to {MOSQUITTO_TOPIC}: {message}")
        except Exception as e:
            print(f"[PUBLISHER] Error: {e}")

        time.sleep(30)

if __name__ == "__main__":
    main()
```

---

# 13. File `subscriber.py`

File này có nhiệm vụ:

* subscribe dữ liệu từ Mosquitto
* lưu dữ liệu vào PostgreSQL
* gửi telemetry sang ThingsBoard

```python
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
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )

def save_to_postgresql(data):
    conn = None
    cur = None
    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        sql = """
        INSERT INTO weather_data
        (device_id, city, temperature, humidity, pressure, wind_speed, weather, recorded_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

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

        conn.commit()
        print("[SUBSCRIBER] Saved to PostgreSQL")

    except Exception as e:
        print(f"[SUBSCRIBER] PostgreSQL error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def forward_to_thingsboard(data):
    if not THINGSBOARD_ACCESS_TOKEN:
        print("[SUBSCRIBER] Skip ThingsBoard: chưa cấu hình token")
        return

    tb_client = None
    try:
        tb_client = mqtt.Client()
        tb_client.username_pw_set(THINGSBOARD_ACCESS_TOKEN)
        tb_client.connect(THINGSBOARD_HOST, THINGSBOARD_PORT, 60)
        tb_client.loop_start()

        telemetry = {
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "pressure": data.get("pressure"),
            "wind_speed": data.get("wind_speed"),
            "city": data.get("city"),
            "weather": data.get("weather")
        }

        info = tb_client.publish(THINGSBOARD_TOPIC, json.dumps(telemetry), qos=1)
        info.wait_for_publish()

        tb_client.loop_stop()
        tb_client.disconnect()
        print("[SUBSCRIBER] Forwarded to ThingsBoard")

    except Exception as e:
        print(f"[SUBSCRIBER] ThingsBoard error: {e}")

def on_connect(client, userdata, flags, rc):
    print(f"[SUBSCRIBER] Connected to Mosquitto with result code {rc}")
    client.subscribe(MOSQUITTO_TOPIC)
    print(f"[SUBSCRIBER] Subscribed to: {MOSQUITTO_TOPIC}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        print(f"[SUBSCRIBER] Received: {payload}")

        data = json.loads(payload)

        save_to_postgresql(data)
        forward_to_thingsboard(data)

    except Exception as e:
        print(f"[SUBSCRIBER] Message handling error: {e}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MOSQUITTO_BROKER, MOSQUITTO_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
```

---

# 14. Test gửi trực tiếp lên ThingsBoard

Tạo file `test_thingsboard.py`:

```python
import json
import time
import paho.mqtt.client as mqtt

THINGSBOARD_HOST = "demo.thingsboard.io"
THINGSBOARD_PORT = 1883
THINGSBOARD_ACCESS_TOKEN = "YOUR_THINGSBOARD_ACCESS_TOKEN"
THINGSBOARD_TOPIC = "v1/devices/me/telemetry"

client = mqtt.Client()
client.username_pw_set(THINGSBOARD_ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, THINGSBOARD_PORT, 60)
client.loop_start()

payload = {
    "temperature": 28.5,
    "humidity": 80,
    "pressure": 1008,
    "wind_speed": 3.1,
    "city": "Hanoi",
    "weather": "test-direct"
}

info = client.publish(THINGSBOARD_TOPIC, json.dumps(payload), qos=1)
info.wait_for_publish()
time.sleep(2)

client.loop_stop()
client.disconnect()

print("Sent direct telemetry:", payload)
```

Chạy:

```bash
python test_thingsboard.py
```

Nếu ThingsBoard nhận được dữ liệu thì cấu hình host và token là đúng.

---

# 15. Cách chạy toàn bộ hệ thống

Mở 4 cửa sổ terminal.

## Terminal 1: chạy Mosquitto Broker

```powershell
cd "D:\Mosquitto"
.\mosquitto.exe -v
```

## Terminal 2: theo dõi MQTT topic

```powershell
cd "D:\Mosquitto"
.\mosquitto_sub.exe -h localhost -t iot/weather/hanoi -v
```

## Terminal 3: chạy subscriber

```powershell
cd "D:\Master UET\GiangDay\IoT trong NN\DemoTh\iot_demo_0403"
python subscriber.py
```

## Terminal 4: chạy publisher

```powershell
cd "D:\Master UET\GiangDay\IoT trong NN\DemoTh\iot_demo_0403"
python publisher.py
```

---

# 16. Cách kiểm tra hệ thống hoạt động đúng

## 16.1. Kiểm tra ở `mosquitto_sub`

Nếu đúng, terminal sẽ hiện dữ liệu JSON như:

```text
iot/weather/hanoi {"device_id": "...", "city": "Hanoi", ...}
```

## 16.2. Kiểm tra ở `subscriber.py`

Nếu đúng, terminal sẽ hiện:

```text
[SUBSCRIBER] Received: {...}
[SUBSCRIBER] Saved to PostgreSQL
[SUBSCRIBER] Forwarded to ThingsBoard
```

## 16.3. Kiểm tra trên PostgreSQL

Trong pgAdmin, chạy:

```sql
SELECT *
FROM weather_data
ORDER BY id DESC
LIMIT 10;
```

Nếu có dữ liệu mới thì subscriber đã lưu DB thành công.

## 16.4. Kiểm tra trên ThingsBoard

Mở đúng thiết bị trong ThingsBoard và vào tab:

```text
Latest telemetry
```

Nếu đúng, sẽ thấy các key:

* `temperature`
* `humidity`
* `pressure`
* `wind_speed`
* `city`
* `weather`

---

# 17. Tạo dashboard trong ThingsBoard

Sau khi đã thấy telemetry, có thể tạo dashboard để hiển thị trực quan.

## Gợi ý các widget nên thêm:

* **Current temperature**
* **Current humidity**
* **Current pressure**
* **Current wind speed**
* **Current weather**
* **Line chart temperature**
* **Line chart humidity**

Như vậy dashboard sẽ đẹp và dễ trình bày trên lớp.

---

# 18. Vai trò của từng thành phần

## OpenWeather API

Đóng vai trò như một cảm biến ảo để cung cấp dữ liệu thời tiết.

## publisher.py

Lấy dữ liệu từ OpenWeather và publish lên MQTT topic.

## Mosquitto

Đóng vai trò MQTT Broker, nhận và phân phối bản tin.

## subscriber.py

Nhận dữ liệu từ topic MQTT, xử lý, lưu database và forward sang ThingsBoard.

## PostgreSQL

Lưu dữ liệu lịch sử để truy vấn và phân tích.

## ThingsBoard

Hiển thị telemetry và dashboard theo thời gian thực.

---

# 19. Các lỗi thường gặp và cách xử lý

## Lỗi 1: `python: can't open file`

Nguyên nhân:

* chạy lệnh ở sai thư mục

Cách xử lý:

* chuyển đúng thư mục chứa file `.py`
* hoặc chạy bằng đường dẫn đầy đủ

---

## Lỗi 2: `password authentication failed for user "postgres"`

Nguyên nhân:

* sai mật khẩu PostgreSQL trong `config.py`

Cách xử lý:

* kiểm tra lại:

```python
PG_PASSWORD = "..."
```

---

## Lỗi 3: OpenWeather trả về 401

Nguyên nhân:

* API key sai hoặc chưa kích hoạt

Cách xử lý:

* kiểm tra lại `OPENWEATHER_API_KEY`

---

## Lỗi 4: Không thấy dữ liệu trong ThingsBoard

Nguyên nhân có thể:

* sai Access Token
* sai host ThingsBoard
* chưa vào đúng thiết bị
* chưa xem đúng tab `Latest telemetry`

Cách xử lý:

* kiểm tra lại:

```python
THINGSBOARD_HOST = "demo.thingsboard.io"
THINGSBOARD_ACCESS_TOKEN = "..."
THINGSBOARD_TOPIC = "v1/devices/me/telemetry"
```

* dùng **Access Token**, không dùng Device ID

---

## Lỗi 5: Mosquitto không nhận được dữ liệu

Nguyên nhân:

* broker chưa chạy
* sai topic
* sai port

Cách xử lý:

* chạy lại Mosquitto bằng:

```powershell
.\mosquitto.exe -v
```

* kiểm tra topic:

```python
MOSQUITTO_TOPIC = "iot/weather/hanoi"
```

---

## Lỗi 6: Subscriber không lưu được dữ liệu vào PostgreSQL

Nguyên nhân:

* sai cấu hình DB
* bảng chưa được tạo
* dữ liệu không khớp cột

Cách xử lý:

* kiểm tra database `iot_demo`
* kiểm tra bảng `weather_data`
* chạy lại câu SQL tạo bảng

---

# 20. Mở rộng bài thực hành

Sau khi chạy thành công demo cơ bản, có thể mở rộng theo nhiều hướng:

* thay OpenWeather bằng dữ liệu random
* thay dữ liệu random bằng ESP32 thật
* thêm nhiều topic MQTT
* thêm nhiều thiết bị
* thêm cảnh báo ngưỡng
* thêm dashboard chi tiết hơn
* thêm biểu đồ trực tiếp từ dữ liệu lịch sử trong PostgreSQL
* thêm API hoặc web app riêng

---

# 21. Kết luận

Project này minh họa đầy đủ một chuỗi xử lý dữ liệu trong hệ thống IoT hiện đại:

**API / cảm biến ảo → MQTT → Broker → Subscriber → Database → IoT Platform**

Thông qua project này, sinh viên có thể:

* hiểu rõ pipeline của hệ thống IoT
* nắm được vai trò của từng thành phần
* biết cách tích hợp dữ liệu, giao thức, cơ sở dữ liệu và nền tảng giám sát
* sẵn sàng mở rộng sang các hệ thống IoT thực tế với cảm biến thật
