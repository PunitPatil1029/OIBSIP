
import requests
from config import API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherAPIError(Exception):
    """Custom error for weather API problems."""
    pass


def fetch_weather(endpoint, city):
    """Fetch weather information from OpenWeatherMap."""

    city = city.strip()

    if not city:
        raise WeatherAPIError("Please enter a city name.")

    url = f"{BASE_URL}/{endpoint}"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code == 401:
            message = data.get("message", "Invalid or inactive API key.")
            raise WeatherAPIError(f"OpenWeatherMap says: {message}")

        if response.status_code == 404:
            raise WeatherAPIError(
                "City not found. Please enter a valid city name."
            )

        if response.status_code != 200:
            message = data.get("message", "Weather service error.")
            raise WeatherAPIError(message.capitalize())

        return data

    except requests.exceptions.Timeout:
        raise WeatherAPIError("Request timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        raise WeatherAPIError(
            "No internet connection. Please check your network."
        )

    except requests.exceptions.RequestException:
        raise WeatherAPIError(
            "Unable to connect to the weather service."
        )

    except ValueError:
        raise WeatherAPIError(
            "Invalid response received from the weather service."
        )


def get_current_weather(city):
    return fetch_weather("weather", city)


def get_forecast(city):
    return fetch_weather("forecast", city)
