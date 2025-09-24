import pywhatkit
import pickle
import googleapiclient.discovery
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from pytube import YouTube
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
from urllib.parse import urljoin
import cv2
import numpy as np
import sounddevice as sd
import win32api
import win32con
import win32ui
import win32gui
import winsound
import threading
import pygame
import datetime
from datetime import datetime, timedelta
import platform

# import playsound
# import eel


# @eel.expose
# def playAssistantSound():
#     music_dir = "frontend\\assets\\audio\\start_sound.mp3"
#     playsound(music_dir)


from compileall import compile_path
import os
import re
from shlex import quote
import ctypes
import struct
import subprocess
import time
import webbrowser
import eel
from hugchat import hugchat
import pyautogui
import os
import subprocess
import time
import psutil
from pynput.keyboard import Key, Controller as KeyboardController
import pyttsx3
import sqlite3
import tempfile
import qrcode

# Audio control imports
try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    from ctypes import cast, POINTER
    
    # Initialize audio control
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
except ImportError:
    print("Warning: pycaw not installed. Volume control features will be limited.")
    volume = None
except Exception as e:
    print(f"Warning: Could not initialize audio control: {e}")
    volume = None


# Add speak function for standalone use
def speak(text):
    """Text-to-speech function"""
    try:
        text = str(text)
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        
        # Choose voice safely - use index 2 if available, otherwise use the last available voice
        if len(voices) > 2:
            engine.setProperty('voice', voices[2].id)
        elif len(voices) > 0:
            engine.setProperty('voice', voices[-1].id)  # Use the last available voice
        # If no voices available, continue with default
        
        engine.setProperty('rate', 174)
        engine.say(text)
        engine.runAndWait()
        print(f"Jarvis: {text}")
    except Exception as e:
        print(f"Speak error: {e}")
        print(f"Jarvis: {text}")


# Database connection and configuration
try:
    conn = sqlite3.connect("jarvis.db")
    cursor = conn.cursor()
except Exception as e:
    print(f"Database connection error: {e}")
    conn = None
    cursor = None

# Import configuration
try:
    from config import ASSISTANT_NAME
except ImportError:
    ASSISTANT_NAME = "jarvis"


# Initialize pygame mixer
pygame.mixer.init()

# Define the function to play sound


@eel.expose
def play_assistant_sound():
    # Get the directory of the current script and build the path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level from backend to project root
    project_root = os.path.dirname(script_dir)
    sound_file = os.path.join(project_root, "frontend",
                              "assets", "audio", "start_sound.mp3")

    if os.path.exists(sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    else:
        print(f"Audio file not found: {sound_file}")


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()  # Fixed: assign result back to query

    app_name = query.strip()

    if app_name != "":

        try:
            # Fixed: Use LIKE for partial matching and better SQL syntax
            cursor.execute(
                'SELECT path FROM sys_command WHERE LOWER(name) LIKE ?', ('%' + app_name + '%',))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + app_name)
                os.startfile(results[0][0])

            else:
                cursor.execute(
                'SELECT url FROM web_command WHERE LOWER(name) LIKE ?', ('%' + app_name + '%',))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening " + app_name)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening " + app_name)
                    try:
                        os.system('start ' + app_name)
                    except:
                        speak("Application not found")
        except Exception as e:
            print(f"Error in openCommand: {e}")
            speak("Sorry, I couldn't open that application")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    """Alternative wake word detection using speech recognition"""
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Improve recognition sensitivity
    recognizer.energy_threshold = 300  # Lower threshold for better detection
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8  # Shorter pause threshold

    print("Wake word detection started. Say 'Hey Jarvis' to activate...")
    print("Adjusting for ambient noise... Please wait.")

    # Adjust for ambient noise
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Ready! Say 'Hey Jarvis' to wake me up.")

    while True:
        try:
            # Listen for wake word with more flexible timing
            with microphone as source:
                # Listen for audio with longer timeout and phrase time
                audio = recognizer.listen(
                    source, timeout=0.5, phrase_time_limit=4)

            # Try to recognize wake word
            try:
                text = recognizer.recognize_google(
                    audio, language='en-US').lower()
                print(f"Heard: {text}")

                # Check for wake words - more flexible matching
                wake_words = ["hey jarvis", "jarvis",
                    "hey alexa", "alexa", "hey davis", "davis"]
                detected = False

                for wake_word in wake_words:
                    if wake_word in text:
                        detected = True
                        break

                # Also check for partial matches
                if not detected:
                    if "hey" in text and ("jar" in text or "jav" in text or "dav" in text):
                        detected = True
                    elif "jarvis" in text or "alexa" in text:
                        detected = True

                if detected:
                    print("✓ Wake word detected! Listening for command...")
                    speak("Yes, I'm listening")

                    # Import here to avoid circular imports
                    from backend.command import takeAllCommands

                    try:
                        print("Processing voice command...")
                        takeAllCommands()  # This will listen for voice input and process commands
                        print("Command processed successfully.")
                    except Exception as e:
                        print(f"Error processing voice command: {e}")
                        speak("Sorry, I couldn't process that command.")

                    print("Returning to wake word detection...")
                    # Brief pause before resuming detection
                    time.sleep(1)

            except sr.UnknownValueError:
                # Speech not recognized, continue listening
                pass
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                # Continue listening even if there's an API error
                pass

        except sr.WaitTimeoutError:
            # No speech detected within timeout, continue listening
            pass
        except KeyboardInterrupt:
            print("\nWake word detection stopped by user.")
            break
        except Exception as e:
            print(f"Wake word detection error: {e}")
            time.sleep(1)  # Brief pause before retrying


