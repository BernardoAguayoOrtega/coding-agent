#!/bin/bash
# Quick installation script for AI Dev Team

set -e

echo "🤖 Installing AI Dev Team..."
echo

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo
echo "✅ Installation complete!"
echo
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo
echo "2. Test the installation:"
echo '   python -m ai_dev_team "Create a hello world Python script"'
echo
echo "3. Read the quick start guide:"
echo "   cat QUICKSTART.md"
echo
echo "Happy building! 🚀"
