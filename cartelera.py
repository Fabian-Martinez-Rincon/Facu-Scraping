import requests
from bs4 import BeautifulSoup
import json

# URL de la API
organizacion = "https://gestiondocente.info.unlp.edu.ar/cartelera/data/0/10?idMateria=61"

# Realizar la solicitud GET
response = requests.get(organizacion)


# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido JSON
    data = response.json()
    mensajes = data.get('mensajes', [])

    # Lista para guardar los mensajes limpios
    mensajes_limpios = []

    for mensaje in mensajes:
        materia = mensaje['materia']
        titulo = mensaje['titulo']
        # Utilizamos BeautifulSoup para eliminar etiquetas HTML y obtener texto limpio
        cuerpo = BeautifulSoup(mensaje['cuerpo'], 'html.parser').get_text(strip=True)
        fecha = mensaje['fecha']
        autor = mensaje['autor']
        adjuntos = mensaje['adjuntos']

        mensaje_limpio = {
            "materia": materia,
            "titulo": titulo,
            "cuerpo": cuerpo,
            "fecha": fecha,
            "autor": autor,
            "adjuntos": adjuntos
        }

        mensajes_limpios.append(mensaje_limpio)

    # Guardar el JSON limpio en un archivo
    with open('mensajes_limpios.json', 'w', encoding='utf-8') as json_file:
        json.dump(mensajes_limpios, json_file, indent=4, ensure_ascii=False)

    print("El JSON limpio ha sido guardado en 'mensajes_limpios.json'")

else:
    print(f"Error al acceder a la API: {response.status_code}")
