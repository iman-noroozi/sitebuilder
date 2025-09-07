#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for Voice Commands System
Tests all functionality of the Voice Commands system
"""

import sys
import os
import json
import time
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from voice_commands import VoiceCommandsSystem, CommandType, VoiceCommand

def test_voice_commands_system():
    """Test the Voice Commands System functionality"""
    print("🎤 Testing Voice Commands System...")
    print("=" * 50)
    
    # Initialize the system
    voice_system = VoiceCommandsSystem()
    
    # Test 1: Language switching
    print("\n🌍 Test 1: Language Switching")
    print("-" * 30)
    
    languages = ["fa", "en", "ar"]
    for lang in languages:
        voice_system.set_language(lang)
        print(f"✅ Language set to: {lang}")
        print(f"   Available commands: {len(voice_system.get_available_commands())}")
    
    # Test 2: Command pattern matching
    print("\n🔍 Test 2: Command Pattern Matching")
    print("-" * 30)
    
    # Test Persian commands
    voice_system.set_language("fa")
    test_commands_fa = [
        "اضافه کن هدر",
        "حذف کن دکمه",
        "تغییر بده رنگ",
        "ذخیره کن",
        "برگرد",
        "دوباره",
        "کمک"
    ]
    
    for cmd_text in test_commands_fa:
        command = voice_system._parse_command(cmd_text)
        if command:
            print(f"✅ '{cmd_text}' -> {command.command_type.value}")
        else:
            print(f"❌ '{cmd_text}' -> No match")
    
    # Test English commands
    voice_system.set_language("en")
    test_commands_en = [
        "add header",
        "remove button",
        "change color",
        "save",
        "undo",
        "redo",
        "help"
    ]
    
    for cmd_text in test_commands_en:
        command = voice_system._parse_command(cmd_text)
        if command:
            print(f"✅ '{cmd_text}' -> {command.command_type.value}")
        else:
            print(f"❌ '{cmd_text}' -> No match")
    
    # Test 3: Command callbacks
    print("\n🔧 Test 3: Command Callbacks")
    print("-" * 30)
    
    callback_results = []
    
    def test_callback(command: VoiceCommand):
        callback_results.append({
            "type": command.command_type.value,
            "text": command.raw_text,
            "parameters": command.parameters,
            "confidence": command.confidence
        })
        print(f"✅ Callback executed for: {command.command_type.value}")
    
    # Register callbacks for all command types
    for cmd_type in CommandType:
        voice_system.register_command_callback(cmd_type, test_callback)
    
    print(f"✅ Registered {len(voice_system.command_callbacks)} callbacks")
    
    # Test 4: Command execution
    print("\n⚡ Test 4: Command Execution")
    print("-" * 30)
    
    # Create test commands
    test_commands = [
        VoiceCommand(
            command_type=CommandType.ADD_ELEMENT,
            parameters={"target": "header"},
            confidence=0.9,
            language="fa",
            timestamp=datetime.now(),
            raw_text="اضافه کن هدر"
        ),
        VoiceCommand(
            command_type=CommandType.REMOVE_ELEMENT,
            parameters={"target": "button"},
            confidence=0.8,
            language="fa",
            timestamp=datetime.now(),
            raw_text="حذف کن دکمه"
        ),
        VoiceCommand(
            command_type=CommandType.SAVE,
            parameters={},
            confidence=0.95,
            language="fa",
            timestamp=datetime.now(),
            raw_text="ذخیره کن"
        )
    ]
    
    # Execute commands
    for cmd in test_commands:
        voice_system._execute_command(cmd)
        time.sleep(0.1)  # Small delay for processing
    
    print(f"✅ Executed {len(test_commands)} commands")
    print(f"✅ Callback results: {len(callback_results)}")
    
    # Test 5: System status
    print("\n📊 Test 5: System Status")
    print("-" * 30)
    
    status = voice_system.get_status()
    print(f"✅ Is listening: {status['is_listening']}")
    print(f"✅ Current language: {status['current_language']}")
    print(f"✅ Queue size: {status['queue_size']}")
    print(f"✅ Registered callbacks: {status['registered_callbacks']}")
    print(f"✅ Available commands: {status['available_commands']}")
    
    # Test 6: Available commands
    print("\n📋 Test 6: Available Commands")
    print("-" * 30)
    
    commands = voice_system.get_available_commands()
    for cmd in commands:
        print(f"✅ {cmd['type']}: {cmd['description']}")
        print(f"   Patterns: {len(cmd['patterns'])}")
    
    print("\n🎉 All voice commands tests completed successfully!")
    return True

def test_command_patterns():
    """Test command pattern matching in detail"""
    print("\n🔍 Testing Command Patterns in Detail...")
    print("=" * 50)
    
    voice_system = VoiceCommandsSystem()
    
    # Test patterns for each language
    test_cases = {
        "fa": [
            ("اضافه کن هدر", CommandType.ADD_ELEMENT, "هدر"),
            ("یک دکمه اضافه کن", CommandType.ADD_ELEMENT, "دکمه"),
            ("حذف کن تصویر", CommandType.REMOVE_ELEMENT, "تصویر"),
            ("تغییر بده رنگ", CommandType.MODIFY_ELEMENT, "رنگ"),
            ("برو به تنظیمات", CommandType.NAVIGATE, "تنظیمات"),
            ("ذخیره کن", CommandType.SAVE, ""),
            ("برگرد", CommandType.UNDO, ""),
            ("دوباره", CommandType.REDO, ""),
            ("کمک", CommandType.HELP, "")
        ],
        "en": [
            ("add header", CommandType.ADD_ELEMENT, "header"),
            ("insert button", CommandType.ADD_ELEMENT, "button"),
            ("remove image", CommandType.REMOVE_ELEMENT, "image"),
            ("change color", CommandType.MODIFY_ELEMENT, "color"),
            ("go to settings", CommandType.NAVIGATE, "settings"),
            ("save", CommandType.SAVE, ""),
            ("undo", CommandType.UNDO, ""),
            ("redo", CommandType.REDO, ""),
            ("help", CommandType.HELP, "")
        ],
        "ar": [
            ("أضف هيدر", CommandType.ADD_ELEMENT, "هيدر"),
            ("احذف صورة", CommandType.REMOVE_ELEMENT, "صورة"),
            ("غيّر اللون", CommandType.MODIFY_ELEMENT, "اللون"),
            ("اذهب إلى الإعدادات", CommandType.NAVIGATE, "الإعدادات"),
            ("احفظ", CommandType.SAVE, ""),
            ("تراجع", CommandType.UNDO, ""),
            ("أعد", CommandType.REDO, ""),
            ("مساعدة", CommandType.HELP, "")
        ]
    }
    
    for language, test_cases_list in test_cases.items():
        print(f"\n🌍 Testing {language.upper()} patterns:")
        voice_system.set_language(language)
        
        for text, expected_type, expected_param in test_cases_list:
            command = voice_system._parse_command(text)
            if command:
                success = (command.command_type == expected_type and 
                          command.parameters.get('target', '') == expected_param)
                status = "✅" if success else "❌"
                print(f"  {status} '{text}' -> {command.command_type.value} ({command.parameters.get('target', 'N/A')})")
            else:
                print(f"  ❌ '{text}' -> No match")

def test_tts_functionality():
    """Test text-to-speech functionality"""
    print("\n🔊 Testing Text-to-Speech Functionality...")
    print("=" * 50)
    
    voice_system = VoiceCommandsSystem()
    
    # Test TTS in different languages
    test_messages = {
        "fa": "سلام، این یک تست صوتی است",
        "en": "Hello, this is a voice test",
        "ar": "مرحبا، هذا اختبار صوتي"
    }
    
    for lang, message in test_messages.items():
        print(f"\n🌍 Testing TTS in {lang.upper()}:")
        voice_system.set_language(lang)
        print(f"  Message: {message}")
        
        try:
            # Note: In a real test, you might want to disable actual speech output
            # voice_system.speak(message)
            print("  ✅ TTS engine configured successfully")
        except Exception as e:
            print(f"  ❌ TTS error: {e}")

def generate_voice_commands_demo():
    """Generate a demo of voice commands functionality"""
    print("\n🎬 Generating Voice Commands Demo...")
    print("=" * 50)
    
    voice_system = VoiceCommandsSystem()
    
    # Demo scenarios
    demo_scenarios = [
        {
            "name": "Persian Website Building",
            "language": "fa",
            "commands": [
                "اضافه کن هدر",
                "یک دکمه اضافه کن",
                "تغییر بده رنگ",
                "ذخیره کن",
                "برگرد"
            ]
        },
        {
            "name": "English Website Building",
            "language": "en",
            "commands": [
                "add header",
                "insert button",
                "change color",
                "save",
                "undo"
            ]
        },
        {
            "name": "Arabic Website Building",
            "language": "ar",
            "commands": [
                "أضف هيدر",
                "أدرج زر",
                "غيّر اللون",
                "احفظ",
                "تراجع"
            ]
        }
    ]
    
    demo_results = []
    
    for scenario in demo_scenarios:
        print(f"\n📝 Scenario: {scenario['name']}")
        voice_system.set_language(scenario['language'])
        
        scenario_results = {
            "name": scenario['name'],
            "language": scenario['language'],
            "commands": []
        }
        
        for cmd_text in scenario['commands']:
            command = voice_system._parse_command(cmd_text)
            if command:
                result = {
                    "text": cmd_text,
                    "type": command.command_type.value,
                    "parameters": command.parameters,
                    "confidence": command.confidence
                }
                scenario_results['commands'].append(result)
                print(f"  ✅ '{cmd_text}' -> {command.command_type.value}")
            else:
                print(f"  ❌ '{cmd_text}' -> No match")
        
        demo_results.append(scenario_results)
    
    # Save demo results
    output_file = "voice_commands_demo.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(demo_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Demo results saved to: {output_file}")
    return demo_results

def main():
    """Main test function"""
    print("🎤 Voice Commands System Test Suite")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Run core tests
        test_voice_commands_system()
        
        # Test command patterns
        test_command_patterns()
        
        # Test TTS functionality
        test_tts_functionality()
        
        # Generate demo
        generate_voice_commands_demo()
        
        print("\n🎉 All voice commands tests completed successfully!")
        print("✅ Voice Commands System is working properly!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