def set_silence_mode(duration_minutes=0):
    """Set the system to silence mode for a specified duration

    Args:
        duration_minutes (int): Duration in minutes to keep in silence mode (0 for indefinite)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get the current volume
        current_volume = get_system_volume()

        # If duration is 0, just toggle silence mode
        if duration_minutes <= 0:
            if current_volume > 0:
                # Set volume to 0 (silence)
                set_system_volume(0)
                speak("Silence mode activated. Volume set to 0.")
            else:
                # Restore volume to previous level (if available)
                try:
                    with open('prev_volume.txt', 'r') as f:
                        prev_volume = int(f.read())
                    set_system_volume(prev_volume)
                    speak(
                        f"Silence mode deactivated. Volume restored to {prev_volume}%.")
                except:
                    # Default to 50% if no previous volume found
                    set_system_volume(50)
                    speak("Silence mode deactivated. Volume set to 50%.")
            return True
        else:
            # Save current volume before changing
            with open('prev_volume.txt', 'w') as f:
                f.write(str(current_volume))

            # Set volume to 0 (silence)
            set_system_volume(0)
            speak(f"Silence mode activated for {duration_minutes} minutes.")

            # Create a timer to restore volume after specified duration
            def restore_volume():
                time.sleep(duration_minutes * 60)  # Convert minutes to seconds
                try:
                    with open('prev_volume.txt', 'r') as f:
                        prev_volume = int(f.read())
                    set_system_volume(prev_volume)
                    speak(
                        f"Silence mode deactivated. Volume restored to {prev_volume}%.")
                except:
                    # Default to 50% if no previous volume found
                    set_system_volume(50)
                    speak("Silence mode deactivated. Volume set to 50%.")

            # Start the timer in a separate thread
            timer_thread = threading.Thread(target=restore_volume)
            timer_thread.start()

            return True

    except Exception as e:
        print(f"Error setting silence mode: {e}")
        speak("Sorry, I couldn't set the silence mode.")
        return False


def get_system_volume():
    """
    Get the current system volume level

    Returns:
        int: Current volume level (0-100) or -1 if error
    """
    try:
        if volume is None:
            print("Volume control not available (pycaw not installed)")
            return 50  # Return default value
            
        # Get current volume (0.0 - 1.0) and convert to percentage
        current_volume = volume.GetMasterVolumeLevelScalar()
        return int(current_volume * 100)
    except Exception as e:
        print(f"Error getting system volume: {e}")
        return 50  # Return default value


def findContact(query):

    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to',
        'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
                       ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0


def whatsApp(Phone, message, flag, name):

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)

    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)


def codeHelper(query):
    """
    Enhanced coding assistant that opens Notepad and writes code
    Detects programming languages and creates appropriate code
    """
    user_input = query.lower()

    # Detect programming language from query
    language_map = {
        'python': ['.py', 'python', 'py'],
        'javascript': ['.js', 'javascript', 'js', 'node'],
        'java': ['.java', 'java'],
        'cpp': ['.cpp', 'c++', 'cpp'],
        'c': ['.c', 'c programming'],
        'html': ['.html', 'html', 'web'],
        'css': ['.css', 'css', 'styling'],
        'sql': ['.sql', 'sql', 'database'],
        'php': ['.php', 'php'],
        'csharp': ['.cs', 'c#', 'csharp'],
        'go': ['.go', 'golang', 'go'],
        'rust': ['.rs', 'rust'],
        'kotlin': ['.kt', 'kotlin'],
        'swift': ['.swift', 'swift']
    }

    detected_language = 'python'  # Default
    file_extension = '.py'

    for lang, keywords in language_map.items():
        for keyword in keywords:
            if keyword in user_input:
                detected_language = lang
                file_extension = keywords[0] if keywords[0].startswith(
                    '.') else '.txt'
                break
        if detected_language != 'python' or lang == 'python':
            break

    # Generate code based on the request
    code_content = generate_code_for_request(user_input, detected_language)

    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(
        mode='w',
        suffix=file_extension,
        prefix=f'{detected_language}_code_',
        delete=False,
        encoding='utf-8'
    )

    try:
        # Write code to file
        temp_file.write(code_content)
        temp_file.flush()
        temp_file.close()

        # Open with Notepad
        subprocess.Popen(['notepad.exe', temp_file.name])

        speak(
            f"I've created a {detected_language} code sample and opened it in Notepad for you. The file has been saved as {os.path.basename(temp_file.name)}")

        print(f"✅ Code generated and opened in Notepad: {temp_file.name}")
        print(f"📝 Language: {detected_language}")
        print(f"📄 Content preview: {code_content[:100]}...")

        return temp_file.name

    except Exception as e:
        print(f"❌ Error opening code in Notepad: {e}")
        speak("Sorry, I couldn't open Notepad with the code. But I can still help you with the code.")
        return None


def generate_code_for_request(query, language):
    """
    Generate appropriate code based on user request and language
    """
    query = query.lower()

    # Common code templates
    if language == 'python':
        if 'hello world' in query or 'basic' in query:
            return '''# Hello World in Python
print("Hello, World!")

# Basic Python example
name = input("Enter your name: ")
print(f"Hello, {name}! Welcome to Python programming.")

# Simple function example
def greet(name):
    return f"Hello, {name}!"

# Call the function
user_name = "Jarvis User"
greeting = greet(user_name)
print(greeting)
'''
        elif 'calculator' in query:
            return '''# Simple Calculator in Python

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Error: Division by zero!"

# Main calculator loop
while True:
    print("\nSimple Calculator")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")

    choice = input("Enter choice (1-5): ")

    if choice == '5':
        print("Goodbye!")
        break

    if choice in ['1', '2', '3', '4']:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        if choice == '1':
            print(f"Result: {add(num1, num2)}")
        elif choice == '2':
            print(f"Result: {subtract(num1, num2)}")
        elif choice == '3':
            print(f"Result: {multiply(num1, num2)}")
        elif choice == '4':
            print(f"Result: {divide(num1, num2)}")
    else:
        print("Invalid choice!")
'''
        elif 'web scraping' in query or 'scrape' in query:
            return '''# Web Scraping Example in Python
import requests
from bs4 import BeautifulSoup
import csv

def scrape_website(url):
    try:
        # Send GET request
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Example: Extract all links
        links = soup.find_all('a', href=True)

        print(f"Found {len(links)} links:")
        for i, link in enumerate(links[:10]):  # Show first 10 links
            print(f"{i+1}. {link.text.strip()} - {link['href']}")

        return links

    except requests.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

# Example usage
if __name__ == "__main__":
    url = "https://example.com"  # Replace with target URL
    scrape_website(url)

    # Note: Always respect robots.txt and website terms of service
    # Consider adding delays between requests for large-scale scraping
'''
        else:
            return f'''# Python Code Template
# Generated by Jarvis AI Assistant
# Request: {query}

import os
import sys
from datetime import datetime

def main():
    """
    Main function for your Python application
    """
    print("Welcome to your Python program!")
    print(f"Current time: {{datetime.now()}}")

    # Your code here
    # TODO: Implement your specific functionality

if __name__ == "__main__":
    main()

# Common Python patterns:
#
# 1. List comprehension:
# numbers = [i**2 for i in range(10)]
#
# 2. Dictionary comprehension:
# squares = {{i: i**2 for i in range(5)}}
#
# 3. Exception handling:
# try:
#     # risky code
#     pass
# except Exception as e:
#     print(f"Error: {{e}}")
#
# 4. Class definition:
# class MyClass:
#     def __init__(self):
#         self.attribute = "value"
#
#     def method(self):
#         return self.attribute
'''

    elif language == 'javascript':
        if 'hello world' in query or 'basic' in query:
            return '''// Hello World in JavaScript
console.log("Hello, World!");

// Basic JavaScript example
const name = prompt("Enter your name:");
console.log(`Hello, ${name}! Welcome to JavaScript programming.`);

// Simple function example
function greet(name) {
    return `Hello, ${name}!`;
}

// Arrow function example
const greetArrow = (name) => `Hello, ${name}!`;

// Call the functions
const userName = "Jarvis User";
const greeting = greet(userName);
console.log(greeting);

// DOM manipulation example (for web pages)
document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('myButton');
    if (button) {
        button.addEventListener('click', function() {
            alert('Button clicked!');
        });
    }
});
'''
        else:
            return f'''// JavaScript Code Template
// Generated by Jarvis AI Assistant
// Request: {query}

// Modern JavaScript features
const currentTime = new Date();
console.log(`Current time: ${{currentTime}}`);

// Your main function
function main() {{
    console.log("Welcome to your JavaScript program!");

    // Your code here
    // TODO: Implement your specific functionality
}}

// Call main function
def check_internet_speed():
    try:
        import speedtest
        speak("Checking your internet speed. This might take a moment...")
        st = speedtest.Speedtest()
        download_speed = st.download() / 1000000  # Convert to Mbps
        upload_speed = st.upload() / 1000000  # Convert to Mbps
        speak(f"Your download speed is {download_speed:.2f} Mbps and upload speed is {upload_speed:.2f} Mbps")
        return f"Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps"
    except ImportError:
        speak("I need the speedtest-cli package to check internet speed. Please install it using pip install speedtest-cli")
        return None
    except Exception as e:
        speak("Sorry, I encountered an issue while checking your internet speed.")
        return None

def get_ip_address():
    try:
        import requests
        speak("Fetching your IP address information...")
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        ip = data.get("ip", "Unknown")
        city = data.get("city", "Unknown")
        region = data.get("region", "Unknown")
        country = data.get("country", "Unknown")
        speak(f"Your IP address is {ip} and you are located in {city}, {region}, {country}")
        return data
    except Exception as e:
        speak("Sorry, I encountered an issue while fetching your IP address information.")
        return None

def latest_news():
    try:
        import requests
        from bs4 import BeautifulSoup
        
        speak("Fetching the latest news headlines...")
        url = "https://news.google.com/rss"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="xml")
        news_items = soup.findAll('item')
        
        headlines = []
        for i, item in enumerate(news_items[:5]):  # Get top 5 news
            headlines.append(item.title.text)
        
        for headline in headlines:
            speak(headline)
        
        return headlines
    except ImportError:
        speak("I need the beautifulsoup4 package to fetch news. Please install it using pip install beautifulsoup4")
        return None
    except Exception as e:
        speak("Sorry, I encountered an issue while fetching the latest news.")
        return None

def screen_recorder(duration=10):
    try:
        import cv2
        import numpy as np
        import pyautogui
        import time
        from datetime import datetime
        
        speak(f"Starting screen recording for {duration} seconds")
        
        # Define the codec and create VideoWriter object
        filename = f"screen_recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
        screen_size = tuple(pyautogui.size())
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        fps = 20.0
        out = cv2.VideoWriter(filename, fourcc, fps, screen_size)
        
        start_time = time.time()
        while (time.time() - start_time) < duration:
            # Take screenshot
            img = pyautogui.screenshot()
            # Convert to numpy array
            frame = np.array(img)
            # Convert from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Write frame to video
            out.write(frame)
            
        # Release the video writer
        out.release()
        speak(f"Screen recording completed and saved as {filename}")
        return filename
    except ImportError:
        speak("I need opencv-python, numpy, and pyautogui packages for screen recording. Please install them.")
        return None
    except Exception as e:
        speak("Sorry, I encountered an issue while recording your screen.")
        return None

def voice_recorder(duration=5):
    try:
        import sounddevice as sd
        import numpy as np
        import scipy.io.wavfile as wav
        from datetime import datetime
        
        speak(f"Starting voice recording for {duration} seconds")
        
        # Set recording parameters
        fs = 44100  # Sample rate
        filename = f"voice_recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        # Record audio
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        
        # Save as WAV file
        wav.write(filename, fs, recording)
        
        speak(f"Voice recording completed and saved as {filename}")
        return filename
    except ImportError:
        speak("I need sounddevice and scipy packages for voice recording. Please install them.")
        return None
    except Exception as e:
        speak("Sorry, I encountered an issue while recording your voice.")
        return None

def access_mobile_camera():
    try:
        import cv2
        import numpy as np
        import socket
        import struct
        import pickle
        
        speak("Attempting to access mobile camera. Please ensure you have IP Webcam app running on your mobile device.")
        
        # You would need to replace this with the actual IP address of your mobile device
        # running IP Webcam or similar app
        mobile_ip = input("Please enter your mobile IP address (e.g., 192.168.1.100:8080): ")
        url = f"http://{mobile_ip}/video"
        
        # Connect to the mobile camera
        cap = cv2.VideoCapture(url)
        
        if not cap.isOpened():
            speak("Failed to connect to mobile camera. Please check the IP address and ensure the app is running.")
            return None
            
        speak("Successfully connected to mobile camera. Press 'q' to quit.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            cv2.imshow("Mobile Camera", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        speak("Mobile camera access ended.")
        return True
    except ImportError:
        speak("I need opencv-python package to access the camera. Please install it.")
        return None
    except Exception as e:
        speak("Sorry, I encountered an issue while accessing your mobile camera.")
        return None

def access_webcam():
    try:
        import cv2
        
        speak("Accessing webcam. Press 'q' to quit.")
        
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            speak("Failed to access webcam. Please check if it's connected properly.")
            return None
            
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            cv2.imshow("Webcam", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        speak("Webcam access ended.")
        return True
    except ImportError:
        speak("I need opencv-python package to access the webcam. Please install it.")
        return None
    except Exception as e:
        speak("Sorry, I encountered an issue while accessing your webcam.")
        return None

def locate_phone_number(phone_number):
    try:
        import phonenumbers
        from phonenumbers import geocoder, carrier
        
        speak(f"Locating information for phone number {phone_number}")
        
        # Parse phone number
        parsed_number = phonenumbers.parse(phone_number)
        
        # Get location
        location = geocoder.description_for_number(parsed_number, "en")
        
        # Get carrier
        service_provider = carrier.name_for_number(parsed_number, "en")
        
        # Check if valid
        is_valid = phonenumbers.is_valid_number(parsed_number)
        
        result = {
            "location": location,
            "service_provider": service_provider,
            "is_valid": is_valid
        }
        
        speak(f"The phone number {phone_number} is from {location} and the service provider is {service_provider}.")
        if not is_valid:
            speak("However, this appears to be an invalid phone number.")
            
        return result
    except ImportError:
        speak("I need the phonenumbers package to locate phone numbers. Please install it.")
        return None
    except Exception as e:
        speak("Sorry, I encountered an issue while locating the phone number information.")
        return None

def read_pdf(pdf_path):
    try:
        import PyPDF2
        
        speak(f"Reading PDF file: {pdf_path}")
        
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            
            # Get number of pages
            num_pages = pdf_reader.numPages
            speak(f"The PDF has {num_pages} pages.")
            
            # Extract text from each page
            text = ""
            for page_num in range(num_pages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
                
            # Speak first 100 characters
            preview = text[:100] + "..." if len(text) > 100 else text
            speak(f"Here's a preview of the content: {preview}")
            
            return text
    except ImportError:
        speak("I need the PyPDF2 package to read PDF files. Please install it.")
        return None
    except Exception as e:
        speak(f"Sorry, I encountered an issue while reading the PDF file: {str(e)}")
        return None

def add_contact(name, phone, email=None, address=None):
    try:
        import sqlite3
        
        speak(f"Adding contact: {name}")
        
        # Connect to database
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Insert new contact
        cursor.execute('''
        INSERT INTO contacts (name, phone, email, address)
        VALUES (?, ?, ?, ?)
        ''', (name, phone, email, address))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        speak(f"Contact {name} has been added successfully.")
        return True
    except Exception as e:
        speak(f"Sorry, I encountered an issue while adding the contact: {str(e)}")
        return None

def search_contact(query):
    try:
        import sqlite3
        
        speak(f"Searching for contact: {query}")
        
        # Connect to database
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contacts'")
        if not cursor.fetchone():
            speak("No contacts database found. Please add contacts first.")
            return []
        
        # Search for contacts
        cursor.execute('''
        SELECT * FROM contacts
        WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR address LIKE ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        
        contacts = cursor.fetchall()
        conn.close()
        
        if contacts:
            speak(f"Found {len(contacts)} contacts matching '{query}'.")
            for contact in contacts:
                speak(f"Name: {contact[1]}, Phone: {contact[2]}")
        else:
            speak(f"No contacts found matching '{query}'.")
            
        return contacts
    except Exception as e:
        speak(f"Sorry, I encountered an issue while searching for contacts: {str(e)}")
        return None

def generate_qr_code(data, filename=None):
    try:
        import qrcode
        from datetime import datetime
        
        speak("Generating QR code...")
        
        # Generate filename if not provided
        if not filename:
            filename = f"qrcode_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create an image from the QR Code
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save the image
        img.save(filename)
        
        speak(f"QR code has been generated and saved as {filename}")
        return filename
    except ImportError:
        speak("I need the qrcode package to generate QR codes. Please install it.")
        return None
    except Exception as e:
        speak(f"Sorry, I encountered an issue while generating the QR code: {str(e)}")
        return None

main();

// Common JavaScript patterns:
//
// 1. Array methods:
// const numbers = [1, 2, 3, 4, 5];
// const doubled = numbers.map(n => n * 2);
// const filtered = numbers.filter(n => n > 2);
//
// 2. Async/Await:
// async function fetchData() {{
//     try {{
//         const response = await fetch('https://api.example.com/data');
//         const data = await response.json();
//         return data;
//     }} catch (error) {{
//         console.error('Error:', error);
//     }}
// }}
//
// 3. Destructuring:
// const {{name, age}} = person;
// const [first, second] = array;
'''

    elif language == 'html':
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Web Page</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        .button {{
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }}
        .button:hover {{
            background-color: #0056b3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Web Page</h1>
        <p>This HTML template was generated by Jarvis AI Assistant.</p>
        <p>Request: {query}</p>

        <h2>Features:</h2>
        <ul>
            <li>Responsive design</li>
            <li>Modern CSS styling</li>
            <li>Clean structure</li>
            <li>Interactive elements</li>
        </ul>

        <button class="button" onclick="sayHello()">Click Me!</button>

        <div id="output"></div>
    </div>

    <script>
        function sayHello() {{
            document.getElementById('output').innerHTML =
                '<p style="color: green; margin-top: 10px;">Hello from Jarvis!</p>';
        }}

        // Add more JavaScript functionality here
        console.log('Page loaded successfully!');
    </script>
</body>
</html>
'''

    elif language == 'java':
        return f'''// Java Code Template
// Generated by Jarvis AI Assistant
// Request: {query}

import java.util.*;
import java.io.*;

public class JavaProgram {{

    public static void main(String[] args) {{
        System.out.println("Hello, World!");
        System.out.println("Welcome to Java programming!");

        // Scanner for user input
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter your name: ");
        String name = scanner.nextLine();

        // Call method
        String greeting = greet(name);
        System.out.println(greeting);

        scanner.close();
    }}

    // Method example
    public static String greet(String name) {{
        return "Hello, " + name + "!";
    }}

    // Common Java patterns:
    //
    // 1. ArrayList usage:
    // ArrayList<String> list = new ArrayList<>();
    // list.add("item");
    //
    // 2. Exception handling:
    // try {{
    //     // risky code
    // }} catch (Exception e) {{
    //     System.err.println("Error: " + e.getMessage());
    // }}
    //
    // 3. Class definition:
    // public class MyClass {{
    //     private String attribute;
    //
    //     public MyClass(String attr) {{
    //         this.attribute = attr;
    //     }}
    //
    //     public String getAttribute() {{
    //         return attribute;
    //     }}
    // }}
}}
'''

    else:
        # Generic template for other languages
        return f'''// {language.upper()} Code Template
// Generated by Jarvis AI Assistant
// Request: {query}

// Your {language} code goes here
// TODO: Implement your specific functionality

/*
 * This is a basic template for {language} programming.
 * Modify this code according to your needs.
 *
 * Generated on: {time.strftime("%Y-%m-%d %H:%M:%S")}
 */

// Main program logic
function main() {{
    // Your code here
    console.log("Hello from {language}!");
}}

// Call main function
main();
'''


def chatBot(query):
    user_input = query.lower()

    # Try OpenAI GPT first (if API key is available)
    try:
        import openai
        import os

        # Set the OpenRouter API key (free with credits)
        openai.api_key = "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"
        openai.api_base = "https://openrouter.ai/api/v1"

        print(f"🚀 Processing with OpenRouter (Free AI): '{user_input}'")

        # Create chat completion with OpenRouter
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",  # OpenRouter model format
            messages=[
                {"role": "system", "content": "You are Jarvis, an intelligent AI assistant like in Iron Man. Be helpful, smart, and slightly witty. Keep responses conversational and under 100 words unless asked for detail. Address the user respectfully."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )

        response_text = response.choices[0].message.content.strip()
        print(f"✅ OpenAI Response: {response_text}")
        speak(response_text)
        return response_text

    except ImportError:
        print("❌ OpenAI library not installed. Installing automatically...")
        try:
            import subprocess
            import sys
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "openai==0.28.1"])
            print("✅ OpenAI installed! Restarting chat function...")
            # Try again after installation
            import openai
            openai.api_key = "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"
            openai.api_base = "https://openrouter.ai/api/v1"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Jarvis, an intelligent AI assistant like in Iron Man. Be helpful, smart, and slightly witty. Keep responses conversational and under 100 words unless asked for detail."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150,
                temperature=0.7
            )
            response_text = response.choices[0].message.content.strip()
            print(f"✅ OpenAI Response (after install): {response_text}")
            speak(response_text)
            return response_text
        except Exception as install_error:
            print(f"❌ Failed to install OpenAI: {install_error}")
            speak(
                "I'm having trouble installing my advanced brain. Let me try other options.")
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        if "quota" in str(e).lower():
            print("💡 OpenAI quota exceeded, trying Google Gemini...")
        else:
            print("💡 OpenAI failed, trying Google Gemini...")

    # Try Google Gemini API as backup
    try:
        import google.generativeai as genai

        # Configure Gemini API (add your Gemini API key here)
        # Replace with actual key when you get one
        GEMINI_API_KEY = "AIzaSyDH38WxGu5GlbUF_w5II_V5rOBkJRGxoOM"
        genai.configure(api_key=GEMINI_API_KEY)

        print(f"🌟 Processing with Google Gemini: '{user_input}'")

        # Create the model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate response
        prompt = f"You are Jarvis, an intelligent AI assistant like in Iron Man. Be helpful, smart, and slightly witty. Keep responses conversational and under 100 words unless asked for detail. User says: {user_input}"
        response = model.generate_content(prompt)

        response_text = response.text.strip()
        print(f"✅ Gemini Response: {response_text}")
        speak(response_text)
        return response_text

    except ImportError:
        print("❌ Gemini library not installed. Installing automatically...")
        try:
            import subprocess
            import sys
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "google-generativeai"])
            print("✅ Gemini installed! Please add your API key and restart.")
            speak("Gemini AI installed. Please add your API key to enable this feature.")
        except Exception as install_error:
            print(f"❌ Failed to install Gemini: {install_error}")

    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        if "API_KEY" in str(e) or "key" in str(e).lower() or "YOUR_GEMINI_API_KEY_HERE" in str(e):
            print(
                "💡 Gemini API key needed. Get one from https://makersuite.google.com/app/apikey")
            speak(
                "I need a Gemini API key to use Google's AI. You can get one for free from Google AI Studio.")
        else:
            print("💡 Gemini failed, trying HugChat...")

    # Fallback to HugChat if both AI services fail
    try:
        from hugchat import hugchat
        print("🔄 Trying HugChat as final AI fallback...")
        chatbot = hugchat.ChatBot(cookie_path=r"backend\cookie.json")
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(user_input)
        print(f"📱 HugChat Response: {response}")
        speak(response)
        return response
    except Exception as e:
        print(f"❌ HugChat error: {e}")
        print("🤖 Using intelligent local responses...")

        # Final fallback to predefined responses
        fallback_responses = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! What can I do for you?",
            "how are you": "I'm doing well, thank you for asking! How can I assist you?",
            "what is your name": "I'm Jarvis, your AI assistant.",
            "who are you": "I'm Jarvis, an intelligent AI assistant created by syed farhan to help you with various tasks.",
            "what can you do": "I can help you open applications, play music on YouTube, send messages, make calls, answer questions, and have conversations. Just ask me!",
            "thank you": "You're welcome! Is there anything else I can help you with?",
            "thanks": "You're welcome! Happy to help!",
            "bye": "Goodbye! Have a great day!",
            "goodbye": "Goodbye! Feel free to call me anytime you need assistance.",
            "time": f"The current time is {time.strftime('%I:%M %p')}",
            "date": f"Today's date is {time.strftime('%A, %B %d, %Y')}",
            "weather": "I don't have access to current weather data, but you can ask me to open a weather website for you.",
            "joke": "Why don't scientists trust atoms? Because they make up everything!",
            "iron man": "Iron Man is a fictional superhero from Marvel Comics. Tony Stark, the genius billionaire behind the Iron Man suit, is quite inspiring!",
            "marvel": "Marvel has created many amazing superheroes! Iron Man, Captain America, Thor, and many others. Do you have a favorite?",
            "music": "I can help you play music! Just say 'play [song name] on YouTube' and I'll open it for you.",
            "help": "I'm here to help! You can ask me to open applications, play music, send messages, answer questions, or just have a conversation. What would you like to do?"
        }

        # Find the best matching response
        response = "I'm sorry, I'm having some technical difficulties right now. However, I can still help you open applications, play music on YouTube, or send messages. What would you like me to do?"

        for key, value in fallback_responses.items():
            if key in user_input:
                response = value
                break

        # Check for more complex patterns
        if "what" in user_input and "time" in user_input:
            response = f"The current time is {time.strftime('%I:%M %p')}"
        elif "what" in user_input and "date" in user_input:
            response = f"Today's date is {time.strftime('%A, %B %d, %Y')}"
        elif "open" in user_input:
            response = "I can help you open applications! Just say 'open' followed by the application name, like 'open YouTube' or 'open Facebook'."
        elif "play" in user_input and "youtube" in user_input:
            response = "I can play music on YouTube! Just say 'play [song name] on YouTube' and I'll search and play it for you."
        elif "test" in user_input or "working" in user_input or "brain" in user_input:
            response = "My brain is working! My basic systems are operational, though my advanced AI features may need OpenAI connectivity. How can I assist you?"
        elif "smart" in user_input or "intelligent" in user_input:
            response = "I strive to be as intelligent as possible! I can process complex questions and help with various tasks. What would you like to know?"

        print(f"🤖 Fallback Response: {response}")
        speak(response)
        return response


def init_news_api():
    """Initialize the News API client"""
    try:
        # Try to get API key from environment variable
        api_key = os.getenv("NEWS_API_KEY")

        # If not found in environment variables, try to read from file
        if not api_key:
            try:
                with open("news_api_key.txt", "r") as f:
                    api_key = f.read().strip()
            except FileNotFoundError:
                pass

        # If API key is still not found, prompt the user
        if not api_key:
            speak("News API key not found. Please provide your News API key")
            from backend.command import takeCommand
            api_key = takeCommand()

            # Save the API key for future use
            if api_key and api_key != "None":
                with open("news_api_key.txt", "w") as f:
                    f.write(api_key)
                speak("API key saved for future use")

        if api_key and api_key != "None":
            return NewsApiClient(api_key=api_key)
        else:
            speak("News API key is required to fetch news")
            return None
    except Exception as e:
        print(f"Error initializing News API: {e}")
        return None


def get_news(topics=None, language="en", num_articles=5):
    """Get news articles based on topics"""
    news_client = init_news_api()

    if not news_client:
        return None

    try:
        if topics:
            # Search for specific topics
            all_articles = []
            for topic in topics:
                articles = news_client.get_top_headlines(
                    q=topic, language=language, page_size=num_articles)
                for article in articles["articles"]:
                    all_articles.append({
                        "title": article["title"],
                        "description": article["description"],
                        "url": article["url"],
                        "source": article["source"]["name"],
                        "topic": topic
                    })
            return all_articles
        else:
            # Get top headlines without specific topics
            articles = news_client.get_top_headlines(
                language=language, page_size=num_articles)

            all_articles = []
            for article in articles["articles"]:
                all_articles.append({
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "source": article["source"]["name"]
                })

            return all_articles
    except Exception as e:
        print(f"Error fetching news: {e}")
        speak("Error fetching news. Please check your internet connection and API key")
        return None


def handle_news_request(query):
    """Handle news fetching requests from the user"""
    # Check if user asked for news
    if "news" in query or "latest news" in query or "current news" in query:
        topics = extract_topics(query)
        if topics:
            articles = get_news(topics=topics)
            if articles:
                speak("Here are the latest news articles:")
                for article in articles:
                    speak(f"{article['title']} from {article['source']}")
            else:
                speak("No news articles found for the specified topics.")
        else:
            articles = get_news()
            if articles:
                speak("Here are the latest news headlines:")
                for article in articles:
                    speak(f"{article['title']} from {article['source']}")
            else:
                speak("No news articles found.")
    else:
        return None


def get_current_time():
    """Get the current time and format it for the user"""
    try:
        # Get current time
        now = datetime.datetime.now()

        # Format time
        current_time = now.strftime("%I:%M %p")  # 12-hour format with AM/PM

        # Generate verbal response
        time_message = f"The current time is {current_time}"
        speak(time_message)

        return current_time
    except Exception as e:
        print(f"Error getting current time: {e}")
        speak("Failed to get current time")
        return None


def handle_time_request(query):
    """Handle current time reporting requests"""
    if "time" in query or "current time" in query or "what time" in query:
        return get_current_time()

    return None


def get_current_day():
    """Get the current day and format it for the user"""
    try:
        # Get current date
        now = datetime.datetime.now()

        # Format date
        # Full day name, month name, day, year
        current_day = now.strftime("%A, %B %d, %Y")

        # Generate verbal response
        day_message = f"Today is {current_day}"
        speak(day_message)

        return current_day
    except Exception as e:
        print(f"Error getting current day: {e}")
        speak("Failed to get current day")
        return None


def handle_day_request(query):
    """Handle current day reporting requests"""
    if "day" in query or "date" in query or "current day" in query or "current date" in query or "what day" in query or "what date" in query:
        return get_current_day()

    return None

    # Find the starting position of the topic
    topic_start = query.find("about")
    if topic_start == -1:
        topic_start = query.find("on")

    if topic_start != -1:
        topics = [query[topic_start+3:].strip()]

        # Get news
        news_articles = get_news(topics)

        if news_articles and len(news_articles) > 0:
            speak(f"Here are the latest {len(news_articles)} news articles:")

            for i, article in enumerate(news_articles[:5], 1):
                print(f"{i}. {article['title']} (Source: {article['source']})")
                speak(f"{i}. {article['title']}")

                # Read the description if available
                if article["description"]:
                    print(f"   {article['description']}")
                    # Speak only the first 200 characters of the description
                    description_preview = article["description"][:200] + (
                        "..." if len(article["description"]) > 200 else "")
                    speak(f"{description_preview}")

                # Add a pause between articles
                if i < len(news_articles):
                    time.sleep(2)

            speak(
                "Would you like me to read a specific article or open one in the browser?")
            return news_articles
        else:
            speak("No news articles found")
            return None

    return None


def handle_news_query(query):
    """Main entry point for handling news requests"""
    return handle_news_request(query)


def read_pdf(file_path):
    """Read text content from a PDF file."""
    if not os.path.exists(file_path):
        speak(f"File not found: {file_path}")
        return None

    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""

            # Extract text from each page
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n\n"

            # Speak the number of pages and some content
            page_count = len(pdf_reader.pages)
            speak(
                f"Found {page_count} page{'s' if page_count != 1 else ''} in the PDF")

            # Show preview of first page
            if text_content.strip():
                preview_length = min(200, len(text_content))
                speak(f"Here's a preview: {text_content[:preview_length]}...")
            else:
                speak("The PDF appears to be empty or contains only non-text content")

            return text_content
    except Exception as e:
        speak("Error reading PDF file")
        print(f"Error reading PDF: {e}")
        return None


def handle_pdf_request(query):
    """Handle PDF reading requests from the user."""
    if "read pdf" in query or "open pdf" in query or "pdf" in query:
        speak("Please provide the path to the PDF file you want me to read")

        # Get file path from user
        from backend.command import takeCommand
        file_path = takeCommand()

        if file_path and os.path.exists(file_path) and file_path.lower().endswith('.pdf'):
            speak(f"Reading PDF file: {file_path}")
            return read_pdf(file_path)
        else:
            speak("Invalid file path or file is not a PDF")
            return None

    return None


def search_wikipedia(query, sentences=2):
    """Search Wikipedia for the given query and return a summary"""
    try:
        # Set the language to English
        wikipedia.set_lang("en")

        # Search for the query
        search_results = wikipedia.search(query)

        if not search_results:
            speak("I couldn't find any information on that topic.")
            return None

        # Get the summary of the first result
        summary = wikipedia.summary(search_results[0], sentences=sentences)

        # Speak the summary
        speak(f"Here's what I found: {summary}")

        return summary
    except Exception as e:
        print(f"Error searching Wikipedia: {e}")
        speak("Failed to search Wikipedia")
        return None


def download_youtube_song(url, output_path=None):
    """Download a YouTube song from the provided URL"""
    try:
        speak("Downloading YouTube song. This may take a few minutes...")

        # Create YouTube object
        yt = YouTube(url)

        # Get the highest resolution audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # If no audio stream found, get the highest resolution video
        if not audio_stream:
            audio_stream = yt.streams.get_highest_resolution()

        # Set output path if not provided
        if not output_path:
            output_path = os.path.join(os.getcwd(), "downloads")
            if not os.path.exists(output_path):
                os.makedirs(output_path)

        # Download the song
        downloaded_file = audio_stream.download(output_path)

        # Get the file name
        file_name = os.path.basename(downloaded_file)

        speak(f"YouTube song downloaded successfully: {file_name}")
        return os.path.join(output_path, file_name)
    except Exception as e:
        print(f"Error downloading YouTube song: {e}")
        speak("Failed to download YouTube song")
        return None


def handle_youtube_downloading(query):
    """Handle YouTube song downloading requests from the user"""
    if "download youtube" in query or "download song" in query or "youtube download" in query:
        speak("Please provide the URL of the YouTube song")
        url = takeCommand()

        if not url or url == "None":
            speak("I couldn't get the YouTube URL")
            return None

        # Optional: Ask for output path
        speak("Where should I save the downloaded song? (Press enter for default)")
        output_path = takeCommand()

        if not output_path or output_path == "None":
            output_path = None


def take_screenshot(filename=None):
    """Take a screenshot and save it with a custom filename"""
    try:
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        # Generate timestamp if no filename provided
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        # Add screenshots directory to filename
        file_path = os.path.join(screenshots_dir, filename)

        # Take and save the screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)

        speak(f"Screenshot saved to {file_path}")
        return file_path
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        speak("Failed to take screenshot")
        return None


def handle_screenshot_capture(query):
    """Handle screenshot capture requests from the user"""
    if "take screenshot" in query or "capture screenshot" in query or "screenshot" in query:
        speak("Should I use a custom filename for the screenshot?")
        use_custom = takeCommand().lower()

        filename = None
        if "yes" in use_custom or "custom" in use_custom:
            speak("What filename should I use for the screenshot?")
            filename = takeCommand()

            # Ensure filename ends with .png
            if filename and not filename.lower().endswith(".png"):
                filename += ".png"

        return take_screenshot(filename)

    return None

    return download_youtube_song(url, output_path)

    return None


def read_pdf_file(file_path):
    """Read PDF file and extract text content."""
    try:
        text_content = read_pdf(file_path)

        if text_content:
            # Ask if user wants to save the text content
            speak("Would you like me to save the text content to a file?")
            response = takeCommand().lower()

            if "yes" in response or "save" in response:
                # Save to a text file
                output_path = file_path.replace('.pdf', '.txt')
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                speak(f"Text content saved to: {output_path}")

        return text_content
    except:
        speak("Invalid PDF file path or format")
        return None


def record_screen_with_audio(duration=10, output_video='screen_recording.mp4', output_audio='audio_recording.wav'):
    """Record screen activity with audio for a specified duration."""
    # Get screen dimensions
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    
    # Create device context
    desktop_dc = win32gui.GetWindowDC(win32gui.GetDesktopWindow())
    capture_dc = win32ui.CreateDCFromHandle(desktop_dc)
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(capture_dc, screen_width, screen_height)
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video, fourcc, 20.0, (screen_width, screen_height))
    
    # Record audio
    fs = 44100  # Sample rate
    audio_recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    
    speak("Started screen recording with audio")
    print(f"Recording screen for {duration} seconds...")
    
    # Capture screen frames
    start_time = time.time()
    while time.time() - start_time < duration:
        capture_dc.BitBlt((0, 0), (screen_width, screen_height), desktop_dc, (left, top), win32con.SRCCOPY)
        bmpstr = bitmap.GetBitmapBits(True)
        
        # Convert to numpy array and reshape
        img = np.frombuffer(bmpstr, dtype=np.uint8)
        img.shape = (screen_height, screen_width, 4)
        
        # Convert to RGB and write to video
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        video_writer.write(img)
        
        # Small delay to control frame rate
        cv2.waitKey(50)
    
    # Stop audio recording
    sd.wait()
    write_wav(output_audio, fs, audio_recording)
    
    # Clean up
    video_writer.release()
    win32gui.DeleteObject(bitmap.GetHandle())
    capture_dc.DeleteDC()
    win32gui.ReleaseDC(win32gui.GetDesktopWindow(), desktop_dc)
    
    # Combine audio and video
    combine_audio_video(output_video, output_audio)
    
    speak("Screen recording completed")
    print(f"Recording saved as {output_video}")


def combine_audio_video(video_path, audio_path):
    """Combine video and audio into a single file."""
    try:
        import moviepy.editor as mpe
        video = mpe.VideoFileClip(video_path)
        audio = mpe.AudioFileClip(audio_path)
        final_video = video.set_audio(audio)
        final_video.write_videofile("final_recording.mp4", codec='libx264', audio_codec='aac')
        
        # Clean up temporary files
        os.remove(video_path)
        os.remove(audio_path)
    except ImportError:
        speak("Moviepy library not installed. Install it to combine audio and video")
        print("Moviepy library not installed. Install it to combine audio and video")


def handle_recording(query):
    """Handle screen recording requests from the user."""
    if "screen recording" in query or "record screen" in query:
        duration = 10  # Default duration in seconds
        
        # Extract duration from query if specified
        import re
        duration_match = re.search(r'(\d+)\s*(seconds?|secs?|sec?)', query, re.IGNORECASE)
        if duration_match:
            duration = int(duration_match.group(1))
        
        speak(f"Starting screen recording for {duration} seconds")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_file = f"screen_recording_{timestamp}.mp4"
        audio_file = f"audio_recording_{timestamp}.wav"
        
        record_screen_with_audio(duration, video_file, audio_file)
        speak("Screen recording completed successfully")


def access_web_camera(camera_index=0):
    """Access built-in or USB web camera."""
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        speak("Could not open web camera")
        return None
    
    speak("Successfully opened web camera")
    return cap


def handle_web_camera(query):
    """Handle web camera access requests."""
    if "open web camera" in query or "access web camera" in query or "open webcam" in query or "access webcam" in query:
        speak("Opening web camera. Press Q to exit")
        
        # Try common camera indexes
        cap = None
        for index in [0, 1, 2]:
            cap = access_web_camera(index)
            if cap is not None:
                break
        
        if cap is not None and cap.isOpened():
            while True:
                ret, frame = cap.read()
                if not ret:
                    speak("Failed to capture frame from camera")
                    break
                
                # Display the frame
                cv2.imshow('Web Camera Feed', frame)
                
                # Exit on 'q' key press
                if cv2.waitKey(1) == ord('q'):
                    break
            
            # Release resources
            cap.release()
            cv2.destroyAllWindows()
            speak("Web camera feed closed")
        else:
            speak("Could not access web camera")
            speak("Make sure a camera is connected and not being used by another application")


def access_mobile_camera(ip_address=None):
    """Access mobile camera through IP Webcam app."""
    if ip_address is None:
        speak("Please provide your phone's IP address from the IP Webcam app")
        return None
    
    # Construct the video stream URL
    base_url = f"http://{ip_address}:8080"
    video_url = urljoin(base_url, "/video")
    
    # Check if the server is reachable
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code != 200:
            speak("Could not connect to mobile camera server")
            return None
    except requests.exceptions.RequestException:
        speak("Could not connect to mobile camera server")
        return None
    
    # Create a VideoCapture object
    cap = cv2.VideoCapture(video_url)
    
    if not cap.isOpened():
        speak("Failed to open mobile camera stream")
        return None
    
    speak("Successfully connected to mobile camera")
    return cap


def handle_mobile_camera(query):
    """Handle mobile camera access requests."""
    if "access mobile camera" in query or "open mobile camera" in query:
        speak("To access your mobile camera, please follow these instructions:")
        speak("1. Install IP Webcam app on your phone")
        speak("2. Make sure your phone and computer are on the same network")
        speak("3. Start the server in IP Webcam app")
        speak("4. Provide the IP address shown in the app")
        
        # Get IP address from user
        from backend.command import takeCommand
        speak("Please provide the IP address from the IP Webcam app")
        ip_address = takeCommand()
        
        if ip_address and "http" not in ip_address:  # Simple validation
            cap = access_mobile_camera(ip_address)
            if cap is not None:
                speak("Now displaying mobile camera feed. Press Q to exit")
                
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Display the frame
                    cv2.imshow('Mobile Camera Feed', frame)
                    
                    # Exit on 'q' key press
                    if cv2.waitKey(1) == ord('q'):
                        break
                
                # Release resources
                cap.release()
                cv2.destroyAllWindows()
                speak("Mobile camera feed closed")
            else:
                speak("Failed to connect to mobile camera")
        else:
            speak("Invalid IP address format")


def get_phone_number_location(phone_number):
    """Get location information for a phone number."""
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number)
        
        # Check if the number is valid
        if not phonenumbers.is_valid_number(parsed_number):
            return {
                "valid": False,
                "error": "Invalid phone number"
            }
        
        # Get location information
        location = geocoder.description_for_number(parsed_number, "en")
        
        # Get carrier information
        carrier_name = carrier.name_for_number(parsed_number, "en")
        
        # Get timezone information
        timezones = timezone.time_zones_for_number(parsed_number)
        
        return {
            "valid": True,
            "original_number": phone_number,
            "country_code": parsed_number.country_code,
            "national_number": parsed_number.national_number,
            "location": location if location else "Unknown",
            "carrier": carrier_name if carrier_name else "Unknown",
            "timezones": list(timezones) if timezones else ["Unknown"],
            "international_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "national_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        }
    
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }


def handle_phone_number_lookup(query):
    """Handle phone number location lookup requests."""
    # Check for phone number related keywords
    phone_keywords = ["phone number location", "number location", "track phone number", "find phone number", "mobile number location"]
    for keyword in phone_keywords:
        if keyword in query:
            speak("Please provide the phone number you want to look up")
            from backend.command import takeCommand
            phone_number = takeCommand()
            
            if phone_number:
                speak(f"Looking up information for {phone_number}")
                result = get_phone_number_location(phone_number)
                
                if result["valid"]:
                    response = f"The phone number {result['international_format']} is registered in {result['location']}"
                    
                    if result["carrier"] != "Unknown":
                        response += f", and is registered to {result['carrier']} carrier"
                    
                    if result["timezones"] and result["timezones"][0] != "Unknown":
                        response += f". The timezone is {result['timezones'][0]}"
                    
                    speak(response)
                    return response
                else:
                    speak("Could not retrieve information about this phone number")
                    return "Invalid phone number"
    
    return None


def init_contacts_table():
    """Initialize the contacts table in the database"""
    conn = sqlite3.connect("jarvis.db")
    cursor = conn.cursor()
    
    # Create contacts table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            email TEXT,
            category TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def add_contact(name, phone, email=None, category="General"):
    """Add a new contact to the database"""
    try:
        conn = sqlite3.connect("jarvis.db")
        cursor = conn.cursor()
        
        # Insert the contact
        cursor.execute(
            "INSERT INTO contacts (name, phone, email, category) VALUES (?, ?, ?, ?)",
            (name, phone, email, category)
        )
        
        conn.commit()
        conn.close()
        
        speak(f"Contact {name} added successfully")
        return True
    except sqlite3.IntegrityError as e:
        speak("Phone number already exists in contacts")
        return False
    except Exception as e:
        speak("Error adding contact")
        print(f"Error adding contact: {e}")
        return False


def search_contacts(query):
    """Search contacts by name or phone number"""
    try:
        conn = sqlite3.connect("jarvis.db")
        cursor = conn.cursor()
        
        # Search for contacts (exact match first)
        cursor.execute(
            "SELECT name, phone, email FROM contacts WHERE name LIKE ? OR phone LIKE ?",
            (f"%{query}%%", f"%{query}%%")
        )
        results = cursor.fetchall()
        
        conn.close()
        
        return results
    except Exception as e:
        print(f"Error searching contacts: {e}")
        return []


def handle_contact_management(query):
    """Handle contact management commands"""
    init_contacts_table()  # Ensure table exists
    
    if "add contact" in query or "save contact" in query:
        speak("Please provide the contact name")
        name = takeCommand()
        
        if not name:
            speak("Contact name is required")
            return
        
        speak(f"Please provide the phone number for {name}")
        phone = takeCommand()
        
        if not phone:
            speak("Phone number is required")
            return
        
        speak(f"Please provide the email for {name} (optional)")
        email = takeCommand()
        
        # Add contact to database
        add_contact(name, phone, email if email and email != "None" else None)
        
    elif "search contact" in query or "find contact" in query or "call" in query or "message" in query:
        speak("Who are you looking for?")
        search_query = takeCommand()
        
        if search_query and search_query != "None":
            results = search_contacts(search_query)
            
            if results:
                speak(f"Found {len(results)} contact(s):")
                for result in results:
                    speak(f"Name: {result[0]}, Phone: {result[1]}, Email: {result[2]}")
            else:
                speak("No contacts found matching your query")
    else:
        speak("I didn't understand your contact management command")


def download_instagram_profile(username, download_path=None):
    """Download an Instagram profile using instaloader"""
    try:
        speak(f"Downloading Instagram profile for {username}")
        
        # Create instaloader instance
        L = instaloader.Instaloader()
        
        # Set download path if provided
        if download_path:
            L.dirname_pattern = download_path
        else:
            # Default download path
            default_path = os.path.join(os.getcwd(), "instagram_profiles", username)
            L.dirname_pattern = default_path
            
            # Create directory if it doesn't exist
            if not os.path.exists(default_path):
                os.makedirs(default_path)
        
        # Download profile
        L.download_profile(username, profile_pic_only=True)
        
        speak(f"Instagram profile for {username} downloaded successfully")
        return True
    except Exception as e:
        print(f"Error downloading Instagram profile: {e}")
        speak(f"Failed to download Instagram profile for {username}")
        return False


def handle_instagram_downloading(query):
    """Handle Instagram profile downloading requests from the user"""
    if "download instagram" in query or "instagram download" in query or "download profile" in query:
        speak("Please provide the Instagram username")
        username = takeCommand()
        
        if not username or username == "None":
            speak("I couldn't get the Instagram username")
            return False
        
        speak("Should I ask for a download location? (Yes/No)")
        ask_path = takeCommand().lower()
        
        download_path = None
        if "yes" in ask_path or "y" in ask_path:
            speak("Please provide the download path")
            download_path = takeCommand()
            
            if not download_path or download_path == "None":
                speak("Using default download path")
                download_path = None
        
        return download_instagram_profile(username, download_path)
    
    return False


def open_url(url):
    """Open the specified URL in the default browser"""
    try:
        # Validate URL format
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        # Open the URL in the default browser
        webbrowser.open(url)
        
        # Speak confirmation
        speak(f"Opening {url}")
        
        return True
    except Exception as e:
        print(f"Error opening URL: {e}")
        speak("Failed to open URL")
        return False


def browser_search(query):
    """Perform a web search using the default browser"""
    try:
        # Format the search query
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        # Open the search results in the default browser
        webbrowser.open(search_url)
        
        # Speak confirmation
        speak(f"I've opened your default browser with search results for: {query}")
        
        return True
    except Exception as e:
        print(f"Error opening browser: {e}")
        speak("Failed to open browser")


def open_account(account_type):
    """Open the specified account type in the default browser"""
    try:
        # Dictionary mapping account types to URLs
        account_urls = {
            "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "instagram": "https://www.instagram.com",
            "linkedin": "https://www.linkedin.com",
            "github": "https://www.github.com",
            "gitlab": "https://www.gitlab.com",
            "stackoverflow": "https://www.stackoverflow.com",
            "reddit": "https://www.reddit.com",
            "youtube": "https://www.youtube.com",
            "whatsapp": "https://web.whatsapp.com",
            "telegram": "https://web.telegram.org",
            "gmail": "https://mail.google.com",
            "outlook": "https://outlook.live.com",
            "amazon": "https://www.amazon.com",
            "netflix": "https://www.netflix.com",
            "spotify": "https://open.spotify.com",
            # Adding more account types
            "zoom": "https://zoom.us/signin",
            "microsoft teams": "https://teams.microsoft.com",
            "google meet": "https://meet.google.com",
            "discord": "https://discord.com/app",
            "prime video": "https://www.amazon.com/Amazon-Video/b?node=2858747011",
            "hotstar": "https://www.hotstar.com/us/login",
            "hulu": "https://www.hulu.com/login",
            "disney plus": "https://www.disneyplus.com/login",
            "google drive": "https://drive.google.com",
            "google docs": "https://docs.google.com",
            "google sheets": "https://sheets.google.com",
            "google slides": "https://slides.google.com",
            "powerpoint": "https://www.office.com/launch/powerpoint?auth=2",
            "word": "https://www.office.com/launch/word?auth=2",
            "excel": "https://www.office.com/launch/excel?auth=2",
            "amazon prime": "https://www.amazon.com/prime",
            "flipkart": "https://www.flipkart.com",
            "ebay": "https://www.ebay.com",
            "aliexpress": "https://www.aliexpress.com",
            "walmart": "https://www.walmart.com",
            "target": "https://www.target.com"
        }
        
        # Convert account type to lowercase for case-insensitive matching
        account_type = account_type.lower()
        
        # Check if the account type is in our dictionary
        if account_type in account_urls:
            webbrowser.open(account_urls[account_type])
            speak(f"Opening {account_type} account")
            return True
        else:
            speak(f"I don't recognize that account type: {account_type}")
            return False
    except Exception as e:
        print(f"Error opening account: {e}")
        speak("Failed to open account")
        return False


def open_application(app_name):
    """Open a PC application by name"""
    try:
        # Common applications and their executable names
        app_executables = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "vlc": "vlc.exe",
            "steam": "steam.exe",
            "discord": "discord.exe"
        }
        
        # Convert app name to lowercase for case-insensitive matching
        app_name = app_name.lower()
        
        # Check if the application is in our dictionary
        if app_name in app_executables:
            subprocess.Popen(app_executables[app_name])
            speak(f"Opening {app_name}")
            return True
        else:
            # Try to find the application in system processes
            for proc in psutil.process_iter(['name']):
                if app_name in proc.info['name'].lower():
                    subprocess.Popen(proc.info['name'])
                    speak(f"Opening {proc.info['name']}")
                    return True
            
            speak(f"I don't recognize that application: {app_name}")
            return False
    except Exception as e:
        print(f"Error opening application: {e}")
        speak("Failed to open application")
        return False

def close_application(app_name):
    """Close a running PC application by name"""
    try:
        # Convert app name to lowercase for case-insensitive matching
        app_name = app_name.lower()
        
        # Iterate through all running processes
        for proc in psutil.process_iter(['name', 'pid']):
            if app_name in proc.info['name'].lower():
                # Terminate the process
                process = psutil.Process(proc.info['pid'])
                process.terminate()
                speak(f"Closing {proc.info['name']}")
                return True
        
        speak(f"Could not find running application: {app_name}")
        return False
    except Exception as e:
        print(f"Error closing application: {e}")
        speak("Failed to close application")
        return False

def system_shutdown(delay=0):
    """Shut down the system after the specified delay (seconds)"""
    try:
        if delay > 0:
            speak(f"System will shut down in {delay} seconds")
            time.sleep(delay)
        
        speak("Shutting down the system now")
        os.system("shutdown /s /t 1")
        return True
    except Exception as e:
        print(f"Error shutting down system: {e}")
        speak("Failed to shut down system")
        return False

def system_restart(delay=0):
    """Restart the system after the specified delay (seconds)"""
    try:
        if delay > 0:
            speak(f"System will restart in {delay} seconds")
            time.sleep(delay)
        
        speak("Restarting the system now")
        os.system("shutdown /r /t 1")
        return True
    except Exception as e:
        print(f"Error restarting system: {e}")
        speak("Failed to restart system")
        return False

def system_sleep():
    """Put the system to sleep"""
    try:
        speak("Putting the system to sleep")
        os.system("rundll32.exe powrprof.dll, SetSuspendState Sleep")
        return True
    except Exception as e:
        print(f"Error putting system to sleep: {e}")
        speak("Failed to put system to sleep")
        return False

def play_music(directory=None):
    """Play a random music file from the specified directory"""
    try:
        # If no directory specified, use default music directory
        if directory is None:
            directory = os.path.expanduser("~/Music")
        
        # Get list of music files
        music_files = [f for f in os.listdir(directory) if f.endswith((".mp3", ".wav", ".ogg"))]
        
        if not music_files:
            speak("No music files found in the directory")
            return False
        
        # Select a random music file
        selected_file = os.path.join(directory, music_files[0])  # For simplicity, just pick the first file
        
        # Play the music
        speak(f"Playing {music_files[0]}")
        os.startfile(selected_file)  # This works on Windows
        return True
    except Exception as e:
        print(f"Error playing music: {e}")
        speak("Failed to play music")
        return False


def handle_contact_management(query):
    """Handle contact management operations"""
    if "add contact" in query:
        # Extract name from query
        name = query.replace("add contact", "").strip()
        
        if not name:
            speak("What is the contact's name?")
            name = takeCommand()
        
        if name and name != "None":
            speak("What is the phone number?")
            phone = takeCommand()
            
            if phone and phone != "None":
                speak("What is the email address? (optional)")
                email = takeCommand()
                
                if email and email == "None":
                    email = ""
                
                # Add contact to database
                result = add_contact(name, phone, email, "General")
                if result:
                    speak(f"Contact {name} added successfully")
                else:
                    speak("Failed to add contact")
            else:
                speak("Phone number is required")
        else:
            speak("Contact name is required")
    
    elif "search contact" in query or "find contact" in query:
        # Extract search term from query
        search_query = query.replace("search contact", "").replace("find contact", "").strip()
        
        if not search_query:
            speak("Who are you looking for?")
            search_query = takeCommand()
        
        if search_query and search_query != "None":
            results = search_contacts(search_query)
            
            if results:
                speak(f"Found {len(results)} contact(s) matching {search_query}")
                
                for i, (name, phone, email) in enumerate(results, 1):
                    print(f"{i}. {name}: {phone} (Email: {email if email else 'No email'})")
                    speak(f"{i}. {name}: {phone}")
                
                speak("Which contact would you like to delete? Please say the number")
                choice = takeCommand()
                
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(results):
                        name, _, _ = results[choice_idx]
                        
                        # Delete contact
                        conn = sqlite3.connect("jarvis.db")
                        cursor = conn.cursor()
                        cursor.execute(
                            "DELETE FROM contacts WHERE name = ?",
                            (name,)
                        )
                        conn.commit()
                        conn.close()
                        speak(f"Contact {name} deleted successfully")
                    else:
                        speak("Invalid contact number")
                except ValueError:
                    speak("Please provide a valid number")
    
    elif "list all contacts" in query or "show all contacts" in query:
        try:
            conn = sqlite3.connect("jarvis.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name, phone, email FROM contacts ORDER BY name")
            results = cursor.fetchall()
            conn.close()
            
            if results:
                speak(f"Found {len(results)} contacts")
                
                for i, (name, phone, email) in enumerate(results, 1):
                    print(f"{i}. {name}: {phone} (Email: {email if email else 'No email'})")
                    speak(f"{i}. {name}: {phone}")
            else:
                speak("Your contact list is empty")
        except Exception as e:
            speak("Error retrieving contacts")
            print(f"Error retrieving contacts: {e}")

    else:
        speak("Contact management options: add, search, delete, or list all contacts")


def generate_qr_code(data, file_name=None, size=300):
    """Generate a QR code from the provided data"""
    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data to QR code
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Generate file name if not provided
        if file_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"qr_code_{timestamp}.png"
        
        # Save QR code
        img.save(file_name)
        
        speak(f"QR code generated and saved as {file_name}")
        return file_name
    except Exception as e:
        speak("Error generating QR code")
        print(f"Error generating QR code: {e}")
        return None


def handle_qr_code_generation(query):
    """Handle QR code generation requests"""
    if "generate qr code" in query or "create qr code" in query or "make qr code" in query:
        speak("What data should I encode in the QR code?")
        data = takeCommand()
        
        if data and data != "None":
            speak("Please provide a custom file name for the QR code (optional)")
            file_name = takeCommand()
            
            # If no file name provided, use default
            if not file_name or file_name == "None":
                file_name = None
            else:
                # Ensure file name ends with .png
                if not file_name.lower().endswith(".png"):
                    file_name += ".png"
            
            speak("Generating QR code...")
            result = generate_qr_code(data, file_name)
            
            if result:
                speak(f"QR code successfully generated and saved as {result}")
                
                # Ask if user wants to display the QR code
                speak("Would you like me to display the QR code?")
                response = takeCommand().lower()
                
                if "yes" in response or "display" in response:
                    try:
                        from PIL import Image
                        img = Image.open(result)
                        img.show()
                    except Exception as e:
                        speak("Error displaying QR code")
# Calendar Integration Functions
def get_calendar_service():
    """Get authenticated Google Calendar service instance"""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import googleapiclient.discovery
        import pickle
        
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        
        # Check for existing credentials
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, perform authentication
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Require credentials.json file
                if not os.path.exists('credentials.json'):
                    speak("Google Calendar credentials file not found. Please set up Google Calendar API.")
                    return None
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    except ImportError:
        speak("Google Calendar API libraries not installed.")
        return None
    except Exception as e:
        print(f"Error setting up calendar service: {e}")
        speak("Error setting up Google Calendar service.")
        return None


def add_calendar_event(title, description, start_time, end_time):
    """Add an event to Google Calendar"""
    try:
        service = get_calendar_service()
        if not service:
            return None
            
        # Convert datetime to RFC 3339 format
        start = start_time.isoformat()
        end = end_time.isoformat()
        
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end,
                'timeZone': 'UTC',
            },
        }
        
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        speak(f"Event '{title}' created successfully")
        return created_event.get('id')
    except Exception as e:
        print(f"Error adding calendar event: {e}")
        speak("Sorry, I couldn't add the event to your calendar.")
        return None


def get_upcoming_events(max_results=5):
    """Get upcoming Google Calendar events"""
    try:
        service = get_calendar_service()
        if not service:
            return None
            
        # Get current time and time 7 days from now
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        one_week_later = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=one_week_later,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime').execute()
        
        events = events_result.get('items', [])
        
        if not events:
            speak('No upcoming events found.')
            return []
        
        # Speak out the events
        speak(f'Here are your next {len(events)} events:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"{event['summary']} - {start}")
            speak(f"{event['summary']} on {start}")
        
        return events
    except Exception as e:
        print(f"Error getting calendar events: {e}")
        speak("Sorry, I couldn't retrieve your calendar events.")
        return None


def remove_calendar_event(event_id):
    """Remove an event from Google Calendar"""
    try:
        service = get_calendar_service()
        if not service:
            return False
            
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        speak("Event successfully removed from your calendar.")
        return True
    except Exception as e:
        print(f"Error removing calendar event: {e}")
        speak("Sorry, I couldn't remove the event from your calendar.")
        return False


def handle_qr_code_generation(query):
    """Handle QR code generation requests"""
    if "generate qr code" in query or "qr code" in query:
        speak("What data should I encode in the QR code?")
        data = takeCommand()
        
        if data:
            try:
                # Generate QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)
                
                # Create an image from the QR Code instance
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Save the image to a file
                img.save("qr_code.png")
                
                # Display the image
                img.show()
                
                result = "QR code generated and displayed successfully"
                speak(result)
            except Exception as e:
                print(f"Error generating QR code: {e}")
                speak("Failed to generate QR code")
                result = "Failed to generate QR code"
            try:
                # Display the image using PIL
                img.show()
            except Exception as e:
                print(f"Error displaying QR code: {e}")
                
                return result
            else:
                speak("Failed to generate QR code")
                return None
        else:
            speak("No data provided for the QR code")
            return None


def handle_qr_code_request(query):
    """Handle all QR code related requests"""
    return handle_qr_code_generation(query)


def send_gmail(subject, body, to_email):
    """Send an email using Gmail's SMTP server"""
    # Your Gmail credentials
    from backend.config import GMAIL_USER, GMAIL_APP_PASSWORD
    
    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = GMAIL_USER
    message['To'] = to_email
    message['Subject'] = subject
    
    # Attach the body
    message.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        
        # Send the email
        text = message.as_string()
        server.sendmail(GMAIL_USER, to_email, text)
        
        server.quit()
        speak("Email sent successfully")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        speak("Failed to send email")
        return False


