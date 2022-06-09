from geopy.geocoders import Nominatim
from typing import NamedTuple

geolocator = Nominatim(user_agent="Meteo")

class Coordinates(NamedTuple):
    latitude: float
    longitude: float

def get_coordinates() -> Coordinates:
    cyti = input("Введите назавание города: ")
    if cyti == "":
        cyti = "Москва"
    location = geolocator.geocode(cyti)
    return Coordinates(longitude=location.longitude, latitude=location.latitude)


if __name__ == "__main__":
    print(get_coordinates())

