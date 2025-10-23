
import requests
from langchain.tools import Tool, tool
from langchain_community.tools import DuckDuckGoSearchRun

from digital_twin.config import settings

# Get API key from https://openweathermap.org/api
# Free tier: 1000 calls/day

WEATHER_API_KEY = settings.OPENWEATHER_API_KEY
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


search_tool = Tool(
    name="WebSearch",
    func=DuckDuckGoSearchRun().run,
    description="""Search the internet for current information.

    Input: Search query as string (e.g., "Tesla stock price 2024", "GDP growth USA")
    Returns: Recent search results and snippets

    Use this when you need:
    - Current/recent information not in your training
    - News or events
    - Statistics or data
    - Real-time facts

    Do NOT use for:
    - General knowledge from training data"""
)

def get_weather_data(city: str) -> dict:
    """
    Fetch current weather data for a given city.

    Args:
        city: City name (e.g., "London", "New York", "Tokyo")

    Returns:
        Dictionary with weather information or error message
    """
    try:
        # Make API request
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"  # Celsius
        }

        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        

        data = response.json()

        # Extract relevant information
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }

        return weather_info

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}
    except KeyError as e:
        return {"error": f"Unexpected API response format: {str(e)}"}


# create the funtion that will be used on the tool
def weather_lookup(city_name: str) -> str:
    """
    Look up current weather for a city.

    This tool provides real-time weather information including
    temperature, conditions, and wind speed.
    """
    data = get_weather_data(city_name)

    if "error" in data:
        return f"Unable to get weather for {city_name}: {data['error']}"

    # Format as natural language response
    return f"""Current weather in {data['city']}, {data['country']}:
- Temperature: {data['temperature']}°C (feels like {data['feels_like']}°C)
- Conditions: {data['description']}
- Humidity: {data['humidity']}%
- Wind speed: {data['wind_speed']} m/s"""

weather_tool = Tool(
    name="WeatherLookup",
    func=weather_lookup,
    description="""Useful for getting current weather information for any city.
    Input should be a city name (e.g., 'Paris', 'New York', 'Tokyo').
    Returns current temperature, conditions, humidity, and wind speed.
    Use this when users ask about weather or current conditions in a location."""
)


@tool
def travel_recommendation(weather_desc: str) -> str:
    """
    Recommend activities based on weather conditions.

    Input: Weather description (e.g., 'sunny', 'rainy', 'cloudy', 'snowy')
    Returns: List of suitable activities
    """
    weather_lower = weather_desc.lower()

    recommendations = {
        "clear/sunny": [
            "Visit outdoor attractions and parks",
            "Walking tours of the city",
            "Outdoor dining at local restaurants",
            "Photography excursions",
            "Beach activities (if coastal)"
        ],
        "clouds": [
            "Museum visits",
            "Indoor markets and shopping",
            "Cultural sites and galleries",
            "Local cuisine food tour",
            "Architecture walking tour"
        ],
        "rain": [
            "Art museums and galleries",
            "Indoor shopping centers",
            "Cooking classes",
            "Spa and wellness centers",
            "Theater or cinema"
        ],
        "snow": [
            "Winter sports (skiing, snowboarding)",
            "Ice skating",
            "Visit winter festivals",
            "Cozy cafes and restaurants",
            "Indoor attractions"
        ]
    }

    # Find matching weather type
    for weather_type, activities in recommendations.items():
        if weather_type in weather_lower:
            return f"Recommended activities for {weather_desc} weather:\n" + \
                   "\n".join(f"- {activity}" for activity in activities)

    return f"For {weather_desc} weather, consider checking indoor and outdoor options based on comfort level."
