#!/usr/bin/env python3
"""
Coding Agent - Un agente de IA autónomo para tareas de programación
Enhanced with reflection techniques and human-in-the-loop capabilities
"""

import argparse
import sys
import re
import json
from pathlib import Path

from model_loader import load_model, generate_response, load_model_config, list_available_models, select_model
import tools

# Import reflection and human loop systems
try:
    from reflection import CodeReflector, format_reflection_results, ReflectionType
    from human_loop import HumanInTheLoop, create_human_loop
    ADVANCED_FEATURES = True
except ImportError:
    ADVANCED_FEATURES = False
    print("⚠️ Advanced features (reflection/human-loop) not available")


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


def build_prompt(user_goal, conversation_history, reflection_enabled=True, language="es"):
    """Construye el prompt para el modelo."""
    
    if language == "es":
        system_msg = """
Eres un agente de IA autónomo especializado en tareas de programación y desarrollo de alta calidad.

REGLAS FUNDAMENTALES:
1. SIEMPRE piensa paso a paso antes de actuar
2. Usa las herramientas disponibles para completar la tarea
3. SIEMPRE verifica el resultado de tus acciones
4. Si algo falla, intenta una solución alternativa
5. MANTÉN la calidad del código como prioridad máxima
"""
        
        if reflection_enabled and ADVANCED_FEATURES:
            system_msg += """
6. USA las herramientas de reflexión para evaluar la calidad del código:
   - analyze_code_quality() para análisis completo
   - lint_code() para verificar errores de sintaxis y estilo
   - check_best_practices() para mejores prácticas
   - check_solid_principles() para principios SOLID
   - check_dry_principle() para principio DRY
   - run_tests() para verificar que los tests pasen
7. NUNCA entregues código sin haberlo verificado con las herramientas de calidad
8. Si el análisis de calidad encuentra problemas, CORRÍGELOS antes de continuar
"""
        
        goal_section = f"\nTu objetivo es: {user_goal}"
        
    else:  # English
        system_msg = """
You are an autonomous AI agent specialized in high-quality programming and development tasks.

FUNDAMENTAL RULES:
1. ALWAYS think step by step before acting
2. Use available tools to complete the task
3. ALWAYS verify the results of your actions
4. If something fails, try an alternative solution
5. MAINTAIN code quality as the maximum priority
"""
        
        if reflection_enabled and ADVANCED_FEATURES:
            system_msg += """
6. USE reflection tools to evaluate code quality:
   - analyze_code_quality() for complete analysis
   - lint_code() to check syntax and style errors
   - check_best_practices() for best practices
   - check_solid_principles() for SOLID principles
   - check_dry_principle() for DRY principle
   - run_tests() to verify tests pass
7. NEVER deliver code without verifying it with quality tools
8. If quality analysis finds issues, FIX them before continuing
"""
        
        goal_section = f"\nYour objective is: {user_goal}"
    
    return f"""
{tools.TOOL_DESCRIPTIONS}

{system_msg}
{goal_section}

HISTORIAL DE CONVERSACIÓN:
{conversation_history}

RESPONDE EN EL SIGUIENTE FORMATO:

Thought:
[Tu razonamiento paso a paso sobre qué hacer a continuación]

Action:
[La llamada a la herramienta que has decidido usar, p.ej. write_file('hello.txt', 'Hola Agente')]

Respuesta:
"""


