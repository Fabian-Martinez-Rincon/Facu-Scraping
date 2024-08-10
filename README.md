# Facu-Scraping

Proyecto para poder notificarme de todas las noticias referentes a la facultad

![image](https://github.com/user-attachments/assets/31d23238-230e-4f73-b826-c253986c2317)

Este código es un ejemplo completo de un script en Python diseñado para hacer web scraping de una página web específica, comparar los datos obtenidos con una versión anterior almacenada, y luego notificar cualquier cambio encontrado. A continuación, te explico cada parte del código en detalle:

### Importaciones

```python
import requests
from bs4 import BeautifulSoup
import json
import os
```

- **`requests`**: Una biblioteca para hacer solicitudes HTTP en Python. Se usa para obtener el contenido de la página web.
- **`BeautifulSoup`**: Parte de la biblioteca `bs4`, utilizada para analizar (parsear) documentos HTML y XML. Permite extraer información específica de páginas web de manera sencilla.
- **`json`**: Una biblioteca estándar de Python que permite trabajar con datos en formato JSON. Se usa para guardar y cargar datos en archivos JSON.
- **`os`**: Biblioteca estándar de Python que permite interactuar con el sistema operativo. Aquí se usa para verificar si un archivo existe.

### Función `fetch_webpage_content`

```python
def fetch_webpage_content(url):
    """Fetches the content of the webpage at the specified URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error al acceder a la página: {e}")
        return None
```

- **Propósito**: Esta función obtiene el contenido HTML de la página web especificada por `url`.
- **`requests.get(url)`**: Hace una solicitud GET al servidor para obtener el contenido de la página web en la URL dada.
- **`response.raise_for_status()`**: Lanza una excepción si la solicitud HTTP falla (por ejemplo, si la página no existe o hay problemas de conexión).
- **`return response.text`**: Devuelve el contenido HTML de la página como una cadena de texto.
- **Manejo de errores**: Si ocurre algún error en la solicitud HTTP, se captura con `except requests.RequestException`, se imprime un mensaje de error y se devuelve `None`.

### Función `parse_materias_from_html`

```python
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
```

- **Propósito**: Analiza el contenido HTML proporcionado y extrae una lista de diccionarios, donde cada diccionario representa una materia con sus detalles correspondientes.
- **`soup = BeautifulSoup(html_content, 'html.parser')`**: Crea un objeto `BeautifulSoup` que permite navegar y buscar en el HTML.
- **`tablas = soup.find_all('table', class_='table table-condensed table-striped table-bordered')`**: Encuentra todas las tablas en el HTML que coinciden con las clases especificadas (esto se basa en la estructura HTML de la página que estás scrapeando).
- **`filas = tabla.find_all('tr')[1:]`**: Para cada tabla, encuentra todas las filas (`tr`). La parte `[1:]` omite la primera fila, que se asume que es un encabezado.
- **`celdas = fila.find_all('td')`**: Dentro de cada fila, encuentra todas las celdas (`td`).
- **Creación de `materia_dict`**: Si hay al menos 5 celdas, se crean pares clave-valor para cada columna relevante (Materia, Carreras, Inicio Cursada, etc.) y se añaden a la lista `materias_list`.

### Función `load_json`

```python
def load_json(filepath):
    """Loads JSON data from the specified file, or returns None if the file does not exist."""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return None
```

- **Propósito**: Carga datos desde un archivo JSON en el sistema de archivos.
- **`os.path.exists(filepath)`**: Comprueba si el archivo especificado existe.
- **`with open(filepath, 'r', encoding='utf-8') as json_file:`**: Abre el archivo JSON en modo lectura con codificación UTF-8.
- **`json.load(json_file)`**: Carga el contenido del archivo JSON en un objeto de Python (normalmente una lista o un diccionario).
- **`return None`**: Si el archivo no existe, devuelve `None`.

### Función `save_json`

```python
def save_json(filepath, data):
    """Saves the given data as JSON to the specified file."""
    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"JSON guardado correctamente en '{filepath}'")
```

- **Propósito**: Guarda los datos proporcionados en un archivo JSON.
- **`with open(filepath, 'w', encoding='utf-8') as json_file:`**: Abre el archivo en modo escritura (`'w'`) con codificación UTF-8.
- **`json.dump(data, json_file, indent=4, ensure_ascii=False)`**: Escribe los datos en el archivo en formato JSON, con indentación de 4 espacios para hacer el archivo legible.
- **Mensaje de confirmación**: Se imprime un mensaje en la consola para confirmar que el archivo se ha guardado correctamente.

### Función `compare_materias`

```python
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
```

- **Propósito**: Compara los datos nuevos con los antiguos y devuelve una lista de los cambios detectados.
- **Conversión a diccionarios (`old_data_dict` y `new_data_dict`)**: Convierte las listas de diccionarios en diccionarios donde la clave es el nombre de la materia. Esto facilita la comparación entre las dos versiones de los datos.
- **Detección de cambios**:
  - **Materia nueva**: Si una materia en los datos nuevos no está en los antiguos, se añade un mensaje indicando que es una materia nueva.
  - **Cambios en los detalles**: Si una materia existe en ambas versiones, se comparan sus valores campo por campo. Si se encuentra una diferencia, se añade un mensaje con el cambio.
  - **Materia eliminada**: Si una materia en los datos antiguos no aparece en los nuevos, se añade un mensaje indicando que fue eliminada.

### Función `main`

```python
def main():
    url = "https://gestiondocente.info.unlp.edu.ar/cursadas/"
    archivo_json = 'materias.json'
    
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
```

- **Propósito**: Controla el flujo principal del programa, coordinando las llamadas a las funciones anteriores.
- **`url` y `archivo_json`**: Define la URL de la página web que se va a analizar y el nombre del archivo donde se almacenarán los datos JSON.
- **Lógica principal**:
  - **Fetch HTML**: Llama a `fetch_webpage_content` para obtener el HTML de la página.
  - **Parse HTML**: Si se obtuvo el HTML, llama a `parse_materias_from_html` para extraer los datos de las materias.
  - **Load previous data**: Intenta cargar los datos previamente guardados desde el archivo JSON.
  - **Compare and save**: Compara los datos nuevos con los antiguos utilizando `compare_materias`. Si hay cambios, se notifica y guarda la nueva versión de los datos. Si no hay cambios, solo se informa.

### Bloque de ejecución

```python
if __name__ == "__main__":
    main()
```

- **Propósito**: Asegura que la función `main` se ejecute solo si el script se está ejecutando directamente (no si se está importando como un módulo en otro script). Esto es una buena práctica en Python para organizar el código y permitir su reutilización.

### Resumen:

Este código es un sistema completo para realizar web scraping de una página, comparar los datos obtenidos con una versión anterior, y notificar cualquier cambio. Es modular, lo que facilita su mantenimiento y ampliación. Además, se asegura de manejar errores y de mantener un registro de los datos en archivos JSON, lo que permite detectar cambios en futuras ejecuciones del script.
