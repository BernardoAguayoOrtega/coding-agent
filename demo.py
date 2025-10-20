#!/usr/bin/env python3
"""
Ejemplo simple del coding agent sin cargar el modelo completo
Útil para probar la lógica sin el overhead del modelo
"""

import sys
from pathlib import Path
import tools

def mock_model_response(prompt):
    """
    Simula respuestas del modelo para testing rápido
    En un caso real, esto vendría del modelo de IA
    """
    
    # Buscar palabras clave en el prompt para simular respuestas
    prompt_lower = prompt.lower()
    
    if "crea" in prompt_lower and "archivo" in prompt_lower and "hello" in prompt_lower:
        return """
        Thought:
        El usuario quiere que cree un archivo llamado hello.py. Voy a usar la herramienta write_file para crear este archivo con un contenido simple que imprima "Hola Mundo".
        
        Action:
        write_file('hello.py', 'print("Hola Mundo")')
        """
    
    elif "lista" in prompt_lower and ("archivos" in prompt_lower or "directorio" in prompt_lower):
        return """
        Thought:
        El usuario quiere ver el contenido del directorio actual. Usaré list_directory para mostrar todos los archivos y carpetas.
        
        Action:
        list_directory('.')
        """
    
    elif "lee" in prompt_lower or "muestra" in prompt_lower:
        return """
        Thought:
        El usuario quiere leer un archivo. Usaré read_file para mostrar su contenido.
        
        Action:
        read_file('hello.py')
        """
    
    else:
        return """
        Thought:
        No estoy seguro de qué hacer con esta solicitud. Voy a listar el directorio actual para entender mejor el contexto.
        
        Action:
        list_directory('.')
        """

def parse_action(response):
    """Parsea la respuesta para extraer la acción"""
    import re
    
    match = re.search(r"Action:\s*(\w+)\((.*?)\)", response, re.DOTALL)
    
    if match:
        function_name = match.group(1)
        args_str = match.group(2)
        
        if args_str.strip():
            # Manejo simple de argumentos
            args = [arg.strip().strip("'\"") for arg in args_str.split(',')]
        else:
            args = []
        
        return function_name, args
    
    return None, None

def run_demo_agent(goal):
    """Ejecuta una demostración del agente sin modelo real"""
    
    print(f"🤖 Demo del Coding Agent")
    print(f"📋 Objetivo: {goal}")
    print("-" * 50)
    
    # Simular el prompt que se enviaría al modelo
    prompt = f"""
    {tools.TOOL_DESCRIPTIONS}
    
    Eres un agente de IA. Tu objetivo es: {goal}
    
    Responde con tu razonamiento y la acción a tomar.
    """
    
    print("💭 Generando respuesta...")
    
    # Obtener respuesta simulada
    response = mock_model_response(prompt)
    print(f"Respuesta del modelo:\n{response}")
    
    # Parsear la acción
    function_name, args = parse_action(response)
    
    if function_name and function_name in tools.AVAILABLE_TOOLS:
        print(f"\n🔧 Ejecutando: {function_name}({', '.join(args)})")
        
        # Ejecutar la herramienta
        function_to_call = tools.AVAILABLE_TOOLS[function_name]
        
        try:
            result = function_to_call(*args)
            print(f"📤 Resultado:\n{result}")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("❌ No se pudo parsear una acción válida")
        return False

def main():
    """Función principal del demo"""
    
    if len(sys.argv) > 1:
        goal = " ".join(sys.argv[1:])
    else:
        goal = "Crea un archivo hello.py que imprima 'Hola Mundo'"
    
    print("🧪 MODO DEMO - Sin modelo real de IA")
    print("Este demo simula el comportamiento del agente para testing rápido\n")
    
    success = run_demo_agent(goal)
    
    if success:
        print("\n✅ Demo completado exitosamente!")
    else:
        print("\n❌ Demo falló")
    
    print("\nPara usar el agente completo con IA real:")
    print("  python main.py 'tu objetivo aquí'")

if __name__ == "__main__":
    main()
