from coordinates import get_coordinates
from weather_api_service import get_weather
from weather_formater import format_weather
from history import save_text_in_file



def main():
    try:
        coordinates = get_coordinates()
    except AttributeError:
        print("Не удалось получить GPS координаты")
        exit(1)
    try:
        weather = get_weather(coordinates)
    except AttributeError:
        print(f"Не удалось получить погоду по координатам {coordinates}")
        exit()
    format_text = format_weather(weather)
    print(format_text)
    save_text_in_file(weather)


if __name__ == "__main__":
    main()

