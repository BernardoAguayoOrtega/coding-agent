#!/bin/bash
# Coding Agent Runner - Ejecuta el agente con el entorno virtual activado

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo "🤖 Coding Agent Runner"
    echo
    echo "Uso:"
    echo "  ./run_agent.sh \"tu objetivo aquí\""
    echo "  ./run_agent.sh --interactive"
    echo "  ./run_agent.sh --demo \"objetivo para demo\""
    echo "  ./run_agent.sh --test"
    echo "  ./run_agent.sh --help"
    echo
    echo "Ejemplos:"
    echo "  ./run_agent.sh \"Crea un archivo hello.py que imprima 'Hola Mundo'\""
    echo "  ./run_agent.sh --interactive"
    echo "  ./run_agent.sh --demo \"Lista todos los archivos Python\""
    echo
}

# Verificar que estamos en el directorio correcto
if [[ ! -f "main.py" ]]; then
    echo -e "${RED}❌ Error: Ejecuta este script desde el directorio raíz del proyecto${NC}"
    exit 1
fi

# Verificar que existe el entorno virtual
if [[ ! -d ".venv" ]]; then
    echo -e "${RED}❌ Error: No se encontró el entorno virtual .venv${NC}"
    echo "Ejecuta primero: uv venv && uv pip install -r requirements.txt"
    exit 1
fi

# Activar entorno virtual
echo -e "${YELLOW}🔧 Activando entorno virtual...${NC}"
source .venv/bin/activate

# Verificar activación
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${RED}❌ Error: No se pudo activar el entorno virtual${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Entorno virtual activado: $VIRTUAL_ENV${NC}"

# Manejar argumentos
case "$1" in
    "--help" | "-h")
        show_help
        exit 0
        ;;
    "--test")
        echo -e "${YELLOW}🧪 Ejecutando tests...${NC}"
        python test_setup.py
        exit $?
        ;;
    "--demo")
        if [[ -z "$2" ]]; then
            echo -e "${YELLOW}🎮 Ejecutando demo con objetivo por defecto...${NC}"
            python demo.py
        else
            echo -e "${YELLOW}🎮 Ejecutando demo: $2${NC}"
            python demo.py "$2"
        fi
        exit $?
        ;;
    "--interactive" | "-i")
        echo -e "${GREEN}🔄 Iniciando modo interactivo...${NC}"
        python main.py --interactive
        exit $?
        ;;
    "")
        echo -e "${YELLOW}ℹ️ No se especificó objetivo. Mostrando ayuda:${NC}"
        python main.py --help
        echo
        show_help
        exit 0
        ;;
    *)
        echo -e "${GREEN}🚀 Ejecutando agente con objetivo: $*${NC}"
        python main.py "$*"
        exit $?
        ;;
esac
