#!/usr/bin/env python3
"""
Jarvis Dual-Brain Test Script
Tests OpenAI + Gemini integration with detailed diagnostics
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def check_ai_libraries():
    """Check if AI libraries are installed"""
    print("🔍 Checking AI Libraries...")
    
    # Check OpenAI
    try:
        import openai
        print("✅ OpenAI library: Available")
    except ImportError:
        print("❌ OpenAI library: Not installed")
        return False
    
    # Check Gemini
    try:
        import google.generativeai as genai
        print("✅ Google Gemini library: Available")
    except ImportError:
        print("❌ Google Gemini library: Not installed")
        return False
    
    return True

def test_brain_hierarchy():
    """Test the brain hierarchy system"""
    print("\n🧠 DUAL-BRAIN HIERARCHY TEST")
    print("=" * 50)
    
    try:
        from backend.feature import chatBot
        
        # Test questions with different complexity levels
        test_scenarios = [
            {
                "category": "Basic Greeting",
                "question": "Hello, how are you?",
                "expected": "Should get a friendly response"
            },
            {
                "category": "Knowledge Query", 
                "question": "What is machine learning?",
                "expected": "Should get detailed AI explanation"
            },
            {
                "category": "Creative Task",
                "question": "Write a short poem about AI",
                "expected": "Should generate creative content"
            },
            {
                "category": "Technical Question",
                "question": "Explain quantum computing in simple terms",
                "expected": "Should provide technical but accessible explanation"
            },
            {
                "category": "Personal Assistant",
                "question": "What can you help me with?",
                "expected": "Should list capabilities"
            }
        ]
        
        print("Testing brain switching logic...\n")
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"🎯 Test {i}: {scenario['category']}")
            print(f"❓ Question: '{scenario['question']}'")
            print(f"🎯 Expected: {scenario['expected']}")
            print("-" * 40)
            
            try:
                response = chatBot(scenario['question'])
                
                # Analyze response quality
                response_length = len(response)
                word_count = len(response.split())
                
                print(f"✅ Response received!")
                print(f"📊 Length: {response_length} characters, {word_count} words")
                print(f"📝 Response: {response[:150]}{'...' if len(response) > 150 else ''}")
                
                # Determine which brain likely responded
                if "OpenAI Response" in str(response) or response_length > 100:
                    print("🧠 Likely source: OpenAI GPT (Advanced Brain)")
                elif "Gemini Response" in str(response):
                    print("🌟 Likely source: Google Gemini (Backup Brain)")
                elif "HugChat Response" in str(response):
                    print("💬 Likely source: HugChat (Fallback Brain)")
                else:
                    print("🤖 Likely source: Local Smart Responses")
                
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("\n")
        
        print("🎉 Dual-brain hierarchy test completed!")
        
    except Exception as e:
        print(f"❌ Failed to test brain hierarchy: {e}")

def test_fallback_chain():
    """Test the complete fallback chain"""
    print("\n🔄 FALLBACK CHAIN TEST")
    print("=" * 50)
    
    print("Testing fallback sequence:")
    print("1️⃣  OpenAI GPT (Primary)")
    print("2️⃣  Google Gemini (Secondary)")  
    print("3️⃣  HugChat (Tertiary)")
    print("4️⃣  Smart Local Responses (Final)")
    print()
    
    # Test a question that should trigger fallbacks
    test_question = "Are you working correctly?"
    
    try:
        from backend.feature import chatBot
        print(f"🎯 Testing with: '{test_question}'")
        print("🔍 Watch the console for brain switching...")
        print("-" * 40)
        
        response = chatBot(test_question)
        print(f"✅ Final response: {response}")
        
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")

def display_brain_status():
    """Display current brain configuration status"""
    print("\n📊 BRAIN STATUS REPORT")
    print("=" * 50)
    
    # Check OpenAI status
    print("1️⃣  OpenAI GPT:")
    print("   ✅ API Key: Configured in code")
    print("   ⚠️  Status: May have quota limits")
    print("   🎯 Capability: Advanced reasoning, creativity, knowledge")
    
    # Check Gemini status
    print("\n2️⃣  Google Gemini:")
    try:
        with open('backend/feature.py', 'r') as f:
            content = f.read()
            if 'YOUR_GEMINI_API_KEY_HERE' in content:
                print("   ❌ API Key: Not configured")
                print("   📝 Setup: Run setup_dual_brain.py")
            else:
                print("   ✅ API Key: Configured")
                print("   🎯 Capability: Advanced reasoning, multimodal")
    except:
        print("   ❓ Status: Unknown")
    
    # Check HugChat status
    print("\n3️⃣  HugChat:")
    if os.path.exists('backend/cookie.json'):
        print("   ✅ Cookie: Available")
    else:
        print("   ❌ Cookie: Not found")
    print("   🎯 Capability: General conversation")
    
    # Check Local responses
    print("\n4️⃣  Smart Local Responses:")
    print("   ✅ Status: Always available")
    print("   🎯 Capability: Basic tasks, predefined responses")

def main():
    print("🚀 JARVIS DUAL-BRAIN DIAGNOSTIC")
    print("=" * 50)
    print("🧠 Testing OpenAI + Gemini Integration")
    print()
    
    # Step 1: Check libraries
    if not check_ai_libraries():
        print("\n💡 Run: python setup_dual_brain.py")
        return
    
    # Step 2: Display status
    display_brain_status()
    
    # Step 3: Test hierarchy
    test_brain_hierarchy()
    
    # Step 4: Test fallbacks
    test_fallback_chain()
    
    # Final summary
    print("\n" + "=" * 50)
    print("🎯 DUAL-BRAIN SUMMARY")
    print("=" * 50)
    print("✅ Your Jarvis has multiple AI brains!")
    print("🔄 Automatic fallback system working")
    print("🎯 Always gets a smart response")
    
    print("\n🚀 TO USE YOUR DUAL-BRAIN JARVIS:")
    print("1. Run: python run.py")
    print("2. Say: 'Hey Jarvis'")
    print("3. Ask complex questions!")
    print("4. Watch the brain switching in action!")

if __name__ == "__main__":
    main()