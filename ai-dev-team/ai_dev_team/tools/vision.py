"""
Vision tools for analyzing images
"""
from pathlib import Path
from typing import Optional
from PIL import Image


class VisionOperations:
    """Tools for image analysis"""

    def __init__(self, groq_client):
        self.groq_client = groq_client

    def analyze_image(self, image_path: str, question: str = "Describe this image in detail") -> str:
        """
        Analyze an image using vision model

        Args:
            image_path: Path to image file
            question: Question about the image

        Returns:
            Analysis result
        """
        try:
            path = Path(image_path)

            if not path.exists():
                return f"❌ Image not found: {image_path}"

            if not path.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
                return f"❌ Unsupported image format: {path.suffix}"

            # Get image info
            with Image.open(path) as img:
                width, height = img.size
                format_name = img.format

            # Analyze with vision model
            result = self.groq_client.chat_with_image(question, str(path))

            analysis = f"🖼️ Image Analysis: {image_path}\n"
            analysis += f"Format: {format_name}, Size: {width}x{height}\n\n"
            analysis += result["content"]

            return analysis

        except Exception as e:
            return f"❌ Error analyzing image: {str(e)}"

    def extract_ui_components(self, image_path: str) -> str:
        """
        Extract UI components from design mockup

        Args:
            image_path: Path to design image

        Returns:
            List of UI components
        """
        question = """Analyze this UI design and list all components you see:
        - Navigation elements
        - Buttons and their labels
        - Input fields and forms
        - Text sections and headings
        - Images and media
        - Layout structure

        Provide a detailed breakdown that can be used to build this UI."""

        return self.analyze_image(image_path, question)

    def compare_images(self, image1_path: str, image2_path: str) -> str:
        """
        Compare two images

        Args:
            image1_path: First image
            image2_path: Second image

        Returns:
            Comparison result
        """
        # For now, analyze each separately
        # TODO: Implement side-by-side comparison when Groq supports it

        analysis1 = self.analyze_image(image1_path, "Describe this image")
        analysis2 = self.analyze_image(image2_path, "Describe this image")

        return f"Image 1:\n{analysis1}\n\nImage 2:\n{analysis2}"
