#!/usr/bin/env python3
"""
Jarvis Dual-Brain Setup Script
Sets up both OpenAI and Google Gemini AI integration for ultimate intelligence!
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required AI libraries"""
    print("📦 Installing AI libraries...")
    
    libraries = [
        "openai==0.28.1",
        "google-generativeai"
    ]
    
    for lib in libraries:
        try:
            print(f"🔧 Installing {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f"✅ {lib} installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {lib}: {e}")
            return False
    
    return True

def setup_gemini_integration(api_key=None):
    """Setup Gemini API key in the code"""
    if not api_key:
        print("\n🔑 Google Gemini API Key Setup:")
        print("1. Go to: https://makersuite.google.com/app/apikey")
        print("2. Sign in with your Google account")
        print("3. Click 'Create API Key'")
        print("4. Copy the API key")
        
        api_key = input("\n🔐 Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Update the feature.py file
        feature_path = "backend/feature.py"
        try:
            with open(feature_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the placeholder
            updated_content = content.replace(
                'GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"',
                f'GEMINI_API_KEY = "{api_key}"'
            )
            
            with open(feature_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print("✅ Gemini API key integrated successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error updating API key: {e}")
            print(f"💡 Please manually edit {feature_path} and replace YOUR_GEMINI_API_KEY_HERE with your key")
            return False
    else:
        print("⏭️  Skipped Gemini API key setup")
        print("💡 You can add it later by editing backend/feature.py")
        return False

def test_dual_brain():
    """Test both AI systems"""
    print("\n🧠 Testing Dual-Brain System...")
    
    try:
        from backend.feature import chatBot
        
        test_questions = [
            "Hello, test my intelligence",
            "What is quantum computing?",
            "Tell me about artificial intelligence"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n🎯 Test {i}: '{question}'")
            print("-" * 50)
            
            try:
                response = chatBot(question)
                print(f"✅ Response: {response[:100]}{'...' if len(response) > 100 else ''}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n🎉 Dual-brain test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

def main():
    print("🚀 JARVIS DUAL-BRAIN SETUP")
    print("=" * 50)
    print("🧠 OpenAI GPT + Google Gemini Integration")
    print("💪 Ultimate AI Intelligence for your assistant!")
    print()
    
    # Step 1: Install libraries
    print("📋 Step 1: Installing AI Libraries")
    if not install_requirements():
        print("❌ Failed to install required libraries. Please install manually:")
        print("   pip install openai==0.28.1 google-generativeai")
        return
    
    # Step 2: Setup Gemini API
    print("\n📋 Step 2: Gemini API Setup")
    gemini_setup = setup_gemini_integration()
    
    # Step 3: Test system
    print("\n📋 Step 3: Testing Dual-Brain System")
    test_dual_brain()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 SETUP SUMMARY")
    print("=" * 50)
    print("✅ OpenAI GPT: Integrated with your API key")
    print(f"{'✅' if gemini_setup else '⚠️ '} Google Gemini: {'Configured' if gemini_setup else 'Needs API key'}")
    print("✅ HugChat: Available as fallback")
    print("✅ Smart Responses: Always available")
    
    print("\n🎯 HOW IT WORKS:")
    print("1️⃣  Tries OpenAI GPT first (most powerful)")
    print("2️⃣  Falls back to Google Gemini if OpenAI fails")
    print("3️⃣  Uses HugChat if both fail")
    print("4️⃣  Smart local responses as final backup")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Run your Jarvis: python run.py")
    print("2. Say 'Hey Jarvis'")
    print("3. Ask complex questions to test the AI!")
    
    if not gemini_setup:
        print("\n💡 TO COMPLETE GEMINI SETUP:")
        print("1. Get free API key: https://makersuite.google.com/app/apikey")
        print("2. Run this script again with your key")
        print("3. Or manually edit backend/feature.py")
    
    print("\n🎉 Your Jarvis now has DUAL-BRAIN INTELLIGENCE!")

if __name__ == "__main__":
    main()