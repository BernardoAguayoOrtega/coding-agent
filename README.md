# Coding Agent 🤖 | Agente de Codificación 🤖

[🇪🇸 Español](#español) | [🇺🇸 English](#english)

---

## English

An autonomous AI agent specialized in programming and development tasks, built with advanced reflection techniques and human-in-the-loop capabilities.

### 🚀 Features

- **Autonomous Agent**: Can plan and execute programming tasks independently
- **Multiple AI Models**: Support for powerful models from Hugging Face (DeepSeek, CodeLlama, etc.)
- **Code Reflection System**: Automatic code quality evaluation with 6 reflection techniques:
  - **Linter**: Syntax and style checking
  - **Best Practices**: Programming best practices validation
  - **Simplicity**: KISS principle evaluation
  - **SOLID**: SOLID principles verification
  - **DRY**: Don't Repeat Yourself principle checking
  - **TDD**: Test-driven development coverage analysis
- **Human-in-the-Loop**: Interactive approval and feedback system
- **Terminal Interface**: Easy to use from command line
- **Interactive Mode**: Multiple tasks in one session
- **Bilingual**: English and Spanish support

### 📋 Requirements

- Python 3.8+
- CUDA compatible GPU (recommended) or Apple Silicon
- At least 8GB of RAM available
- Internet connection (for first model download)

### � Installation

#### Option 1: With UV (Recommended)

1. **Install UV** (if you don't have it):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone the repository:**
```bash
git clone https://github.com/BernardoAguayoOrtega/coding-agent.git
cd coding-agent
```

3. **Create virtual environment and install dependencies:**
```bash
uv venv
uv pip install -r requirements.txt
```

4. **Activate virtual environment:**
```bash
source .venv/bin/activate  # On macOS/Linux
# or on Windows: .venv\Scripts\activate
```

#### Option 2: With traditional pip

1. **Clone the repository:**
```bash
git clone https://github.com/BernardoAguayoOrtega/coding-agent.git
cd coding-agent
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or on Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

#### Installation verification

Run the test script to verify everything works:
```bash
python test_setup.py
```

### 🎯 Usage

⚠️ **Important**: Always activate the virtual environment before using the agent.

#### Option 1: Execution script (Recommended)

The `run_agent.sh` script automatically handles virtual environment activation:

```bash
# Execute a specific task
./run_agent.sh "Create a hello.py file that prints 'Hello World'"

# Interactive mode
./run_agent.sh --interactive

# Run tests
./run_agent.sh --test

# Quick demo (without real model)
./run_agent.sh --demo "your goal here"

# Show help
./run_agent.sh --help
```

#### Option 2: Manual execution

```bash
# Activate virtual environment
source .venv/bin/activate

# Execute a specific task
python main.py "Create a hello.py file that prints 'Hello World'"

# Interactive mode
python main.py --interactive

# List available models
python main.py --list-models

# Select a model
python main.py --select-model codellama-13b

# English interface
python main.py --language en "Create a Python project"
```

#### Available Options

```bash
python main.py --help
```

- `-i, --interactive`: Interactive mode
- `-s, --steps`: Maximum number of steps (default: 10)
- `-v, --verbose`: Verbose mode
- `-m, --model`: Model to use
- `--list-models`: List available models
- `--select-model`: Select default model
- `--no-reflection`: Disable code reflection
- `--no-human-loop`: Disable human-in-the-loop
- `--language`: Interface language (en/es)

### 🔧 Example Tasks

#### Development Tasks

```bash
# Create a Python project with basic structure
python main.py "Create a Python project with basic structure: main.py, requirements.txt and README.md"

# Analyze existing code
python main.py "Analyze all .py files in current directory and create a summary"

# Run tests
python main.py "Run tests in tests/ directory and report results"

# Generate documentation
python main.py "Generate documentation for all functions in main.py"
```

#### System Tasks

```bash
# File operations
python main.py "List all .py files and show their size"

# Code search
python main.py "Find all files containing the word 'TODO'"

# Project cleanup
python main.py "Remove all __pycache__ files from the project"
```

### 🧠 Available Models

| Model | Size | Memory | Description |
|-------|------|---------|-------------|
| `deepseek-6.7b` | 6.7B | ~14GB | Fast and efficient for most coding tasks |
| `deepseek-33b` | 33B | ~66GB | More powerful reasoning and complex code generation |
| `codellama-13b` | 13B | ~26GB | Meta's specialized coding model |
| `codellama-34b` | 34B | ~68GB | Largest CodeLlama model, superior understanding |
| `phind-34b` | 34B | ~68GB | Fine-tuned for problem solving and debugging |
| `wizardcoder-15b` | 15B | ~30GB | Specialized in following instructions precisely |

### 🔍 Reflection System

The agent automatically evaluates code quality using 6 reflection techniques:

1. **Linter**: Syntax errors, style issues, long lines
2. **Best Practices**: Docstrings, naming conventions, code structure
3. **Simplicity**: Cyclomatic complexity, nesting depth, parameter count
4. **SOLID**: Single responsibility, dependency management
5. **DRY**: Code duplication detection and analysis
6. **TDD**: Test coverage and testing framework usage

### 🤝 Human-in-the-Loop

The system requests human approval for:
- Critical file operations
- Code with quality issues
- Error resolution
- Important decisions

### 📁 Project Structure

```
coding-agent/
├── main.py              # Main entry point and agent logic
├── model_loader.py      # AI model management and loading
├── tools.py            # Available tools for the agent
├── reflection.py       # Code quality reflection system
├── human_loop.py       # Human-in-the-loop system
├── requirements.txt    # Python dependencies
├── run_agent.sh        # Execution script with virtual environment
├── demo.py             # Quick demo without real model
├── test_setup.py       # Setup verification script
├── README.md          # This file
└── .venv/             # Virtual environment (created after installation)
```

---

## Español

Un agente de IA autónomo especializado en tareas de programación y desarrollo, construido con técnicas avanzadas de reflexión y capacidades de human-in-the-loop.

### 🚀 Características

- **Agente Autónomo**: Puede planificar y ejecutar tareas de programación de manera independiente
- **Múltiples Modelos de IA**: Soporte para modelos potentes de Hugging Face (DeepSeek, CodeLlama, etc.)
- **Sistema de Reflexión de Código**: Evaluación automática de calidad con 6 técnicas de reflexión:
  - **Linter**: Verificación de sintaxis y estilo
  - **Mejores Prácticas**: Validación de mejores prácticas de programación
  - **Simplicidad**: Evaluación del principio KISS
  - **SOLID**: Verificación de principios SOLID
  - **DRY**: Verificación del principio "No te repitas"
  - **TDD**: Análisis de cobertura de desarrollo guiado por tests
- **Human-in-the-Loop**: Sistema interactivo de aprobación y retroalimentación
- **Interfaz de Terminal**: Fácil de usar desde línea de comandos
- **Modo Interactivo**: Múltiples tareas en una sesión
- **Bilingüe**: Soporte para inglés y español

### 📋 Requisitos

- Python 3.8+
- GPU compatible con CUDA (recomendado) o Apple Silicon
- Al menos 8GB de RAM libre
- Conexión a internet (para la primera descarga del modelo)

### 🛠 Instalación

#### Opción 1: Con UV (Recomendado)

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

#### Opción 2: Con pip tradicional

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

#### Verificación de la instalación

Ejecuta el script de prueba para verificar que todo funciona:
```bash
python test_setup.py
```

### 🎯 Uso

⚠️ **Importante**: Siempre activa el entorno virtual antes de usar el agente.

#### Opción 1: Script de ejecución (Recomendado)

El script `run_agent.sh` maneja automáticamente la activación del entorno virtual:

```bash
# Ejecutar una tarea específica
./run_agent.sh "Crea un archivo hello.py que imprima 'Hola Mundo'"

# Modo interactivo
./run_agent.sh --interactive

# Ejecutar tests
./run_agent.sh --test

# Demo rápido (sin modelo real)
./run_agent.sh --demo "tu objetivo aquí"

# Mostrar ayuda
./run_agent.sh --help
```

#### Opción 2: Ejecución manual

```bash
# Activar entorno virtual
source .venv/bin/activate

# Ejecutar una tarea específica
python main.py "Crea un archivo hello.py que imprima 'Hola Mundo'"

# Modo interactivo
python main.py --interactive

# Listar modelos disponibles
python main.py --list-models

# Seleccionar un modelo
python main.py --select-model codellama-13b

# Interfaz en inglés
python main.py --language en "Create a Python project"
```

#### Opciones Disponibles

```bash
python main.py --help
```

- `-i, --interactive`: Modo interactivo
- `-s, --steps`: Número máximo de pasos (default: 10)
- `-v, --verbose`: Modo detallado
- `-m, --model`: Modelo a usar
- `--list-models`: Listar modelos disponibles
- `--select-model`: Seleccionar modelo por defecto
- `--no-reflection`: Desactivar reflexión de código
- `--no-human-loop`: Desactivar human-in-the-loop
- `--language`: Idioma de interfaz (en/es)

### 🔧 Ejemplos de Tareas

#### Tareas de Desarrollo

```bash
# Crear un proyecto Python con estructura básica
python main.py "Crea un proyecto Python con estructura básica: main.py, requirements.txt y README.md"

# Analizar código existente
python main.py "Analiza todos los archivos .py en el directorio actual y crea un resumen"

# Ejecutar tests
python main.py "Ejecuta los tests en el directorio tests/ y reporta los resultados"

# Generar documentación
python main.py "Genera documentación para todas las funciones en main.py"
```

#### Tareas de Sistema

```bash
# Operaciones de archivos
python main.py "Lista todos los archivos .py y muestra su tamaño"

# Búsqueda de código
python main.py "Encuentra todos los archivos que contengan la palabra 'TODO'"

# Limpieza de proyecto
python main.py "Elimina todos los archivos __pycache__ del proyecto"
```

### 🧠 Modelos Disponibles

| Modelo | Tamaño | Memoria | Descripción |
|--------|--------|---------|-------------|
| `deepseek-6.7b` | 6.7B | ~14GB | Rápido y eficiente para la mayoría de tareas |
| `deepseek-33b` | 33B | ~66GB | Razonamiento más potente y generación compleja |
| `codellama-13b` | 13B | ~26GB | Modelo especializado de Meta para código |
| `codellama-34b` | 34B | ~68GB | Modelo CodeLlama más grande, comprensión superior |
| `phind-34b` | 34B | ~68GB | Afinado para resolución de problemas y debugging |
| `wizardcoder-15b` | 15B | ~30GB | Especializado en seguir instrucciones precisamente |

### 🔍 Sistema de Reflexión

El agente evalúa automáticamente la calidad del código usando 6 técnicas de reflexión:

1. **Linter**: Errores de sintaxis, problemas de estilo, líneas largas
2. **Mejores Prácticas**: Docstrings, convenciones de nombres, estructura
3. **Simplicidad**: Complejidad ciclomática, profundidad de anidamiento
4. **SOLID**: Responsabilidad única, gestión de dependencias
5. **DRY**: Detección y análisis de duplicación de código
6. **TDD**: Cobertura de tests y uso de frameworks de testing

### 🤝 Human-in-the-Loop

El sistema solicita aprobación humana para:
- Operaciones críticas de archivos
- Código con problemas de calidad
- Resolución de errores
- Decisiones importantes

### 📁 Estructura del Proyecto

```
coding-agent/
├── main.py              # Punto de entrada y lógica principal
├── model_loader.py      # Gestión y carga del modelo de IA
├── tools.py            # Herramientas disponibles para el agente
├── reflection.py       # Sistema de reflexión de calidad de código
├── human_loop.py       # Sistema de human-in-the-loop
├── requirements.txt    # Dependencias de Python
├── run_agent.sh        # Script de ejecución con entorno virtual
├── demo.py             # Demo rápido sin modelo real
├── test_setup.py       # Script de verificación del setup
├── README.md          # Este archivo
└── .venv/             # Entorno virtual (creado tras instalación)
```

### 🐛 Solución de Problemas / Troubleshooting

#### Error de Memoria GPU / GPU Memory Error
```bash
# Usar CPU en lugar de GPU / Use CPU instead of GPU
export CUDA_VISIBLE_DEVICES=""
python main.py "tu tarea / your task"
```

#### Modelo No Se Descarga / Model Won't Download
```bash
# Verificar conexión y limpiar caché / Check connection and clear cache
rm -rf ~/.cache/coding-agent
python main.py --verbose "test simple"
```

### 🤝 Contribuir / Contributing

1. Fork el proyecto / Fork the project
2. Crea una rama para tu feature / Create a feature branch (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios / Commit your changes (`git commit -am 'Añade nueva característica'`)
4. Push a la rama / Push to the branch (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request / Create a Pull Request

### 📝 Licencia / License

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.
This project is under the MIT License. See `LICENSE` for more details.

### 🙏 Agradecimientos / Acknowledgments

- [DeepSeek AI](https://github.com/deepseek-ai) por el modelo DeepSeek Coder / for the DeepSeek Coder model
- [Hugging Face](https://huggingface.co/) por la infraestructura de transformers / for the transformers infrastructure  
- [Accelerate](https://github.com/huggingface/accelerate) por la gestión de dispositivos / for device management
