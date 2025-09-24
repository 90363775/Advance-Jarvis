#!/usr/bin/env python3
"""
Test script for the new Code Helper feature in Jarvis
This feature opens Notepad and writes code when you ask for coding help
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.feature import codeHelper

def test_code_helper():
    """Test the code helper functionality with various requests"""
    
    print("🚀 Testing Jarvis Code Helper Feature")
    print("=" * 50)
    
    # Test cases for different programming languages and requests
    test_cases = [
        "write a python hello world program",
        "create a javascript calculator",
        "help me with python web scraping code",
        "write a java program for me",
        "create an html webpage",
        "write a python calculator code",
        "help me code a basic python script"
    ]
    
    print("📝 Available test cases:")
    for i, case in enumerate(test_cases, 1):
        print(f"  {i}. {case}")
    
    print("\n" + "=" * 50)
    
    while True:
        try:
            print("\n🎯 Choose a test case (1-7) or type 'custom' for your own request:")
            print("   Type 'quit' to exit")
            
            choice = input("➤ Your choice: ").strip().lower()
            
            if choice == 'quit':
                print("👋 Goodbye!")
                break
            elif choice == 'custom':
                custom_request = input("➤ Enter your coding request: ").strip()
                if custom_request:
                    print(f"\n🔧 Processing: '{custom_request}'")
                    result = codeHelper(custom_request)
                    if result:
                        print(f"✅ Code file created: {result}")
                    else:
                        print("❌ Failed to create code file")
                else:
                    print("❌ Empty request, please try again")
            elif choice.isdigit() and 1 <= int(choice) <= len(test_cases):
                selected_case = test_cases[int(choice) - 1]
                print(f"\n🔧 Processing: '{selected_case}'")
                result = codeHelper(selected_case)
                if result:
                    print(f"✅ Code file created: {result}")
                else:
                    print("❌ Failed to create code file")
            else:
                print("❌ Invalid choice, please try again")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def demo_voice_commands():
    """Show examples of voice commands that trigger the code helper"""
    
    print("\n🎤 Voice Commands that trigger Code Helper:")
    print("=" * 50)
    
    voice_examples = [
        "Hey Jarvis, write a Python hello world program",
        "Hey Jarvis, help me code a calculator in JavaScript", 
        "Hey Jarvis, create a web scraping script",
        "Hey Jarvis, I need help with Java programming",
        "Hey Jarvis, write some HTML code for me",
        "Hey Jarvis, create a basic Python script",
        "Hey Jarvis, help me with coding"
    ]
    
    for i, example in enumerate(voice_examples, 1):
        print(f"  {i}. \"{example}\"")
    
    print("\n💡 Keywords that trigger Code Helper:")
    keywords = [
        "code", "programming", "write code", "create code", "help me code",
        "python code", "javascript code", "java code", "html code", 
        "css code", "sql code", "coding help", "program", "script",
        "algorithm", "function", "class", "method", "calculator code", 
        "web scraping", "hello world"
    ]
    
    for keyword in keywords:
        print(f"  • {keyword}")

if __name__ == "__main__":
    print("🤖 Jarvis Code Helper Test Tool")
    print("This feature automatically opens Notepad with generated code!")
    
    while True:
        print("\n" + "=" * 60)
        print("Choose an option:")
        print("1. Test Code Helper functionality")
        print("2. View voice command examples")
        print("3. Exit")
        
        choice = input("\n➤ Your choice (1-3): ").strip()
        
        if choice == '1':
            test_code_helper()
        elif choice == '2':
            demo_voice_commands()
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice, please try again")