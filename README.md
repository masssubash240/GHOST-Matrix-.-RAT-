# 🔍 TROJAN - Advanced Remote Administration Tool
GHOST rat  is a sophisticated Python-based remote administration and system monitoring tool designed for legitimate security research, authorized penetration testing, and educational purposes. The tool leverages Telegram's Bot API to provide a secure command-and-control interface for remote system management.

**Primary Use Cases:**
- Authorized penetration testing and red team exercises
- IT system administration and remote troubleshooting
- Cybersecurity education and research
- Digital forensics and incident response training
- Remote work environment management

## 🚀 Features

### 📹 Media Capture Module
**Screenshot Capability**
- Instant screen capture with quality optimization
- JPEG compression (60% quality) for faster transmission
- Temporary file cleanup after transmission

**Screen Recording**
- Configurable recording duration (1-20 seconds)
- XVID codec compression for optimal file size
- Real-time frame capture using PIL and OpenCV
- Automatic video cleanup after sending

**Camera Operations**
- Webcam photo capture with fallback handling
- Camera video recording (up to 15 seconds)
- Multiple camera device support
- Frame rate optimization for smooth video

**Audio Surveillance**
- Dual microphone recording implementations:
  - Primary: PyAudio with configurable sample rates
  - Alternative: SoundDevice for cross-platform compatibility
- Adjustable recording duration (10-45 seconds)
- Audio compression and format conversion
- Real-time audio stream processing

### ⌨️ Keylogger Module
**Advanced Keystroke Monitoring**
- Real-time keyboard event capture using pynput
- Smart buffering system (20-character threshold)
- Special key handling (space, enter, modifiers)
- Markdown-formatted transmission for readability
- Thread-safe operation with start/stop controls

### 📁 File System Explorer
**Directory Navigation**
- Recursive file and folder listing
- File size reporting in human-readable format
- Path validation and error handling
- Smart truncation for large directories

**File Operations**
- Secure file download with size limits (50MB)
- File content reading with encoding fallback
- Pattern-based file search across directories
- URL-based file downloading with progress tracking

### 🌐 System Intelligence
**Hardware & OS Information**
- Comprehensive system profiling:
  - Operating system and version details
  - User account information
  - Current working directory
  - Python environment data

**Geolocation Services**
- IP-based geolocation using ip-api.com
- ISP and network information
- Coordinate mapping with Telegram location sharing
- Offline capability with graceful failure

**System Control**
- Remote system lockdown (Windows support)
- System restart/shutdown commands
- Process management capabilities
- Session control operations

### 🔧 Technical Features
**Cross-Platform Compatibility**
- Windows, Linux, and macOS support
- Platform-specific optimizations
- Graceful feature degradation on unsupported systems

**Error Handling & Reliability**
- Comprehensive exception handling
- Connection timeout management
- Automatic resource cleanup
- Fail-safe operation modes

## 🛠 Installation

### Prerequisites
- Python 3.7 or higher
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Administrative privileges (for certain features)

### Step-by-Step Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/jarvis-remote-admin.git
cd jarvis-remote-admin
```

2. **Create Virtual Environment (Recommended)**
```bash
python -m venv jarvis_env
source jarvis_env/bin/activate  # Linux/macOS
jarvis_env\Scripts\activate    # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

**Required Packages:**
```text
telebot==0.0.5
opencv-python==4.8.1.78
pyaudio==0.2.11
pillow==10.0.1
pynput==1.7.6
sounddevice==0.4.6
soundfile==0.12.1
numpy==1.24.3
requests==2.31.0
```

4. **Platform-Specific Setup**

**Windows:**
- Ensure Windows Media Foundation is enabled
- Grant camera/microphone permissions

**Linux:**
```bash
# Install audio dependencies
sudo apt-get install portaudio19-dev python3-tk
# For camera access
sudo apt-get install libopencv-dev python3-opencv
```

**macOS:**
```bash
# Install portaudio for microphone
brew install portaudio
```

## ⚙️ Configuration

### Bot Setup
1. **Create Telegram Bot**
   - Message @BotFather on Telegram
   - Use `/newbot` command
   - Follow prompts to get your API token

2. **Configuration File**
```python
# config.py
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
YOUR_ID = "YOUR_TELEGRAM_USER_ID"

# Optional settings
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
SCREENSHOT_QUALITY = 60
AUDIO_SAMPLE_RATE = 16000
```

3. **Find Your Telegram ID**
   - Message @userinfobot on Telegram
   - Note your numerical user ID

### Security Configuration
```python
# Security settings
ALLOWED_USERS = [6265371619]  # Your Telegram ID
AUTO_DELETE_TEMP_FILES = True
ENCRYPT_COMMUNICATION = False  # Set to True for production
```

## 📖 Usage Guide

### Basic Commands
| Command | Parameters | Description |
|---------|------------|-------------|
| `/start` | None | Initialize bot connection |
| `/help` | None | Display command reference |
| `/info` | None | System information |

### Media Commands
| Command | Parameters | Description |
|---------|------------|-------------|
| `/screen` | None | Capture screenshot |
| `/record` | [seconds] | Record screen (max 20s) |
| `/cam` | None | Capture camera image |
| `/cam_video` | [seconds] | Record camera (max 15s) |
| `/mic` | [seconds] | Record audio (max 30s) |
| `/mic2` | [seconds] | Alternative audio (max 45s) |