def run_agent(user_goal, max_steps=10, verbose=False, model_key=None, enable_reflection=True, enable_human_loop=True, language="es"):
    """Ejecuta el agente para completar una tarea."""
    print(f"🤖 Iniciando agente de codificación avanzado...")
    print(f"📋 Objetivo: {user_goal}")
    
    # Configuración
    config = load_model_config()
    if enable_reflection and ADVANCED_FEATURES:
        print("🔍 Reflexión de código: ACTIVADA")
    if enable_human_loop and ADVANCED_FEATURES:
        print("🤝 Human-in-the-loop: ACTIVADO")
    
    print("-" * 50)
    
    # Crear sistema human-in-the-loop
    human_loop = None
    if enable_human_loop and ADVANCED_FEATURES:
        human_loop = create_human_loop(language=language, auto_approve=False)
    
    # Cargar el modelo
    model, tokenizer = load_model(model_key)
    
    # Historial de conversación
    conversation_history = ""
    
    # Bucle principal del agente
    for step in range(1, max_steps + 1):
        print(f"\n🔄 Paso {step}/{max_steps}")
        
        # Construir el prompt
        prompt = build_prompt(user_goal, conversation_history, enable_reflection, language)
        
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
            print(f"\n🔧 Acción propuesta: {function_name}({', '.join(args)})")
            
            # Human-in-the-loop: solicitar aprobación para acciones importantes
            if human_loop and function_name in ['write_file', 'run_terminal_command', 'create_directory']:
                approval = human_loop.request_approval(
                    title=f"Aprobar acción: {function_name}",
                    description=f"El agente quiere ejecutar: {function_name}({', '.join(args)})\n\nRazonamiento: {raw_response.split('Action:')[0].replace('Thought:', '').strip()}",
                    context={"step": step, "function": function_name, "args": args}
                )
                
                if not approval.approved:
                    print("❌ Acción rechazada por el usuario")
                    if approval.feedback:
                        print(f"💭 Feedback: {approval.feedback}")
                        conversation_history += f"\nPaso {step} - Acción rechazada:\n"
                        conversation_history += f"Acción propuesta: {function_name}({', '.join(args)})\n"
                        conversation_history += f"Feedback del usuario: {approval.feedback}\n"
                        conversation_history += "El usuario rechazó la acción. Considera el feedback e intenta un enfoque diferente.\n"
                        continue
                    else:
                        break
            
            # Ejecutar la herramienta
            function_to_call = tools.AVAILABLE_TOOLS[function_name]
            
            try:
                tool_result = function_to_call(*args)
                print(f"📤 Resultado: {tool_result}")
                
                # Reflexión automática en archivos de código creados/modificados
                if (enable_reflection and ADVANCED_FEATURES and 
                    function_name == 'write_file' and 
                    len(args) >= 1 and 
                    args[0].endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c'))):
                    
                    print(f"\n🔍 Ejecutando reflexión automática en {args[0]}...")
                    reflection_result = tools.analyze_code_quality(args[0], "all")
                    print(reflection_result)
                    
                    # Si hay problemas críticos, solicitar revisión humana
                    if human_loop and ("❌ FALLÓ" in reflection_result or "Error" in reflection_result):
                        review = human_loop.request_reflection_review(
                            reflection_results=[],  # Simplificado para esta demo
                            proposed_action=f"Continuar con el archivo {args[0]} que tiene problemas de calidad",
                            context={"reflection_output": reflection_result}
                        )
                        
                        if review.selected_option == "modificar":
                            print("🔧 Usuario solicitó modificaciones al código")
                            conversation_history += f"\nReflexión de calidad encontró problemas en {args[0]}:\n{reflection_result}\n"
                            conversation_history += "El usuario solicitó modificaciones. Corrige los problemas identificados.\n"
                            continue
                        elif review.selected_option == "abortar":
                            print("🛑 Usuario solicitó abortar")
                            break
                
                # Actualizar historial
                conversation_history += f"\nPaso {step}:\n"
                conversation_history += f"Thought: {raw_response.split('Action:')[0].replace('Thought:', '').strip()}\n"
                conversation_history += f"Action: {function_name}({', '.join(args)})\n"
                conversation_history += f"Result: {tool_result}\n"
                
                # Verificar si la tarea se completó
                if any(keyword in tool_result.lower() for keyword in ['exitosamente', 'éxito', 'completado', 'creado']):
                    print("\n✅ ¡Tarea completada exitosamente!")
                    
                    # Reflexión final si se crearon archivos
                    if enable_reflection and ADVANCED_FEATURES:
                        print("\n🔍 Ejecutando reflexión final...")
                        # Buscar archivos Python creados
                        py_files = []
                        for line in conversation_history.split('\n'):
                            if 'write_file(' in line and '.py' in line:
                                # Extraer nombre del archivo
                                match = re.search(r"write_file\('([^']+\.py)'", line)
                                if match:
                                    py_files.append(match.group(1))
                        
                        for py_file in py_files:
                            if Path(py_file).exists():
                                print(f"\n📊 Análisis final de {py_file}:")
                                final_analysis = tools.analyze_code_quality(py_file, "all")
                                print(final_analysis)
                    
                    return True
                    
            except Exception as e:
                error_msg = f"Error al ejecutar la herramienta: {e}"
                print(f"❌ {error_msg}")
                
                # Human-in-the-loop para resolución de errores
                if human_loop:
                    resolution = human_loop.request_error_resolution(
                        error=str(e),
                        attempted_action=f"{function_name}({', '.join(args)})",
                        context={"step": step}
                    )
                    
                    if resolution.selected_option == "abortar":
                        print("🛑 Usuario decidió abortar debido al error")
                        break
                    elif resolution.selected_option == "modificar":
                        conversation_history += f"\nError en paso {step}: {error_msg}\n"
                        conversation_history += "El usuario solicitó modificar el enfoque debido al error.\n"
                        continue
                
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
        description="Coding Agent - Agente de IA avanzado para tareas de programación",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py "Crea un archivo hello.py que imprima 'Hola Mundo'"
  python main.py "Lista todos los archivos .py en el directorio actual"
  python main.py --interactive --model codellama-13b
  python main.py --list-models
  python main.py --select-model deepseek-33b
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
    
    parser.add_argument(
        "-m", "--model",
        type=str,
        help="Modelo a usar (ej: deepseek-6.7b, codellama-13b, deepseek-33b)"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="Lista todos los modelos disponibles"
    )
    
    parser.add_argument(
        "--select-model",
        type=str,
        help="Selecciona y configura un modelo por defecto"
    )
    
    parser.add_argument(
        "--no-reflection",
        action="store_true",
        help="Desactiva el sistema de reflexión de código"
    )
    
    parser.add_argument(
        "--no-human-loop",
        action="store_true",
        help="Desactiva human-in-the-loop (modo automático)"
    )
    
    parser.add_argument(
        "--language",
        choices=["es", "en"],
        default="es",
        help="Idioma de la interfaz (es/en)"
    )
    
    args = parser.parse_args()
    
    # Manejar comandos especiales
    if args.list_models:
        models = list_available_models()
        print("\n🧠 MODELOS DISPONIBLES:")
        print("=" * 50)
        
        for key, info in models.items():
            status = "✅ Recomendado" if info.get("recommended") else ""
            if info.get("fits_in_memory"):
                memory_status = "💚 Compatible con tu memoria"
            else:
                memory_status = f"⚠️ Requiere {info['memory_gb']}GB (puede ser lento)"
            
            print(f"\n🔹 {key}")
            print(f"   Nombre: {info['name']}")
            print(f"   Tamaño: {info['size']}")
            print(f"   Memoria: {info['memory_gb']}GB - {memory_status}")
            print(f"   Descripción: {info['description_es' if args.language == 'es' else 'description']}")
            if status:
                print(f"   {status}")
        
        print(f"\n💡 Usa --select-model <modelo> para cambiar el modelo por defecto")
        return 0
    
    if args.select_model:
        if select_model(args.select_model):
            print(f"✅ Modelo {args.select_model} seleccionado como predeterminado")
        else:
            print(f"❌ Modelo {args.select_model} no válido. Usa --list-models para ver opciones")
            return 1
        return 0
    
    # Configuración de características
    enable_reflection = not args.no_reflection and ADVANCED_FEATURES
    enable_human_loop = not args.no_human_loop and ADVANCED_FEATURES
    
    if not ADVANCED_FEATURES:
        print("⚠️ Características avanzadas no disponibles. Instalando dependencias...")
        print("   Las funciones de reflexión y human-in-the-loop estarán limitadas.")
    
    # Modo interactivo
    if args.interactive:
        if args.language == "es":
            print("🔄 Modo interactivo activado. Escribe 'quit' para salir.")
            print("🔧 Comandos especiales:")
            print("   'config' - Cambiar configuración")
            print("   'models' - Ver modelos disponibles") 
            print("   'reflection on/off' - Activar/desactivar reflexión")
            print("   'human-loop on/off' - Activar/desactivar human-in-the-loop")
        else:
            print("🔄 Interactive mode activated. Type 'quit' to exit.")
            print("🔧 Special commands:")
            print("   'config' - Change configuration")
            print("   'models' - View available models")
            print("   'reflection on/off' - Enable/disable reflection")
            print("   'human-loop on/off' - Enable/disable human-in-the-loop")
        
        while True:
            try:
                prompt_text = "\n📝 Ingresa tu objetivo: " if args.language == "es" else "\n📝 Enter your goal: "
                goal = input(prompt_text).strip()
                
                if goal.lower() in ['quit', 'exit', 'salir']:
                    print("👋 ¡Hasta luego!" if args.language == "es" else "👋 Goodbye!")
                    break
                elif goal.lower() == 'config':
                    print(f"🔧 Reflexión: {'ON' if enable_reflection else 'OFF'}")
                    print(f"🤝 Human-in-loop: {'ON' if enable_human_loop else 'OFF'}")
                    print(f"🌐 Idioma: {args.language}")
                    continue
                elif goal.lower() == 'models':
                    models = list_available_models()
                    for key, info in models.items():
                        status = " (actual)" if info.get("recommended") else ""
                        print(f"   {key}: {info['size']}{status}")
                    continue
                elif goal.startswith('reflection '):
                    action = goal.split(' ')[1].lower()
                    if action == 'on':
                        enable_reflection = True and ADVANCED_FEATURES
                        print("✅ Reflexión activada")
                    elif action == 'off':
                        enable_reflection = False
                        print("❌ Reflexión desactivada")
                    continue
                elif goal.startswith('human-loop '):
                    action = goal.split(' ')[1].lower()
                    if action == 'on':
                        enable_human_loop = True and ADVANCED_FEATURES
                        print("✅ Human-in-the-loop activado")
                    elif action == 'off':
                        enable_human_loop = False
                        print("❌ Human-in-the-loop desactivado")
                    continue
                
                if goal:
                    run_agent(
                        goal, 
                        args.steps, 
                        args.verbose, 
                        args.model,
                        enable_reflection,
                        enable_human_loop,
                        args.language
                    )
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!" if args.language == "es" else "\n👋 Goodbye!")
                break
                
    elif args.goal:
        run_agent(
            args.goal, 
            args.steps, 
            args.verbose, 
            args.model,
            enable_reflection,
            enable_human_loop,
            args.language
        )
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())