def handle_gmail_sending(query):
    """Handle Gmail sending requests from the user"""
    if "send email" in query or "send gmail" in query or "email" in query:
        speak("What should I put in the email?")
        body = takeCommand()
        
        if not body:
            speak("I couldn't get the email content")
            return False
        
        speak("Who should I send this email to?")
        to_email = takeCommand()
        
        if not to_email:
            speak("I couldn't get the recipient's email")
            return False
        
        # Get the subject from the body
        # Take the first line as the subject
        subject = body.split("\n", 1)[0] if "\n" in body else "No subject"
        
        # Send the email
        return send_gmail(subject, body, to_email)
    
    return False


def send_whatsapp_message(phone_number, message):
    """Send a WhatsApp message to the specified phone number"""
    try:
        # Set up the Selenium driver
        driver = webdriver.Chrome()
        
        # Open WhatsApp Web
        driver.get(f"https://web.whatsapp.com/send?phone={phone_number}&text={message}")
        
        # Wait for WhatsApp Web to load
        wait = WebDriverWait(driver, 30)
        chat_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")))
        
        # Wait for the message to be sent
        time.sleep(5)
        
        # Press enter to send the message
        chat_box.send_keys(Keys.ENTER)
        
        # Wait for the message to be delivered
        time.sleep(5)
        
        # Close the driver
        driver.quit()
        
        speak("WhatsApp message sent successfully")
        return True
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        speak("Failed to send WhatsApp message")
        return False


