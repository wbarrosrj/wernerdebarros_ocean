# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 16:44:33 2021

@author: Werner
"""

import requests
import os
from datetime import datetime

api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=d415c3e11c3918481f6d1574033ab1b6&q='

#api_address2 = 'http://api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid=d415c3e11c3918481f6d1574033ab1b6&q='
cidade = input('País:') # Rio de Janeiro, BR
#estado = input('estado:')
#pais = input('pais:')

url = api_address + cidade

json_data = requests.get(url).json()


temp_city = ((json_data['main']['temp']) - 273.15)
coordenadas = json_data['coord']
weather_desc = json_data['weather'][0]['description']
hmdt = json_data['main']['humidity']
pressure = json_data['main']['pressure']
wind_spd = json_data['wind']['speed']
date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

print ("-------------------------------------------------------------")
print ("Clima para o Estado do - {}  || {}".format(cidade.upper(), date_time))
print ("-------------------------------------------------------------")
print("Posição Geográfica",coordenadas)
print ("Temperature atual: {:.2f} deg C".format(temp_city))
print ("Condições Climáticas  :",weather_desc)
print ("Umidade      :",hmdt, '%')
print ("Pressão      :",pressure, 'hPa')
print ("Velocidade do Vento    :",wind_spd ,'m/s')

#formatted_data = json_data['weather'][0]['main'] #nublado
#formatted_data = json_data['weather'][0]['description'] #nublado
#print(formatted_data)



