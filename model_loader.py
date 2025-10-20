"""
Model Loader - Carga y gestiona el modelo de IA para el agente de codificación
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from pathlib import Path

# Configuración del modelo
MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-instruct"
CACHE_DIR = Path.home() / ".cache" / "coding-agent"


def load_model():
    """
    Carga el modelo y el tokenizador desde Hugging Face.
    Usa 'accelerate' para la carga automática de dispositivos (GPU/CPU).
    """
    print(f"🧠 Cargando modelo: {MODEL_NAME}...")
    
    # Crear directorio de caché si no existe
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Cargar tokenizador
    print("📚 Cargando tokenizador...")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        cache_dir=CACHE_DIR
    )
    
    # Configurar pad_token si no existe
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Cargar modelo
    print("🔧 Cargando modelo...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16,  # Media precisión para ahorrar memoria
        device_map="auto",          # Distribución automática en GPU/CPU
        cache_dir=CACHE_DIR,
        trust_remote_code=True      # Necesario para algunos modelos
    )
    
    print("✅ Modelo y tokenizador cargados exitosamente.")
    
    # Mostrar información del dispositivo
    if hasattr(model, 'hf_device_map'):
        print(f"📍 Mapa de dispositivos: {model.hf_device_map}")
    
    return model, tokenizer


def generate_response(model, tokenizer, prompt, max_new_tokens=300, temperature=0.7):
    """
    Genera una respuesta del modelo basada en un prompt.
    
    Args:
        model: El modelo cargado
        tokenizer: El tokenizador cargado
        prompt: El prompt de entrada
        max_new_tokens: Máximo número de tokens nuevos a generar
        temperature: Controla la creatividad (0.0 = determinista, 1.0 = muy creativo)
    """
    try:
        # Tokenizar el prompt
        inputs = tokenizer(
            prompt, 
            return_tensors="pt", 
            truncation=True,
            max_length=2048  # Límite para evitar prompts muy largos
        )
        
        # Mover inputs al dispositivo del modelo
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Generar respuesta
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.1,  # Evita repeticiones
                no_repeat_ngram_size=3   # Evita repetir n-gramas
            )
        
        # Decodificar solo los tokens nuevos
        new_tokens = outputs[0][inputs['input_ids'].shape[1]:]
        response = tokenizer.decode(
            new_tokens, 
            skip_special_tokens=True
        ).strip()
        
        return response
        
    except Exception as e:
        return f"Error al generar respuesta: {e}"


def get_model_info():
    """Retorna información sobre el modelo configurado."""
    return {
        "model_name": MODEL_NAME,
        "cache_dir": str(CACHE_DIR),
        "gpu_available": torch.cuda.is_available(),
        "mps_available": torch.backends.mps.is_available() if hasattr(torch.backends, 'mps') else False
    }