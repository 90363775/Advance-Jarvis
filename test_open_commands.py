import sys
sys.path.insert(0, '.')

# Mock the speak function to avoid eel dependency in test
def mock_speak(text):
    print(f"[SPEAK]: {text}")

# Replace the speak function
import backend.feature
backend.feature.speak = mock_speak

from backend.feature import openCommand

# Test web applications
print("Testing web applications...")
print("\n1. Testing YouTube:")
openCommand("open youtube")

print("\n2. Testing Facebook:")  
openCommand("open facebook")

print("\n3. Testing Google:")
openCommand("open google")

# Test system applications
print("\n\nTesting system applications...")
print("\n4. Testing Notepad:")
openCommand("open notepad")

print("\n5. Testing Calculator:")
openCommand("open calculator")

print("\n6. Testing unknown app:")
openCommand("open unknown_app")