import requests
import time
from keys import WEATHER_KEY

api_url = 'http://api.openweathermap.org/data/2.5/weather?'

def get_weather(city='Saint Petersburg'):
    url = f"""{api_url}appid={WEATHER_KEY}&q={city}&units=metric&lang=en"""
    weather_data = requests.get(url).json()

    if weather_data['cod'] in ('404', '400'):
        return weather_data['message'].capitalize()

    lon = weather_data['coord']['lon']
    lat = weather_data['coord']['lat']

    lon_degrees = int(lon) # degrees°
    lon_minutes = int((lon - lon_degrees) * 60) # minutes'
    lon_seconds = int((lon - lon_degrees - lon_minutes/60) * 3600) # seconds''

    lat_degrees = int(lat) # degrees°
    lat_minutes = int((lat - lat_degrees) * 60) # minutes'
    lat_seconds = int((lat - lat_degrees - lat_minutes/60) * 3600) # seconds''

    longitude = f"{lon_degrees}°{lon_minutes}'{lon_seconds}'' N"
    latitude = f"{lat_degrees}°{lat_minutes}'{lat_seconds}'' E"

    return f"""Weather in: {weather_data['sys']['country']}, {weather_data['name']} ({longitude}, {latitude})\nTime: {time.ctime()}
    • Weather: \t{weather_data['weather'][0]['description'].capitalize()}
    • Temperature: \t{weather_data['main']['temp']}℃ (feels {weather_data['main']['feels_like']}℃)
    • Humidity: \t{weather_data['main']['humidity']}%
    • Pressure: \t{weather_data['main']['pressure']} hPa """

def get_location_weather(lon=30.2642, lat=59.8944):
    ''' Longitude and latitude geographic coordinates. '''
    url = f"""{api_url}appid={WEATHER_KEY}&lon={lon}&lat={lat}&units=metric&lang=en"""
    weather_data = requests.get(url).json()

    if weather_data['cod'] in ('404', '400'):
        # Wrong latitude or wrong latitude
        return weather_data['message'].capitalize()

    lon_degrees = int(lon) # degrees°
    lon_minutes = int((lon - lon_degrees) * 60) # minutes'
    lon_seconds = int((lon - lon_degrees - lon_minutes/60) * 3600) # seconds''

    lat_degrees = int(lat) # degrees°
    lat_minutes = int((lat - lat_degrees) * 60) # minutes'
    lat_seconds = int((lat - lat_degrees - lat_minutes/60) * 3600) # seconds''

    longitude = f"{lon_degrees}°{lon_minutes}'{lon_seconds}'' N"
    latitude = f"{lat_degrees}°{lat_minutes}'{lat_seconds}'' E"

    return f"""Weather in: {weather_data['sys']['country']}, {weather_data['name']} ({longitude}, {latitude})\nTime: {time.ctime()}
    • Weather: \t{weather_data['weather'][0]['description'].capitalize()}
    • Temperature: \t{weather_data['main']['temp']}℃ (feels {weather_data['main']['feels_like']}℃)
    • Humidity: \t{weather_data['main']['humidity']}%
    • Pressure: \t{weather_data['main']['pressure']} hPa """

if __name__ == '__main__':
    print(get_location_weather(10, 43))
