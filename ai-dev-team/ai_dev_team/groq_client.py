"""
Groq API client for fast, low-cost LLM inference
"""
from groq import Groq
from typing import List, Dict, Optional
from .config import Config
import base64


class GroqClient:
    """Groq API client wrapper with cost tracking and vision support"""

    def __init__(self):
        Config.validate()
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0

    def chat(
        self,
        messages: List[Dict[str, any]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> Dict:
        """
        Send chat completion request to Groq

        Args:
            messages: List of message dicts with 'role' and 'content'
                     For vision: content can be list with text and image_url
            model: Model to use (defaults to config)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response

        Returns:
            Dict with 'content', 'usage', and 'cost'
        """
        model = model or Config.GROQ_MODEL

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stream=False,
            )

            # Extract response
            content = response.choices[0].message.content

            # Track usage
            usage = {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

            # Calculate cost
            cost = Config.estimate_cost(usage["input_tokens"], usage["output_tokens"], model)

            # Update totals
            self.total_input_tokens += usage["input_tokens"]
            self.total_output_tokens += usage["output_tokens"]
            self.total_cost += cost

            return {"content": content, "usage": usage, "cost": cost}

        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

    def chat_with_image(
        self,
        text: str,
        image_path: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> Dict:
        """
        Send chat completion with image

        Args:
            text: Text prompt
            image_path: Path to image file
            model: Vision model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens

        Returns:
            Dict with 'content', 'usage', and 'cost'
        """
        model = model or Config.GROQ_VISION_MODEL

        # Read and encode image
        with open(image_path, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode("utf-8")

        # Determine image type
        ext = image_path.lower().split(".")[-1]
        mime_types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
        }
        mime_type = mime_types.get(ext, "image/jpeg")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{image_data}"},
                    },
                ],
            }
        ]

        return self.chat(messages, model=model, temperature=temperature, max_tokens=max_tokens)

    def get_stats(self) -> Dict:
        """Get usage statistics"""
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
        }

    def reset_stats(self):
        """Reset usage statistics"""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
