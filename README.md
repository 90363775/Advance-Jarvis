# 🤖 Advanced Jarvis AI Assistant

An advanced AI assistant inspired by Tony Stark's JARVIS, featuring voice recognition, modern web interface, and 30+ powerful capabilities for productivity and automation.

![Jarvis Logo](frontend/assets/img/logo.ico)

## ✨ Features Overview

### 🎯 Core Capabilities
- 🎤 **Voice Recognition & Wake Word Detection** - "Hey Jarvis" activation
- 🗣️ **Text-to-Speech** - Natural voice responses
- 🖥️ **Modern Web Interface** - Clean EEL-based GUI
- 🧠 **Multi-AI Integration** - OpenAI GPT, Google Gemini, HugChat
- 💻 **Intelligent Code Helper** - Generate code in 10+ languages
- 📱 **WhatsApp Integration** - Messages, calls, video calls
- 🎵 **YouTube Integration** - Play and download songs
- 🌐 **Smart Web Automation** - Open apps and websites

### 🚀 Advanced Features

#### 🎥 Media & Recording
- 📹 **Screen Recording** with voice recording
- 🎙️ **Voice Recording** standalone
- 📷 **Camera Access** (Mobile & Web)
- 📸 **Custom Screenshot Tool**

#### 📱 Communication & Connectivity
- 📞 **Phone Number Location Finder**
- 📧 **Gmail Integration** 
- 📱 **WhatsApp Automation** (Individual & Group)
- 📇 **Contact Management** (Add/Search)

#### 🔧 System & Utilities
- 💻 **System Monitoring** & health check
- 🔊 **Volume Control** automation
- ⚡ **Power Management** (Shutdown/Restart/Sleep)
- 🌐 **Internet Speed Test**
- 📍 **IP Address & Location Detection**
- 🔇 **Smart Silence Mode** with timer

#### 📚 Information & Entertainment
- 📄 **PDF Reader** 
- 📰 **Latest News** updates
- 📚 **Wikipedia Search** (5-line summaries)
- 🍰 **How-to Instructions** generator
- 😄 **Programming Jokes**
- ⏰ **Time & Date Information**
- 📅 **Schedule Management**

#### 🛠️ Productivity Tools
- 🔗 **QR Code Generator** for links/text
- 🎶 **Music Player** for local files
- 🔍 **Web Search** automation
- 📱 **Quick Access Hub**:
  - Social Media platforms
  - Meeting platforms (Zoom, Teams, etc.)
  - OTT platforms (Netflix, Prime, etc.)
  - Google Apps suite
  - Presentation tools (Canva, Google Slides)
  - Shopping websites

#### 🎮 Special Functions
- 💤 **Sleep Until Wake** - Voice-activated sleep mode
- 🔄 **Application Control** - Open/Close any PC application
- 🎯 **Smart Command Recognition** - Context-aware responses

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (Python 3.10+ recommended)
- **Windows OS** (Tested on Windows 10/11)
- **Microphone & Speakers**
- **Internet Connection**

### 📦 Installation

