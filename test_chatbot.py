import sys
sys.path.insert(0, '.')

# Mock the speak function to avoid eel dependency in test
def mock_speak(text):
    print(f"[SPEAK]: {text}")

# Replace the speak function
import backend.feature
backend.feature.speak = mock_speak

from backend.feature import chatBot

# Test the fallback functionality
print("Testing chatbot with fallback...")
result = chatBot("hello")
print(f"Result: {result}")

print("\nTesting Iron Man query...")
result = chatBot("tell me about iron man")
print(f"Result: {result}")