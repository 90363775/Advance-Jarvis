#!/usr/bin/env python3
"""
OpenRouter API Key Tester
Tests the OpenRouter API key and checks credit status
"""

import sys
import os
import openai
import time

def test_openrouter_api():
    """Test OpenRouter API key and check credit status"""
    print("🔍 Testing OpenRouter API Key...")
    print("=" * 50)
    
    # Set up OpenRouter API
    api_key = "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"
    openai.api_key = api_key
    openai.api_base = "https://openrouter.ai/api/v1"
    
    print(f"🔑 API Key: {api_key[:20]}...{api_key[-10:]}")
    print(f"🌐 Base URL: {openai.api_base}")
    
    # Test multiple requests to check credit usage
    test_count = 5
    successful_requests = 0
    
    for i in range(test_count):
        try:
            print(f"\n📡 Test Request {i+1}/{test_count}...")
            
            response = openai.ChatCompletion.create(
                model="openai/gpt-3.5-turbo",  # OpenRouter model format
                messages=[
                    {"role": "user", "content": f"Hello, this is test #{i+1}. Please respond with 'API Working!'"}
                ],
                max_tokens=50,
                temperature=0.7
            )
            
            message = response.choices[0].message.content.strip()
            print(f"✅ Response: {message}")
            successful_requests += 1
            
            # Small delay between requests
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error in request {i+1}: {str(e)}")
            if "quota" in str(e).lower() or "credit" in str(e).lower():
                print("💸 Looks like credits are exhausted!")
                break
            elif "rate limit" in str(e).lower():
                print("⏱️ Rate limited - waiting longer...")
                time.sleep(5)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"✅ Successful Requests: {successful_requests}/{test_count}")
    
    if successful_requests == test_count:
        print("🎉 API Key: VALID and WORKING")
        print("💰 Credits: SUFFICIENT for testing")
        print("🔄 Note: OpenRouter free tier typically has limited credits, not unlimited")
    elif successful_requests > 0:
        print("⚠️ API Key: WORKING but may have limited credits")
        print("💰 Credits: PARTIALLY AVAILABLE")
    else:
        print("❌ API Key: NOT WORKING or NO CREDITS")
    
    print("\n📋 OpenRouter Free Tier Info:")
    print("• Free tier usually provides limited credits")
    print("• Credits reset monthly or require payment")
    print("• Check OpenRouter dashboard for exact usage")
    print("• Unlimited credits typically require paid plans")

if __name__ == "__main__":
    test_openrouter_api()
