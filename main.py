from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Elige tu modelo de codificación
MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-instruct"

def load_model():
    """
    Carga el modelo y el tokenizador desde Hugging Face.
    Usa 'accelerate' para la carga automática de dispositivos (GPU/CPU).
    """
    print(f"Cargando modelo: {MODEL_NAME}...")
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16,  # Usa media precisión para ahorrar memoria
        device_map="auto",          # 'accelerate' distribuye el modelo en GPU/CPU
    )
    
    print("✅ Modelo y tokenizador cargados.")
    return model, tokenizer

def generate_response(model, tokenizer, prompt):
    """
    Genera una respuesta del modelo basada en un prompt.
    """
    # Envía el prompt al mismo dispositivo que el modelo
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    # Genera la salida
    outputs = model.generate(
        **inputs, 
        max_new_tokens=200,  # Limita el tamaño de la respuesta
        pad_token_id=tokenizer.eos_token_id # Evita warnings
    )
    
    # Decodifica solo los tokens nuevos (la respuesta)
    response = tokenizer.decode(
        outputs[0][inputs.input_ids.shape[1]:], 
        skip_special_tokens=True
    )
    
    return response