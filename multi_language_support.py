#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Language Support System - Comprehensive Internationalization
Supports 50+ languages with RTL/LTR, localization, and cultural adaptation
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import logging
from pathlib import Path
import babel
from babel import Locale, numbers, dates, core
import googletrans
from googletrans import Translator
import langdetect
from langdetect import detect, detect_langs

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LanguageDirection(Enum):
    """Text direction for languages"""
    LTR = "ltr"  # Left-to-Right
    RTL = "rtl"  # Right-to-Left

class LanguageFamily(Enum):
    """Language families"""
    INDO_EUROPEAN = "indo_european"
    SEMITIC = "semitic"
    SINO_TIBETAN = "sino_tibetan"
    NIGER_CONGO = "niger_congo"
    AUSTROASIATIC = "austroasiatic"
    URALIC = "uralic"
    ALTAIC = "altaic"
    DRAVIDIAN = "dravidian"
    AUSTRONESIAN = "austronesian"

@dataclass
class Language:
    """Language information"""
    code: str
    name: str
    native_name: str
    direction: LanguageDirection
    family: LanguageFamily
    region: str
    script: str
    is_rtl: bool = False
    plural_forms: int = 2
    date_format: str = "%Y-%m-%d"
    time_format: str = "%H:%M:%S"
    number_format: str = "en_US"
    currency: str = "USD"
    locale: str = "en_US"

@dataclass
class Translation:
    """Translation entry"""
    key: str
    text: str
    language: str
    context: Optional[str] = None
    plural_forms: Optional[Dict[str, str]] = None
    variables: Optional[Dict[str, Any]] = None

