import requests
from bs4 import BeautifulSoup
import json
import os

news_text = '''
╔═╗┌─┐┌─┐┬ ┬  ╔═╗┌─┐┬─┐┌─┐┌─┐┬┌┐┌┌─┐
╠╣ ├─┤│  │ │  ╚═╗│  ├┬┘├─┤├─┘│││││ ┬
╚  ┴ ┴└─┘└─┘  ╚═╝└─┘┴└─┴ ┴┴  ┴┘└┘└─┘
'''

def fetch_data_from_api(url):
    """Fetches the JSON data from the API at the specified URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al acceder a la API: {e}")
        return None

def clean_mensajes_data(data):
    """Cleans the 'mensajes' data from the API response, removing HTML tags."""
    mensajes = data.get('mensajes', [])
    mensajes_limpios = []

    for mensaje in mensajes:
        materia = mensaje['materia']
        titulo = mensaje['titulo']
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

    return mensajes_limpios

def load_json(filepath):
    """Loads JSON data from the specified file, or returns None if the file does not exist."""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return None

def save_json(filepath, data):
    """Saves the given data as JSON to the specified file."""
    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"JSON guardado correctamente en '{filepath}'")

def create_composite_key(materia_info):
    """Crea una clave compuesta usando los atributos relevantes para identificar una entrada única."""
    return f"{materia_info['materia']}|{materia_info['titulo']}|{materia_info['fecha']}"

def compare_data(new_data, old_data):
    """Compares the new data with the old data and returns a list of new or updated materias."""
    new_materias = []
    
    # Crear un diccionario de las materias antiguas usando una clave compuesta
    old_data_dict = {create_composite_key(materia): materia for materia in old_data}
    
    # Crear un diccionario de las materias nuevas usando una clave compuesta
    new_data_dict = {create_composite_key(materia): materia for materia in new_data}
    
    for key, new_info in new_data_dict.items():
        if key not in old_data_dict:
            new_materias.append(new_info)
        else:
            old_info = old_data_dict[key]
            for campo, valor_nuevo in new_info.items():
                valor_viejo = old_info.get(campo)
                if valor_nuevo != valor_viejo:
                    new_materias.append(new_info)
                    break  # Salimos del bucle una vez que encontramos una diferencia
    
    return new_materias

def imprimir_informacion_materia(materia_info):
    """Imprime de forma clara y formateada la información de una materia."""
    print(f"Materia: {materia_info['materia']}")
    print(f"Título: {materia_info['titulo']}")
    print("Cuerpo:")
    print(materia_info['cuerpo'])
    print(f"Fecha: {materia_info['fecha']}")
    print(f"Autor: {materia_info['autor']}")
    if materia_info['adjuntos']:
        print("Adjuntos:")
        for adjunto in materia_info['adjuntos']:
            print(f"- {adjunto['nombre']}: {adjunto['public_path']}")
    else:
        print("Adjuntos: No hay archivos adjuntos.")
    print("\n" + "="*50 + "\n")

def main():
    api_url = "https://gestiondocente.info.unlp.edu.ar/cartelera/data/0/10?idMateria="
    archivo_json = 'mensajes_limpios.json'
    os.system('cls')
    print(news_text)
    # Fetch the new data from the API
    raw_data = fetch_data_from_api(api_url)
    if raw_data:
        # Clean the data
        datos_nuevos = clean_mensajes_data(raw_data)

        # Load the previously saved data
        datos_guardados = load_json(archivo_json)
        
        if datos_guardados:
            # Compare the new data with the old data and get new materias
            nuevas_materias = compare_data(datos_nuevos, datos_guardados)
            if nuevas_materias:
                print("¡Se han agregado nuevas materias!")
                print("\n" + "="*50 + "\n")
                for nueva_materia in nuevas_materias:
                    imprimir_informacion_materia(nueva_materia)
                # Save the new data
                save_json(archivo_json, datos_nuevos)
            else:
                print("No hay nuevas materias.")
        else:
            print("No se encontraron datos previos. Guardando los datos actuales.")
            save_json(archivo_json, datos_nuevos)

if __name__ == "__main__":
    main()