### File System Commands
| Command | Parameters | Description |
|---------|------------|-------------|
| `/ls` | [path] | List directory contents |
| `/download` | <filepath> | Download file |
| `/upload` | <url> | Download from URL |
| `/read` | <filepath> | Read file content |
| `/search` | <pattern> | Search files |

### System Commands
| Command | Parameters | Description |
|---------|------------|-------------|
| `/key_start` | None | Start keylogger |
| `/key_stop` | None | Stop keylogger |
| `/loc` | None | Get geolocation |
| `/lock` | None | Lock workstation |
| `/restart` | None | Restart system |
| `/exit` | None | Terminate bot |

### Advanced Usage Examples

**Remote System Monitoring:**
```bash
# Continuous monitoring script
/screen
/info
/ls /home/user/documents
```

**Forensic Data Collection:**
```bash
# Comprehensive system survey
/info
/loc
/ls C:\Users
/search *.txt
```

**Incident Response:**
```bash
# Quick assessment commands
/screen
/cam
/mic 10
/key_start
```

## 🏗 Technical Architecture

### Module Structure
```
jarvis/
├── core/
│   ├── bot_client.py      # Telegram bot interface
│   ├── security.py        # Authentication & encryption
│   └── utils.py          # Common utilities
├── modules/
│   ├── media_capture.py   # Screen/camera/audio
│   ├── file_manager.py    # File operations
│   ├── keylogger.py       # Keystroke monitoring
│   └── system_info.py     # System data collection
└── temp/                  # Temporary files
```

### Data Flow
1. **Command Reception**: Telegram Bot API → Message Parser
2. **Authentication**: User ID Validation → Permission Check
3. **Execution**: Module Dispatch → System Interaction
4. **Response**: Data Processing → Telegram Response
5. **Cleanup**: Temporary File Removal → Resource Release

### Security Layers
- **Authentication**: Telegram User ID verification
- **Authorization**: Command-level permission checks
- **Isolation**: Sandboxed temporary file operations
- **Cleanup**: Automatic resource deallocation

## 🔒 Security Considerations

### Protection Mechanisms
- **User Whitelisting**: Only pre-approved Telegram users
- **Command Validation**: Input sanitization and validation
- **Resource Limits**: File size and operation duration caps
- **Temporary Storage**: Secure temp directory usage

### Risk Mitigation
- **Network Security**: Use VPN for sensitive operations
- **Data Encryption**: Enable SSL/TLS for communications
- **Access Logging**: Maintain operation audit trails
- **Regular Updates**: Keep dependencies patched

### Detection Avoidance
- **Process Names**: Use inconspicuous naming
- **Network Traffic**: Mimic legitimate applications
- **File Operations**: Clean temporary files promptly
- **System Footprint**: Minimal resource consumption

## ⚖️ Legal Disclaimer

### IMPORTANT LEGAL NOTICE

**This software is provided for educational and authorized security testing purposes only. Users are solely responsible for ensuring compliance with all applicable laws.**

### Authorized Usage Scenarios
- ✅ Testing your own systems
- ✅ Penetration testing with written client authorization
- ✅ Educational environments with proper supervision
- ✅ Corporate security assessments with management approval

### Prohibited Usage
- ❌ Unauthorized access to computer systems
- ❌ Surveillance without consent
- ❌ Data theft or privacy violation
- ❌ Any illegal activities

### Legal Framework Compliance
Users must comply with:
- Computer Fraud and Abuse Act (CFAA)
- General Data Protection Regulation (GDPR)
- Local computer misuse laws
- Privacy and surveillance regulations

## 🤝 Contributing

### Development Guidelines
1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push branch (`git push origin feature/improvement`)
5. Create Pull Request

### Code Standards
- Follow PEP 8 Python style guide
- Include comprehensive docstrings
- Add unit tests for new features
- Update documentation accordingly

### Feature Requests
We welcome contributions in:
- Enhanced cross-platform compatibility
- Additional security features
- Performance optimizations
- Documentation improvements

## ❓ FAQ

### Q: Is this tool detectable by antivirus software?
A: Like many security tools, it may trigger heuristic detection. Use only in authorized environments.

### Q: Can I use this on mobile devices?
A: The tool is designed for desktop operating systems (Windows, Linux, macOS).

### Q: How do I ensure my usage is legal?
A: Always obtain written permission from system owners and consult legal counsel.

### Q: What happens if I lose my Telegram token?
A: Regenerate the token via @BotFather and update your configuration.

### Q: Can the tool be customized for specific needs?
A: Yes, the modular architecture allows for easy customization and extension.

### Q: Is there a graphical user interface?
A: Currently, the tool operates via Telegram commands only.

## 📞 Support

For technical support and security concerns:
- **Issues**: GitHub Issues page
- **Security Reports**: Private vulnerability reporting
- **Documentation**: Project wiki and README updates

---

**⚠️ WARNING: Use responsibly and only in legal contexts. The developers assume no liability for misuse.**

*Last Updated: December 2024 | Version: 2.0 | License: Educational Use Only*
