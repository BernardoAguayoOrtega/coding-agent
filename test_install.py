#!/usr/bin/env python3
"""
Test script to verify AI Dev Team installation
"""
import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")

    try:
        import groq
        print("  ✓ groq")
    except ImportError as e:
        print(f"  ✗ groq: {e}")
        return False

    try:
        import click
        print("  ✓ click")
    except ImportError as e:
        print(f"  ✗ click: {e}")
        return False

    try:
        from rich.console import Console
        print("  ✓ rich")
    except ImportError as e:
        print(f"  ✗ rich: {e}")
        return False

    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv")
    except ImportError as e:
        print(f"  ✗ python-dotenv: {e}")
        return False

    try:
        import radon
        print("  ✓ radon")
    except ImportError as e:
        print(f"  ✗ radon: {e}")
        return False

    try:
        from PIL import Image
        print("  ✓ pillow")
    except ImportError as e:
        print(f"  ✗ pillow: {e}")
        return False

    return True

def test_ai_dev_team():
    """Test that ai_dev_team package is accessible"""
    print("\n🧪 Testing AI Dev Team package...")

    try:
        from ai_dev_team.config import Config
        print("  ✓ config")
    except ImportError as e:
        print(f"  ✗ config: {e}")
        return False

    try:
        from ai_dev_team.groq_client import GroqClient
        print("  ✓ groq_client")
    except ImportError as e:
        print(f"  ✗ groq_client: {e}")
        return False

    try:
        from ai_dev_team.tools import FileOperations
        print("  ✓ tools")
    except ImportError as e:
        print(f"  ✗ tools: {e}")
        return False

    try:
        from ai_dev_team.agents import OrchestratorAgent
        print("  ✓ agents")
    except ImportError as e:
        print(f"  ✗ agents: {e}")
        return False

    return True

def test_config():
    """Test configuration"""
    print("\n🧪 Testing configuration...")

    try:
        from ai_dev_team.config import Config

        # Check API key is set
        if Config.GROQ_API_KEY and Config.GROQ_API_KEY != "your_groq_api_key_here":
            print(f"  ✓ GROQ_API_KEY is set (length: {len(Config.GROQ_API_KEY)})")
        else:
            print("  ✗ GROQ_API_KEY not set properly")
            print("    Edit .env file and add your API key")
            return False

        print(f"  ✓ Model: {Config.GROQ_MODEL}")
        print(f"  ✓ Max iterations: {Config.MAX_ITERATIONS}")

        return True
    except Exception as e:
        print(f"  ✗ Configuration error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("AI Dev Team - Installation Test")
    print("=" * 60)

    all_passed = True

    if not test_imports():
        all_passed = False

    if not test_ai_dev_team():
        all_passed = False

    if not test_config():
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! AI Dev Team is ready to use.")
        print("\nTry running:")
        print('  python -m ai_dev_team "Create a hello world Python script"')
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()