def handle_whatsapp_messaging(query):
    """Handle WhatsApp messaging requests from the user"""
    if "send whatsapp" in query or "send whatsapp message" in query or "whatsapp" in query:
        speak("What message should I send via WhatsApp?")
        message = takeCommand()
        
        if not message:
            speak("I couldn't get the message content")
            return False
        
        speak("What's the phone number to send this message to?")
        phone_number = takeCommand()
        
        if not phone_number:
            speak("I couldn't get the phone number")
            return False
        
        # Format the phone number
        # Remove any non-digit characters
        phone_number = "+" + "".join(filter(str.isdigit, phone_number))
        
        # Send the WhatsApp message
        return send_whatsapp_message(phone_number, message)
    
    return False


def play_youtube_song(song_name):
    """Play a YouTube song using pywhatkit"""
    try:
        speak(f"Playing {song_name} on YouTube")
        
        # Use pywhatkit to play the YouTube video
        kit.playonyt(song_name)
        
        # Add a delay to allow the video to start
        time.sleep(5)
        
        return True
    except Exception as e:
        print(f"Error playing YouTube song: {e}")
        speak("Failed to play YouTube song")
        return False


def handle_youtube_playing(query):
    """Handle YouTube song playing requests from the user"""
    if "play youtube" in query or "play song" in query or "youtube" in query:
        speak("What song should I play on YouTube?")
        song_name = takeCommand()
        
        if not song_name or song_name == "None":
            speak("I couldn't get the song name")
            return False
        
        return play_youtube_song(song_name)
    
    return False


