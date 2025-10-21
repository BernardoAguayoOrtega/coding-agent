"""
Configuration management for AI Dev Team
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Global configuration"""

    # API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GROQ_VISION_MODEL = os.getenv("GROQ_VISION_MODEL", "llama-3.2-90b-vision-preview")

    # Agent Configuration
    MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "50"))
    VERBOSE = os.getenv("VERBOSE", "false").lower() == "true"

    # Cost Tracking
    TRACK_COSTS = os.getenv("TRACK_COSTS", "true").lower() == "true"

    # Human-in-the-Loop
    AUTO_APPROVE = os.getenv("AUTO_APPROVE", "false").lower() == "true"
    APPROVAL_TIMEOUT = int(os.getenv("APPROVAL_TIMEOUT", "300"))

    # Model pricing (USD per 1M tokens)
    GROQ_PRICING = {
        "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
        "llama-3.1-70b-versatile": {"input": 0.59, "output": 0.79},
        "llama-3.2-90b-vision-preview": {"input": 0.90, "output": 0.90},
        "mixtral-8x7b-32768": {"input": 0.24, "output": 0.24},
    }

    # Working directory
    WORK_DIR = Path.cwd() / "workspace"

    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in .env file or environment.\n"
                "Get your API key from: https://console.groq.com/keys"
            )

        # Create workspace directory
        cls.WORK_DIR.mkdir(exist_ok=True)

    @classmethod
    def estimate_cost(cls, input_tokens: int, output_tokens: int, model: str = None) -> float:
        """Estimate cost for token usage"""
        model = model or cls.GROQ_MODEL
        pricing = cls.GROQ_PRICING.get(model, cls.GROQ_PRICING["llama-3.3-70b-versatile"])
        cost = (input_tokens / 1_000_000 * pricing["input"]) + (
            output_tokens / 1_000_000 * pricing["output"]
        )
        return cost
