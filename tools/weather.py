import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_weather(city: str, api_key: str = None) -> dict:
    """
    Get current weather for a city using OpenWeatherMap API.
    """
    if not api_key:
        api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return {
            "success": False,
            "error": "API key not provided. Set OPENWEATHER_API_KEY in .env file"
        }
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  # Celsius
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "success": True,
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }

