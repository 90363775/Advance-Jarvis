import os
import time
import datetime
import webbrowser
import subprocess
import psutil
import pyautogui
import wikipedia
import requests
import cv2
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write as write_wav
import pywhatkit
import pytube
import instaloader
import psutil
import pyjokes
import random

# Test the current time reporting
def test_current_time():
    print("\n--- Testing Current Time Reporting ---")
    try:
        # Import the feature module
        from backend.feature import get_current_time
        
        # Call the function
        current_time = get_current_time()
        
        print(f"Current time: {current_time}")
        return True
    except Exception as e:
        print(f"Error testing current time: {e}")
        return False

# Test the current day reporting
def test_current_day():
    print("\n--- Testing Current Day Reporting ---")
    try:
        # Import the feature module
        from backend.feature import get_current_day
        
        # Call the function
        current_day = get_current_day()
        
        print(f"Current day: {current_day}")
        return True
    except Exception as e:
        print(f"Error testing current day: {e}")
        return False

# Test random programming joke generation
def test_programming_joke():
    print("\n--- Testing Programming Joke Generation ---")
    try:
        # Import the feature module
        from backend.feature import get_programming_joke
        
        # Call the function
        joke = get_programming_joke()
        
        if joke:
            print(f"Programming joke: {joke}")
            return True
        else:
            print("No joke returned")
            return False
    except Exception as e:
        print(f"Error testing programming joke: {e}")
        return False

# Test Wikipedia search
def test_wikipedia_search():
    print("\n--- Testing Wikipedia Search ---")
    try:
        # Import the feature module
        from backend.feature import search_wikipedia
        
        # Call the function with a test query
        summary = search_wikipedia("Python programming language")
        
        if summary:
            print(f"Wikipedia summary: {summary}")
            return True
        else:
            print("No summary returned")
            return False
    except Exception as e:
        print(f"Error testing Wikipedia search: {e}")
        return False

# Test browser search
def test_browser_search():
    print("\n--- Testing Browser Search ---")
    try:
        # Import the feature module
        from backend.feature import browser_search
        
        # Call the function with a test query
        result = browser_search("Python programming")
        
        print(f"Browser search result: {result}")
        return True
    except Exception as e:
        print(f"Error testing browser search: {e}")
        return False

# Test system volume control
def test_system_volume():
    print("\n--- Testing System Volume Control ---")
    try:
        # Import the feature module
        from backend.feature import set_system_volume
        
        # Test setting volume to 50%
        print("Setting volume to 50%...")
        result = set_system_volume(50)
        print(f"Volume set result: {result}")
        
        # Test setting volume to 100%
        print("Setting volume to 100%...")
        result = set_system_volume(100)
        print(f"Volume set result: {result}")
        
        return result
    except Exception as e:
        print(f"Error testing system volume: {e}")
        return False

# Run all tests
def run_all_tests():
    print("🚀 Starting Comprehensive Feature Tests 🚀")
    print(f"Test started at: {datetime.datetime.now()}")
    
    # Run tests in sequence
    test_results = []
    
    # Test 1: Current time
    test_results.append(("Current Time Reporting", test_current_time()))
    
    # Test 2: Current day
    test_results.append(("Current Day Reporting", test_current_day()))
    
    # Test 3: Programming jokes
    test_results.append(("Programming Joke Generation", test_programming_joke()))
    
    # Test 4: Wikipedia search
    test_results.append(("Wikipedia Search", test_wikipedia_search()))
    
    # Test 5: Browser search
    test_results.append(("Browser Search", test_browser_search()))
    
    # Test 6: System volume control
    test_results.append(("System Volume Control", test_system_volume()))
    
    # Print summary
    print("\n--- Test Summary ---")
    for test_name, test_result in test_results:
        status = "✅ Passed" if test_result else "❌ Failed"
        print(f"{test_name}: {status}")
    
    print(f"\nTest completed at: {datetime.datetime.now()}")
    print("\nNote: Some tests may fail if the system doesn't have the required applications installed.")
    print("For example, volume control requires pycaw to be properly installed.")
    
    return all(test_results[i][1] for i in range(len(test_results)))

# Run all tests if this script is executed directly
if __name__ == "__main__":
    run_all_tests()