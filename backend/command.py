import time
import pyttsx3
import speech_recognition as sr
import eel
import re
from datetime import datetime, timedelta
import random

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices)
    
    # Choose voice safely - use index 2 if available, otherwise use the last available voice
    if len(voices) > 2:
        engine.setProperty('voice', voices[2].id)
    elif len(voices) > 0:
        engine.setProperty('voice', voices[-1].id)  # Use the last available voice
    # If no voices available, continue with default
    
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 174)
    eel.receiverText(text)

# Expose the Python function to JavaScript

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...")
        eel.DisplayMessage("I'm listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 8)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        
        
        speak(query)
    except Exception as e:
        print(f"Error: {str(e)}\n")
        return None

    return query.lower()



@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()  # If no message is passed, listen for voice input
        if not query:
            return  # Exit if no query is received
        print(query)
        eel.senderText(query)
    else:
        query = message  # If there's a message, use it
        print(f"Message received: {query}")
        eel.senderText(query)
    
    try:
        if query:
            # Calendar management commands
            if any(keyword in query for keyword in ["schedule", "calendar", "event"]):
                from backend.feature import add_calendar_event, get_upcoming_events
                
                if "add" in query or "create" in query:
                    # Extract event details from query
                    # This is a simplified implementation
                    title = "Meeting"
                    description = "Scheduled meeting"
                    
                    # Default to tomorrow at 3 PM
                    start_time = datetime.now() + timedelta(days=1)
                    start_time = start_time.replace(hour=15, minute=0, second=0, microsecond=0)
                    end_time = start_time + timedelta(hours=1)
                    
                    add_calendar_event(title, description, start_time, end_time)
                elif "upcoming" in query or "next" in query:
                    get_upcoming_events()
                else:
                    speak("Would you like to add an event or check your upcoming events?")
            
            # Silence mode commands
            elif "silence" in query or "quiet" in query:
                from backend.feature import set_silence_mode
                
                if "cancel" in query or "deactivate" in query:
                    # Deactivate silence mode
                    set_silence_mode(0)
                else:
                    # Activate silence mode
                    # Try to extract duration from query
                    duration = 0
                    time_match = re.search(r"\d+", query)
                    if time_match:
                        duration = int(time_match.group())
                    
                    set_silence_mode(duration)
            
            # Application control commands
            elif "open" in query:
                from backend.feature import open_application
                # Extract application name from query
                app_name = query.replace("open", "").strip()
                if app_name:
                    open_application(app_name)
            
            elif "close" in query or "quit" in query or "exit" in query:
                from backend.feature import close_application
                # Extract application name from query
                app_name = query.replace("close", "").replace("quit", "").replace("exit", "").strip()
                if app_name:
                    close_application(app_name)
            
            # Sleep/wake command
            elif "sleep" in query or "sleep until wake up" in query or "sleep until you say wake up" in query:
                from backend.feature import sleep_until_wake
                speak("Entering sleep mode. Say 'wake up' to resume.")
                sleep_until_wake()
            
            # Screen and voice recording
            elif any(keyword in query for keyword in ["screen recording", "record screen", "capture screen"]):
                from backend.feature import screen_recording
                screen_recording()
            
            # Voice recording
            elif any(keyword in query for keyword in ["voice recording", "record voice", "record audio"]):
                from backend.feature import voice_recording
                voice_recording()
            
            # Camera access
            elif any(keyword in query for keyword in ["mobile camera", "open mobile camera", "access mobile camera"]):
                from backend.feature import access_mobile_camera
                access_mobile_camera()
            elif any(keyword in query for keyword in ["web camera", "webcam", "open camera"]):
                from backend.feature import access_web_camera
                access_web_camera()
            
            # Phone number location
            elif any(keyword in query for keyword in ["phone location", "locate phone", "find phone number"]):
                from backend.feature import find_phone_location
                # Extract phone number from query if present
                find_phone_location(query)
            
            # PDF reading
            elif any(keyword in query for keyword in ["read pdf", "open pdf"]):
                from backend.feature import read_pdf
                read_pdf(query)
            
            # Contacts management
            elif any(keyword in query for keyword in ["add contact", "new contact"]):
                from backend.feature import add_contact
                add_contact()
            elif any(keyword in query for keyword in ["search contact", "find contact"]):
                from backend.feature import search_contact
                search_contact(query)
            
            # QR code generation
            elif any(keyword in query for keyword in ["qr code", "generate qr", "create qr"]):
                from backend.feature import generate_qr_code
                speak("What text or link would you like to convert to QR code?")
                qr_text = takecommand()
                if qr_text:
                    generate_qr_code(qr_text)
            
            # Internet speed
            elif any(keyword in query for keyword in ["internet speed", "check speed", "network speed"]):
                from backend.feature import check_internet_speed
                check_internet_speed()
            
            # IP address
            elif any(keyword in query for keyword in ["ip address", "my ip", "what is my ip"]):
                from backend.feature import get_ip_address
                get_ip_address()
            
            # Latest news
            elif any(keyword in query for keyword in ["news", "latest news", "headlines"]):
                from backend.feature import get_latest_news
                get_latest_news()
            
            # System condition
            elif any(keyword in query for keyword in ["system condition", "system status", "pc status"]):
                from backend.feature import check_system_condition
                check_system_condition()
            
            # Email
            elif any(keyword in query for keyword in ["send email", "send gmail", "email"]):
                from backend.feature import send_gmail
                send_gmail(query)
            
            # WhatsApp messaging
            elif "send message" in query or "whatsapp message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query or "whatsapp message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        query = takecommand()  # Ask for the message text
                    elif "call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(Phone, query, flag, name)
            
            # YouTube features
            elif "on youtube" in query or "play youtube" in query:
                from backend.feature import PlayYoutube
                PlayYoutube(query)
            elif any(keyword in query for keyword in ["download youtube", "youtube download"]):
                from backend.feature import download_youtube
                download_youtube(query)
            
            # Instagram download
            elif any(keyword in query for keyword in ["instagram profile", "download instagram"]):
                from backend.feature import download_instagram_profile
                download_instagram_profile(query)
            
            # Current location
            elif any(keyword in query for keyword in ["current location", "where am i", "my location"]):
                from backend.feature import get_current_location
                get_current_location()
            
            # Screenshot
            elif any(keyword in query for keyword in ["screenshot", "take screenshot", "capture screen"]):
                from backend.feature import take_screenshot
                # Extract filename if provided
                filename = None
                if "name" in query:
                    # Simple extraction, can be improved
                    parts = query.split("name")
                    if len(parts) > 1:
                        filename = parts[1].strip()
                take_screenshot(filename)
            
            # Time and day
            elif any(keyword in query for keyword in ["current time", "what time", "tell time"]):
                from backend.feature import get_current_time
                current_time = get_current_time()
                speak(f"The current time is {current_time}")
            elif any(keyword in query for keyword in ["current day", "what day", "tell day"]):
                from backend.feature import get_current_day
                current_day = get_current_day()
                speak(f"Today is {current_day}")
            
            # Programming jokes
            elif any(keyword in query for keyword in ["programming joke", "tell joke", "random joke"]):
                from backend.feature import get_programming_joke
                joke = get_programming_joke()
                speak(joke)
            
            # Daily schedule
            elif any(keyword in query for keyword in ["schedule", "my schedule", "today's schedule"]):
                from backend.feature import get_daily_schedule
                get_daily_schedule()
            
            # Wikipedia search
            elif any(keyword in query for keyword in ["wikipedia", "search wikipedia"]):
                from backend.feature import search_wikipedia
                # Extract search term
                search_term = query.replace("wikipedia", "").replace("search", "").strip()
                if search_term:
                    result = search_wikipedia(search_term)
                    speak(result)
            
            # Browser search
            elif any(keyword in query for keyword in ["search browser", "browser search", "search for"]):
                from backend.feature import browser_search
                search_term = query.replace("search browser", "").replace("browser search", "").replace("search for", "").strip()
                if search_term:
                    browser_search(search_term)
            
            # System volume control
            elif any(keyword in query for keyword in ["volume", "set volume", "change volume"]):
                from backend.feature import set_system_volume
                # Try to extract volume level
                volume_level = 50  # Default
                level_match = re.search(r"\d+", query)
                if level_match:
                    volume_level = int(level_match.group())
                set_system_volume(volume_level)
            
            # System power activities
            elif any(keyword in query for keyword in ["shutdown", "turn off computer"]):
                from backend.feature import system_shutdown
                system_shutdown()
            elif any(keyword in query for keyword in ["restart", "reboot"]):
                from backend.feature import system_restart
                system_restart()
            
            # Play music
            elif any(keyword in query for keyword in ["play music", "play song"]):
                from backend.feature import play_music
                play_music(query)
            
            # Open websites and applications
            elif "open" in query:
                # Social media
                if any(keyword in query for keyword in ["facebook", "twitter", "instagram", "linkedin", "github"]):
                    from backend.feature import open_social_media
                    platform = next((keyword for keyword in ["facebook", "twitter", "instagram", "linkedin", "github"] if keyword in query), None)
                    if platform:
                        open_social_media(platform)
                # Meeting platforms
                elif any(keyword in query for keyword in ["zoom", "teams", "meet", "webex"]):
                    from backend.feature import open_meeting_platform
                    platform = next((keyword for keyword in ["zoom", "teams", "meet", "webex"] if keyword in query), None)
                    if platform:
                        open_meeting_platform(platform)
                # OTT platforms
                elif any(keyword in query for keyword in ["netflix", "prime", "disney", "hotstar", "hulu"]):
                    from backend.feature import open_ott_platform
                    platform = next((keyword for keyword in ["netflix", "prime", "disney", "hotstar", "hulu"] if keyword in query), None)
                    if platform:
                        open_ott_platform(platform)
                # Google apps
                elif any(keyword in query for keyword in ["gmail", "drive", "docs", "sheets", "slides"]):
                    from backend.feature import open_google_app
                    app = next((keyword for keyword in ["gmail", "drive", "docs", "sheets", "slides"] if keyword in query), None)
                    if app:
                        open_google_app(app)
                # Presentation tools
                elif any(keyword in query for keyword in ["canva", "google slide", "powerpoint"]):
                    from backend.feature import open_presentation_tool
                    tool = next((keyword for keyword in ["canva", "google slide", "powerpoint"] if keyword in query), None)
                    if tool:
                        open_presentation_tool(tool)
                # Shopping websites
                elif any(keyword in query for keyword in ["amazon", "flipkart", "ebay", "walmart"]):
                    from backend.feature import open_shopping_website
                    site = next((keyword for keyword in ["amazon", "flipkart", "ebay", "walmart"] if keyword in query), None)
                    if site:
                        open_shopping_website(site)
                # URL links
                elif "http" in query or "www" in query or ".com" in query:
                    from backend.feature import open_url
                    # Extract URL - simple approach
                    words = query.split()
                    url = next((word for word in words if "http" in word or "www" in word or ".com" in word), None)
                    if url:
                        open_url(url)
                # PC applications
                else:
                    from backend.feature import open_application
                    app_name = query.replace("open", "").strip()
                    if app_name:
                        open_application(app_name)
            
            # Code helper
            elif any(keyword in query for keyword in [
                "code", "programming", "write code", "create code", "help me code", 
                "python code", "javascript code", "java code", "html code", 
                "css code", "sql code", "coding help", "program", "script",
                "algorithm", "function", "class", "method", "variable",
                "calculator code", "web scraping", "hello world"
            ]):
                from backend.feature import codeHelper
                codeHelper(query)
            else:
                from backend.feature import chatBot
                chatBot(query)
        else:
            speak("No command was given.")
    except ImportError as ie:
        print(f"Import error: {ie}")
        speak("I'm having trouble accessing that feature. It might not be available in this version.")
    except ModuleNotFoundError as mnf:
        print(f"Module not found: {mnf}")
        speak("I'm missing some components needed for that feature. Please check the installation.")
    except AttributeError as ae:
        print(f"Attribute error: {ae}")
        speak("That specific feature function seems to be missing. Please check the feature implementation.")
    except Exception as e:
        print(f"An error occurred: {e}")
        # More specific error handling
        if "cookie" in str(e).lower():
            speak("I'm having trouble with my advanced features right now, but I can still help you with basic tasks.")
        elif "not defined" in str(e).lower() or "has no attribute" in str(e).lower():
            speak("That feature is not properly implemented yet. I'll make a note to fix it.")
        else:
            speak("I encountered an issue while processing your request. Let me try a different approach.")
    
    eel.ShowHood()
