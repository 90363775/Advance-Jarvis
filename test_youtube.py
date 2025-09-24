import sys
sys.path.insert(0, '.')

# Mock the speak function
def mock_speak(text):
    print(f"[SPEAK]: {text}")

# Replace the speak function
import backend.feature
backend.feature.speak = mock_speak

from backend.feature import PlayYoutube

# Test YouTube functionality
print("Testing YouTube playback...")
print("\n1. Testing 'play music on youtube':")
PlayYoutube("play music on youtube")

print("\n2. Testing 'play iron man on youtube':")
PlayYoutube("play iron man on youtube")