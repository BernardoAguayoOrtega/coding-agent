import model_loader
import tools
import re # Usaremos regex para analizar la respuesta del modelo

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
        
        # Limpieza simple de argumentos (esto es básico, se puede mejorar)
        # Asume que los argumentos son strings, los separamos por coma
        args = [arg.strip().strip("'\"") for arg in args_str.split(',')]
        
        return function_name, args
    
    return None, None

def main():
    # 1. Cargar el cerebro
    model, tokenizer = model_loader.load_model()

    # 2. Definir el objetivo
    user_goal = "Crea un nuevo archivo llamado 'hello.txt' que contenga el texto 'Hola Agente'."
    
    # 3. Historial de conversación (para que el agente recuerde)
    conversation_history = ""
    
    # 4. El bucle del agente (limitado a 5 pasos por seguridad)
    for _ in range(5):
        # 5. Construir el Prompt (¡La parte más importante!)
        prompt = f"""
        {tools.TOOL_DESCRIPTIONS}

        Eres un agente de IA autónomo. Tu objetivo es: {user_goal}

        HISTORIAL DE CONVERSACIÓN:
        {conversation_history}

        RESPONDE EN EL SIGUIENTE FORMATO:

        Thought:
        [Tu razonamiento paso a paso sobre qué hacer a continuación]

        Action:
        [La llamada a la herramienta que has decidido usar, p.ej. write_file('hello.txt', 'Hola Agente')]
        
        Agente:
        """
        
        # 6. Obtener la decisión del cerebro
        raw_response = model_loader.generate_response(model, tokenizer, prompt)
        print(f"\n===== RESPUESTA DEL MODELO =====\n{raw_response}\n============================\n")
        
        # 7. Analizar la decisión
        function_name, args = parse_action(raw_response)
        
        if function_name and function_name in tools.AVAILABLE_TOOLS:
            # 8. Ejecutar la herramienta (las manos)
            function_to_call = tools.AVAILABLE_TOOLS[function_name]
            
            try:
                # Desempaqueta los argumentos para la función
                tool_result = function_to_call(*args)
            except TypeError as e:
                tool_result = f"Error al llamar a la herramienta: {e}"
            
            # 9. Actualizar el historial
            conversation_history += f"Thought:\n... (pensamiento omitido) ...\n"
            conversation_history += f"Action:\n{function_name}({', '.join(args)})\n"
            conversation_history += f"System:\n{tool_result}\n"
            
            # (Opcional) Comprobación de finalización
            if "exitosamente" in tool_result.lower():
                print("✅ Objetivo completado.")
                break
        else:
            print("El modelo no dio una acción válida. Deteniendo.")
            break
            
    print("\n--- Simulación del Agente Finalizada ---")

if __name__ == "__main__":
    main()