1. **Clone the Repository**
```bash
git clone https://github.com/90363775/Advance-Jarvis.git
cd Advance-Jarvis
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Set Up Database**
```bash
python setup_commands.py
```

4. **Run Jarvis**
```bash
python run.py
```

### 🎮 First Use
1. The web interface will open automatically
2. Say **"Hey Jarvis"** to activate voice mode
3. Try commands like:
   - "Open YouTube"
   - "What's the time?"
   - "Generate Python code for calculator"
   - "Send WhatsApp message"
   - "Take a screenshot"

## ⚙️ Configuration

### 🔑 API Keys (Optional but Recommended)

#### OpenAI Integration
1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Edit `backend/config.txt`:
```
OPENAI_API_KEY=your_api_key_here
```

#### Google Gemini Integration
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Edit `backend/feature.py` line ~1342:
```python
GEMINI_API_KEY = "your_gemini_api_key_here"
```

#### OpenRouter Integration (Free Credits Available)
1. Get API key from [OpenRouter](https://openrouter.ai/)
2. Edit `backend/feature.py` line ~1279:
```python
openai.api_key = "your_openrouter_api_key_here"
```

### 🎙️ Voice Commands Examples

| Category | Command Examples |
|----------|------------------|
| **System** | "Open Chrome", "Close Notepad", "Shutdown computer" |
| **Media** | "Play songs on YouTube", "Take screenshot", "Start recording" |
| **Communication** | "Send WhatsApp to John", "Check my emails" |
| **Information** | "What's my IP address?", "Check internet speed", "Latest news" |
| **Productivity** | "Generate QR code for my website", "Search Wikipedia for AI" |
| **AI Chat** | "Tell me about machine learning", "Help me debug this code" |

## 🏗️ Project Structure

```
Advance-Jarvis/
├── 📁 backend/
│   ├── 🔐 auth/              # Face recognition system
│   ├── 📝 command.py         # Command processing engine
│   ├── ⚡ feature.py         # Core features implementation
│   ├── ⚙️ config.py          # Configuration management
│   ├── 🗄️ db.py              # Database operations
│   └── 🛠️ helper.py          # Utility functions
├── 📁 frontend/
│   ├── 🎨 assets/            # Images, sounds, styles
│   ├── 🌐 index.html         # Main web interface
│   ├── 💫 style.css          # Modern UI styling
│   └── ⚡ script.js          # Frontend interactions
├── 📁 tests/
│   ├── 🧪 test_features.py   # Feature testing suite
│   ├── 🎤 test_microphone.py # Audio system tests
│   └── 🔬 test_*.py          # Individual feature tests
├── 🚀 main.py                # Application core
├── ▶️ run.py                 # Application launcher
└── 📖 README.md              # This file
```

## 🧪 Testing

### Run All Tests
```bash
python test_features.py
```

### Test Specific Features
```bash
python test_microphone.py    # Test audio system
python test_youtube.py       # Test YouTube integration
python test_brain.py         # Test AI responses
```

### Automated Testing
```bash
python automated_test.py     # Comprehensive test suite
```

## 🔧 Development

### Adding New Features
1. **Add function to `backend/feature.py`**
```python
@eel.expose
def your_new_feature(query):
    # Your implementation
    speak("Feature executed successfully!")
    return True
```

2. **Add command recognition to `backend/command.py`**
```python
elif "your trigger phrase" in query:
    from backend.feature import your_new_feature
    your_new_feature(query)
```

3. **Test your feature**
```python
python test_your_feature.py
```

### Voice Command Patterns
- Use clear, natural language triggers
- Support multiple variations ("open", "launch", "start")
- Provide audio feedback for all actions
- Handle errors gracefully with user-friendly messages

## 🐛 Troubleshooting

### Common Issues

#### 🎤 Microphone Problems
- **Issue**: Voice not recognized
- **Solution**: Check Windows microphone permissions
```bash
# Test microphone
python test_microphone.py
```

#### 🌐 Interface Not Loading
- **Issue**: Web interface doesn't open
- **Solution**: Check if port 8080 is available
```bash
netstat -an | findstr :8080
```

#### 🔑 API Errors
- **Issue**: AI features not working
- **Solution**: Verify API keys in config files
```bash
# Basic functionality works without API keys
# AI chat requires OpenAI/Gemini keys
```

#### 📱 WhatsApp Integration
- **Issue**: WhatsApp commands fail
- **Solution**: Ensure WhatsApp Web is accessible
- Add contacts to database first

### Debug Mode
```bash
python run.py --debug
```

### Reset Configuration
```bash
python setup_commands.py --reset
```

## 📊 Performance

- **Response Time**: < 2 seconds for most commands
- **Memory Usage**: ~150MB typical usage
- **CPU Usage**: Low when idle, moderate during processing
- **Supports**: Windows 10/11, Python 3.8+

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the Repository**
2. **Create Feature Branch**
```bash
git checkout -b feature/amazing-feature
```
3. **Make Changes**
4. **Test Thoroughly**
```bash
python test_features.py
```
5. **Submit Pull Request**

### Contribution Guidelines
- Follow Python PEP 8 style guide
- Add tests for new features
- Update documentation
- Ensure cross-platform compatibility

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Inspiration**: Marvel's JARVIS from Iron Man
- **Framework**: Python EEL for desktop/web hybrid interface
- **AI Integration**: OpenAI, Google Gemini, HugChat
- **Community**: Open-source Python ecosystem

## 📞 Support

### Get Help
- 📚 **Documentation**: Check this README and test files
- 🐛 **Issues**: [Create an issue](https://github.com/90363775/Advance-Jarvis/issues)
- 💬 **Discussions**: [Start a discussion](https://github.com/90363775/Advance-Jarvis/discussions)

### Feature Requests
Have an idea? We'd love to hear it! Create an issue with the "enhancement" label.

---

## ⭐ Star This Project

If you find this project useful, please consider giving it a star! It helps others discover the project and motivates continued development.

---

**Built with ❤️ by the Jarvis AI Team**

> "Sometimes you gotta run before you can walk." - Tony Stark

---

*Note: This project is for educational and personal use. Some features require additional setup and API keys. The assistant works with basic functionality even without external API keys.*