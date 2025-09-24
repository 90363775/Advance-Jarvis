#!/usr/bin/env python3
"""
Jarvis OpenAI Setup Script
This script will install the required OpenAI library and guide you through setup.
"""

import subprocess
import sys
import os

def install_openai():
    """Install the OpenAI library"""
    print("🔧 Installing OpenAI library...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai==0.28.1"])
        print("✅ OpenAI library installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install OpenAI library: {e}")
        return False

def check_openai():
    """Check if OpenAI library is already installed"""
    try:
        import openai
        print("✅ OpenAI library is already installed!")
        return True
    except ImportError:
        print("📦 OpenAI library not found. Installing...")
        return install_openai()

def setup_config():
    """Guide user through API key setup"""
    config_path = "backend/config.txt"
    
    print("\n🔑 OpenAI API Key Setup:")
    print("1. Go to: https://platform.openai.com/api-keys")
    print("2. Sign up or log in to your OpenAI account")
    print("3. Click 'Create new secret key'")
    print("4. Copy the API key (starts with 'sk-')")
    print("5. Paste it below")
    
    api_key = input("\n🔐 Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if api_key:
        if api_key.startswith('sk-'):
            # Update config file
            try:
                with open(config_path, 'r') as f:
                    content = f.read()
                
                # Replace the placeholder
                updated_content = content.replace(
                    "# OPENAI_API_KEY=your_api_key_here",
                    f"OPENAI_API_KEY={api_key}"
                )
                
                with open(config_path, 'w') as f:
                    f.write(updated_content)
                
                print("✅ API key saved successfully!")
                print("🎉 Jarvis is now ready to use OpenAI GPT!")
                
            except Exception as e:
                print(f"❌ Error saving API key: {e}")
                print(f"💡 Please manually edit {config_path} and add your API key")
        else:
            print("❌ Invalid API key format. API keys should start with 'sk-'")
            print(f"💡 Please manually edit {config_path} and add your API key")
    else:
        print("⏭️  Skipped API key setup")
        print(f"💡 You can manually edit {config_path} later to add your API key")

def test_openai():
    """Test OpenAI integration"""
    try:
        # Try to import and test
        from backend.feature import chatBot
        print("\n🧪 Testing OpenAI integration...")
        response = chatBot("Hello, are you working?")
        print(f"🤖 Response: {response}")
    except Exception as e:
        print(f"❌ Test failed: {e}")

def main():
    print("🚀 Jarvis OpenAI Integration Setup")
    print("="*40)
    
    # Step 1: Install OpenAI library
    if not check_openai():
        print("❌ Setup failed. Please install OpenAI manually: pip install openai==0.28.1")
        return
    
    # Step 2: Setup API key
    setup_config()
    
    print("\n📋 Setup Summary:")
    print("✅ OpenAI library installed")
    print("✅ Configuration file created")
    print("\n🎯 Next Steps:")
    print("1. Make sure you've added your OpenAI API key to backend/config.txt")
    print("2. Run your Jarvis application: python run.py")
    print("3. Say 'Hey Jarvis' and ask any question!")
    print("\n💡 Benefits of OpenAI Integration:")
    print("  • Much smarter conversations")
    print("  • Better understanding of complex questions")
    print("  • More natural responses")
    print("  • No more cookie.json issues!")

if __name__ == "__main__":
    main()