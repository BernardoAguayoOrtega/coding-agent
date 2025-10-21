"""
Setup script for AI Dev Team
"""
from setuptools import setup, find_packages

setup(
    name="ai-dev-team",
    version="0.1.0",
    description="Your own AI software development team powered by Groq",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "groq>=0.11.0",
        "python-dotenv>=1.0.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
        "autopep8>=2.0.0",
        "black>=23.0.0",
        "pylint>=3.0.0",
        "radon>=6.0.0",
        "pillow>=10.0.0",
        "requests>=2.31.0",
        "pyyaml>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-dev-team=ai_dev_team.cli:main",
        ],
    },
    python_requires=">=3.8",
)
