import requests

latitud = -32
longitud = -58
fecha = '2021-09-01'

respuesta = requests.get(f'https://api.sunrise-sunset.org/json?lat={latitud}&lng={longitud}&date={fecha}')

print(respuesta.json())

print(respuesta.json()['status'])

print(respuesta.json()['results']['sunset'])