#!/usr/bin/env python3
"""
Coding Agent - Un agente de IA autónomo para tareas de programación
"""

import argparse
import sys
import re
from pathlib import Path

from model_loader import load_model, generate_response
import tools


def parse_action(model_response):
    """
    Analiza la respuesta del modelo para encontrar una llamada a una herramienta.
    Busca un patrón como: Action: function_name(arg1, arg2)
    """
    # Patrón Regex para buscar: Action: nombre_funcion(argumentos)
    match = re.search(r"Action:\s*(\w+)\((.*?)\)", model_response, re.DOTALL)
    
    if match:
        function_name = match.group(1)
        args_str = match.group(2)
        
        # Limpieza simple de argumentos
        if args_str.strip():
            args = [arg.strip().strip("'\"") for arg in args_str.split(',')]
        else:
            args = []
        
        return function_name, args
    
    return None, None


def build_prompt(user_goal, conversation_history):
    """Construye el prompt para el modelo."""
    return f"""
{tools.TOOL_DESCRIPTIONS}

Eres un agente de IA autónomo especializado en tareas de programación y desarrollo. 
Tu objetivo es: {user_goal}

REGLAS IMPORTANTES:
1. Piensa paso a paso antes de actuar
2. Usa las herramientas disponibles para completar la tarea
3. Siempre verifica el resultado de tus acciones
4. Si algo falla, intenta una solución alternativa

HISTORIAL DE CONVERSACIÓN:
{conversation_history}

RESPONDE EN EL SIGUIENTE FORMATO:

Thought:
[Tu razonamiento paso a paso sobre qué hacer a continuación]

Action:
[La llamada a la herramienta que has decidido usar, p.ej. write_file('hello.txt', 'Hola Agente')]

Respuesta:
"""


def run_agent(user_goal, max_steps=10, verbose=False):
    """Ejecuta el agente para completar una tarea."""
    print(f"🤖 Iniciando agente de codificación...")
    print(f"📋 Objetivo: {user_goal}")
    print("-" * 50)
    
    # Cargar el modelo
    model, tokenizer = load_model()
    
    # Historial de conversación
    conversation_history = ""
    
    # Bucle principal del agente
    for step in range(1, max_steps + 1):
        print(f"\n🔄 Paso {step}/{max_steps}")
        
        # Construir el prompt
        prompt = build_prompt(user_goal, conversation_history)
        
        # Obtener respuesta del modelo
        if verbose:
            print("\n--- Prompt enviado al modelo ---")
            print(prompt[-500:] + "..." if len(prompt) > 500 else prompt)
            print("--- Fin del prompt ---\n")
        
        raw_response = generate_response(model, tokenizer, prompt)
        print(f"\n💭 Respuesta del modelo:")
        print(raw_response)
        
        # Analizar la acción
        function_name, args = parse_action(raw_response)
        
        if function_name and function_name in tools.AVAILABLE_TOOLS:
            print(f"\n🔧 Ejecutando: {function_name}({', '.join(args)})")
            
            # Ejecutar la herramienta
            function_to_call = tools.AVAILABLE_TOOLS[function_name]
            
            try:
                tool_result = function_to_call(*args)
                print(f"📤 Resultado: {tool_result}")
                
                # Actualizar historial
                conversation_history += f"\nPaso {step}:\n"
                conversation_history += f"Thought: {raw_response.split('Action:')[0].replace('Thought:', '').strip()}\n"
                conversation_history += f"Action: {function_name}({', '.join(args)})\n"
                conversation_history += f"Result: {tool_result}\n"
                
                # Verificar si la tarea se completó
                if any(keyword in tool_result.lower() for keyword in ['exitosamente', 'éxito', 'completado', 'creado']):
                    print("\n✅ ¡Tarea completada exitosamente!")
                    return True
                    
            except Exception as e:
                error_msg = f"Error al ejecutar la herramienta: {e}"
                print(f"❌ {error_msg}")
                conversation_history += f"\nPaso {step}:\n"
                conversation_history += f"Action: {function_name}({', '.join(args)})\n"
                conversation_history += f"Error: {error_msg}\n"
        else:
            print("❌ El modelo no proporcionó una acción válida.")
            break
    
    print(f"\n⚠️ Agente detenido después de {max_steps} pasos.")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Coding Agent - Agente de IA para tareas de programación",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py "Crea un archivo hello.py que imprima 'Hola Mundo'"
  python main.py "Lista todos los archivos .py en el directorio actual"
  python main.py --interactive
        """
    )
    
    parser.add_argument(
        "goal",
        nargs="?",
        help="Objetivo o tarea que el agente debe completar"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Modo interactivo - permite introducir múltiples tareas"
    )
    
    parser.add_argument(
        "-s", "--steps",
        type=int,
        default=10,
        help="Número máximo de pasos (default: 10)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verbose - muestra más detalles del proceso"
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        print("🔄 Modo interactivo activado. Escribe 'quit' para salir.")
        while True:
            try:
                goal = input("\n📝 Ingresa tu objetivo: ").strip()
                if goal.lower() in ['quit', 'exit', 'salir']:
                    print("👋 ¡Hasta luego!")
                    break
                if goal:
                    run_agent(goal, args.steps, args.verbose)
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
    elif args.goal:
        run_agent(args.goal, args.steps, args.verbose)
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())