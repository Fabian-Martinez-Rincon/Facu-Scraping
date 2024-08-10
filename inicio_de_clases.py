import requests
from bs4 import BeautifulSoup
import json
import os


def fetch_webpage_content(url):
    """Fetches the content of the webpage at the specified URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error al acceder a la página: {e}")
        return None

def parse_materias_from_html(html_content):
    """Parses the HTML content and extracts a list of dictionaries representing each 'materia'."""
    soup = BeautifulSoup(html_content, 'html.parser')
    tablas = soup.find_all('table', class_='table table-condensed table-striped table-bordered')
    
    materias_list = []
    for tabla in tablas:
        filas = tabla.find_all('tr')[1:]  # Skip the header row
        for fila in filas:
            celdas = fila.find_all('td')
            if len(celdas) >= 5:
                materia_dict = {
                    "Materia": celdas[0].text.strip(),
                    "Carreras": celdas[1].text.strip(),
                    "Inicio Cursada": celdas[2].text.strip(),
                    "Horarios Cursada": celdas[3].text.strip(),
                    "Última modificación": celdas[4].text.strip()
                }
                materias_list.append(materia_dict)
    
    return materias_list


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


def compare_materias(new_data, old_data):
    """Compares the new data with the old data and returns a list of changes."""
    changes = []
    
    old_data_dict = {
        materia['Materia']: materia 
        for materia in old_data
    }
    
    new_data_dict = {
        materia['Materia']: materia 
        for materia in new_data
    }
    
    for materia, new_info in new_data_dict.items():
        if materia not in old_data_dict:
            changes.append(f"Nueva materia agregada: {materia}")
        else:
            old_info = old_data_dict[materia]
            for key, new_value in new_info.items():
                old_value = old_info.get(key)
                if new_value != old_value:
                    changes.append(f"Cambio en {materia} - {key}: '{old_value}' -> '{new_value}'")
    
    for materia in old_data_dict:
        if materia not in new_data_dict:
            changes.append(f"Materia eliminada: {materia}")
    
    return changes


def main():
    url = "https://gestiondocente.info.unlp.edu.ar/cursadas/"
    archivo_json = 'materias.json'
    print("Inicio de Clases - Segundo Semestre 2024:")
    html_content = fetch_webpage_content(url)
    if html_content:
        datos_nuevos = parse_materias_from_html(html_content)
        datos_guardados = load_json(archivo_json)
        
        if datos_guardados:
            cambios = compare_materias(datos_nuevos, datos_guardados)
            if cambios:
                print("¡La página ha sido actualizada!")
                for cambio in cambios:
                    print(cambio)
                save_json(archivo_json, datos_nuevos)
            else:
                print("No hay cambios en la página.")
        else:
            print("No se encontraron datos previos. Guardando los datos actuales.")
            save_json(archivo_json, datos_nuevos)


if __name__ == "__main__":
    main()