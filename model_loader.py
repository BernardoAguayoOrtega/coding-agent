"""
Model Loader - Carga y gestiona el modelo de IA para el agente de codificación
Supports multiple powerful coding models with automatic selection based on hardware
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Configuración de modelos disponibles
AVAILABLE_MODELS = {
    "deepseek-6.7b": {
        "name": "deepseek-ai/deepseek-coder-6.7b-instruct",
        "size": "6.7B",
        "memory_gb": 14,
        "description": "Fast and efficient for most coding tasks",
        "description_es": "Rápido y eficiente para la mayoría de tareas de codificación"
    },
    "deepseek-33b": {
        "name": "deepseek-ai/deepseek-coder-33b-instruct", 
        "size": "33B",
        "memory_gb": 66,
        "description": "More powerful reasoning and complex code generation",
        "description_es": "Razonamiento más potente y generación de código complejo"
    },
    "codellama-13b": {
        "name": "codellama/CodeLlama-13b-Instruct-hf",
        "size": "13B", 
        "memory_gb": 26,
        "description": "Meta's specialized coding model, excellent for code completion",
        "description_es": "Modelo especializado de Meta, excelente para completar código"
    },
    "codellama-34b": {
        "name": "codellama/CodeLlama-34b-Instruct-hf",
        "size": "34B",
        "memory_gb": 68,
        "description": "Largest CodeLlama model, superior code understanding",
        "description_es": "Modelo CodeLlama más grande, comprensión superior del código"
    },
    "phind-34b": {
        "name": "Phind/Phind-CodeLlama-34B-v2",
        "size": "34B",
        "memory_gb": 68,
        "description": "Fine-tuned for problem solving and debugging",
        "description_es": "Afinado para resolución de problemas y depuración"
    },
    "wizardcoder-15b": {
        "name": "WizardLM/WizardCoder-15B-V1.0",
        "size": "15B",
        "memory_gb": 30,
        "description": "Specialized in following instructions precisely",
        "description_es": "Especializado en seguir instrucciones con precisión"
    }
}

# Modelo por defecto
DEFAULT_MODEL = "deepseek-6.7b"
CACHE_DIR = Path.home() / ".cache" / "coding-agent"
CONFIG_FILE = CACHE_DIR / "model_config.json"


def get_available_memory_gb() -> float:
    """Estima la memoria disponible para el modelo."""
    try:
        if torch.cuda.is_available():
            # GPU memory
            return torch.cuda.get_device_properties(0).total_memory / (1024**3)
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            # Apple Silicon - estimate based on system
            import psutil
            return psutil.virtual_memory().total / (1024**3) * 0.7  # 70% for model
        else:
            # CPU memory
            import psutil
            return psutil.virtual_memory().available / (1024**3) * 0.5  # 50% for model
    except Exception:
        return 16.0  # Conservative default


def get_recommended_model() -> str:
    """Recomienda un modelo basado en la memoria disponible."""
    available_memory = get_available_memory_gb()
    
    # Sort models by memory requirement (ascending)
    sorted_models = sorted(
        AVAILABLE_MODELS.items(), 
        key=lambda x: x[1]["memory_gb"]
    )
    
    # Find the largest model that fits in memory
    for model_key, model_info in reversed(sorted_models):
        if model_info["memory_gb"] <= available_memory:
            return model_key
    
    # If nothing fits, return the smallest
    return sorted_models[0][0]


def load_model_config() -> Dict:
    """Carga la configuración del modelo."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    
    # Default config
    recommended = get_recommended_model()
    return {
        "current_model": recommended,
        "reflection_enabled": True,
        "human_in_loop": True,
        "language": "es"  # Default to Spanish
    }


def save_model_config(config: Dict):
    """Guarda la configuración del modelo."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def list_available_models() -> Dict:
    """Lista todos los modelos disponibles con sus características."""
    memory_available = get_available_memory_gb()
    
    result = {}
    for key, info in AVAILABLE_MODELS.items():
        result[key] = {
            **info,
            "fits_in_memory": info["memory_gb"] <= memory_available,
            "recommended": key == get_recommended_model()
        }
    
    return result


def select_model(model_key: str) -> bool:
    """Selecciona un modelo y guarda la configuración."""
    if model_key not in AVAILABLE_MODELS:
        return False
    
    config = load_model_config()
    config["current_model"] = model_key
    save_model_config(config)
    return True


def load_model(model_key: Optional[str] = None):
    """
    Carga el modelo y el tokenizador desde Hugging Face.
    Usa 'accelerate' para la carga automática de dispositivos (GPU/CPU).
    """
    config = load_model_config()
    
    if model_key:
        if model_key not in AVAILABLE_MODELS:
            raise ValueError(f"Model {model_key} not available. Use list_available_models() to see options.")
        current_model = model_key
        # Update config
        config["current_model"] = model_key
        save_model_config(config)
    else:
        current_model = config.get("current_model", get_recommended_model())
    
    model_info = AVAILABLE_MODELS[current_model]
    model_name = model_info["name"]
    
    print(f"🧠 Cargando modelo: {model_name} ({model_info['size']})...")
    print(f"📊 Memoria requerida: ~{model_info['memory_gb']}GB")
    
    # Crear directorio de caché si no existe
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Cargar tokenizador
    print("📚 Cargando tokenizador...")
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        cache_dir=CACHE_DIR
    )
    
    # Configurar pad_token si no existe
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Cargar modelo
    print("🔧 Cargando modelo...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
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
    config = load_model_config()
    current_model = config.get("current_model", get_recommended_model())
    model_info = AVAILABLE_MODELS[current_model]
    
    return {
        "model_key": current_model,
        "model_name": model_info["name"],
        "model_size": model_info["size"],
        "cache_dir": str(CACHE_DIR),
        "gpu_available": torch.cuda.is_available(),
        "mps_available": torch.backends.mps.is_available() if hasattr(torch.backends, 'mps') else False,
        "memory_required_gb": model_info["memory_gb"],
        "memory_available_gb": get_available_memory_gb(),
        "reflection_enabled": config.get("reflection_enabled", True),
        "human_in_loop": config.get("human_in_loop", True)
    }