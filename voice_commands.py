#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voice Commands System - Advanced Voice Control for Site Builder
Supports multiple languages with intelligent command recognition
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue
import json
import re
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommandType(Enum):
    """Types of voice commands"""
    ADD_ELEMENT = "add_element"
    REMOVE_ELEMENT = "remove_element"
    MODIFY_ELEMENT = "modify_element"
    NAVIGATE = "navigate"
    SAVE = "save"
    UNDO = "undo"
    REDO = "redo"
    HELP = "help"
    SETTINGS = "settings"
    AI_GENERATE = "ai_generate"

@dataclass
class VoiceCommand:
    """Voice command structure"""
    command_type: CommandType
    parameters: Dict
    confidence: float
    language: str
    timestamp: datetime
    raw_text: str

class VoiceCommandsSystem:
    """Advanced Voice Commands System with multilingual support"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Command queue for processing
        self.command_queue = queue.Queue()
        self.is_listening = False
        self.current_language = "fa"
        
        # Command patterns for different languages
        self.command_patterns = self._load_command_patterns()
        
        # Callbacks for different commands
        self.command_callbacks = {}
        
        # Initialize TTS
        self._setup_tts()
        
        # Calibrate microphone
        self._calibrate_microphone()
    
    def _load_command_patterns(self) -> Dict:
        """Load command patterns for different languages"""
        return {
            "fa": {
                CommandType.ADD_ELEMENT: [
                    r"اضافه کن (.+)",
                    r"یک (.+) اضافه کن",
                    r"بذار (.+)",
                    r"درج کن (.+)"
                ],
                CommandType.REMOVE_ELEMENT: [
                    r"حذف کن (.+)",
                    r"پاک کن (.+)",
                    r"بردار (.+)",
                    r"حذف (.+)"
                ],
                CommandType.MODIFY_ELEMENT: [
                    r"تغییر بده (.+)",
                    r"ویرایش کن (.+)",
                    r"عوض کن (.+)",
                    r"به (.+) تغییر بده"
                ],
                CommandType.NAVIGATE: [
                    r"برو به (.+)",
                    r"نمایش (.+)",
                    r"باز کن (.+)",
                    r"انتقال به (.+)"
                ],
                CommandType.SAVE: [
                    r"ذخیره کن",
                    r"سیو کن",
                    r"نگه دار",
                    r"حفظ کن"
                ],
                CommandType.UNDO: [
                    r"برگرد",
                    r"لغو کن",
                    r"undo",
                    r"برگشت"
                ],
                CommandType.REDO: [
                    r"دوباره",
                    r"redo",
                    r"تکرار کن",
                    r"بازگردان"
                ],
                CommandType.HELP: [
                    r"کمک",
                    r"راهنما",
                    r"help",
                    r"دستورات"
                ],
                CommandType.SETTINGS: [
                    r"تنظیمات",
                    r"settings",
                    r"پیکربندی",
                    r"گزینه‌ها"
                ],
                CommandType.AI_GENERATE: [
                    r"تولید کن (.+)",
                    r"ساخت کن (.+)",
                    r"ایجاد کن (.+)",
                    r"ai (.+)"
                ]
            },
            "en": {
                CommandType.ADD_ELEMENT: [
                    r"add (.+)",
                    r"insert (.+)",
                    r"create (.+)",
                    r"put (.+)"
                ],
                CommandType.REMOVE_ELEMENT: [
                    r"remove (.+)",
                    r"delete (.+)",
                    r"clear (.+)",
                    r"take out (.+)"
                ],
                CommandType.MODIFY_ELEMENT: [
                    r"change (.+)",
                    r"edit (.+)",
                    r"modify (.+)",
                    r"update (.+)"
                ],
                CommandType.NAVIGATE: [
                    r"go to (.+)",
                    r"show (.+)",
                    r"open (.+)",
                    r"navigate to (.+)"
                ],
                CommandType.SAVE: [
                    r"save",
                    r"save it",
                    r"keep it",
                    r"store"
                ],
                CommandType.UNDO: [
                    r"undo",
                    r"go back",
                    r"revert",
                    r"cancel"
                ],
                CommandType.REDO: [
                    r"redo",
                    r"repeat",
                    r"again",
                    r"restore"
                ],
                CommandType.HELP: [
                    r"help",
                    r"commands",
                    r"what can you do",
                    r"assistance"
                ],
                CommandType.SETTINGS: [
                    r"settings",
                    r"options",
                    r"configuration",
                    r"preferences"
                ],
                CommandType.AI_GENERATE: [
                    r"generate (.+)",
                    r"create (.+)",
                    r"make (.+)",
                    r"ai (.+)"
                ]
            },
            "ar": {
                CommandType.ADD_ELEMENT: [
                    r"أضف (.+)",
                    r"ضع (.+)",
                    r"أدرج (.+)",
                    r"أنشئ (.+)"
                ],
                CommandType.REMOVE_ELEMENT: [
                    r"احذف (.+)",
                    r"امسح (.+)",
                    r"أزل (.+)",
                    r"شطب (.+)"
                ],
                CommandType.MODIFY_ELEMENT: [
                    r"غيّر (.+)",
                    r"عدّل (.+)",
                    r"حرّر (.+)",
                    r"حدّث (.+)"
                ],
                CommandType.NAVIGATE: [
                    r"اذهب إلى (.+)",
                    r"اعرض (.+)",
                    r"افتح (.+)",
                    r"انتقل إلى (.+)"
                ],
                CommandType.SAVE: [
                    r"احفظ",
                    r"خزّن",
                    r"احتفظ",
                    r"سجّل"
                ],
                CommandType.UNDO: [
                    r"تراجع",
                    r"ألغ",
                    r"ارجع",
                    r"undo"
                ],
                CommandType.REDO: [
                    r"أعد",
                    r"كرّر",
                    r"redo",
                    r"استرجع"
                ],
                CommandType.HELP: [
                    r"مساعدة",
                    r"مساعدة",
                    r"help",
                    r"الأوامر"
                ],
                CommandType.SETTINGS: [
                    r"الإعدادات",
                    r"settings",
                    r"التكوين",
                    r"الخيارات"
                ],
                CommandType.AI_GENERATE: [
                    r"أنشئ (.+)",
                    r"اصنع (.+)",
                    r"توليد (.+)",
                    r"ai (.+)"
                ]
            }
        }
    
    def _setup_tts(self):
        """Setup text-to-speech engine"""
        try:
            # Set voice properties
            voices = self.tts_engine.getProperty('voices')
            
            # Try to find appropriate voice for current language
            if self.current_language == "fa":
                # Look for Persian voice
                for voice in voices:
                    if 'persian' in voice.name.lower() or 'farsi' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            elif self.current_language == "ar":
                # Look for Arabic voice
                for voice in voices:
                    if 'arabic' in voice.name.lower() or 'ar' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.8)
            
            logger.info("TTS engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Error setting up TTS: {e}")
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                logger.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            logger.info("Microphone calibration completed")
        except Exception as e:
            logger.error(f"Error calibrating microphone: {e}")
    
    def set_language(self, language: str):
        """Set the current language for voice commands"""
        if language in self.command_patterns:
            self.current_language = language
            self._setup_tts()  # Reconfigure TTS for new language
            logger.info(f"Language set to: {language}")
        else:
            logger.warning(f"Unsupported language: {language}")
    
    def register_command_callback(self, command_type: CommandType, callback: Callable):
        """Register a callback function for a specific command type"""
        self.command_callbacks[command_type] = callback
        logger.info(f"Registered callback for {command_type.value}")
    
    def start_listening(self):
        """Start listening for voice commands"""
        if self.is_listening:
            logger.warning("Already listening for voice commands")
            return
        
        self.is_listening = True
        self._listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listen_thread.start()
        logger.info("Started listening for voice commands")
    
    def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        logger.info("Stopped listening for voice commands")
    
    def _listen_loop(self):
        """Main listening loop"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Recognize speech
                try:
                    text = self.recognizer.recognize_google(
                        audio, 
                        language=self._get_google_language_code()
                    )
                    
                    if text:
                        logger.info(f"Recognized: {text}")
                        command = self._parse_command(text)
                        if command:
                            self.command_queue.put(command)
                            
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    pass
                except sr.RequestError as e:
                    logger.error(f"Speech recognition error: {e}")
                    
            except sr.WaitTimeoutError:
                # Timeout waiting for speech
                pass
            except Exception as e:
                logger.error(f"Error in listening loop: {e}")
    
    def _get_google_language_code(self) -> str:
        """Get Google Speech Recognition language code"""
        language_codes = {
            "fa": "fa-IR",
            "en": "en-US",
            "ar": "ar-SA"
        }
        return language_codes.get(self.current_language, "en-US")
    
    def _parse_command(self, text: str) -> Optional[VoiceCommand]:
        """Parse recognized text into a voice command"""
        text_lower = text.lower()
        
        # Try to match against command patterns
        for command_type, patterns in self.command_patterns[self.current_language].items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    parameters = {}
                    
                    # Extract parameters from the match
                    if match.groups():
                        parameters['target'] = match.group(1)
                    
                    # Calculate confidence based on pattern match
                    confidence = 0.8 if match.groups() else 0.9
                    
                    return VoiceCommand(
                        command_type=command_type,
                        parameters=parameters,
                        confidence=confidence,
                        language=self.current_language,
                        timestamp=datetime.now(),
                        raw_text=text
                    )
        
        # No pattern matched
        return None
    
    def process_commands(self):
        """Process queued voice commands"""
        while not self.command_queue.empty():
            try:
                command = self.command_queue.get_nowait()
                self._execute_command(command)
            except queue.Empty:
                break
            except Exception as e:
                logger.error(f"Error processing command: {e}")
    
    def _execute_command(self, command: VoiceCommand):
        """Execute a voice command"""
        logger.info(f"Executing command: {command.command_type.value}")
        
        # Call registered callback if available
        if command.command_type in self.command_callbacks:
            try:
                self.command_callbacks[command.command_type](command)
            except Exception as e:
                logger.error(f"Error executing command callback: {e}")
                self.speak("خطا در اجرای دستور")
        else:
            # Default command handling
            self._handle_default_command(command)
    
    def _handle_default_command(self, command: VoiceCommand):
        """Handle commands with default behavior"""
        if command.command_type == CommandType.HELP:
            self._show_help()
        elif command.command_type == CommandType.SAVE:
            self.speak("ذخیره شد")
        elif command.command_type == CommandType.UNDO:
            self.speak("برگشت انجام شد")
        elif command.command_type == CommandType.REDO:
            self.speak("تکرار انجام شد")
        else:
            self.speak("دستور دریافت شد")
    
    def _show_help(self):
        """Show available voice commands"""
        help_text = "دستورات صوتی موجود: اضافه کن، حذف کن، تغییر بده، ذخیره کن، برگرد، دوباره، کمک"
        self.speak(help_text)
        logger.info("Help displayed")
    
    def speak(self, text: str):
        """Convert text to speech"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
    
    def get_available_commands(self) -> List[Dict]:
        """Get list of available voice commands"""
        commands = []
        
        for command_type, patterns in self.command_patterns[self.current_language].items():
            commands.append({
                "type": command_type.value,
                "patterns": patterns,
                "description": self._get_command_description(command_type)
            })
        
        return commands
    
    def _get_command_description(self, command_type: CommandType) -> str:
        """Get description for a command type"""
        descriptions = {
            CommandType.ADD_ELEMENT: "اضافه کردن عنصر جدید",
            CommandType.REMOVE_ELEMENT: "حذف عنصر",
            CommandType.MODIFY_ELEMENT: "تغییر عنصر",
            CommandType.NAVIGATE: "ناوبری",
            CommandType.SAVE: "ذخیره کردن",
            CommandType.UNDO: "برگشت",
            CommandType.REDO: "تکرار",
            CommandType.HELP: "نمایش راهنما",
            CommandType.SETTINGS: "تنظیمات",
            CommandType.AI_GENERATE: "تولید با هوش مصنوعی"
        }
        return descriptions.get(command_type, "دستور نامشخص")
    
    def get_status(self) -> Dict:
        """Get current system status"""
        return {
            "is_listening": self.is_listening,
            "current_language": self.current_language,
            "queue_size": self.command_queue.qsize(),
            "registered_callbacks": len(self.command_callbacks),
            "available_commands": len(self.get_available_commands())
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize voice commands system
    voice_system = VoiceCommandsSystem()
    
    # Set language
    voice_system.set_language("fa")
    
    # Register some command callbacks
    def handle_add_element(command: VoiceCommand):
        print(f"Adding element: {command.parameters.get('target', 'unknown')}")
        voice_system.speak(f"عنصر {command.parameters.get('target', '')} اضافه شد")
    
    def handle_remove_element(command: VoiceCommand):
        print(f"Removing element: {command.parameters.get('target', 'unknown')}")
        voice_system.speak(f"عنصر {command.parameters.get('target', '')} حذف شد")
    
    def handle_save(command: VoiceCommand):
        print("Saving project...")
        voice_system.speak("پروژه ذخیره شد")
    
    # Register callbacks
    voice_system.register_command_callback(CommandType.ADD_ELEMENT, handle_add_element)
    voice_system.register_command_callback(CommandType.REMOVE_ELEMENT, handle_remove_element)
    voice_system.register_command_callback(CommandType.SAVE, handle_save)
    
    # Show available commands
    print("🎤 Available Voice Commands:")
    commands = voice_system.get_available_commands()
    for cmd in commands:
        print(f"  {cmd['type']}: {cmd['description']}")
        for pattern in cmd['patterns'][:2]:  # Show first 2 patterns
            print(f"    - {pattern}")
    
    # Start listening
    print("\n🎧 Starting voice recognition...")
    print("Say commands like: 'اضافه کن هدر' or 'حذف کن دکمه'")
    
    voice_system.start_listening()
    
    try:
        # Process commands in main thread
        while True:
            voice_system.process_commands()
            import time
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping voice recognition...")
        voice_system.stop_listening()
        print("✅ Voice commands system stopped")
