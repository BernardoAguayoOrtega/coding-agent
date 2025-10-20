# Coding Agent 🤖

Un agente de IA autónomo especializado en tareas de programación y desarrollo, construido con DeepSeek Coder y Transformers.

## 🚀 Características

- **Agente Autónomo**: Puede planificar y ejecutar tareas de programación de manera independiente
- **Herramientas Integradas**: Acceso a sistema de archivos, terminal y operaciones de desarrollo
- **Interfaz de Terminal**: Fácil de usar desde la línea de comandos
- **Modo Interactivo**: Permite múltiples tareas en una sesión
- **Modelo Avanzado**: Utiliza DeepSeek Coder 6.7B para razonamiento de código

## 📋 Requisitos

- Python 3.8+
- CUDA compatible GPU (recomendado) o Apple Silicon
- Al menos 8GB de RAM libre
- Conexión a internet (para la primera descarga del modelo)

## 🛠 Instalación

### Opción 1: Con UV (Recomendado)

1. **Instalar UV** (si no lo tienes):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clonar el repositorio:**
```bash
git clone https://github.com/BernardoAguayoOrtega/coding-agent.git
cd coding-agent
```

3. **Crear entorno virtual e instalar dependencias:**
```bash
uv venv
uv pip install -r requirements.txt
```

4. **Activar el entorno virtual:**
```bash
source .venv/bin/activate  # En macOS/Linux
# o en Windows: .venv\Scripts\activate
```

### Opción 2: Con pip tradicional

1. **Clonar el repositorio:**
```bash
git clone https://github.com/BernardoAguayoOrtega/coding-agent.git
cd coding-agent
```

2. **Crear entorno virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # En macOS/Linux
# o en Windows: .venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### Verificación de la instalación

Ejecuta el script de prueba para verificar que todo funciona:
```bash
python test_setup.py
```

## 🎯 Uso

⚠️ **Importante**: Siempre activa el entorno virtual antes de usar el agente:
```bash
source .venv/bin/activate  # En macOS/Linux
```

### Modo Simple
Ejecuta una tarea específica:

```bash
python main.py "Crea un archivo hello.py que imprima 'Hola Mundo'"
```

### Modo Interactivo
Para múltiples tareas en una sesión:

```bash
python main.py --interactive
```

### Opciones Disponibles

```bash
python main.py --help
```

- `-i, --interactive`: Modo interactivo
- `-s, --steps`: Número máximo de pasos (default: 10)
- `-v, --verbose`: Modo detallado

## 🔧 Ejemplos de Uso

### Tareas de Desarrollo

```bash
# Crear un proyecto Python básico
python main.py "Crea un proyecto Python con estructura básica: main.py, requirements.txt y README.md"

# Analizar código existente
python main.py "Analiza todos los archivos .py en el directorio actual y crea un resumen"

# Ejecutar tests
python main.py "Ejecuta los tests en el directorio tests/ y reporta los resultados"

# Crear documentación
python main.py "Genera documentación para todas las funciones en main.py"
```

### Tareas de Sistema

```bash
# Operaciones de archivos
python main.py "Lista todos los archivos .py y muestra su tamaño"

# Búsqueda de código
python main.py "Encuentra todos los archivos que contengan la palabra 'TODO'"

# Limpieza de proyecto
python main.py "Elimina todos los archivos __pycache__ del proyecto"
```

## 🧠 Herramientas Disponibles

El agente tiene acceso a las siguientes herramientas:

| Herramienta | Descripción |
|-------------|-------------|
| `run_terminal_command` | Ejecuta comandos de terminal |
| `read_file` | Lee el contenido de archivos |
| `write_file` | Crea o modifica archivos |
| `list_directory` | Lista contenido de directorios |
| `create_directory` | Crea directorios |
| `find_files` | Busca archivos por patrón |
| `get_working_directory` | Obtiene directorio actual |

## ⚙️ Configuración

### Cambiar Modelo

Edita `model_loader.py` para usar un modelo diferente:

```python
MODEL_NAME = "tu-modelo/preferido"
```

### Ajustar Parámetros

En `model_loader.py` puedes modificar:

- `max_new_tokens`: Longitud máxima de respuestas
- `temperature`: Creatividad del modelo (0.0-1.0)
- `repetition_penalty`: Penalización por repetición

## 🐛 Solución de Problemas

### Error de Memoria GPU
```bash
# Usar CPU en lugar de GPU
export CUDA_VISIBLE_DEVICES=""
python main.py "tu tarea"
```

### Modelo No Se Descarga
```bash
# Verificar conexión y limpiar caché
rm -rf ~/.cache/coding-agent
python main.py --verbose "test simple"
```

### Permisos de Archivos
```bash
# Verificar permisos del directorio
ls -la
chmod +w archivo_problema
```

## 📁 Estructura del Proyecto

```
coding-agent/
├── main.py              # Punto de entrada y lógica principal
├── model_loader.py      # Carga y gestión del modelo
├── tools.py            # Herramientas disponibles para el agente
├── requirements.txt    # Dependencias de Python
├── README.md          # Este archivo
└── .venv/             # Entorno virtual (creado tras instalación)
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [DeepSeek AI](https://github.com/deepseek-ai) por el modelo DeepSeek Coder
- [Hugging Face](https://huggingface.co/) por la infraestructura de transformers
- [Accelerate](https://github.com/huggingface/accelerate) por la gestión de dispositivos

## 📞 Soporte

Si encuentras problemas o tienes preguntas:

1. Revisa la sección de [Issues](https://github.com/tu-usuario/coding-agent/issues)
2. Crea un nuevo issue con detalles del problema
3. Incluye la salida del modo verbose (`-v`) si es relevante
