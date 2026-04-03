/**
 * ========================================================================
 * IoT Weather Simulator
 * ========================================================================
 * 
 * Nhiệm vụ: 
 * 1. Gọi OpenWeather API mỗi 15 giây để lấy dữ liệu thời tiết Hà Nội
 * 2. Chuyển đổi dữ liệu thành JSON
 * 3. Publish lên MQTT topic "iot/weather/hanoi"
 * 
 * Kiến trúc học tập:
 * - axios: HTTP client để gọi API
 * - mqtt: MQTT client để kết nối broker và publish data
 * - dotenv: Quản lý environment variables
 * 
 * ========================================================================
 */

// ====== Bước 1: Import thư viện ======
require('dotenv').config();
const axios = require('axios');
const mqtt = require('mqtt');

// ====== Bước 2: Cấu hình từ environment variables ======
const config = {
    // Cấu hình OpenWeather API
    openweatherApiKey: process.env.OPENWEATHER_API_KEY || 'your_api_key_here',
    openweatherCity: process.env.OPENWEATHER_CITY || 'Hanoi',
    openweatherCountry: process.env.OPENWEATHER_COUNTRY_CODE || 'VN',
    
    // Cấu hình MQTT
    mqttBrokerUrl: process.env.MQTT_BROKER_URL || 'mqtt://localhost:1883',
    mqttTopic: process.env.MQTT_TOPIC || 'iot/weather/hanoi',
    mqttClientId: process.env.MQTT_CLIENT_ID || 'weather-simulator-' + Date.now(),
    
    // Cấu hình khác
    publishInterval: parseInt(process.env.PUBLISH_INTERVAL || 15000), // 15 giây
    logLevel: process.env.LOG_LEVEL || 'info'
};

// ====== Bước 3: Hàm logging ======
/**
 * Hàm in log ra console với timestamp
 * @param {string} level - Mức độ log (info, error, success)
 * @param {string} message - Nội dung message
 * @param {any} data - Dữ liệu kèm theo (tùy chọn)
 */
function log(level, message, data = '') {
    const timestamp = new Date().toLocaleString('vi-VN');
    console.log(`[${timestamp}] [${level.toUpperCase()}] ${message}`, data);
}

// ====== Bước 4: Biến toàn cục ======
let mqttClient = null;
let publishIntervalId = null;
let isConnected = false;

// ====== Bước 5: Hàm kết nối MQTT ======
/**
 * Kết nối đến MQTT Broker
 */
function connectMQTT() {
    log('info', 'Đang kết nối đến MQTT broker...', config.mqttBrokerUrl);
    
    mqttClient = mqtt.connect(config.mqttBrokerUrl, {
        clientId: config.mqttClientId,
        clean: true,
        reconnectPeriod: 5000,
        connectTimeout: 10000
    });
    
    // ===== Events xử lý kết nối =====
    
    // Khi kết nối thành công
    mqttClient.on('connect', function() {
        isConnected = true;
        log('success', '✓ Kết nối MQTT thành công!');
        log('info', 'MQTT Broker:', config.mqttBrokerUrl);
        log('info', 'MQTT Topic:', config.mqttTopic);
        log('info', 'Tần suất gửi dữ liệu:', (config.publishInterval / 1000) + ' giây');
        
        // Bắt đầu gửi dữ liệu định kỳ
        startPublishing();
    });
    
    // Khi mất kết nối
    mqttClient.on('disconnect', function() {
        isConnected = false;
        log('error', '✗ Mất kết nối MQTT');
        if (publishIntervalId) {
            clearInterval(publishIntervalId);
        }
    });
    
    // Khi gặp lỗi
    mqttClient.on('error', function(err) {
        log('error', 'Lỗi MQTT:', err.message);
    });
    
    // Khi reconnect
    mqttClient.on('reconnect', function() {
        log('info', 'Đang kết nối lại đến MQTT...');
    });
}

// ====== Bước 6: Hàm gọi OpenWeather API ======
/**
 * Gọi OpenWeather API để lấy dữ liệu thời tiết
 * @returns {Promise} - Promise trả về dữ liệu thời tiết
 */
