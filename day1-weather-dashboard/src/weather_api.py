import requests
import time
from datetime import datetime

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather_data(self, city):
        """Fetch weather data for a given city."""
        try:
            api = f"{self.base_url}?q={city}&appid={self.api_key}"
            return requests.get(api).json()
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None

    def format_weather_display(self, weather_data):
        """Format weather data for display."""
        if not weather_data:
            return "Error fetching weather data", "Please try again"

        condition = weather_data['weather'][0]['main']
        temp = int(weather_data['main']['temp'] - 273.15)
        min_temp = int(weather_data['main']['temp_min'] - 273.15)
        max_temp = int(weather_data['main']['temp_max'] - 273.15)
        pressure = weather_data['main']['pressure']
        humidity = weather_data['main']['humidity']
        wind = weather_data['wind']['speed']
        sunrise = time.strftime('%I:%M:%S', time.gmtime(weather_data['sys']['sunrise'] - 21600))
        sunset = time.strftime('%I:%M:%S', time.gmtime(weather_data['sys']['sunset'] - 21600))

        main_info = f"{condition}\n{temp}°C"
        detailed_info = (f"\nMin Temp: {min_temp}°C\n"
                        f"Max Temp: {max_temp}°C\n"
                        f"Pressure: {pressure}\n"
                        f"Humidity: {humidity}\n"
                        f"Wind Speed: {wind}\n"
                        f"Sunrise: {sunrise}\n"
                        f"Sunset: {sunset}")

        return main_info, detailed_info