def run_speed_test():
    """Run a speed test and return the results"""
    try:
        speak("Running internet speed test. This may take a few seconds...")
        results = speedtest.Speedtest()
        results.download()
        results.upload()
        download_speed = results.download() / 1_000_000
        upload_speed = results.upload() / 1_000_000
        speak(f"Download speed: {download_speed:.2f} Mbps")
        speak(f"Upload speed: {upload_speed:.2f} Mbps")
        return True
    except Exception as e:
        print(f"Error running speed test: {e}")
        speak("Failed to run speed test")
        return False


def set_system_volume(level):
    """Set the system volume to the specified level (0-100)"""
    try:
        if volume is None:
            print("Volume control not available (pycaw not installed)")
            speak(f"Cannot set volume to {level}% - audio library not available")
            return False
            
        # Convert level to float between 0.0 and 1.0
        volume_level = level / 100.0
        # Set the system volume
        volume.SetMasterVolumeLevelScalar(volume_level, None)
        speak(f"Volume set to {level}%")
        return True
    except Exception as e:
        print(f"Error setting volume: {e}")
        speak("Failed to set volume")
        return False


def sleep_until_wake():
    """Put the system to sleep until a wake-up command is received"""
    try:
        speak("Entering sleep mode. I'll wait until you say 'wake up' to resume")
        
        # Import speech recognition here to avoid circular imports
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("Sleep mode activated. Say 'wake up' to resume...")
        
        # Listen for wake-up command
        while True:
            try:
                with microphone as source:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
                try:
                    text = recognizer.recognize_google(audio).lower()
                    print(f"Heard: {text}")
                    
                    if "wake up" in text:
                        speak("I'm awake and ready to assist you!")
                        return True
                except sr.UnknownValueError:
                    # Speech not understood, continue listening
                    pass
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    # If we can't reach Google, just check every few seconds
                    time.sleep(2)
            except Exception as e:
                print(f"Error listening: {e}")
                time.sleep(2)
    except Exception as e:
        print(f"Error in sleep_until_wake: {e}")
        speak("Sorry, I couldn't enter sleep mode.")
        return False
            # In a real implementation, you would use your speech recognition system
            # to detect the "wake up" command
            # 
            # For demonstration purposes, we'll just exit after 30 seconds
            # speak("Wake up command detected")
            # break
            # 
            # For now, we'll just demonstrate the sleep functionality
            # and exit after 30 seconds
        # Remove this test condition in the real implementation
        # The break statement was removed as it was outside any loop
        return True
    except Exception as e:
        print(f"Error in sleep mode: {e}")
        speak("Error in sleep mode")
        return False
        
        # Set volume for each session
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume.SetMasterVolume(volume_level, None)
        
        # Speak confirmation
        speak(f"System volume set to {level}%")
        
        return True
    except Exception as e:
        print(f"Error setting system volume: {e}")
        speak("Failed to set system volume")
        return False

        
        # Create a speedtest instance
        st = speedtest.Speedtest()
        
        # Get server list
        speak("Finding the best server for testing")
        st.get_best_server()
        
        # Test download speed
        speak("Testing download speed")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        # Test upload speed
        speak("Testing upload speed")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        
        # Get ping
        ping = st.results.ping
        
        # Get client info
        client = st.get_config()['client']
        client_ip = client['ip']
        client_country = client['country']
        
        # Get server info
        server = st.results.server
        server_location = server['name']
        server_country = server['country']
        server_ping = server['latency']
        
        result = {
            "download_speed": round(download_speed, 2),
            "upload_speed": round(upload_speed, 2),
            "ping": round(ping, 2),
            "client_ip": client_ip,
            "client_country": client_country,
            "server_location": server_location,
            "server_country": server_country,
            "server_ping": round(server_ping, 2)
        }
        
        # Generate a verbal report
        report = f"Your internet speed test results: Download speed is {result['download_speed']} Mbps, Upload speed is {result['upload_speed']} Mbps, and Ping is {result['ping']} ms."
        
        speak(report)
        
        return result
    except Exception as e:
        speak("Error running speed test")
        print(f"Error in speed test: {e}")
        return None


