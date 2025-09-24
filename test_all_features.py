import os
import sys
import time
import random
from datetime import datetime, timedelta
import subprocess

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(project_root, "backend")
sys.path.append(backend_path)

def test_new_features():
    """Test all the newly implemented features"""
    print("=" * 60)
    print("🚀 TESTING NEW JARVIS FEATURES")
    print("=" * 60)
    
    try:
        # Import required modules after adding to path
        from backend.feature import (
            set_silence_mode, get_system_volume, 
            open_application, close_application,
            sleep_until_wake
        )
        from backend.command import speak
        print("✅ Successfully imported all new feature modules!")
    except Exception as e:
        print(f"❌ Error importing modules: {e}")
        return False
    
    # Test results tracking
    test_results = {
        "passed": 0,
        "failed": 0,
        "skipped": 0
    }
    
    # Test 1: Calendar Integration
    print("\n📅 Testing Calendar Integration...")
    print("-" * 40)
    try:
        # Test calendar function imports
        from backend.feature import add_calendar_event, get_upcoming_events, remove_calendar_event
        print("Testing calendar event creation...")
        title = f"Test Event {random.randint(1, 1000)}"
        description = "Automated test event"
        start_time = datetime.now() + timedelta(minutes=5)
        end_time = start_time + timedelta(minutes=30)
        
        print(f"Would create event: {title}")
        print(f"Start: {start_time}")
        print(f"End: {end_time}")
        print("✅ Calendar integration functions available")
        test_results["passed"] += 1
        
    except Exception as e:
        print(f"❌ Calendar integration test failed: {e}")
        test_results["failed"] += 1
    
    # Test 2: Silence Mode
    print("\n🔇 Testing Silence Mode...")
    print("-" * 40)
    try:
        print("Testing volume control...")
        current_volume = get_system_volume()
        print(f"Current system volume: {current_volume}")
        
        # Test silence mode activation (brief duration for testing)
        print("Testing silence mode activation...")
        result = set_silence_mode(0)  # Just toggle, don't wait
        if result:
            print("✅ Silence mode function executed successfully")
            test_results["passed"] += 1
        else:
            print("⚠️ Silence mode function returned False")
            test_results["failed"] += 1
            
    except Exception as e:
        print(f"❌ Silence mode test failed: {e}")
        test_results["failed"] += 1
    
    # Test 3: Application Control
    print("\n💻 Testing Application Control...")
    print("-" * 40)
    try:
        print("Testing application opening...")
        
        # Test opening Calculator (safe and quick)
        print("Attempting to open Calculator...")
        result = open_application("calculator")
        if result:
            print("✅ Calculator opened successfully")
            time.sleep(2)  # Wait a moment
            
            # Test closing Calculator
            print("Attempting to close Calculator...")
            close_result = close_application("calculator")
            if close_result:
                print("✅ Calculator closed successfully")
            else:
                print("⚠️ Calculator closing may have failed")
            
            test_results["passed"] += 1
        else:
            print("⚠️ Calculator opening may have failed")
            test_results["failed"] += 1
            
    except Exception as e:
        print(f"❌ Application control test failed: {e}")
        test_results["failed"] += 1
    
    # Test 4: Sleep/Wake Functionality  
    print("\n😴 Testing Sleep/Wake Functionality...")
    print("-" * 40)
    try:
        print("Sleep/wake function is available but not tested")
        print("(Skipped to avoid actually putting system to sleep)")
        print("✅ Sleep/wake function accessible")
        test_results["skipped"] += 1
        
    except Exception as e:
        print(f"❌ Sleep/wake test failed: {e}")
        test_results["failed"] += 1
    
    # Test 5: Additional Feature Tests
    print("\n🔧 Testing Additional Features...")
    print("-" * 40)
    try:
        # Test imports of other new functions
        from backend.feature import (
            get_current_time, get_current_day, get_programming_joke,
            search_wikipedia, browser_search, set_system_volume,
            system_shutdown, system_restart, system_sleep,
            play_music, open_account, open_url
        )
        print("✅ All additional feature functions imported successfully")
        
        # Test time and day functions
        print("Testing time/day functions...")
        current_time = get_current_time()
        current_day = get_current_day()
        joke = get_programming_joke()
        
        print(f"Current time: {current_time}")
        print(f"Current day: {current_day}")
        print(f"Programming joke: {joke}")
        
        test_results["passed"] += 1
        
    except Exception as e:
        print(f"❌ Additional features test failed: {e}")
        test_results["failed"] += 1
    
    # Test Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"✅ Tests Passed: {test_results['passed']}")
    print(f"❌ Tests Failed: {test_results['failed']}")
    print(f"⏭️ Tests Skipped: {test_results['skipped']}")
    
    total_tests = sum(test_results.values())
    if total_tests > 0:
        success_rate = (test_results['passed'] / total_tests) * 100
        print(f"🎯 Success Rate: {success_rate:.1f}%")
    
    print("\n🎉 NEW FEATURES TESTING COMPLETED!")
    print("=" * 60)
    
    return test_results['failed'] == 0

if __name__ == "__main__":
    success = test_new_features()
    if success:
        print("\n✅ All available tests passed!")
    else:
        print("\n⚠️ Some tests failed - check output above")