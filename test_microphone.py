#!/usr/bin/env python3

import sys
import os
import speech_recognition as sr

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_microphone():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    print("🎤 Testing microphone and wake word detection...")
    print("📢 Say 'Hey Jarvis' clearly and wait for response...")
    print("🔄 Press Ctrl+C to exit\n")
    
    # Improve recognition sensitivity
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    
    # Adjust for ambient noise
    with microphone as source:
        print("🔧 Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
    
    print("✅ Ready! Say 'Hey Jarvis' now...")
    
    while True:
        try:
            with microphone as source:
                # Listen for audio with flexible timing
                audio = recognizer.listen(source, timeout=0.5, phrase_time_limit=4)
            
            try:
                text = recognizer.recognize_google(audio, language='en-US').lower()
                print(f"🎯 Heard: '{text}'")
                
                # Check for wake words
                wake_words = ["hey jarvis", "jarvis", "hey alexa", "alexa"]
                detected = False
                
                for wake_word in wake_words:
                    if wake_word in text:
                        detected = True
                        break
                
                # Also check for partial matches
                if not detected:
                    if "hey" in text and ("jar" in text or "jav" in text):
                        detected = True
                    elif "jarvis" in text or "alexa" in text:
                        detected = True
                
                if detected:
                    print("🎉 ✅ WAKE WORD DETECTED! This would trigger Jarvis!")
                    print("💡 The wake word system is working correctly!")
                    print("🔄 Continuing to listen...")
                        
            except sr.UnknownValueError:
                # No speech recognized, show a dot to indicate it's listening
                print(".", end="", flush=True)
                
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
                
        except sr.WaitTimeoutError:
            # No speech detected, show listening indicator
            print(".", end="", flush=True)
            
        except KeyboardInterrupt:
            print("\n\n👋 Test stopped by user.")
            break
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_microphone()