async function fetchWeatherData() {
    try {
        log('info', 'Đang gọi OpenWeather API...');
        
        // API endpoint
        const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${config.openweatherCity},${config.openweatherCountry}&units=metric&lang=vi&appid=${config.openweatherApiKey}`;
        
        // Gọi API
        const response = await axios.get(apiUrl, {
            timeout: 5000 // 5 giây timeout
        });
        
        const data = response.data;
        
        // Xử lý dữ liệu từ API
        const weatherData = {
            // Thông tin vị trí
            location: data.name,
            country: data.sys.country,
            latitude: data.coord.lat,
            longitude: data.coord.lon,
            
            // Dữ liệu chính
            temperature: data.main.temp,          // Nhiệt độ (°C)
            feels_like: data.main.feels_like,     // Cảm thấy như
            temp_min: data.main.temp_min,         // Nhiệt độ tối thiểu
            temp_max: data.main.temp_max,         // Nhiệt độ tối đa
            humidity: data.main.humidity,         // Độ ẩm (%)
            pressure: data.main.pressure,         // Áp suất (hPa)
            
            // Thời tiết
            weather_main: data.weather[0].main,           // Loại chính (Clear, Clouds, Rain, v.v.)
            weather_description: data.weather[0].description, // Mô tả chi tiết
            
            // Gió
            wind_speed: data.wind.speed,          // Tốc độ gió (m/s)
            wind_deg: data.wind.deg || 0,         // Hướng gió (độ)
            
            // Tầm nhìn và mây
            visibility: data.visibility,          // Tầm nhìn (m)
            cloudiness: data.clouds.all,          // Độ mây (%)
            
            // Thời gian
            timestamp: new Date(data.dt * 1000).toISOString(),
            sunrise: new Date(data.sys.sunrise * 1000).toISOString(),
            sunset: new Date(data.sys.sunset * 1000).toISOString()
        };
        
        log('success', '✓ Lấy dữ liệu thời tiết thành công!');
        log('info', `Nhiệt độ: ${weatherData.temperature}°C, Độ ẩm: ${weatherData.humidity}%`);
        
        return weatherData;
        
    } catch (error) {
        if (error.response) {
            // API trả về lỗi
            if (error.response.status === 401) {
                log('error', 'API Key không hợp lệ! Vui lòng kiểm tra OPENWEATHER_API_KEY');
            } else {
                log('error', `API lỗi: ${error.response.status} - ${error.response.data?.message}`);
            }
        } else if (error.code === 'ENOTFOUND') {
            log('error', 'Không thể kết nối đến openweathermap.org (kiểm tra internet)');
        } else if (error.message.includes('timeout')) {
            log('error', 'API timeout - yêu cầu quá lâu');
        } else {
            log('error', `Lỗi gọi API: ${error.message}`);
        }
        return null;
    }
}

// ====== Bước 7: Hàm publish dữ liệu lên MQTT ======
/**
 * Publish dữ liệu thời tiết lên MQTT topic
 * @param {object} weatherData - Dữ liệu thời tiết cần gửi
 */
function publishToMQTT(weatherData) {
    if (!isConnected) {
        log('error', 'MQTT chưa kết nối, không thể publish');
        return;
    }
    
    try {
        // Chuyển object thành JSON string
        const payload = JSON.stringify(weatherData);
        
        // Publish lên topic với QoS = 1 (Guaranteed At Least Once)
        // QoS 0: At most once (không đảm bảo)
        // QoS 1: At least once (đảm bảo ít nhất 1 lần)
        // QoS 2: Exactly once (đảm bảo đúng 1 lần - chậm hơn)
        mqttClient.publish(
            config.mqttTopic,
            payload,
            { qos: 1 },
            function(err) {
                if (err) {
                    log('error', 'Lỗi publish MQTT:', err.message);
                } else {
                    log('success', '✓ Đã publish dữ liệu lên MQTT');
                }
            }
        );
        
    } catch (error) {
        log('error', 'Lỗi xử lý dữ liệu:', error.message);
    }
}

// ====== Bước 8: Hàm bắt đầu gửi dữ liệu định kỳ ======
/**
 * Bắt đầu gửi dữ liệu thời tiết mỗi N giây
 */
async function startPublishing() {
    log('info', `Bắt đầu gửi dữ liệu mỗi ${config.publishInterval / 1000} giây...`);
    
    // Gửi dữ liệu ngay lập tức (không chờ)
    const weatherData = await fetchWeatherData();
    if (weatherData) {
        publishToMQTT(weatherData);
    }
    
    // Sau đó gửi dữ liệu định kỳ
    publishIntervalId = setInterval(async () => {
        log('info', '------- Chu kỳ gửi dữ liệu -------');
        const weatherData = await fetchWeatherData();
        if (weatherData) {
            publishToMQTT(weatherData);
        }
    }, config.publishInterval);
}

// ====== Bước 9: Xử lý tín hiệu dừng chương trình ======
/**
 * Xử lý khi nhận tín hiệu dừng (Ctrl+C hoặc kill)
 */
process.on('SIGINT', () => {
    log('info', '\nNhận tín hiệu dừng, đang đóng...');
    
    // Dừng gửi dữ liệu
    if (publishIntervalId) {
        clearInterval(publishIntervalId);
    }
    
    // Ngắt kết nối MQTT
    if (mqttClient) {
        mqttClient.end();
    }
    
    log('success', '✓ Ứng dụng đã dừng');
    process.exit(0);
});

// ====== Bước 10: Kiểm tra cấu hình ======
/**
 * Kiểm tra cấu hình trước khi chạy
 */
function validateConfig() {
    log('info', '========= KIỂM TRA CẤU HÌNH =========');
    
    if (config.openweatherApiKey === 'your_api_key_here') {
        log('error', '⚠ API Key chưa được cấu hình!');
        log('info', '  1. Đăng ký tài khoản miễn phí tại: https://openweathermap.org/api');
        log('info', '  2. Lấy API key');
        log('info', '  3. Đặt vào biến OPENWEATHER_API_KEY trong file .env');
        return false;
    }
    
    log('success', '✓ Cấu hình hợp lệ');
    log('info', 'OpenWeather API Key:', '***' + config.openweatherApiKey.slice(-4));
    log('info', 'MQTT Broker:', config.mqttBrokerUrl);
    
    return true;
}

// ====== Bước 11: Hàm main - chạy ứng dụng ======
/**
 * Hàm chính - khởi động ứng dụng
 */
async function main() {
    console.log('\n');
    console.log('╔════════════════════════════════════════════════════╗');
    console.log('║     IoT Weather Simulator - MQTT Publisher         ║');
    console.log('║         Lấy dữ liệu OpenWeather & Publish MQTT    ║');
    console.log('╚════════════════════════════════════════════════════╝');
    console.log('\n');
    
    // Kiểm tra cấu hình
    if (!validateConfig()) {
        process.exit(1);
    }
    
    console.log('\n');
    
    // Kết nối MQTT
    connectMQTT();
}

// ====== BẮT ĐẦU CHƯƠNG TRÌNH ======
main();
