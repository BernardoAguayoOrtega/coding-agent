"""
Tools - Herramientas disponibles para el agente de codificación
Enhanced with reflection and code quality tools
"""

import subprocess
import os
import shutil
import json
import ast
from pathlib import Path
from typing import List, Dict, Any

# Import reflection and human loop systems
try:
    from reflection import CodeReflector, format_reflection_results, ReflectionType
    from human_loop import HumanInTheLoop, create_human_loop
    REFLECTION_AVAILABLE = True
except ImportError:
    REFLECTION_AVAILABLE = False
    print("⚠️ Reflection system not available")


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


def analyze_code_quality(filepath: str, reflection_types: str = "all") -> str:
    """
    Analiza la calidad del código usando el sistema de reflexión.
    
    Args:
        filepath: Ruta del archivo a analizar
        reflection_types: Tipos de reflexión separados por coma o "all"
    Returns:
        Resultados del análisis de calidad
    """
    if not REFLECTION_AVAILABLE:
        return "Error: Sistema de reflexión no disponible"
    
    print(f"🔍 Analizando calidad de código: {filepath}")
    
    try:
        # Leer el archivo
        path = Path(filepath)
        if not path.exists():
            return f"Error: El archivo {filepath} no existe"
        
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Configurar tipos de reflexión
        if reflection_types.lower() == "all":
            types = list(ReflectionType)
        else:
            type_names = [t.strip().lower() for t in reflection_types.split(',')]
            types = []
            for type_name in type_names:
                try:
                    types.append(ReflectionType(type_name))
                except ValueError:
                    pass
        
        # Ejecutar reflexión
        reflector = CodeReflector()
        results = reflector.reflect_on_code(code, filepath, types)
        
        # Formatear resultados
        return format_reflection_results(results)
        
    except Exception as e:
        return f"Error analizando código: {e}"


def lint_code(filepath: str) -> str:
    """
    Ejecuta linter específicamente en un archivo.
    
    Args:
        filepath: Ruta del archivo a verificar
    Returns:
        Resultados del linter
    """
    if not REFLECTION_AVAILABLE:
        return "Error: Sistema de reflexión no disponible"
    
    print(f"🔍 Ejecutando linter en: {filepath}")
    
    try:
        path = Path(filepath)
        if not path.exists():
            return f"Error: El archivo {filepath} no existe"
        
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        reflector = CodeReflector()
        results = reflector.reflect_on_code(code, filepath, [ReflectionType.LINTER])
        
        if results:
            result = results[0]
            output = f"📊 LINTER RESULTS - Score: {result.score}/100\n"
            output += "=" * 40 + "\n"
            
            if result.issues:
                output += "❌ Issues found:\n"
                for issue in result.issues:
                    output += f"  • {issue}\n"
            
            if result.suggestions:
                output += "\n💡 Suggestions:\n"
                for suggestion in result.suggestions:
                    output += f"  • {suggestion}\n"
            
            if not result.issues:
                output += "✅ No issues found!\n"
            
            return output
        else:
            return "Error: No se pudieron obtener resultados del linter"
        
    except Exception as e:
        return f"Error ejecutando linter: {e}"


def check_best_practices(filepath: str) -> str:
    """
    Verifica mejores prácticas en un archivo de código.
    
    Args:
        filepath: Ruta del archivo a verificar
    Returns:
        Resultados de mejores prácticas
    """
    if not REFLECTION_AVAILABLE:
        return "Error: Sistema de reflexión no disponible"
    
    return analyze_code_quality(filepath, "best_practices")


def check_solid_principles(filepath: str) -> str:
    """
    Verifica principios SOLID en un archivo de código.
    
    Args:
        filepath: Ruta del archivo a verificar
    Returns:
        Resultados de principios SOLID
    """
    if not REFLECTION_AVAILABLE:
        return "Error: Sistema de reflexión no disponible"
    
    return analyze_code_quality(filepath, "solid")


def check_dry_principle(filepath: str) -> str:
    """
    Verifica principio DRY en un archivo de código.
    
    Args:
        filepath: Ruta del archivo a verificar
    Returns:
        Resultados de principio DRY
    """
    if not REFLECTION_AVAILABLE:
        return "Error: Sistema de reflexión no disponible"
    
    return analyze_code_quality(filepath, "dry")


