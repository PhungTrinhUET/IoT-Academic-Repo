# IoT Weather Simulator

## Giới thiệu

**Simulator** là thành phần giả lập thiết bị IoT trong kiến trúc demo. Nó thực hiện những công việc sau:

1. Gọi **OpenWeather API** mỗi 15 giây để lấy dữ liệu thời tiết thực tế của Hà Nội
2. Xử lý dữ liệu JSON từ API
3. **Publish lên MQTT topic** `iot/weather/hanoi` 

Giống như một cảm biến thực tế nhưng thay vì đọc từ phần cứng, nó lấy từ API.

## Kiến trúc

```
┌─────────────────┐          ┌──────────────────┐          ┌─────────────┐
│  OpenWeather    │          │    Simulator     │          │ MQTT Broker │
│     API         │  ←────→  │    (Node.js)     │  ←────→  │  Mosquitto  │
│  (Internet)     │ Request  │   (app.js)       │ Publish  │             │
└─────────────────┘  JSON    └──────────────────┘  Topic   └─────────────┘
                                                    iot/weather/hanoi
```

## Cài đặt

### Bước 1: Tạo file `.env`

Sao chép từ `.env.example`:

```bash
cp .env.example .env
```

### Bước 2: Cấu hình API Key

Đăng ký tài khoản miễn phí tại: https://openweathermap.org/api

Tại trang API:
1. Chọn **"Current weather data"** (free tier)
2. Lấy **API Key**
3. Mở file `.env` và điền vào `OPENWEATHER_API_KEY`

Ví dụ:
```env
OPENWEATHER_API_KEY=YOUR_API_KEY_HERE
```

### Bước 3: Cài đặt Dependencies

```bash
npm install
```

## Chạy Simulator

**Chế độ phát triển (có auto-reload):**
```bash
npm run dev
```

**Chế độ sản xuất:**
```bash
npm start
```

## Cấu hình

Chỉnh sửa file `.env`:

| Biến | Mô tả | Giá trị mặc định |
|------|-------|-----------------|
| `OPENWEATHER_API_KEY` | API Key từ OpenWeather | - |
| `OPENWEATHER_CITY` | Thành phố | `Hanoi` |
| `OPENWEATHER_COUNTRY_CODE` | Mã quốc gia | `VN` |
| `MQTT_BROKER_URL` | URL MQTT Broker | `mqtt://localhost:1883` |
| `MQTT_TOPIC` | MQTT Topic | `iot/weather/hanoi` |
| `PUBLISH_INTERVAL` | Tần suất gửi (ms) | `15000` (15 giây) |
| `LOG_LEVEL` | Mức độ log | `info` |

## Hiểu code

### File `app.js` - các thành phần chính:

1. **Import thư viện** (line ~20)
   - `axios`: HTTP client
   - `mqtt`: MQTT client
   - `dotenv`: Quản lý biến môi trường

2. **Cấu hình** (line ~30)
   - Lấy biến từ `.env` file

3. **Kết nối MQTT** (line ~70)
   - Hàm `connectMQTT()`: Kết nối đến MQTT Broker
   - Xử lý sự kiện kết nối/mất kết nối

4. **Gọi OpenWeather API** (line ~120)
   - Hàm `fetchWeatherData()`: HTTP GET request
   - Xử lý response JSON
   - Trích xuất dữ liệu cần thiết

5. **Publish MQTT** (line ~180)
   - Hàm `publishToMQTT()`: Gửi JSON lên MQTT topic
   - QoS = 1 (đảm bảo ít nhất 1 lần)

6. **Vòng lặp định kỳ** (line ~210)
   - Hàm `startPublishing()`: Dùng `setInterval()` để gửi mỗi N giây

## Kiểm tra hoạt động

### Cách 1: Xem log của Simulator

Khi chạy `npm start`, bạn sẽ thấy:

```
[10/04/2026 14:30:45] [SUCCESS] ✓ Kết nối MQTT thành công!
[10/04/2026 14:30:45] [INFO] MQTT Broker: mqtt://localhost:1883
[10/04/2026 14:30:45] [INFO] MQTT Topic: iot/weather/hanoi
[10/04/2026 14:30:46] [SUCCESS] ✓ Lấy dữ liệu thời tiết thành công!
[10/04/2026 14:30:46] [INFO] Nhiệt độ: 28.5°C, Độ ẩm: 65%
[10/04/2026 14:30:46] [SUCCESS] ✓ Đã publish dữ liệu lên MQTT
```

### Cách 2: Dùng script test MQTT

Xem `scripts/test-mqtt.js` để subscribe topic và nhận dữ liệu.

## Lỗi thường gặp

### "API Key không hợp lệ"
- Kiểm tra file `.env` có đúng API Key không
- API Key có bị expired không (thường hết khi không sử dụng)

### "Không thể kết nối đến MQTT Broker"
- Kiểm tra MQTT Broker có chạy không (`docker-compose up`)
- Kiểm tra URL MQTT đúng không (mặc định `localhost:1883`)

### "Timeout gọi API"
- Kiểm tra kết nối Internet
- OpenWeather API có thể bị chậm, tăng timeout trong code

## Bài tập cho sinh viên

1. **Thay đổi tần suất**: Sửa `PUBLISH_INTERVAL` để gửi 1 giây 1 lần
2. **Thêm city khác**: Sửa code để publish dữ liệu từ nhiều thành phố
3. **Lọc dữ liệu**: Chỉ publish khi nhiệt độ thay đổi hơn 1°C
4. **Error handling**: Tái kết nối tự động khi API fail
5. **Lưu log**: Ghi dữ liệu mỗi lần publish vào file

## Tài liệu tham khảo

- OpenWeather API: https://openweathermap.org/api
- MQTT Protocol: https://mqtt.org/
- Node.js mqtt library: https://github.com/mqttjs/MQTT.js
