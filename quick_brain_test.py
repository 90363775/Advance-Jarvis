#!/usr/bin/env python3
"""
Quick Dual-Brain Test
Tests both OpenAI and Gemini with a simple question
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def simple_brain_test():
    print("🧠 QUICK DUAL-BRAIN TEST")
    print("=" * 40)
    
    try:
        # Import chatBot function
        from backend.feature import chatBot
        
        # Simple test question
        question = "Hello, are you working?"
        
        print(f"🎯 Testing: '{question}'")
        print("🔍 Watching brain switching...")
        print("-" * 40)
        
        # Test the chatBot function
        response = chatBot(question)
        
        print(f"\n✅ Final Response: {response}")
        print("\n🎉 Test completed!")
        
        # Analyze which brain likely responded
        if "Hello" in response and len(response) > 50:
            print("🧠 Likely AI-powered response!")
        else:
            print("🤖 Likely fallback response")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_brain_test()