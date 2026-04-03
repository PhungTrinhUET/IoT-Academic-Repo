"""
Test OpenWeather API

Script này để test kết nối và lấy dữ liệu từ OpenWeather API.
Chạy trước để đảm bảo API key và cấu hình đúng.

Cách chạy:
    python test_openweather.py
"""

import requests
from config import OPENWEATHER_API_KEY, CITY

def test_openweather():
    """Test kết nối OpenWeather API"""
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": CITY,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    print(f"=== TEST OPENWEATHER API ===")
    print(f"City: {CITY}")
    print(f"URL: {url}")
    print(f"Params: {params}")
    print()

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✓ Kết nối OpenWeather API thành công!")
            print()
            print("Dữ liệu nhận được:")
            print(f"  - City: {data['name']}")
            print(f"  - Temperature: {data['main']['temp']}°C")
            print(f"  - Humidity: {data['main']['humidity']}%")
            print(f"  - Pressure: {data['main']['pressure']} hPa")
            print(f"  - Wind Speed: {data['wind']['speed']} m/s")
            print(f"  - Weather: {data['weather'][0]['description']}")
            print()
            print("Raw JSON:")
            print(response.text)
        else:
            print(f"✗ Lỗi! Status code: {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("✗ Lỗi kết nối! Kiểm tra internet connection")
    except requests.exceptions.Timeout:
        print("✗ Timeout! API không phản hồi")
    except Exception as e:
        print(f"✗ Lỗi: {e}")


if __name__ == "__main__":
    print()
    test_openweather()
    print()