def handle_speed_test(query):
    """Handle internet speed test requests"""
    if "internet speed" in query or "network speed" in query or "speed test" in query:
        # Run speed test in a separate thread to avoid blocking
        def run_test():
            result = run_speed_test()
            if result:
                print(f"Download: {result['download_speed']} Mbps")
                print(f"Upload: {result['upload_speed']} Mbps")
                print(f"Ping: {result['ping']} ms")
                print(f"Server: {result['server_location']}, {result['server_country']}")
                print(f"Client IP: {result['client_ip']}, Country: {result['client_country']}")
        
        # Start the speed test in a background thread
        test_thread = threading.Thread(target=run_test)
        test_thread.start()
        
        return True
    return False


def get_ip_info():
    """Get public IP address information from an API"""
    try:
        # Use ip-api.com API for IP information
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        
        if data['status'] == 'success':
            # Format the IP information
            result = {
                'ip': data['query'],
                'country': data['country'],
                'region': data['regionName'],
                'city': data['city'],
                'zip': data['zip'],
                'lat': data['lat'],
                'lon': data['lon'],
                'timezone': data['timezone'],
                'isp': data['isp'],
                'org': data['org'],
                'as': data['as'],
                'asname': data['asname'],
                'mobile': data['mobile'],
                'proxy': data['proxy'],
                'hosting': data['hosting']
            }
            
            # Generate verbal response
            ip_message = f"Your public IP address is {data['query']}, located in {data['city']}, {data['regionName']}, {data['country']}"
            ip_message += f". Latitude: {data['lat']}, Longitude: {data['lon']}, ZIP code: {data['zip']}"
            ip_message += f". ISP: {data['isp']}, Organization: {data['org']}, AS: {data['as']} ({data['asname']})"
            ip_message += f". Mobile: {'Yes' if data['mobile'] else 'No'}, Proxy: {'Yes' if data['proxy'] else 'No'}, Hosting: {'Yes' if data['hosting'] else 'No'}"
            
            speak(ip_message)
            return result
        else:
            speak("Failed to retrieve IP information")
            return None
    except Exception as e:
        speak("Error retrieving IP information")
        print(f"Error in get_ip_info: {e}")
        return None


