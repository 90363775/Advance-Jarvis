import os
import eel
from backend.auth import recoganize
from backend.auth.recoganize import AuthenticateFace
from backend.feature import *
from backend.feature import (
    take_screenshot, get_current_time, get_current_day, get_programming_joke, search_wikipedia, browser_search, set_system_volume, system_shutdown, system_restart, system_sleep, play_music, open_account, open_application, close_application, sleep_until_wake, open_url, add_calendar_event, get_upcoming_events, remove_calendar_event, set_silence_mode, open_application, close_application
    )
from backend.command import *

# Import all required functions

def start():
    # Get the directory of the current script and build the frontend path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_path = os.path.join(script_dir, "frontend")
    
    eel.init(frontend_path) 
    
    play_assistant_sound()
    @eel.expose
    def init():
        eel.hideLoader()
        speak("Welcome to Jarvis")
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag ==1:
            speak("Face recognized successfully")
            eel.hideFaceAuth()
            eel.hideFaceAuthSuccess()
            speak("Welcome to Your Assistant")
            eel.hideStart()
            play_assistant_sound()
        else:
            speak("Face not recognized. Please try again")
        
    @eel.expose
    def takeScreenshot(filename=None):
        return take_screenshot(filename)

    @eel.expose
    def getCurrentTime():
        return get_current_time()

    @eel.expose
    def getCurrentDay():
        return get_current_day()

    @eel.expose
    def getProgrammingJoke():
        return get_programming_joke()

    @eel.expose
    def searchWikipedia(query):
        return search_wikipedia(query)

    @eel.expose
    def browserSearch(query):
        return browser_search(query)

    @eel.expose
    def setSystemVolume(level):
        return set_system_volume(level)

    @eel.expose
    def systemShutdown(delay=0):
        return system_shutdown(delay)

    @eel.expose
    def systemRestart(delay=0):
        return system_restart(delay)

    @eel.expose
    def systemSleep():
        return system_sleep()

    @eel.expose
    def playMusic(directory=None):
        return play_music(directory)

    @eel.expose
    def openAccount(account_type):
        return open_account(account_type)

    @eel.expose
    def openApplication(app_name):
        return open_application(app_name)

    @eel.expose
    def closeApplication(app_name):
        return close_application(app_name)

    @eel.expose
    def addCalendarEvent(title, description, start_time, end_time):
        return add_calendar_event(title, description, start_time, end_time)

    @eel.expose
    def getUpcomingEvents(max_results=5):
        return get_upcoming_events(max_results)

    @eel.expose
    def removeCalendarEvent(event_id):
        return remove_calendar_event(event_id)

    @eel.expose
    def sleepUntilWake():
        return sleep_until_wake()

    @eel.expose
    def openUrl(url):
        return open_url(url)

    @eel.expose
    def setSilenceMode(duration_minutes=0):
        return set_silence_mode(duration_minutes)

    os.system('start msedge.exe --app="http://127.0.0.1:8002/index.html"')
    
    
    
    eel.start("index.html", mode=None, host="localhost", port=8002, block=True) 