class MultiLanguageSupport:
    """Comprehensive Multi-Language Support System"""
    
    def __init__(self, translations_dir: str = "translations"):
        self.translations_dir = Path(translations_dir)
        self.translations_dir.mkdir(exist_ok=True)
        
        # Initialize translator
        self.translator = Translator()
        
        # Supported languages
        self.supported_languages = self._initialize_supported_languages()
        
        # Current language
        self.current_language = "en"
        self.fallback_language = "en"
        
        # Translation cache
        self.translation_cache = {}
        
        # Load translations
        self._load_translations()
        
        logger.info(f"Multi-Language Support initialized with {len(self.supported_languages)} languages")
    
    def _initialize_supported_languages(self) -> Dict[str, Language]:
        """Initialize supported languages"""
        languages = {
            # European Languages
            "en": Language("en", "English", "English", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "US", "Latin"),
            "es": Language("es", "Spanish", "Español", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "ES", "Latin"),
            "fr": Language("fr", "French", "Français", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "FR", "Latin"),
            "de": Language("de", "German", "Deutsch", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "DE", "Latin"),
            "it": Language("it", "Italian", "Italiano", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "IT", "Latin"),
            "pt": Language("pt", "Portuguese", "Português", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "PT", "Latin"),
            "ru": Language("ru", "Russian", "Русский", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "RU", "Cyrillic"),
            "pl": Language("pl", "Polish", "Polski", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "PL", "Latin"),
            "nl": Language("nl", "Dutch", "Nederlands", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "NL", "Latin"),
            "sv": Language("sv", "Swedish", "Svenska", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "SE", "Latin"),
            "no": Language("no", "Norwegian", "Norsk", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "NO", "Latin"),
            "da": Language("da", "Danish", "Dansk", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "DK", "Latin"),
            "fi": Language("fi", "Finnish", "Suomi", LanguageDirection.LTR, LanguageFamily.URALIC, "FI", "Latin"),
            "el": Language("el", "Greek", "Ελληνικά", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "GR", "Greek"),
            "tr": Language("tr", "Turkish", "Türkçe", LanguageDirection.LTR, LanguageFamily.ALTAIC, "TR", "Latin"),
            
            # Middle Eastern & African Languages
            "ar": Language("ar", "Arabic", "العربية", LanguageDirection.RTL, LanguageFamily.SEMITIC, "SA", "Arabic", True),
            "fa": Language("fa", "Persian", "فارسی", LanguageDirection.RTL, LanguageFamily.INDO_EUROPEAN, "IR", "Arabic", True),
            "ur": Language("ur", "Urdu", "اردو", LanguageDirection.RTL, LanguageFamily.INDO_EUROPEAN, "PK", "Arabic", True),
            "he": Language("he", "Hebrew", "עברית", LanguageDirection.RTL, LanguageFamily.SEMITIC, "IL", "Hebrew", True),
            "ku": Language("ku", "Kurdish", "Kurdî", LanguageDirection.RTL, LanguageFamily.INDO_EUROPEAN, "IQ", "Arabic", True),
            "am": Language("am", "Amharic", "አማርኛ", LanguageDirection.LTR, LanguageFamily.SEMITIC, "ET", "Ethiopic"),
            "sw": Language("sw", "Swahili", "Kiswahili", LanguageDirection.LTR, LanguageFamily.NIGER_CONGO, "KE", "Latin"),
            
            # Asian Languages
            "zh": Language("zh", "Chinese", "中文", LanguageDirection.LTR, LanguageFamily.SINO_TIBETAN, "CN", "Han"),
            "ja": Language("ja", "Japanese", "日本語", LanguageDirection.LTR, LanguageFamily.SINO_TIBETAN, "JP", "Hiragana"),
            "ko": Language("ko", "Korean", "한국어", LanguageDirection.LTR, LanguageFamily.SINO_TIBETAN, "KR", "Hangul"),
            "hi": Language("hi", "Hindi", "हिन्दी", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "IN", "Devanagari"),
            "bn": Language("bn", "Bengali", "বাংলা", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "BD", "Bengali"),
            "ta": Language("ta", "Tamil", "தமிழ்", LanguageDirection.LTR, LanguageFamily.DRAVIDIAN, "IN", "Tamil"),
            "te": Language("te", "Telugu", "తెలుగు", LanguageDirection.LTR, LanguageFamily.DRAVIDIAN, "IN", "Telugu"),
            "th": Language("th", "Thai", "ไทย", LanguageDirection.LTR, LanguageFamily.AUSTROASIATIC, "TH", "Thai"),
            "vi": Language("vi", "Vietnamese", "Tiếng Việt", LanguageDirection.LTR, LanguageFamily.AUSTROASIATIC, "VN", "Latin"),
            "id": Language("id", "Indonesian", "Bahasa Indonesia", LanguageDirection.LTR, LanguageFamily.AUSTRONESIAN, "ID", "Latin"),
            "ms": Language("ms", "Malay", "Bahasa Melayu", LanguageDirection.LTR, LanguageFamily.AUSTRONESIAN, "MY", "Latin"),
            "tl": Language("tl", "Filipino", "Filipino", LanguageDirection.LTR, LanguageFamily.AUSTRONESIAN, "PH", "Latin"),
            
            # Other Languages
            "uk": Language("uk", "Ukrainian", "Українська", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "UA", "Cyrillic"),
            "cs": Language("cs", "Czech", "Čeština", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "CZ", "Latin"),
            "sk": Language("sk", "Slovak", "Slovenčina", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "SK", "Latin"),
            "hr": Language("hr", "Croatian", "Hrvatski", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "HR", "Latin"),
            "sr": Language("sr", "Serbian", "Српски", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "RS", "Cyrillic"),
            "bg": Language("bg", "Bulgarian", "Български", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "BG", "Cyrillic"),
            "ro": Language("ro", "Romanian", "Română", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "RO", "Latin"),
            "hu": Language("hu", "Hungarian", "Magyar", LanguageDirection.LTR, LanguageFamily.URALIC, "HU", "Latin"),
            "et": Language("et", "Estonian", "Eesti", LanguageDirection.LTR, LanguageFamily.URALIC, "EE", "Latin"),
            "lv": Language("lv", "Latvian", "Latviešu", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "LV", "Latin"),
            "lt": Language("lt", "Lithuanian", "Lietuvių", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "LT", "Latin"),
            "sl": Language("sl", "Slovenian", "Slovenščina", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "SI", "Latin"),
            "mt": Language("mt", "Maltese", "Malti", LanguageDirection.LTR, LanguageFamily.SEMITIC, "MT", "Latin"),
            "is": Language("is", "Icelandic", "Íslenska", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "IS", "Latin"),
            "ga": Language("ga", "Irish", "Gaeilge", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "IE", "Latin"),
            "cy": Language("cy", "Welsh", "Cymraeg", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "GB", "Latin"),
            "eu": Language("eu", "Basque", "Euskera", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "ES", "Latin"),
            "ca": Language("ca", "Catalan", "Català", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "ES", "Latin"),
            "gl": Language("gl", "Galician", "Galego", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "ES", "Latin"),
            "sq": Language("sq", "Albanian", "Shqip", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "AL", "Latin"),
            "mk": Language("mk", "Macedonian", "Македонски", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "MK", "Cyrillic"),
            "be": Language("be", "Belarusian", "Беларуская", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "BY", "Cyrillic"),
            "ka": Language("ka", "Georgian", "ქართული", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "GE", "Georgian"),
            "hy": Language("hy", "Armenian", "Հայերեն", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "AM", "Armenian"),
            "az": Language("az", "Azerbaijani", "Azərbaycan", LanguageDirection.LTR, LanguageFamily.ALTAIC, "AZ", "Latin"),
            "kk": Language("kk", "Kazakh", "Қазақша", LanguageDirection.LTR, LanguageFamily.ALTAIC, "KZ", "Cyrillic"),
            "ky": Language("ky", "Kyrgyz", "Кыргызча", LanguageDirection.LTR, LanguageFamily.ALTAIC, "KG", "Cyrillic"),
            "uz": Language("uz", "Uzbek", "O'zbek", LanguageDirection.LTR, LanguageFamily.ALTAIC, "UZ", "Latin"),
            "tg": Language("tg", "Tajik", "Тоҷикӣ", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "TJ", "Cyrillic"),
            "mn": Language("mn", "Mongolian", "Монгол", LanguageDirection.LTR, LanguageFamily.ALTAIC, "MN", "Cyrillic"),
            "my": Language("my", "Burmese", "မြန်မာ", LanguageDirection.LTR, LanguageFamily.SINO_TIBETAN, "MM", "Myanmar"),
            "km": Language("km", "Khmer", "ខ្មែរ", LanguageDirection.LTR, LanguageFamily.AUSTROASIATIC, "KH", "Khmer"),
            "lo": Language("lo", "Lao", "ລາວ", LanguageDirection.LTR, LanguageFamily.SINO_TIBETAN, "LA", "Lao"),
            "si": Language("si", "Sinhala", "සිංහල", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "LK", "Sinhala"),
            "ne": Language("ne", "Nepali", "नेपाली", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "NP", "Devanagari"),
            "gu": Language("gu", "Gujarati", "ગુજરાતી", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "IN", "Gujarati"),
            "pa": Language("pa", "Punjabi", "ਪੰਜਾਬੀ", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "IN", "Gurmukhi"),
            "or": Language("or", "Odia", "ଓଡ଼ିଆ", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "IN", "Odia"),
            "as": Language("as", "Assamese", "অসমীয়া", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "IN", "Assamese"),
            "ml": Language("ml", "Malayalam", "മലയാളം", LanguageDirection.LTR, LanguageFamily.DRAVIDIAN, "IN", "Malayalam"),
            "kn": Language("kn", "Kannada", "ಕನ್ನಡ", LanguageDirection.LTR, LanguageFamily.DRAVIDIAN, "IN", "Kannada"),
            "mr": Language("mr", "Marathi", "मराठी", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "IN", "Devanagari"),
            "sa": Language("sa", "Sanskrit", "संस्कृतम्", LanguageDirection.LTR, LanguageFamily.INDO_EUROPEAN, "IN", "Devanagari"),
        }
        
        return languages
    
    def _load_translations(self):
        """Load translation files"""
        for lang_code in self.supported_languages:
            translation_file = self.translations_dir / f"{lang_code}.json"
            if translation_file.exists():
                try:
                    with open(translation_file, 'r', encoding='utf-8') as f:
                        self.translation_cache[lang_code] = json.load(f)
                except Exception as e:
                    logger.error(f"Error loading translations for {lang_code}: {e}")
            else:
                # Create default translation file
                self._create_default_translations(lang_code)
    
    def _create_default_translations(self, lang_code: str):
        """Create default translation file for a language"""
        default_translations = {
            "common": {
                "save": "Save",
                "cancel": "Cancel",
                "delete": "Delete",
                "edit": "Edit",
                "add": "Add",
                "remove": "Remove",
                "search": "Search",
                "filter": "Filter",
                "sort": "Sort",
                "loading": "Loading...",
                "error": "Error",
                "success": "Success",
                "warning": "Warning",
                "info": "Information",
                "yes": "Yes",
                "no": "No",
                "ok": "OK",
                "close": "Close",
                "back": "Back",
                "next": "Next",
                "previous": "Previous",
                "submit": "Submit",
                "reset": "Reset",
                "clear": "Clear",
                "select": "Select",
                "all": "All",
                "none": "None",
                "required": "Required",
                "optional": "Optional"
            },
            "navigation": {
                "home": "Home",
                "about": "About",
                "contact": "Contact",
                "services": "Services",
                "products": "Products",
                "blog": "Blog",
                "news": "News",
                "help": "Help",
                "support": "Support",
                "settings": "Settings",
                "profile": "Profile",
                "logout": "Logout",
                "login": "Login",
                "register": "Register",
                "dashboard": "Dashboard",
                "admin": "Admin"
            },
            "forms": {
                "name": "Name",
                "email": "Email",
                "password": "Password",
                "confirm_password": "Confirm Password",
                "phone": "Phone",
                "address": "Address",
                "city": "City",
                "country": "Country",
                "zip_code": "ZIP Code",
                "message": "Message",
                "subject": "Subject",
                "description": "Description",
                "title": "Title",
                "content": "Content",
                "category": "Category",
                "tags": "Tags",
                "date": "Date",
                "time": "Time",
                "price": "Price",
                "quantity": "Quantity",
                "total": "Total",
                "subtotal": "Subtotal",
                "tax": "Tax",
                "discount": "Discount"
            },
            "messages": {
                "welcome": "Welcome",
                "goodbye": "Goodbye",
                "thank_you": "Thank you",
                "please_wait": "Please wait",
                "operation_successful": "Operation successful",
                "operation_failed": "Operation failed",
                "invalid_input": "Invalid input",
                "field_required": "This field is required",
                "email_invalid": "Invalid email address",
                "password_too_short": "Password is too short",
                "passwords_dont_match": "Passwords don't match",
                "login_successful": "Login successful",
                "login_failed": "Login failed",
                "logout_successful": "Logout successful",
                "registration_successful": "Registration successful",
                "registration_failed": "Registration failed",
                "data_saved": "Data saved successfully",
                "data_deleted": "Data deleted successfully",
                "confirm_delete": "Are you sure you want to delete this item?",
                "no_data_found": "No data found",
                "loading_data": "Loading data...",
                "saving_data": "Saving data...",
                "deleting_data": "Deleting data..."
            },
            "time": {
                "now": "Now",
                "today": "Today",
                "yesterday": "Yesterday",
                "tomorrow": "Tomorrow",
                "this_week": "This week",
                "last_week": "Last week",
                "next_week": "Next week",
                "this_month": "This month",
                "last_month": "Last month",
                "next_month": "Next month",
                "this_year": "This year",
                "last_year": "Last year",
                "next_year": "Next year",
                "january": "January",
                "february": "February",
                "march": "March",
                "april": "April",
                "may": "May",
                "june": "June",
                "july": "July",
                "august": "August",
                "september": "September",
                "october": "October",
                "november": "November",
                "december": "December",
                "monday": "Monday",
                "tuesday": "Tuesday",
                "wednesday": "Wednesday",
                "thursday": "Thursday",
                "friday": "Friday",
                "saturday": "Saturday",
                "sunday": "Sunday"
            }
        }
        
        # Translate to target language if not English
        if lang_code != "en":
            try:
                translated = self._translate_dictionary(default_translations, lang_code)
                self.translation_cache[lang_code] = translated
            except Exception as e:
                logger.error(f"Error translating default translations to {lang_code}: {e}")
                self.translation_cache[lang_code] = default_translations
        
        # Save to file
        translation_file = self.translations_dir / f"{lang_code}.json"
        try:
            with open(translation_file, 'w', encoding='utf-8') as f:
                json.dump(self.translation_cache[lang_code], f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving translations for {lang_code}: {e}")
    
    def _translate_dictionary(self, dictionary: Dict, target_lang: str) -> Dict:
        """Translate a dictionary to target language"""
        translated = {}
        
        for key, value in dictionary.items():
            if isinstance(value, dict):
                translated[key] = self._translate_dictionary(value, target_lang)
            elif isinstance(value, str):
                try:
                    translated_text = self.translator.translate(value, dest=target_lang).text
                    translated[key] = translated_text
                except Exception as e:
                    logger.error(f"Translation error for '{value}': {e}")
                    translated[key] = value
            else:
                translated[key] = value
        
        return translated
    
    def set_language(self, language_code: str):
        """Set current language"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            logger.info(f"Language set to: {language_code}")
        else:
            logger.warning(f"Unsupported language: {language_code}")
    
    def get_language(self) -> str:
        """Get current language"""
        return self.current_language
    
    def get_supported_languages(self) -> List[Language]:
        """Get list of supported languages"""
        return list(self.supported_languages.values())
    
    def get_language_info(self, language_code: str) -> Optional[Language]:
        """Get language information"""
        return self.supported_languages.get(language_code)
    
    def translate(self, key: str, language: str = None, **kwargs) -> str:
        """Translate a key to specified language"""
        target_lang = language or self.current_language
        
        if target_lang not in self.translation_cache:
            target_lang = self.fallback_language
        
        # Navigate through nested keys (e.g., "common.save")
        keys = key.split('.')
        translation = self.translation_cache[target_lang]
        
        try:
            for k in keys:
                translation = translation[k]
            
            # Handle variables in translation
            if kwargs:
                translation = translation.format(**kwargs)
            
            return translation
        except (KeyError, TypeError):
            # Fallback to English if translation not found
            if target_lang != self.fallback_language:
                return self.translate(key, self.fallback_language, **kwargs)
            else:
                return key  # Return key if no translation found
    
    def add_translation(self, key: str, text: str, language: str = None):
        """Add or update a translation"""
        target_lang = language or self.current_language
        
        if target_lang not in self.translation_cache:
            self.translation_cache[target_lang] = {}
        
        # Navigate to nested key location
        keys = key.split('.')
        current = self.translation_cache[target_lang]
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = text
        
        # Save to file
        self._save_translations(target_lang)
    
    def _save_translations(self, language: str):
        """Save translations to file"""
        translation_file = self.translations_dir / f"{language}.json"
        try:
            with open(translation_file, 'w', encoding='utf-8') as f:
                json.dump(self.translation_cache[language], f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving translations for {language}: {e}")
    
    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        try:
            detected = detect(text)
            return detected
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return self.fallback_language
    
    def detect_languages(self, text: str) -> List[Tuple[str, float]]:
        """Detect multiple possible languages with confidence scores"""
        try:
            languages = detect_langs(text)
            return [(lang.lang, lang.prob) for lang in languages]
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return [(self.fallback_language, 1.0)]
    
    def auto_translate(self, text: str, target_language: str = None) -> str:
        """Automatically translate text to target language"""
        target_lang = target_language or self.current_language
        
        if target_lang == "en":
            return text
        
        try:
            translated = self.translator.translate(text, dest=target_lang).text
            return translated
        except Exception as e:
            logger.error(f"Auto-translation error: {e}")
            return text
    
    def format_number(self, number: float, language: str = None) -> str:
        """Format number according to language locale"""
        target_lang = language or self.current_language
        lang_info = self.get_language_info(target_lang)
        
        if lang_info:
            try:
                locale = Locale(lang_info.locale)
                return numbers.format_number(number, locale=locale)
            except Exception as e:
                logger.error(f"Number formatting error: {e}")
        
        return str(number)
    
    def format_currency(self, amount: float, currency: str = None, language: str = None) -> str:
        """Format currency according to language locale"""
        target_lang = language or self.current_language
        lang_info = self.get_language_info(target_lang)
        
        if lang_info:
            try:
                locale = Locale(lang_info.locale)
                currency_code = currency or lang_info.currency
                return numbers.format_currency(amount, currency_code, locale=locale)
            except Exception as e:
                logger.error(f"Currency formatting error: {e}")
        
        return f"{amount} {currency or 'USD'}"
    
    def format_date(self, date: datetime, format_type: str = "medium", language: str = None) -> str:
        """Format date according to language locale"""
        target_lang = language or self.current_language
        lang_info = self.get_language_info(target_lang)
        
        if lang_info:
            try:
                locale = Locale(lang_info.locale)
                return dates.format_date(date, format=format_type, locale=locale)
            except Exception as e:
                logger.error(f"Date formatting error: {e}")
        
        return date.strftime("%Y-%m-%d")
    
    def format_time(self, time: datetime, format_type: str = "medium", language: str = None) -> str:
        """Format time according to language locale"""
        target_lang = language or self.current_language
        lang_info = self.get_language_info(target_lang)
        
        if lang_info:
            try:
                locale = Locale(lang_info.locale)
                return dates.format_time(time, format=format_type, locale=locale)
            except Exception as e:
                logger.error(f"Time formatting error: {e}")
        
        return time.strftime("%H:%M:%S")
    
    def format_datetime(self, datetime_obj: datetime, format_type: str = "medium", language: str = None) -> str:
        """Format datetime according to language locale"""
        target_lang = language or self.current_language
        lang_info = self.get_language_info(target_lang)
        
        if lang_info:
            try:
                locale = Locale(lang_info.locale)
                return dates.format_datetime(datetime_obj, format=format_type, locale=locale)
            except Exception as e:
                logger.error(f"DateTime formatting error: {e}")
        
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_text_direction(self, language: str = None) -> str:
        """Get text direction for language"""
        target_lang = language or self.current_language
        lang_info = self.get_language_info(target_lang)
        
        if lang_info:
            return lang_info.direction.value
        
        return LanguageDirection.LTR.value
    
    def is_rtl_language(self, language: str = None) -> bool:
        """Check if language is RTL"""
        target_lang = language or self.current_language
        lang_info = self.get_language_info(target_lang)
        
        if lang_info:
            return lang_info.is_rtl
        
        return False
    
    def get_plural_form(self, count: int, language: str = None) -> str:
        """Get plural form for count"""
        target_lang = language or self.current_language
        lang_info = self.get_language_info(target_lang)
        
        if lang_info:
            try:
                locale = Locale(lang_info.locale)
                return core.get_plural_rule(locale)(count)
            except Exception as e:
                logger.error(f"Plural form error: {e}")
        
        return "other" if count != 1 else "one"
    
    def get_language_family(self, language: str = None) -> str:
        """Get language family"""
        target_lang = language or self.current_language
        lang_info = self.get_language_info(target_lang)
        
        if lang_info:
            return lang_info.family.value
        
        return LanguageFamily.INDO_EUROPEAN.value
    
    def get_related_languages(self, language: str = None) -> List[str]:
        """Get related languages in the same family"""
        target_lang = language or self.current_language
        lang_info = self.get_language_info(target_lang)
        
        if lang_info:
            family = lang_info.family
            return [
                code for code, info in self.supported_languages.items()
                if info.family == family and code != target_lang
            ]
        
        return []
    
    def export_translations(self, language: str, format: str = "json") -> str:
        """Export translations in specified format"""
        if language not in self.translation_cache:
            return ""
        
        translations = self.translation_cache[language]
        
        if format.lower() == "json":
            return json.dumps(translations, ensure_ascii=False, indent=2)
        elif format.lower() == "csv":
            # Convert to CSV format
            csv_lines = ["Key,Translation"]
            for key, value in self._flatten_dict(translations):
                csv_lines.append(f'"{key}","{value}"')
            return "\n".join(csv_lines)
        else:
            return str(translations)
    
    def _flatten_dict(self, d: Dict, parent_key: str = "") -> List[Tuple[str, str]]:
        """Flatten nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key))
            else:
                items.append((new_key, str(v)))
        return items
    
    def import_translations(self, language: str, translations_data: str, format: str = "json"):
        """Import translations from specified format"""
        try:
            if format.lower() == "json":
                translations = json.loads(translations_data)
            elif format.lower() == "csv":
                # Parse CSV format
                lines = translations_data.strip().split('\n')
                translations = {}
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        key, value = line.split(',', 1)
                        key = key.strip('"')
                        value = value.strip('"')
                        self._set_nested_key(translations, key, value)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.translation_cache[language] = translations
            self._save_translations(language)
            logger.info(f"Imported translations for {language}")
            
        except Exception as e:
            logger.error(f"Import error for {language}: {e}")
    
    def _set_nested_key(self, d: Dict, key: str, value: str):
        """Set nested key in dictionary"""
        keys = key.split('.')
        current = d
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
    
    def get_translation_stats(self) -> Dict[str, int]:
        """Get translation statistics"""
        stats = {}
        for lang_code in self.supported_languages:
            if lang_code in self.translation_cache:
                translations = self.translation_cache[lang_code]
                stats[lang_code] = len(self._flatten_dict(translations))
            else:
                stats[lang_code] = 0
        return stats

