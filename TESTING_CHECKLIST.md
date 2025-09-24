# 🤖 JARVIS TESTING CHECKLIST

## 🎯 QUICK TEST COMMANDS

### Wake Word Test
- [ ] Say: "Hey Jarvis" (should respond with confirmation)
- [ ] Wait for "Ready!" message before testing

### Basic Response Test  
- [ ] "Hello Jarvis" → Should greet you back
- [ ] "What is your name?" → Should say "I'm Jarvis"
- [ ] "What can you do?" → Should list capabilities

### Intelligence Test (Tests AI Brain)
- [ ] "What is artificial intelligence?" → Should give detailed explanation
- [ ] "Tell me about Iron Man" → Should mention Tony Stark
- [ ] "Tell me a joke" → Should tell a joke

### App Control Test
- [ ] "Open YouTube" → Should open YouTube
- [ ] "Open Google" → Should open Google
- [ ] "Play music on YouTube" → Should search and play

### Brain Switching Test (Watch Terminal)
- [ ] Ask complex questions and watch for:
  - 🧠 "Processing with OpenAI" (if quota available)
  - 🌟 "Processing with Google Gemini" (backup)
  - 🤖 "Fallback Response" (final backup)

## 🏆 SUCCESS INDICATORS

✅ **EXCELLENT (9-10/10)**
- Wake word works 95%+ of the time
- Complex AI responses (100+ words)
- Apps open correctly
- Brain switching visible in terminal
- Natural, witty responses

✅ **GOOD (7-8/10)** 
- Wake word works 80%+ of the time
- Good AI responses (50+ words)
- Most apps open correctly
- Some brain switching
- Helpful responses

⚠️ **FAIR (5-6/10)**
- Wake word works 60%+ of the time
- Basic responses (20+ words)
- Some apps work
- Fallback responses mostly
- Functional but limited

❌ **NEEDS WORK (Below 5/10)**
- Wake word unreliable
- Very short responses
- Apps don't open
- Only fallback responses
- Frequent errors

## 🔧 TROUBLESHOOTING

### If Wake Word Doesn't Work:
1. Check microphone permissions
2. Speak louder and clearer
3. Wait for "Ready!" message
4. Try "JARVIS" instead of "Hey Jarvis"

### If Responses Are Poor:
1. Check internet connection
2. Look for API errors in terminal
3. Test with simple questions first
4. Check if Gemini API key is working

### If Apps Don't Open:
1. Try exact app names: "Open YouTube"
2. Check if apps are installed
3. Test with common apps first

## 🎯 RECOMMENDED TEST SEQUENCE

1. **Start System**: `python run.py`
2. **Wait**: For "Ready! Say Hey Jarvis to wake me up"
3. **Basic Test**: "Hey Jarvis" → "Hello"
4. **Intelligence Test**: "What is AI?"
5. **App Test**: "Open YouTube"  
6. **Creative Test**: "Tell me a joke"
7. **Complex Test**: "Explain quantum computing"

## 📊 RATE YOUR JARVIS

**Wake Word Detection**: ___/10
**Voice Recognition**: ___/10
**AI Intelligence**: ___/10
**App Control**: ___/10
**Response Quality**: ___/10
**Overall Performance**: ___/10

**Notes:**
_________________________________
_________________________________
_________________________________

## 🚀 ADVANCED TESTING

For comprehensive testing, run:
- `python automated_test.py` (Text-based tests)
- `python jarvis_test_questions.py` (Full question list)
- Manual voice testing with categories above

**Your Jarvis is ready when all basic tests pass!** 🎉