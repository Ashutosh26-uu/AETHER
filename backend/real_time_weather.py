import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import asyncio

class RealTimeWeatherService:
    def __init__(self):
        # Using OpenWeatherMap API (free tier)
        self.api_key = "demo_key"  # Replace with actual API key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    async def get_current_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        cache_key = f"{lat}_{lon}_current"
        
        # Check cache first
        if self.is_cache_valid(cache_key):
            return self.cache[cache_key]["data"]
        
        try:
            # For demo, using realistic weather simulation based on location
            weather_data = self.simulate_realistic_weather(lat, lon)
            
            # Cache the result
            self.cache[cache_key] = {
                "data": weather_data,
                "timestamp": datetime.now()
            }
            
            return weather_data
            
        except Exception as e:
            print(f"Weather API error: {e}")
            return self.get_fallback_weather()
    
    def simulate_realistic_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        # Simulate realistic weather based on geographic location
        import random
        import math
        
        # Delhi coordinates: 28.6139, 77.2090
        # Adjust temperature based on latitude (closer to equator = warmer)
        base_temp = 25 + (30 - abs(lat)) * 0.5
        
        # Add seasonal variation
        day_of_year = datetime.now().timetuple().tm_yday
        seasonal_adjustment = 10 * math.sin((day_of_year - 80) * 2 * math.pi / 365)
        
        # Add daily variation
        hour = datetime.now().hour
        daily_adjustment = 8 * math.sin((hour - 6) * math.pi / 12)
        
        temperature = base_temp + seasonal_adjustment + daily_adjustment + random.uniform(-3, 3)
        
        # Humidity based on temperature and location
        humidity = max(30, min(90, 80 - (temperature - 20) * 2 + random.uniform(-10, 10)))
        
        # Wind speed
        wind_speed = random.uniform(5, 25)
        
        # Weather conditions based on humidity and temperature
        if humidity > 80 and temperature < 25:
            condition = "Rain"
            visibility = random.uniform(2, 8)
        elif humidity > 70:
            condition = "Cloudy"
            visibility = random.uniform(8, 12)
        elif temperature > 35:
            condition = "Hot"
            visibility = random.uniform(10, 15)
        else:
            condition = "Clear"
            visibility = random.uniform(12, 20)
        
        return {
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "wind_speed": round(wind_speed, 1),
            "visibility": round(visibility, 1),
            "condition": condition,
            "pressure": round(1013 + random.uniform(-20, 20), 1),
            "uv_index": max(0, min(11, int((temperature - 15) / 3) + random.randint(-2, 2))),
            "air_quality": {
                "aqi": random.randint(50, 200),
                "pm25": round(random.uniform(10, 100), 1),
                "co2": round(random.uniform(400, 600), 1),
                "pollution_level": random.choice(["LOW", "MODERATE", "HIGH"])
            },
            "forecast_6h": self.generate_forecast(temperature, condition, 6),
            "forecast_24h": self.generate_forecast(temperature, condition, 24),
            "location": {"lat": lat, "lon": lon},
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_forecast(self, base_temp: float, base_condition: str, hours: int) -> Dict[str, Any]:
        import random
        
        temp_change = random.uniform(-5, 5)
        conditions = ["Clear", "Cloudy", "Rain", "Fog"]
        
        if base_condition == "Rain":
            next_condition = random.choice(["Rain", "Cloudy", "Clear"])
        else:
            next_condition = random.choice(conditions)
        
        return {
            "temperature": round(base_temp + temp_change, 1),
            "condition": next_condition,
            "precipitation_chance": random.randint(0, 100),
            "hours_ahead": hours
        }
    
    def is_cache_valid(self, cache_key: str) -> bool:
        if cache_key not in self.cache:
            return False
        
        cache_time = self.cache[cache_key]["timestamp"]
        return (datetime.now() - cache_time).seconds < self.cache_duration
    
    def get_fallback_weather(self) -> Dict[str, Any]:
        return {
            "temperature": 25.0,
            "humidity": 60.0,
            "wind_speed": 10.0,
            "visibility": 10.0,
            "condition": "Clear",
            "pressure": 1013.0,
            "uv_index": 5,
            "air_quality": {
                "aqi": 100,
                "pm25": 50.0,
                "co2": 400.0,
                "pollution_level": "MODERATE"
            },
            "location": {"lat": 28.6139, "lon": 77.2090},
            "timestamp": datetime.now().isoformat(),
            "source": "fallback"
        }

# Global weather service instance
weather_service = RealTimeWeatherService()