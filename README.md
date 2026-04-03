# 🌐 IoT Demo: OpenWeather → Mosquitto → PostgreSQL → ThingsBoard

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

> A complete IoT end-to-end demo project for students learning IoT architecture and data pipeline management.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Learning Objectives](#learning-objectives)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [Running the Project](#running-the-project)
- [Troubleshooting](#troubleshooting)
- [References](#references)

---

## 🎯 Overview

Đây là project demo IoT hoàn chỉnh dành cho sinh viên mới bắt đầu học IoT.  
Project này mô phỏng một hệ thống IoT end-to-end với đầy đủ các thành phần quan trọng:

- 📡 **Nguồn dữ liệu** (OpenWeather API - cảm biến ảo)
- 🔄 **MQTT Broker** (Mosquitto)
- 💾 **Database** (PostgreSQL)
- 📊 **Visualization** (ThingsBoard)
- ⚙️ **Data Processing** (Publisher/Subscriber)

Thay vì dùng cảm biến thật (ESP32, DHT11), dữ liệu sẽ được lấy từ **OpenWeather API**, giúp sinh viên focus vào kiến trúc IoT mà không phụ thuộc vào phần cứng.

---

## 🎓 Learning Objectives

Sau khi hoàn thành project này, bạn sẽ hiểu được:

✅ Cách lấy dữ liệu từ API bên ngoài  
✅ Cách tổ chức một data pipeline IoT  
✅ Giao thức **MQTT** và cơ chế publish/subscribe  
✅ Vai trò của **MQTT Broker** (Mosquitto)  
✅ Viết **Publisher** - thu thập & gửi dữ liệu  
✅ Viết **Subscriber** - xử lý dữ liệu nhận được  
✅ Lưu dữ liệu vào **PostgreSQL**  
✅ Tích hợp **ThingsBoard** để visualize dữ liệu  
✅ Debug và troubleshoot từng component  

---

## 🏗️ System Architecture

**Quy trình hoạt động chi tiết:**

```
┌─────────────────┐
│ OpenWeather API │ ◄── Cảm biến ảo (Virtual Sensor)
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  publisher.py       │ ◄── Fetch dữ liệu & publish
│ (Data Collector)    │
└────────┬────────────┘
         │ HTTP GET
         │ MQTT Publish
         ▼
┌─────────────────────┐
│ Mosquitto Broker    │ ◄── Message Queue
│ (MQTT Broker)       │     Port: 1883
└────────┬────────────┘
         │
         ▼ MQTT Subscribe
┌─────────────────────┐
│  subscriber.py      │ ◄── Data Processing
│(Data Consumer)      │
└────┬────────┬───────┘
     │        │
     ▼        ▼
┌─────────┐  ┌──────────────────┐
│PostgreSQL│  │  ThingsBoard     │
│          │  │ (Visualization)  │
└──────────┘  └──────────────────┘
```

---

## 📁 Project Structure

Cấu trúc thư mục project:



```
.
├── config.py                    # ⚙️  Cấu hình toàn bộ project
├── publisher.py                 # 📤 Thu thập dữ liệu & publish lên Mosquitto
├── subscriber.py                # 📥 Subscribe từ Mosquitto, lưu DB & ThingsBoard
├── test_openweather.py          # 🧪 Test OpenWeather API
├── test_thingsboard.py          # 🧪 Test kết nối ThingsBoard
└── README.md                    # 📖 Tài liệu này
```

### File Description

| File | Mục đích |
|------|---------|
| `config.py` | Lưu toàn bộ thông tin cấu hình (API keys, host, port, ...) |
| `publisher.py` | Gọi OpenWeather API & đẩy dữ liệu lên MQTT Broker |
| `subscriber.py` | Lấy dữ liệu từ MQTT, lưu PostgreSQL, gửi ThingsBoard |
| `test_openweather.py` | Kiểm tra kết nối OpenWeather API |
| `test_thingsboard.py` | Kiểm tra kết nối ThingsBoard MQTT |

---

## 🛠️ Technology Stack

Công nghệ & công cụ sử dụng:

| Component | Version | Mục đích |
|-----------|---------|---------|
| **Python** | 3.8+ | Ngôn ngữ lập trình |
| **Mosquitto** | Latest | MQTT Broker |
| **PostgreSQL** | 12+ | Database |
| **pgAdmin 4** | Latest | Web UI quản lý PostgreSQL |
| **ThingsBoard** | Cloud/Local | IoT Platform visualize |
| **requests** | Latest | Call HTTP API |
| **paho-mqtt** | Latest | MQTT Client Python |
| **psycopg2-binary** | Latest | PostgreSQL adapter |

---

## ✅ Prerequisites

Yêu cầu trước khi bắt đầu:

- 💻 **Windows 10+** (hoặc Linux/macOS)
- 🐍 **Python 3.8 or higher**
- 📡 **Mosquitto MQTT Broker**
- 🗄️ **PostgreSQL 12+**
- 🌐 **OpenWeather API Key** (miễn phí tại [openweathermap.org](https://openweathermap.org/api))
- ☁️ **ThingsBoard Account** (dùng [demo.thingsboard.io](https://demo.thingsboard.io) hoặc local instance)
- 📝 **Text Editor hoặc IDE** (VS Code, PyCharm, ...)

---

## 📦 Installation & Setup

### 1️⃣ Install Python 3

**Download:** https://www.python.org/downloads/

**Trong lúc cài:**
- ✅ Tick vào `Add Python to PATH`
- Chọn path cài đặt (mặc định được)
- Chọn `Disable path length limit` (optional nhưng tốt)

**Kiểm tra cài đặt:**

```bash
python --version
# Hoặc
py --version
```

Nếu hiện phiên bản → ✅ **Thành công**

---

### 2️⃣ Install Mosquitto MQTT Broker

**Download:** https://mosquitto.org/download/

**Cài đặt:**
- Chạy file `.exe` installer
- Giữ nguyên các tùy chọn mặc định
- Port mặc định: `1883`

**Chạy Mosquitto:**

```bash
# Windows: Mở PowerShell
cd "C:\Program Files\mosquitto"  # Hoặc path cài đặt của bạn
.\mosquitto.exe -v
```

✅ Nếu thấy log `listening on port 1883` → **Thành công**

**Test MQTT (3 cửa sổ PowerShell):**

Terminal 1 - Subscribe:
```bash
.\mosquitto_sub.exe -h localhost -t test/topic -v
```

Terminal 2 - Publish:
```bash
.\mosquitto_pub.exe -h localhost -t test/topic -m "hello mqtt"
```

✅ Nếu Terminal 1 nhận được message → **MQTT hoạt động**

---

### 3️⃣ Install PostgreSQL & pgAdmin 4

**Download:** https://www.postgresql.org/download/

**Trong lúc cài:**
- ✅ Chọn **PostgreSQL Server**
- ✅ Chọn **pgAdmin 4**
- ✅ Chọn **Command Line Tools**
- Default port: `5432`
- **🔐 Ghi nhớ mật khẩu user `postgres`** ← QUAN TRỌNG!

**Mở pgAdmin:**
- Sau cài xong, truy cập: [http://localhost:5050](http://localhost:5050)
- Đăng nhập bằng mật khẩu PostgreSQL

---

### 4️⃣ Get OpenWeather API Key

1. Truy cập: https://openweathermap.org/api
2. Click **Sign Up** → tạo tài khoản
3. Xác nhận email
4. Vào **API keys** tab → copy key mặc định
5. Lưu lại (sẽ dùng ở file `config.py`)

---

### 5️⃣ ThingsBoard Setup

**Option A: Dùng Cloud Demo**
- Truy cập: https://demo.thingsboard.io
- Đăng nhập (hoặc tạo tài khoản)
- **Devices** → **Add new device** → tạo device
- Mở device → **Credentials** → copy **Access Token**

**Option B: Local Instance**
- Follow hướng dẫn: https://thingsboard.io/docs/installation/

---

## ⚙️ Configuration

### Tạo `config.py`

Tạo file **`config.py`** tại root thư mục project với nội dung:

```python
# ============ OpenWeather ============
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"  # Lấy từ openweathermap.org
CITY = "Hanoi"

# ============ Mosquitto MQTT Broker ============
MOSQUITTO_BROKER = "localhost"
MOSQUITTO_PORT = 1883
MOSQUITTO_TOPIC = "iot/weather/hanoi"

# ============ PostgreSQL ============
PG_HOST = "localhost"
PG_PORT = 5432
PG_DATABASE = "iot_demo"
PG_USER = "postgres"
PG_PASSWORD = "YOUR_POSTGRES_PASSWORD"  # Mật khẩu đã set khi cài PostgreSQL

# ============ ThingsBoard ============
THINGSBOARD_HOST = "demo.thingsboard.io"  # Hoặc IP local instance
THINGSBOARD_PORT = 1883
THINGSBOARD_ACCESS_TOKEN = "YOUR_THINGSBOARD_ACCESS_TOKEN"  # Copy từ ThingsBoard device credentials
THINGSBOARD_TOPIC = "v1/devices/me/telemetry"
```

### Cấu hình Chi tiết

| Biến | Nguồn | Mô tả |
|------|-------|-------|
| `OPENWEATHER_API_KEY` | [openweathermap.org](https://openweathermap.org/api) | API key để gọi OpenWeather |
| `CITY` | Tùy chọn | Thành phố cần lấy dữ liệu thời tiết |
| `MOSQUITTO_BROKER` | Cài đặt | Host MQTT broker (localhost nếu cài local) |
| `MOSQUITTO_PORT` | Cài đặt | Port MQTT (mặc định 1883) |
| `PG_PASSWORD` | Cài đặt PostgreSQL | Password của user `postgres` |
| `THINGSBOARD_ACCESS_TOKEN` | [demo.thingsboard.io](https://demo.thingsboard.io) | Token của device trên ThingsBoard |

---

### Install Python Dependencies

Mở terminal tại thư mục project:**

```bash
pip install -r requirements.txt
```

Hoặc cài từng package:

```bash
pip install requests paho-mqtt psycopg2-binary
```

---

## 🚀 Quick Start

Hướng dẫn nhanh để chạy project (giả sử tất cả đã cài và cấu hình):

**1. Chắc chắn Mosquitto đang chạy:**
```bash
# PowerShell
cd "C:\Program Files\mosquitto"
.\mosquitto.exe -v
```

**2. Test OpenWeather API:**
```bash
python test_openweather.py
# Output: Status code: 200
```

**3. Run Publisher (Thu thập dữ liệu):**
```bash
python publisher.py
# [PUBLISHER] Published to iot/weather/hanoi: {...}
```

**4. Run Subscriber (Xử lý & lưu dữ liệu) - Terminal khác:**
```bash
python subscriber.py
# [SUBSCRIBER] Received: {...}
# [SUBSCRIBER] Saved to PostgreSQL
# [SUBSCRIBER] Sent to ThingsBoard
```

**5. Kiểm tra dữ liệu:**
- pgAdmin: [http://localhost:5050](http://localhost:5050) → Query `SELECT * FROM weather_data`
- ThingsBoard: [https://demo.thingsboard.io](https://demo.thingsboard.io) → Device → Latest Telemetry

---

## 📖 Running the Project

### Các bước chi tiết

**1. Database & Mosquitto:**
- Đảm bảo PostgreSQL chạy (Windows Service hoặc chạy thủ công)
- Đảm bảo Mosquitto chạy

**2. Terminal 1 - Publisher:**
```bash
cd <your_project_folder>
python publisher.py
```

**3. Terminal 2 - Subscriber:**
```bash
cd <your_project_folder>
python subscriber.py
```

**Kết quả:**
- Publisher: Gọi OpenWeather API mỗi 30 giây → publish lên Mosquitto
- Subscriber: Nhận từ Mosquitto → lưu PostgreSQL → gửi ThingsBoard
- Data sẽ hiện trên pgAdmin & ThingsBoard

---

## 🔧 Troubleshooting

### ❌ `[PUBLISHER] Error: Failed to fetch weather data`
**Nguyên nhân:** OpenWeather API key sai hoặc hết timeout  
**Giải pháp:**
- Kiểm tra API key ở `config.py`
- Test: `python test_openweather.py`
- Kiểm tra internet

### ❌ `Connection refused` hoặc `Address already in use` (port 1883)
**Nguyên nhân:** Mosquitto không chạy hoặc port bị chiếm  
**Giải pháp:**
```bash
# Kiểm tra Mosquitto chạy hay không
netstat -an | findstr 1883

# Nếu port bị chiếm, kill process
taskkill /PID <PID> /F
```

### ❌ `psycopg2.OperationalError: could not connect to server`
**Nguyên nhân:** PostgreSQL không chạy hoặc mật khẩu sai  
**Giải pháp:**
- Kiểm tra PostgreSQL service đang chạy
- Verify mật khẩu ở `config.py`
- Test connect pgAdmin

### ❌ `No attribute 'publis'` hoặc import error
**Nguyên nhân:** Thư viện chưa cài  
**Giải pháp:**
```bash
pip install paho-mqtt requests psycopg2-binary --upgrade
```

### ❌ Database error: `relation "weather_data" does not exist`
**Nguyên nhân:** Table chưa được tạo  
**Giải pháp:**
- Mở pgAdmin → database `iot_demo` → Query Tool
- Copy & run SQL tạo table (xem phần Configuration)

---

## 📚 References

- [MQTT Protocol](https://mqtt.org/)
- [Mosquitto Documentation](https://mosquitto.org/documentation/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [ThingsBoard Documentation](https://thingsboard.io/docs/)
- [OpenWeather API Docs](https://openweathermap.org/api)
- [Paho MQTT Python](https://github.com/eclipse/paho.mqtt.python)

---

## 📄 File Details

### `publisher.py`
Thu thập dữ liệu từ OpenWeather API và publish lên MQTT Broker

**Chức năng:**
- Gọi OpenWeather API mỗi 30 giây
- Lấy dữ liệu: nhiệt độ, độ ẩm, áp suất, tốc độ gió
- Publish JSON message lên MQTT topic

**Chạy:**
```bash
python publisher.py
```

### `subscriber.py`
Subscribe dữ liệu từ MQTT, lưu vào PostgreSQL và ThingsBoard

**Chức năng:**
- Subscribe từ Mosquitto topic
- Nhận JSON message
- Lưu dữ liệu vào PostgreSQL table
- Forward dữ liệu tới ThingsBoard

**Chạy:**
```bash
python subscriber.py
```

### `test_openweather.py`
Test kết nối và lấy dữ liệu từ OpenWeather API

```bash
python test_openweather.py
```

### `test_thingsboard.py`
Test gửi dữ liệu trực tiếp tới ThingsBoard

```bash
python test_thingsboard.py
```

---

## 🎓 Tips for Learning

- 💡 **Hiểu data flow:** Trace dữ liệu từ API → Mosquitto → PostgreSQL → ThingsBoard
- 🔍 **Debug từng component:** Test từng phần riêng rẽ trước khi chạy toàn bộ
- 📊 **Monitor dữ liệu:** Dùng pgAdmin và ThingsBoard để xem real-time data
- 🛠️ **Modify & Experiment:** Thay đổi topic, frequency, fields để hiểu hệ thống
- 📚 **Read Documentation:** Tham khảo docs của từng công nghệ

---

## 📞 Support

Gặp vấn đề? Kiểm tra:
1. ✅ Tất cả services đang chạy (Mosquitto, PostgreSQL)
2. ✅ Credentials đúng (API keys, passwords)
3. ✅ Network connection
4. ✅ Ports không bị block (1883, 5432)
5. ✅ Troubleshooting section ở trên

---

**Last Update:** April 2026  
**Status:** Active & Maintained

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
