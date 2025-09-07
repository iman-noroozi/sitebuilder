#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Security System - Comprehensive Security Framework
Implements multi-layered security with encryption, authentication, and monitoring
"""

import hashlib
import hmac
import secrets
import jwt
import bcrypt
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging
import ipaddress
import re
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security levels for different operations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatType(Enum):
    """Types of security threats"""
    BRUTE_FORCE = "brute_force"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    CSRF = "csrf"
    DDOS = "ddos"
    MALWARE = "malware"
    PHISHING = "phishing"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DATA_BREACH = "data_breach"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"

@dataclass
class SecurityEvent:
    """Security event record"""
    id: str
    type: ThreatType
    level: SecurityLevel
    source_ip: str
    user_id: Optional[str]
    timestamp: datetime
    description: str
    details: Dict
    resolved: bool = False
    action_taken: Optional[str] = None

@dataclass
class UserSession:
    """User session information"""
    session_id: str
    user_id: str
    ip_address: str
    user_agent: str
    created_at: datetime
    last_activity: datetime
    is_active: bool = True
    security_level: SecurityLevel = SecurityLevel.MEDIUM

class AdvancedSecurity:
    """Advanced Security System with comprehensive protection"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or self._generate_secret_key()
        self.encryption_key = self._generate_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        
        # Security configurations
        self.max_login_attempts = 5
        self.lockout_duration = 300  # 5 minutes
        self.session_timeout = 3600  # 1 hour
        self.password_min_length = 8
        self.require_2fa = False
        
        # Security monitoring
        self.security_events: List[SecurityEvent] = []
        self.active_sessions: Dict[str, UserSession] = {}
        self.failed_attempts: Dict[str, List[datetime]] = defaultdict(list)
        self.blocked_ips: Dict[str, datetime] = {}
        self.suspicious_activities: Dict[str, List[datetime]] = defaultdict(list)
        
        # Rate limiting
        self.rate_limits: Dict[str, deque] = defaultdict(lambda: deque())
        self.rate_limit_config = {
            "login": {"max_attempts": 5, "window": 300},  # 5 attempts per 5 minutes
            "api": {"max_attempts": 100, "window": 3600},  # 100 requests per hour
            "password_reset": {"max_attempts": 3, "window": 3600},  # 3 attempts per hour
        }
        
        # Initialize security policies
        self._initialize_security_policies()
        
        logger.info("Advanced Security System initialized")
    
    def _generate_secret_key(self) -> str:
        """Generate a secure secret key"""
        return secrets.token_urlsafe(32)
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key"""
        return Fernet.generate_key()
    
    def _initialize_security_policies(self):
        """Initialize security policies and rules"""
        self.security_policies = {
            "password_policy": {
                "min_length": 8,
                "require_uppercase": True,
                "require_lowercase": True,
                "require_numbers": True,
                "require_special_chars": True,
                "forbidden_patterns": ["password", "123456", "qwerty"]
            },
            "session_policy": {
                "max_duration": 3600,
                "require_https": True,
                "secure_cookies": True,
                "same_site": "strict"
            },
            "ip_policy": {
                "max_connections_per_ip": 10,
                "block_suspicious_ips": True,
                "whitelist_ips": [],
                "blacklist_ips": []
            },
            "content_policy": {
                "block_xss": True,
                "block_sql_injection": True,
                "sanitize_input": True,
                "max_file_size": 10 * 1024 * 1024  # 10MB
            }
        }
    
    # Password Security
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def validate_password_strength(self, password: str) -> Tuple[bool, List[str]]:
        """Validate password strength"""
        errors = []
        policy = self.security_policies["password_policy"]
        
        if len(password) < policy["min_length"]:
            errors.append(f"Password must be at least {policy['min_length']} characters long")
        
        if policy["require_uppercase"] and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if policy["require_lowercase"] and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if policy["require_numbers"] and not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        if policy["require_special_chars"] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        for pattern in policy["forbidden_patterns"]:
            if pattern.lower() in password.lower():
                errors.append(f"Password cannot contain '{pattern}'")
        
        return len(errors) == 0, errors
    
    def generate_secure_password(self, length: int = 12) -> str:
        """Generate a secure random password"""
        import string
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    
    # Encryption/Decryption
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            encrypted = self.fernet.encrypt(data.encode('utf-8'))
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            decoded = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted = self.fernet.decrypt(decoded)
            return decrypted.decode('utf-8')
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise
    
    def generate_rsa_keypair(self) -> Tuple[str, str]:
        """Generate RSA key pair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        public_key = private_key.public_key()
        
        # Serialize keys
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem.decode('utf-8'), public_pem.decode('utf-8')
    
    # JWT Token Management
    def generate_jwt_token(self, user_id: str, additional_claims: Dict = None) -> str:
        """Generate JWT token"""
        payload = {
            "user_id": user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iss": "site_builder",
            "aud": "site_builder_users"
        }
        
        if additional_claims:
            payload.update(additional_claims)
        
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token
    
    def verify_jwt_token(self, token: str) -> Tuple[bool, Dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, {"error": "Token expired"}
        except jwt.InvalidTokenError:
            return False, {"error": "Invalid token"}
    
    def refresh_jwt_token(self, token: str) -> str:
        """Refresh JWT token"""
        is_valid, payload = self.verify_jwt_token(token)
        if is_valid:
            return self.generate_jwt_token(payload["user_id"], payload)
        else:
            raise ValueError("Invalid token for refresh")
    
    # Session Management
    def create_session(self, user_id: str, ip_address: str, user_agent: str) -> str:
        """Create a new user session"""
        session_id = secrets.token_urlsafe(32)
        
        session = UserSession(
            session_id=session_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        self.active_sessions[session_id] = session
        logger.info(f"Created session for user {user_id}")
        return session_id
    
    def validate_session(self, session_id: str) -> Tuple[bool, Optional[UserSession]]:
        """Validate user session"""
        if session_id not in self.active_sessions:
            return False, None
        
        session = self.active_sessions[session_id]
        
        # Check if session is expired
        if datetime.now() - session.last_activity > timedelta(seconds=self.session_timeout):
            self.active_sessions.pop(session_id, None)
            return False, None
        
        # Update last activity
        session.last_activity = datetime.now()
        return True, session
    
    def terminate_session(self, session_id: str):
        """Terminate user session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            logger.info(f"Terminated session {session_id}")
    
    def terminate_all_user_sessions(self, user_id: str):
        """Terminate all sessions for a user"""
        sessions_to_remove = [
            sid for sid, session in self.active_sessions.items()
            if session.user_id == user_id
        ]
        
        for session_id in sessions_to_remove:
            self.terminate_session(session_id)
        
        logger.info(f"Terminated all sessions for user {user_id}")
    
    # Rate Limiting
    def check_rate_limit(self, identifier: str, action: str) -> Tuple[bool, Dict]:
        """Check if action is within rate limits"""
        if action not in self.rate_limit_config:
            return True, {}
        
        config = self.rate_limit_config[action]
        now = time.time()
        
        # Clean old attempts
        while (self.rate_limits[identifier] and 
               self.rate_limits[identifier][0] < now - config["window"]):
            self.rate_limits[identifier].popleft()
        
        # Check if limit exceeded
        if len(self.rate_limits[identifier]) >= config["max_attempts"]:
            return False, {
                "limit_exceeded": True,
                "max_attempts": config["max_attempts"],
                "window": config["window"],
                "retry_after": int(self.rate_limits[identifier][0] + config["window"] - now)
            }
        
        # Add current attempt
        self.rate_limits[identifier].append(now)
        return True, {}
    
    # Input Validation and Sanitization
    def sanitize_input(self, input_data: str) -> str:
        """Sanitize user input to prevent XSS and injection attacks"""
        # Remove HTML tags
        import html
        sanitized = html.escape(input_data)
        
        # Remove potential SQL injection patterns
        sql_patterns = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
            r"(--|#|\/\*|\*\/)",
            r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
            r"(\b(OR|AND)\s+'.*'\s*=\s*'.*')"
        ]
        
        for pattern in sql_patterns:
            sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_ip_address(self, ip: str) -> bool:
        """Validate IP address format"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    # Security Monitoring
    def log_security_event(self, event_type: ThreatType, level: SecurityLevel, 
                          source_ip: str, description: str, details: Dict = None,
                          user_id: str = None):
        """Log a security event"""
        event = SecurityEvent(
            id=secrets.token_urlsafe(16),
            type=event_type,
            level=level,
            source_ip=source_ip,
            user_id=user_id,
            timestamp=datetime.now(),
            description=description,
            details=details or {}
        )
        
        self.security_events.append(event)
        
        # Keep only last 1000 events
        if len(self.security_events) > 1000:
            self.security_events = self.security_events[-1000:]
        
        logger.warning(f"Security event: {event_type.value} - {description}")
        
        # Take automatic actions based on threat level
        self._handle_security_event(event)
    
    def _handle_security_event(self, event: SecurityEvent):
        """Handle security event automatically"""
        if event.level == SecurityLevel.CRITICAL:
            # Block IP immediately
            self.block_ip(event.source_ip, duration=3600)  # 1 hour
            logger.critical(f"Blocked IP {event.source_ip} due to critical security event")
        
        elif event.level == SecurityLevel.HIGH:
            # Add to suspicious activities
            self.suspicious_activities[event.source_ip].append(datetime.now())
            
            # Block if too many suspicious activities
            if len(self.suspicious_activities[event.source_ip]) > 5:
                self.block_ip(event.source_ip, duration=1800)  # 30 minutes
    
    def block_ip(self, ip: str, duration: int = 3600):
        """Block IP address for specified duration"""
        self.blocked_ips[ip] = datetime.now() + timedelta(seconds=duration)
        logger.info(f"Blocked IP {ip} for {duration} seconds")
    
    def is_ip_blocked(self, ip: str) -> bool:
        """Check if IP is blocked"""
        if ip not in self.blocked_ips:
            return False
        
        if datetime.now() > self.blocked_ips[ip]:
            del self.blocked_ips[ip]
            return False
        
        return True
    
    def unblock_ip(self, ip: str):
        """Unblock IP address"""
        if ip in self.blocked_ips:
            del self.blocked_ips[ip]
            logger.info(f"Unblocked IP {ip}")
    
    # Brute Force Protection
    def record_failed_attempt(self, identifier: str, ip: str):
        """Record failed login attempt"""
        now = datetime.now()
        self.failed_attempts[identifier].append(now)
        
        # Clean old attempts
        cutoff = now - timedelta(seconds=self.lockout_duration)
        self.failed_attempts[identifier] = [
            attempt for attempt in self.failed_attempts[identifier]
            if attempt > cutoff
        ]
        
        # Check if should be locked out
        if len(self.failed_attempts[identifier]) >= self.max_login_attempts:
            self.log_security_event(
                ThreatType.BRUTE_FORCE,
                SecurityLevel.HIGH,
                ip,
                f"Brute force attack detected for {identifier}",
                {"attempts": len(self.failed_attempts[identifier])},
                identifier
            )
    
    def is_locked_out(self, identifier: str) -> bool:
        """Check if identifier is locked out"""
        if identifier not in self.failed_attempts:
            return False
        
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.lockout_duration)
        recent_attempts = [
            attempt for attempt in self.failed_attempts[identifier]
            if attempt > cutoff
        ]
        
        return len(recent_attempts) >= self.max_login_attempts
    
    def clear_failed_attempts(self, identifier: str):
        """Clear failed attempts for identifier"""
        if identifier in self.failed_attempts:
            del self.failed_attempts[identifier]
    
    # Two-Factor Authentication
    def generate_2fa_secret(self) -> str:
        """Generate 2FA secret key"""
        import pyotp
        return pyotp.random_base32()
    
    def generate_2fa_qr_code(self, user_email: str, secret: str) -> str:
        """Generate QR code for 2FA setup"""
        import pyotp
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=user_email,
            issuer_name="Site Builder"
        )
    
    def verify_2fa_code(self, secret: str, code: str) -> bool:
        """Verify 2FA code"""
        import pyotp
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)
    
    # Security Reports
    def get_security_report(self, hours: int = 24) -> Dict:
        """Generate security report"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_events = [
            event for event in self.security_events
            if event.timestamp > cutoff
        ]
        
        # Group events by type
        events_by_type = defaultdict(int)
        events_by_level = defaultdict(int)
        
        for event in recent_events:
            events_by_type[event.type.value] += 1
            events_by_level[event.level.value] += 1
        
        return {
            "period_hours": hours,
            "total_events": len(recent_events),
            "events_by_type": dict(events_by_type),
            "events_by_level": dict(events_by_level),
            "blocked_ips": len(self.blocked_ips),
            "active_sessions": len(self.active_sessions),
            "failed_attempts": sum(len(attempts) for attempts in self.failed_attempts.values()),
            "recent_events": [
                {
                    "type": event.type.value,
                    "level": event.level.value,
                    "source_ip": event.source_ip,
                    "description": event.description,
                    "timestamp": event.timestamp.isoformat()
                }
                for event in recent_events[-10:]  # Last 10 events
            ]
        }
    
    def get_security_status(self) -> Dict:
        """Get current security status"""
        return {
            "active_sessions": len(self.active_sessions),
            "blocked_ips": len(self.blocked_ips),
            "failed_attempts": len(self.failed_attempts),
            "suspicious_activities": len(self.suspicious_activities),
            "total_security_events": len(self.security_events),
            "security_level": "HIGH" if len(self.security_events) > 10 else "MEDIUM"
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize security system
    security = AdvancedSecurity()
    
    # Test password security
    print("🔐 Testing Password Security...")
    password = "MySecurePassword123!"
    is_valid, errors = security.validate_password_strength(password)
    print(f"Password valid: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    hashed = security.hash_password(password)
    print(f"Password hashed: {hashed[:20]}...")
    print(f"Password verified: {security.verify_password(password, hashed)}")
    
    # Test encryption
    print("\n🔒 Testing Encryption...")
    data = "Sensitive data to encrypt"
    encrypted = security.encrypt_data(data)
    print(f"Encrypted: {encrypted[:20]}...")
    decrypted = security.decrypt_data(encrypted)
    print(f"Decrypted: {decrypted}")
    
    # Test JWT tokens
    print("\n🎫 Testing JWT Tokens...")
    token = security.generate_jwt_token("user123", {"role": "admin"})
    print(f"Token generated: {token[:20]}...")
    is_valid, payload = security.verify_jwt_token(token)
    print(f"Token valid: {is_valid}")
    if is_valid:
        print(f"Payload: {payload}")
    
    # Test session management
    print("\n👤 Testing Session Management...")
    session_id = security.create_session("user123", "192.168.1.1", "Mozilla/5.0")
    print(f"Session created: {session_id[:20]}...")
    is_valid, session = security.validate_session(session_id)
    print(f"Session valid: {is_valid}")
    
    # Test rate limiting
    print("\n⏱️ Testing Rate Limiting...")
    for i in range(7):
        allowed, info = security.check_rate_limit("192.168.1.1", "login")
        print(f"Attempt {i+1}: Allowed: {allowed}")
        if not allowed:
            print(f"Rate limit info: {info}")
            break
    
    # Test input sanitization
    print("\n🧹 Testing Input Sanitization...")
    malicious_input = "<script>alert('XSS')</script>SELECT * FROM users"
    sanitized = security.sanitize_input(malicious_input)
    print(f"Original: {malicious_input}")
    print(f"Sanitized: {sanitized}")
    
    # Test security monitoring
    print("\n🛡️ Testing Security Monitoring...")
    security.log_security_event(
        ThreatType.BRUTE_FORCE,
        SecurityLevel.HIGH,
        "192.168.1.100",
        "Multiple failed login attempts",
        {"attempts": 10}
    )
    
    report = security.get_security_report()
    print(f"Security report: {report}")
    
    print("\n✅ All security tests completed!")
