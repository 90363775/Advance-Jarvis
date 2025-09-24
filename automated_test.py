#!/usr/bin/env python3
"""
Automated Jarvis Test Runner
Automatically tests core functionality without voice input
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def run_automated_tests():
    print("🚀 AUTOMATED JARVIS TEST RUNNER")
    print("=" * 50)
    
    try:
        from backend.feature import chatBot
        
        # Define test categories
        test_categories = {
            "🔧 Basic Functionality": [
                "Hello Jarvis",
                "What is your name?",
                "How are you?", 
                "Are you working?",
                "What can you do?"
            ],
            "🧠 Intelligence": [
                "What is artificial intelligence?",
                "Tell me about Iron Man",
                "Explain machine learning",
                "What is quantum computing?"
            ],
            "🎨 Creativity": [
                "Tell me a joke",
                "Write a short poem",
                "Tell me something interesting"
            ],
            "🔍 Problem Solving": [
                "What is 25 times 4?",
                "How do I learn programming?",
                "What's the best way to study?"
            ],
            "🚨 Error Handling": [
                "asdfghjkl",
                "What is xyzabc?",
                "Random meaningless input"
            ]
        }
        
        total_tests = 0
        passed_tests = 0
        
        for category, questions in test_categories.items():
            print(f"\n{category}")
            print("-" * 40)
            
            for i, question in enumerate(questions, 1):
                total_tests += 1
                print(f"\n{i}. Testing: '{question}'")
                
                try:
                    response = chatBot(question)
                    
                    # Basic validation
                    if response and len(response.strip()) > 0:
                        passed_tests += 1
                        print(f"   ✅ PASS - Response: {response[:80]}{'...' if len(response) > 80 else ''}")
                    else:
                        print(f"   ❌ FAIL - Empty or no response")
                        
                except Exception as e:
                    print(f"   ❌ FAIL - Error: {e}")
        
        # Results summary
        print("\n" + "=" * 50)
        print("🎯 TEST RESULTS SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! Your Jarvis is working perfectly!")
        elif passed_tests > total_tests * 0.8:
            print("✅ GOOD! Most tests passed. Minor issues may exist.")
        elif passed_tests > total_tests * 0.5:
            print("⚠️  FAIR. Some functionality working, but needs attention.")
        else:
            print("❌ POOR. Major issues detected. Check your setup.")
            
        print("\n💡 NEXT STEPS:")
        print("1. Run: python run.py")
        print("2. Test with voice commands")
        print("3. Use: python jarvis_test_questions.py for full test list")
        
    except Exception as e:
        print(f"❌ Failed to run automated tests: {e}")
        print("💡 Make sure you're in the correct directory and all dependencies are installed.")

if __name__ == "__main__":
    run_automated_tests()