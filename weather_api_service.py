from datetime import datetime
from typing import NamedTuple, Literal
from enum import Enum
import ssl
import json
import urllib.request

import config
from coordinates import Coordinates


class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморозь"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"

Celsius = int

class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates : Coordinates) -> Weather:
    try:
        open_weateher_respons = _get_openweather_respons(latitude=coordinates.latitude, longitude=coordinates.longitude)

    except TypeError:
        print(f"Не удалось получить погоду по координатам {coordinates} отработал файл ApiService")
        exit(1)
    try:
        weather = _parse_openweather_respons(open_weateher_respons)
    except TypeError:
        print(f"Не удалось получить погоду по координатам {coordinates} отработал файл ApiService")
        exit(1)
    return weather


def _get_openweather_respons(latitude:float, longitude:float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)
    return urllib.request.urlopen(url).read()


def _parse_openweather_respons(open_weateher_respons: str) -> Weather:
    openweather_dict = json.loads(open_weateher_respons)
    return Weather(
        temperature = _parse_temperature(openweather_dict),
        weather_type = _parse_weater_type(openweather_dict),
        sunrise = _parse_sun_time(openweather_dict, "sunrise"),
        sunset = _parse_sun_time(openweather_dict, "sunset"),
        city = _parse_city(openweather_dict)
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict["main"]["temp"])

def _parse_weater_type(openweather_dict:dict) -> WeatherType:
    weather_type_id = str(openweather_dict["weather"][0]["id"])
    weather_types = {
        "1": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type

def _parse_sun_time(openweather_dict:dict, time:Literal["sunrise"] or Literal["sunset"]) -> datetime:
    return datetime.fromtimestamp(openweather_dict["sys"][time])

def _parse_city(openweather_dict:dict) -> str:
    return openweather_dict["name"]


if __name__ == "__main__":
    print(get_weather(Coordinates(latitude=55.7, longitude=37.6)))
