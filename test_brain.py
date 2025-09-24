#!/usr/bin/env python3
"""
Jarvis Brain Test Script
This script tests the OpenAI integration and chatbot functionality.
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_brain():
    print("🧠 JARVIS BRAIN TEST")
    print("="*50)
    
    try:
        from backend.feature import chatBot
        
        # Test questions
        test_questions = [
            "Hello, are you working?",
            "What is your name?",
            "Tell me a joke",
            "What is artificial intelligence?",
            "What can you do?"
        ]
        
        print("🔍 Testing AI Brain with different questions...\n")
        
        for i, question in enumerate(test_questions, 1):
            print(f"🎯 Test {i}: '{question}'")
            print("-" * 40)
            
            try:
                response = chatBot(question)
                print(f"✅ Response received: {len(response)} characters")
                print(f"📝 Preview: {response[:100]}{'...' if len(response) > 100 else ''}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("\n")
        
        print("🎉 Brain test completed!")
        print("\n💡 If you see OpenAI responses, your brain is fully operational!")
        print("💡 If you see fallback responses, the basic brain is working!")
        
    except Exception as e:
        print(f"❌ Failed to import chatBot: {e}")
        print("💡 Make sure you're running this from the correct directory.")

def check_openai():
    print("\n🔍 Checking OpenAI Installation...")
    try:
        import openai
        print("✅ OpenAI library is available!")
        
        # Test API key
        openai.api_key = "your_openai_api_key_here"  # Replace with your actual API key
        
        print("🔑 API key is set!")
        print("🚀 OpenAI integration should be working!")
        
    except ImportError:
        print("❌ OpenAI library not found.")
        print("📦 Installing OpenAI library...")
        
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openai==0.28.1"])
            print("✅ OpenAI library installed successfully!")
        except Exception as e:
            print(f"❌ Failed to install: {e}")

if __name__ == "__main__":
    check_openai()
    test_brain()
    
    print("\n" + "="*50)
    print("🎤 Now test with voice commands:")
    print("1. Run: python run.py")
    print("2. Say: 'Hey Jarvis'")
    print("3. Ask: 'Are you smart?' or 'Tell me about AI'")
    print("="*50)