def handle_ip_lookup(query):
    """Handle IP address lookup requests"""
    if "ip address" in query or "my ip" in query or "ip info" in query or "public ip" in query:
        speak("Getting your IP address information")
        return get_ip_info()
    return None


def get_system_info():
    """Get comprehensive system information"""
    try:
        # Get basic system info
        system_info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "platform": platform.platform(),
            "boot_time": datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Get CPU info
        system_info["cpu_count"] = psutil.cpu_count()
        system_info["cpu_percent"] = psutil.cpu_percent(interval=1)
        system_info["cpu_times"] = psutil.cpu_times()._asdict()
        
        # Get memory info
        system_info["virtual_memory"] = psutil.virtual_memory()._asdict()
        system_info["swap_memory"] = psutil.swap_memory()._asdict()
        
        # Get disk info
        system_info["disk_usage"] = {}
        for i, partition in enumerate(psutil.disk_partitions()):
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                system_info["disk_usage"][partition.device] = {
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "mountpoint": partition.mountpoint,
                }
            except PermissionError:
                # This can be caught due to the disk that isn't ready
                continue
        
        # Get network info
        system_info["net_io"] = psutil.net_io_counters()._asdict()
        
        # Get sensors info
        system_info["sensors_temperatures"] = psutil.sensors_temperatures()
        system_info["sensors_fans"] = psutil.sensors_fans()
        system_info["sensors_battery"] = psutil.sensors_battery()
        
        return system_info
    except Exception as e:
        speak("Error retrieving system information")
        print(f"Error in get_system_info: {e}")
        return None