def run_tests(directory: str = ".", test_pattern: str = "test_*.py") -> str:
    """
    Ejecuta tests en un directorio usando pytest o unittest.
    
    Args:
        directory: Directorio donde buscar tests
        test_pattern: Patrón de archivos de test
    Returns:
        Resultados de los tests
    """
    print(f"🧪 Ejecutando tests en: {directory}")
    
    try:
        # Intentar con pytest primero
        pytest_result = subprocess.run(
            ["python", "-m", "pytest", directory, "-v"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if pytest_result.returncode == 0:
            return f"✅ Tests ejecutados exitosamente con pytest:\n{pytest_result.stdout}"
        else:
            # Intentar con unittest
            unittest_result = subprocess.run(
                ["python", "-m", "unittest", "discover", "-s", directory, "-p", test_pattern, "-v"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if unittest_result.returncode == 0:
                return f"✅ Tests ejecutados exitosamente con unittest:\n{unittest_result.stdout}"
            else:
                return f"❌ Tests fallaron:\npytest: {pytest_result.stderr}\nunittest: {unittest_result.stderr}"
    
    except subprocess.TimeoutExpired:
        return "⏰ Timeout ejecutando tests (>120s)"
    except FileNotFoundError:
        return "❌ Error: Python no encontrado en el PATH"
    except Exception as e:
        return f"❌ Error ejecutando tests: {e}"


def format_code(filepath: str, formatter: str = "autopep8") -> str:
    """
    Formatea código usando autopep8, black u otro formateador.
    
    Args:
        filepath: Ruta del archivo a formatear
        formatter: Formateador a usar ("autopep8", "black")
    Returns:
        Resultado del formateo
    """
    print(f"🎨 Formateando código: {filepath}")
    
    try:
        path = Path(filepath)
        if not path.exists():
            return f"Error: El archivo {filepath} no existe"
        
        if formatter == "autopep8":
            result = subprocess.run(
                ["python", "-m", "autopep8", "--in-place", "--aggressive", str(path)],
                capture_output=True,
                text=True,
                timeout=30
            )
        elif formatter == "black":
            result = subprocess.run(
                ["python", "-m", "black", str(path)],
                capture_output=True,
                text=True,
                timeout=30
            )
        else:
            return f"Error: Formateador '{formatter}' no soportado"
        
        if result.returncode == 0:
            return f"✅ Código formateado exitosamente con {formatter}"
        else:
            return f"❌ Error formateando: {result.stderr}"
    
    except subprocess.TimeoutExpired:
        return "⏰ Timeout formateando código"
    except FileNotFoundError:
        return f"❌ Error: {formatter} no encontrado. Instala con: pip install {formatter}"
    except Exception as e:
        return f"❌ Error formateando código: {e}"


# Mapeo de herramientas disponibles
AVAILABLE_TOOLS = {
    "run_terminal_command": run_terminal_command,
    "read_file": read_file,
    "write_file": write_file,
    "list_directory": list_directory,
    "create_directory": create_directory,
    "find_files": find_files,
    "get_working_directory": get_working_directory,
    "analyze_code_quality": analyze_code_quality,
    "lint_code": lint_code,
    "check_best_practices": check_best_practices,
    "check_solid_principles": check_solid_principles,
    "check_dry_principle": check_dry_principle,
    "run_tests": run_tests,
    "format_code": format_code,
}

# Descripciones de herramientas para el modelo de IA
TOOL_DESCRIPTIONS = """
---
HERRAMIENTAS DISPONIBLES

Puedes usar las siguientes herramientas para completar tareas:

## HERRAMIENTAS BÁSICAS

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
   Ejemplo: list_directory('.') o list_directory('/ruta/proyecto')

5. **create_directory(path: str)**
   Crea un directorio (y directorios padre si es necesario).
   Ejemplo: create_directory('nuevo_proyecto/src')

6. **find_files(pattern: str, directory: str)**
   Busca archivos que coincidan con un patrón en un directorio.
   Ejemplo: find_files('*.py', '.') o find_files('test_*', 'tests')

7. **get_working_directory()**
   Obtiene el directorio de trabajo actual.
   Ejemplo: get_working_directory()

## HERRAMIENTAS DE CALIDAD DE CÓDIGO

8. **analyze_code_quality(filepath: str, reflection_types: str)**
   Analiza la calidad del código usando múltiples técnicas de reflexión.
   reflection_types: "all", "linter", "best_practices", "simplicity", "solid", "dry", "tdd"
   Ejemplo: analyze_code_quality('main.py', 'all')

9. **lint_code(filepath: str)**
   Ejecuta verificación de linter específicamente.
   Ejemplo: lint_code('main.py')

10. **check_best_practices(filepath: str)**
    Verifica mejores prácticas de programación.
    Ejemplo: check_best_practices('main.py')

11. **check_solid_principles(filepath: str)**
    Evalúa principios SOLID en el código.
    Ejemplo: check_solid_principles('main.py')

12. **check_dry_principle(filepath: str)**
    Verifica principio DRY (Don't Repeat Yourself).
    Ejemplo: check_dry_principle('main.py')

13. **run_tests(directory: str, test_pattern: str)**
    Ejecuta tests usando pytest o unittest.
    Ejemplo: run_tests('.', 'test_*.py')

14. **format_code(filepath: str, formatter: str)**
    Formatea código usando autopep8 o black.
    Ejemplo: format_code('main.py', 'autopep8')

IMPORTANTE:
- Usa comillas simples para strings en los argumentos
- Siempre verifica el resultado de tus acciones
- Para tareas complejas, divídelas en pasos más pequeños
- Usa las herramientas de calidad ANTES de finalizar cualquier código
- El sistema de reflexión te ayudará a mejorar la calidad del código automáticamente
---
"""