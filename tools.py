"""
Tools - Herramientas disponibles para el agente de codificación
"""

import subprocess
import os
import shutil
import json
from pathlib import Path
from typing import List, Dict, Any


def run_terminal_command(command: str) -> str:
    """
    Ejecuta un comando en la terminal y devuelve su salida.
    
    Args:
        command: Comando a ejecutar
    Returns:
        Salida del comando o mensaje de error
    """
    print(f"🖥️ Ejecutando: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            timeout=60,  # Timeout más largo para comandos complejos
            cwd=os.getcwd()  # Usar directorio actual
        )
        output = result.stdout.strip()
        if result.stderr:
            output += f"\n[stderr]: {result.stderr.strip()}"
        return f"Éxito: {output}" if output else "Comando ejecutado exitosamente (sin salida)"
    except subprocess.CalledProcessError as e:
        return f"Error (código {e.returncode}): {e.stderr.strip() if e.stderr else e.stdout.strip()}"
    except subprocess.TimeoutExpired:
        return "Error: El comando tardó demasiado en ejecutarse (timeout 60s)"
    except Exception as e:
        return f"Error inesperado: {e}"


def read_file(filepath: str) -> str:
    """
    Lee el contenido completo de un archivo.
    
    Args:
        filepath: Ruta del archivo a leer
    Returns:
        Contenido del archivo o mensaje de error
    """
    print(f"📄 Leyendo: {filepath}")
    try:
        path = Path(filepath)
        if not path.exists():
            return f"Error: El archivo {filepath} no existe"
        
        if path.is_dir():
            return f"Error: {filepath} es un directorio, no un archivo"
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Mostrar información del archivo
        size = len(content)
        lines = content.count('\n') + 1 if content else 0
        return f"Archivo leído exitosamente:\nTamaño: {size} caracteres, {lines} líneas\n\n{content}"
        
    except UnicodeDecodeError:
        return f"Error: No se puede leer {filepath} - archivo binario o codificación incompatible"
    except PermissionError:
        return f"Error: Sin permisos para leer {filepath}"
    except Exception as e:
        return f"Error al leer el archivo: {e}"


def write_file(filepath: str, content: str) -> str:
    """
    Escribe contenido en un archivo (sobrescribe si existe).
    
    Args:
        filepath: Ruta del archivo
        content: Contenido a escribir
    Returns:
        Mensaje de confirmación o error
    """
    print(f"✍️ Escribiendo: {filepath}")
    try:
        path = Path(filepath)
        
        # Crear directorios padre si no existen
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        size = len(content)
        lines = content.count('\n') + 1 if content else 0
        return f"Archivo {filepath} escrito exitosamente. Tamaño: {size} caracteres, {lines} líneas."
        
    except PermissionError:
        return f"Error: Sin permisos para escribir en {filepath}"
    except Exception as e:
        return f"Error al escribir el archivo: {e}"


def list_directory(path: str = ".") -> str:
    """
    Lista el contenido de un directorio.
    
    Args:
        path: Ruta del directorio (por defecto: directorio actual)
    Returns:
        Lista de archivos y directorios
    """
    print(f"📁 Listando directorio: {path}")
    try:
        dir_path = Path(path)
        if not dir_path.exists():
            return f"Error: El directorio {path} no existe"
        
        if not dir_path.is_dir():
            return f"Error: {path} no es un directorio"
        
        items = []
        for item in sorted(dir_path.iterdir()):
            if item.is_dir():
                items.append(f"📁 {item.name}/")
            else:
                size = item.stat().st_size
                items.append(f"📄 {item.name} ({size} bytes)")
        
        if not items:
            return f"El directorio {path} está vacío"
        
        return f"Contenido de {path}:\n" + "\n".join(items)
        
    except PermissionError:
        return f"Error: Sin permisos para acceder a {path}"
    except Exception as e:
        return f"Error al listar directorio: {e}"


def create_directory(path: str) -> str:
    """
    Crea un directorio (y sus directorios padre si es necesario).
    
    Args:
        path: Ruta del directorio a crear
    Returns:
        Mensaje de confirmación o error
    """
    print(f"📁 Creando directorio: {path}")
    try:
        dir_path = Path(path)
        dir_path.mkdir(parents=True, exist_ok=True)
        return f"Directorio {path} creado exitosamente"
    except PermissionError:
        return f"Error: Sin permisos para crear el directorio {path}"
    except Exception as e:
        return f"Error al crear directorio: {e}"


def find_files(pattern: str, directory: str = ".") -> str:
    """
    Busca archivos que coincidan con un patrón.
    
    Args:
        pattern: Patrón de búsqueda (ej: "*.py", "test_*")
        directory: Directorio donde buscar
    Returns:
        Lista de archivos encontrados
    """
    print(f"🔍 Buscando archivos: {pattern} en {directory}")
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return f"Error: El directorio {directory} no existe"
        
        matches = list(dir_path.rglob(pattern))
        
        if not matches:
            return f"No se encontraron archivos que coincidan con '{pattern}' en {directory}"
        
        result = f"Archivos encontrados ({len(matches)}):\n"
        for match in sorted(matches):
            relative_path = match.relative_to(dir_path)
            result += f"📄 {relative_path}\n"
        
        return result.strip()
        
    except Exception as e:
        return f"Error en la búsqueda: {e}"


def get_working_directory() -> str:
    """
    Obtiene el directorio de trabajo actual.
    
    Returns:
        Ruta del directorio actual
    """
    current_dir = os.getcwd()
    print(f"📍 Directorio actual: {current_dir}")
    return f"Directorio actual: {current_dir}"


# Mapeo de herramientas disponibles
AVAILABLE_TOOLS = {
    "run_terminal_command": run_terminal_command,
    "read_file": read_file,
    "write_file": write_file,
    "list_directory": list_directory,
    "create_directory": create_directory,
    "find_files": find_files,
    "get_working_directory": get_working_directory,
}

# Descripciones de herramientas para el modelo de IA
TOOL_DESCRIPTIONS = """
---
HERRAMIENTAS DISPONIBLES

Puedes usar las siguientes herramientas para completar tareas:

1. **run_terminal_command(command: str)**
   Ejecuta un comando en la terminal del sistema.
   Ejemplo: run_terminal_command('ls -la')

2. **read_file(filepath: str)**
   Lee el contenido completo de un archivo.
   Ejemplo: read_file('main.py')

3. **write_file(filepath: str, content: str)**
   Escribe contenido en un archivo (lo crea o sobrescribe).
   Ejemplo: write_file('hello.py', 'print("Hola Mundo")')

4. **list_directory(path: str)**
   Lista el contenido de un directorio.
   Ejemplo: list_directory('.') o list_directory('/Users/usuario/proyecto')

5. **create_directory(path: str)**
   Crea un directorio (y directorios padre si es necesario).
   Ejemplo: create_directory('nuevo_proyecto/src')

6. **find_files(pattern: str, directory: str)**
   Busca archivos que coincidan con un patrón en un directorio.
   Ejemplo: find_files('*.py', '.') o find_files('test_*', 'tests')

7. **get_working_directory()**
   Obtiene el directorio de trabajo actual.
   Ejemplo: get_working_directory()

IMPORTANTE:
- Usa comillas simples para strings en los argumentos
- Siempre verifica el resultado de tus acciones
- Para tareas complejas, divídelas en pasos más pequeños
---
"""