# Example usage and testing
if __name__ == "__main__":
    # Initialize multi-language support
    ml_support = MultiLanguageSupport()
    
    # Test language detection
    print("🌍 Testing Language Detection...")
    test_texts = [
        "Hello, how are you?",
        "مرحبا، كيف حالك؟",
        "Bonjour, comment allez-vous?",
        "Hola, ¿cómo estás?",
        "Привет, как дела?",
        "你好，你好吗？",
        "こんにちは、元気ですか？",
        "안녕하세요, 어떻게 지내세요?"
    ]
    
    for text in test_texts:
        detected = ml_support.detect_language(text)
        print(f"✅ '{text[:20]}...' -> {detected}")
    
    # Test translation
    print("\n🔄 Testing Translation...")
    ml_support.set_language("fa")
    translated = ml_support.translate("common.save")
    print(f"✅ 'common.save' in Persian: {translated}")
    
    ml_support.set_language("ar")
    translated = ml_support.translate("common.save")
    print(f"✅ 'common.save' in Arabic: {translated}")
    
    # Test auto-translation
    print("\n🤖 Testing Auto-Translation...")
    english_text = "Welcome to our website"
    persian_text = ml_support.auto_translate(english_text, "fa")
    print(f"✅ English: {english_text}")
    print(f"✅ Persian: {persian_text}")
    
    # Test formatting
    print("\n📊 Testing Formatting...")
    now = datetime.now()
    ml_support.set_language("fa")
    formatted_date = ml_support.format_date(now)
    formatted_number = ml_support.format_number(1234.56)
    formatted_currency = ml_support.format_currency(99.99)
    print(f"✅ Date: {formatted_date}")
    print(f"✅ Number: {formatted_number}")
    print(f"✅ Currency: {formatted_currency}")
    
    # Test RTL detection
    print("\n📝 Testing RTL Detection...")
    rtl_languages = ["ar", "fa", "he", "ur"]
    for lang in rtl_languages:
        is_rtl = ml_support.is_rtl_language(lang)
        direction = ml_support.get_text_direction(lang)
        print(f"✅ {lang}: RTL={is_rtl}, Direction={direction}")
    
    # Test language info
    print("\nℹ️ Testing Language Info...")
    lang_info = ml_support.get_language_info("fa")
    if lang_info:
        print(f"✅ Persian: {lang_info.native_name}, Family: {lang_info.family.value}, Script: {lang_info.script}")
    
    # Test translation stats
    print("\n📈 Testing Translation Stats...")
    stats = ml_support.get_translation_stats()
    for lang, count in list(stats.items())[:5]:
        print(f"✅ {lang}: {count} translations")
    
    print("\n✅ All multi-language tests completed!")
