
import pyowm
from config import OWM_TOKEN

owm = pyowm.OWM(OWM_TOKEN)
def get_forecast(place):
	observation = owm.weather_at_place(place)
	weather = observation.get_weather()
	temperature = weather.get_temperature('celsius')["temp"]
	wind = weather.get_wind()['speed']
	clouds = weather.get_clouds()
	humidity = weather.get_humidity()
	forecast = f" В {place} сейчас  \nТемпература {temperature} °C \nВетер {wind} m/s \nОблачно {clouds} % \nВлажность {humidity} %"
	return forecast