def handle_system_info(query):
    """Handle system information requests"""
    if "system info" in query or "system information" in query or "sys info" in query:
        speak("Getting system information")
        system_info = get_system_info()
        
        if system_info:
            # Generate verbal response
            info_message = f"System: {system_info['system']} {system_info['release']} {system_info['version']}"
            info_message += f". Machine: {system_info['machine']}, Processor: {system_info['processor']}"
            info_message += f". Boot time: {system_info['boot_time']}"
            info_message += f". CPU: {system_info['cpu_count']} cores, {system_info['cpu_percent']}% usage"
            info_message += f". Memory: {system_info['virtual_memory']['total'] / (1024 ** 3):.2f} GB total, {system_info['virtual_memory']['used'] / (1024 ** 3):.2f} GB used, {system_info['virtual_memory']['free'] / (1024 ** 3):.2f} GB free"
            info_message += f". Swap: {system_info['swap_memory']['total'] / (1024 ** 3):.2f} GB total, {system_info['swap_memory']['used'] / (1024 ** 3):.2f} GB used, {system_info['swap_memory']['free'] / (1024 ** 3):.2f} GB free"
            info_message += f". Disk: {system_info['disk_usage']}"
            info_message += f". Network: {system_info['net_io']}"
            info_message += f". Sensors: {system_info['sensors_temperatures']}, {system_info['sensors_fans']}, {system_info['sensors_battery']}"
            
            speak(info_message)
            return system_info
        else:
            speak("Failed to retrieve system information")
            return None
    
    return None


def get_current_location():
    """Get the current location based on IP geolocation"""
    try:
        # Use ip-api.com API for location
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        
        if data['status'] == 'success':
            # Format the location information
            result = {
                'city': data['city'],
                'region': data['regionName'],
                'country': data['country'],
                'lat': data['lat'],
                'lon': data['lon'],
                'query': data['query'],
                'timezone': data['timezone'],
                'zip': data['zip'],
                'org': data['org']
            }
            
            # Generate verbal response
            location_message = f"You are currently in {data['city']}, {data['regionName']}, {data['country']}"
            location_message += f". Latitude: {data['lat']}, Longitude: {data['lon']}, ZIP code: {data['zip']}"
            location_message += f". Your public IP address is {data['query']} and you are in the {data['timezone']} timezone"
            
            speak(location_message)
            return result
        else:
            speak("Failed to retrieve location information")
            return None
    except Exception as e:
        print(f"Error getting current location: {e}")
        speak("Error retrieving current location")
        return None


def handle_location_lookup(query):
    """Handle current location lookup requests"""
    if "current location" in query or "where am i" in query or "my location" in query:
        speak("Getting your current location information")
        return get_current_location()
    
    return None


def get_programming_joke():
    """Get a random programming joke"""
    try:
        # Get a random programming joke
        joke = pyjokes.get_joke()
        
        # Generate verbal response
        speak(joke)
        
        return joke
    except Exception as e:
        print(f"Error getting programming joke: {e}")
        speak("Failed to get a programming joke")
        return None


def handle_programming_joke(query):
    """Handle programming joke requests from the user"""
    if "joke" in query or "tell me a joke" in query or "programming joke" in query:
        return get_programming_joke()
    
    return None


def get_disk_usage():
    """Get disk usage information"""
    try:
        # Get disk usage information
        partitions = psutil.disk_partitions()
        disk_usage_info = []
        
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage_info.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        
        # Generate verbal response
        usage_message = "Disk usage information:\n"
        for info in disk_usage_info:
            usage_message += f"Device: {info['device']}, Mountpoint: {info['mountpoint']}, Filesystem: {info['fstype']}\n"
            usage_message += f"Total: {info['total']} bytes, Used: {info['used']} bytes, Free: {info['free']} bytes, Percent: {info['percent']}%\n"
        
        speak(usage_message)
        return disk_usage_info
    except Exception as e:
        print(f"Error getting disk usage information: {e}")
        speak("Error retrieving disk usage information")
        return None


def handle_disk_usage(query):
    """Handle disk usage information requests"""
    if "disk usage" in query or "disk space" in query or "storage" in query:
        speak("Getting disk usage information")
        return get_disk_usage()
    
    return None


def get_system_info():
    """Get comprehensive system information"""
    try:
        system_info = {}
        
        # Basic system info
        system_info["system"] = platform.system()
        system_info["node"] = platform.node()
        system_info["release"] = platform.release()
        system_info["version"] = platform.version()
        system_info["machine"] = platform.machine()
        system_info["processor"] = platform.processor()
        
        # Boot time
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        system_info["boot_time"] = boot_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # CPU info
        system_info["cpu_count"] = psutil.cpu_count(logical=True)
        system_info["cpu_percent"] = psutil.cpu_percent()
        system_info["cpu_times"] = psutil.cpu_times()._asdict()
        
        # Memory info
        system_info["virtual_memory"] = psutil.virtual_memory()._asdict()
        system_info["swap_memory"] = psutil.swap_memory()._asdict()
        
        # Disk info
        disk_usage = {}
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.device] = {
                    "total": partition_usage.total,
                    "used": partition_usage.used,
                    "free": partition_usage.free,
                    "percent": (partition_usage.used / partition_usage.total) * 100,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "opts": partition.opts
                }
            except PermissionError:
                # This can happen for removable drives
                continue
        
        system_info["disk_usage"] = disk_usage
        
        # Get network info
        system_info["net_io"] = psutil.net_io_counters()._asdict()
        system_info["net_connections"] = len(psutil.net_connections())
        
        # Get battery info
        battery = psutil.sensors_battery()
        if battery:
            system_info["battery"] = battery._asdict()
        
        return system_info
    except Exception as e:
        print(f"Error getting system info: {e}")
        return None


def get_condition_report():
    """Generate a user-friendly system condition report"""
    system_info = get_system_info()
    if system_info:
        report = f"System Condition Report\n"
        report += f"System: {system_info['system']} {system_info['release']}\n"
        report += f"Boot Time: {system_info['boot_time']}\n\n"
        
        # CPU Report
        report += f"CPU Information\n"
        report += f"CPU Count: {system_info['cpu_count']}\n"
        report += f"CPU Percent: {system_info['cpu_percent']}%\n"
        report += f"CPU Times: {system_info['cpu_times']['user']}s user, {system_info['cpu_times']['system']}s system, {system_info['cpu_times']['idle']}s idle\n\n"
        
        # Memory Report
        report += "Memory Information\n"
        total_memory = system_info['virtual_memory']['total'] / (1024**3)
        available_memory = system_info['virtual_memory']['available'] / (1024**3)
        used_memory = system_info['virtual_memory']['used'] / (1024**3)
        free_memory = system_info['virtual_memory']['free'] / (1024**3)
        
        report += f"Total: {total_memory:.2f} GB\n"
        report += f"Available: {available_memory:.2f} GB\n"
        report += f"Used: {used_memory:.2f} GB\n"
        report += f"Free: {free_memory:.2f} GB\n\n"
        
        # Disk Report
        report += "Disk Information\n"
        for device, usage in system_info["disk_usage"].items():
            total_disk = usage['total'] / (1024**3)
            used_disk = usage['used'] / (1024**3)
            free_disk = usage['free'] / (1024**3)
            report += f"{device}: {total_disk:.2f} GB total, {used_disk:.2f} GB used, {free_disk:.2f} GB free\n"
            report += f"Mountpoint: {usage['mountpoint']}, FSType: {usage['fstype']}, Opts: {usage['opts']}\n\n"
        
        # Network Report
        net_io = system_info["net_io"]
        report += "Network Information\n"
        bytes_sent = net_io['bytes_sent'] / (1024**2)
        bytes_recv = net_io['bytes_recv'] / (1024**2)
        report += f"Bytes Sent: {bytes_sent:.2f} MB\n"
        report += f"Bytes Received: {bytes_recv:.2f} MB\n"
        report += f"Packets Sent: {net_io['packets_sent']}\n"
        report += f"Packets Received: {net_io['packets_recv']}\n\n"
        
        # Battery Report
        if "battery" in system_info:
            battery = system_info["battery"]
            report += f"Battery Information\n"
            report += f"Battery Percent: {battery['percent']}%\n"
            report += f"Power Plugged: {'Yes' if battery['power_plugged'] else 'No'}\n"
            report += f"Seconds Left: {battery['secsleft'] if battery['secsleft'] != -1 else 'N/A'}\n\n"
        
        # Temperature Information
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                report += f"Temperature Information\n"
                for name, entries in temps.items():
                    for i, entry in enumerate(entries):
                        report += f"{name} {i}: {entry.current}°C\n"
        
        return report
    else:
        return "Failed to retrieve system information"


def handle_system_monitoring(query):
    """Handle system monitoring requests from the user"""
    if "system condition" in query or "system info" in query or "system status" in query or "system monitoring" in query:
        speak("Getting system condition report. This may take a moment...")
        
        # Get the system report
        report = get_condition_report()
        
        if report:
            # Print the full report
            print(report)
            
            # Speak the report in chunks to avoid overwhelming
            # Split by paragraphs and speak each one
            for paragraph in report.split("\n\n"):
                # Remove any leading/trailing whitespace and newlines
                paragraph = paragraph.strip()
                if paragraph:  # Skip empty paragraphs
                    speak(paragraph)
                    # Pause between sections
                    time.sleep(3)
            
            # Save the report to a file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"system_condition_report_{timestamp}.txt"
            
            with open(filename, "w") as f:
                f.write(report)
                
            speak(f"System condition report saved to {filename}")
            return filename
        else:
            speak("Failed to retrieve system condition")
            return None