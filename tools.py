import subprocess
import os

def run_terminal_command(command):
    """
    Ejecuta un comando en la terminal y devuelve su salida (stdout y stderr).
    """
    print(f"🖥️ Ejecutando: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            timeout=30 # Añade un timeout de seguridad
        )
        return f"Éxito:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Error:\n{e.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: El comando tardó demasiado en ejecutarse."

def read_file(filepath):
    """
    Lee el contenido de un archivo en la ruta especificada.
    """
    print(f"📄 Leyendo: {filepath}")
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error al leer el archivo: {e}"

def write_file(filepath, content):
    """
    Escribe (o sobrescribe) contenido en un archivo.
    """
    print(f"✍️ Escribiendo en: {filepath}")
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Archivo {filepath} escrito exitosamente."
    except Exception as e:
        return f"Error al escribir el archivo: {e}"

# --- Mapeo y Descripciones de Herramientas ---

# Un diccionario para encontrar la función por su nombre
AVAILABLE_TOOLS = {
    "run_terminal_command": run_terminal_command,
    "read_file": read_file,
    "write_file": write_file,
}

# Una descripción que el modelo de IA entenderá
TOOL_DESCRIPTIONS = """
---
HERRAMIENTAS DISPONIBLES
Puedes usar las siguientes herramientas:

1.  **run_terminal_command(command: str)**
    Descripción: Ejecuta un comando de terminal (shell).
    Úsalo para listar archivos (ls -F), navegar directorios (cd), etc.

2.  **read_file(filepath: str)**
    Descripción: Lee el contenido completo de un archivo.
    
3.  **write_file(filepath: str, content: str)**
    Descripción: Escribe contenido en un archivo. Si el archivo existe, lo sobrescribe.
---
"""