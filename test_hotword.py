#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from backend.feature import hotword
    print("Starting hotword detection test...")
    print("Say 'Hey Jarvis' or 'Hey Alexa' to test...")
    hotword()
except KeyboardInterrupt:
    print("\nHotword detection stopped by user.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()