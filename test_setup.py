#!/usr/bin/env python3
"""
Test script para verificar que el coding agent funciona correctamente
"""

import sys
import os
from pathlib import Path

# Añadir el directorio actual al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent))

try:
    import torch
    print("✅ PyTorch importado correctamente")
    print(f"   Versión: {torch.__version__}")
    print(f"   CUDA disponible: {torch.cuda.is_available()}")
    if hasattr(torch.backends, 'mps'):
        print(f"   MPS (Apple Silicon) disponible: {torch.backends.mps.is_available()}")
except ImportError as e:
    print(f"❌ Error importando PyTorch: {e}")
    sys.exit(1)

try:
    import transformers
    print("✅ Transformers importado correctamente")
    print(f"   Versión: {transformers.__version__}")
except ImportError as e:
    print(f"❌ Error importando Transformers: {e}")
    sys.exit(1)

try:
    import tools
    print("✅ Módulo tools importado correctamente")
    print(f"   Herramientas disponibles: {list(tools.AVAILABLE_TOOLS.keys())}")
except ImportError as e:
    print(f"❌ Error importando tools: {e}")
    sys.exit(1)

try:
    import model_loader
    print("✅ Módulo model_loader importado correctamente")
    
    # Obtener información del modelo
    info = model_loader.get_model_info()
    print(f"   Modelo configurado: {info['model_name']}")
    print(f"   Directorio de caché: {info['cache_dir']}")
    
except ImportError as e:
    print(f"❌ Error importando model_loader: {e}")
    sys.exit(1)

print("\n🧪 Probando herramientas básicas...")

# Test de herramientas
try:
    # Test get_working_directory
    result = tools.get_working_directory()
    print(f"✅ get_working_directory: {result}")
    
    # Test list_directory
    result = tools.list_directory(".")
    print(f"✅ list_directory: Listado exitoso")
    
    # Test write_file y read_file
    test_file = "test_agent.txt"
    test_content = "¡Hola desde el coding agent!"
    
    write_result = tools.write_file(test_file, test_content)
    print(f"✅ write_file: {write_result}")
    
    read_result = tools.read_file(test_file)
    print(f"✅ read_file: Archivo leído correctamente")
    
    # Limpiar archivo de test
    os.remove(test_file)
    print(f"✅ Archivo de prueba eliminado")
    
except Exception as e:
    print(f"❌ Error probando herramientas: {e}")
    sys.exit(1)

print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
print("\nEl coding agent está listo para usar. Prueba:")
print("  python main.py --help")
print("  python main.py 'Crea un archivo hello.py que imprima Hola Mundo'")
print("  python main.py --interactive")
