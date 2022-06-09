from weather_api_service import Weather
from weather_formater import format_weather
from datetime import datetime

from pathlib import Path


def save_text_in_file(text: Weather):
    file = Path.cwd()/"history.txt"
    date = datetime.now()
    with open(file, "a") as f:
        f.write(f"\n{format_weather(text)}\n Request geting is {date}\n")

