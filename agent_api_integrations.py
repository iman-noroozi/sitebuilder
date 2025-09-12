#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 Agent API Integrations - سیستم یکپارچه‌سازی API های مختلف
قابلیت‌های پیشرفته:
- اتصال به 100+ API مختلف
- مدیریت Authentication
- Rate Limiting و Retry Logic
- Real-time Monitoring
- Custom API Builder
"""

import os
import json
import asyncio
import aiohttp
import hashlib
import hmac
import base64
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging
from urllib.parse import urlencode, urlparse
import jwt
import requests
from requests_oauthlib import OAuth2Session

class APIType(Enum):
    """انواع API"""
    REST = "rest"
    GRAPHQL = "graphql"
    SOAP = "soap"
    WEBHOOK = "webhook"
    WEBSOCKET = "websocket"

class AuthType(Enum):
    """انواع Authentication"""
    NONE = "none"
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer_token"
    BASIC_AUTH = "basic_auth"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    HMAC = "hmac"

@dataclass
class APIConfig:
    """تنظیمات API"""
    name: str
    base_url: str
    api_type: APIType
    auth_type: AuthType
    auth_config: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    rate_limit: int = 100  # requests per minute
    timeout: int = 30
    retry_attempts: int = 3
    endpoints: Dict[str, Dict] = field(default_factory=dict)

@dataclass
class APIRequest:
    """درخواست API"""
    method: str
    endpoint: str
    params: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    body: Any = None
    timeout: Optional[int] = None

@dataclass
class APIResponse:
    """پاسخ API"""
    status_code: int
    data: Any
    headers: Dict[str, str]
    success: bool
    error: Optional[str] = None
    execution_time: float = 0.0

class AgentAPIIntegrations:
    """سیستم یکپارچه‌سازی API ها"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.api_configs = {}
        self.http_client = None
        self.rate_limits = {}
        self.request_history = []
        
        # تنظیم logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # API های پیش‌تعریف شده
        self.predefined_apis = self._load_predefined_apis()
        
    async def initialize(self):
        """مقداردهی اولیه"""
        self.http_client = aiohttp.ClientSession()
        await self._load_api_configs()
    
    async def close(self):
        """بستن منابع"""
        if self.http_client:
            await self.http_client.close()
    
    def _load_predefined_apis(self) -> Dict[str, APIConfig]:
        """بارگذاری API های پیش‌تعریف شده"""
        return {
            # Social Media APIs
            "twitter": APIConfig(
                name="Twitter API",
                base_url="https://api.twitter.com/2",
                api_type=APIType.REST,
                auth_type=AuthType.BEARER_TOKEN,
                rate_limit=300,
                endpoints={
                    "tweet": {
                        "method": "POST",
                        "path": "/tweets",
                        "description": "ارسال توییت"
                    },
                    "search": {
                        "method": "GET",
                        "path": "/tweets/search/recent",
                        "description": "جستجوی توییت‌ها"
                    }
                }
            ),
            
            "instagram": APIConfig(
                name="Instagram API",
                base_url="https://graph.instagram.com",
                api_type=APIType.REST,
                auth_type=AuthType.OAUTH2,
                rate_limit=200,
                endpoints={
                    "post": {
                        "method": "POST",
                        "path": "/{user-id}/media",
                        "description": "ارسال پست"
                    },
                    "stories": {
                        "method": "POST",
                        "path": "/{user-id}/media",
                        "description": "ارسال استوری"
                    }
                }
            ),
            
            # Communication APIs
            "telegram": APIConfig(
                name="Telegram Bot API",
                base_url="https://api.telegram.org/bot{token}",
                api_type=APIType.REST,
                auth_type=AuthType.API_KEY,
                rate_limit=30,
                endpoints={
                    "send_message": {
                        "method": "POST",
                        "path": "/sendMessage",
                        "description": "ارسال پیام"
                    },
                    "send_photo": {
                        "method": "POST",
                        "path": "/sendPhoto",
                        "description": "ارسال عکس"
                    }
                }
            ),
            
            "whatsapp": APIConfig(
                name="WhatsApp Business API",
                base_url="https://graph.facebook.com/v17.0",
                api_type=APIType.REST,
                auth_type=AuthType.BEARER_TOKEN,
                rate_limit=1000,
                endpoints={
                    "send_message": {
                        "method": "POST",
                        "path": "/{phone-number-id}/messages",
                        "description": "ارسال پیام واتساپ"
                    }
                }
            ),
            
            # Email APIs
            "sendgrid": APIConfig(
                name="SendGrid API",
                base_url="https://api.sendgrid.com/v3",
                api_type=APIType.REST,
                auth_type=AuthType.API_KEY,
                rate_limit=600,
                endpoints={
                    "send_email": {
                        "method": "POST",
                        "path": "/mail/send",
                        "description": "ارسال ایمیل"
                    }
                }
            ),
            
            "mailgun": APIConfig(
                name="Mailgun API",
                base_url="https://api.mailgun.net/v3",
                api_type=APIType.REST,
                auth_type=AuthType.BASIC_AUTH,
                rate_limit=10000,
                endpoints={
                    "send_email": {
                        "method": "POST",
                        "path": "/{domain}/messages",
                        "description": "ارسال ایمیل"
                    }
                }
            ),
            
            # Payment APIs
            "stripe": APIConfig(
                name="Stripe API",
                base_url="https://api.stripe.com/v1",
                api_type=APIType.REST,
                auth_type=AuthType.API_KEY,
                rate_limit=100,
                endpoints={
                    "create_payment": {
                        "method": "POST",
                        "path": "/payment_intents",
                        "description": "ایجاد پرداخت"
                    },
                    "create_customer": {
                        "method": "POST",
                        "path": "/customers",
                        "description": "ایجاد مشتری"
                    }
                }
            ),
            
            "paypal": APIConfig(
                name="PayPal API",
                base_url="https://api-m.paypal.com/v2",
                api_type=APIType.REST,
                auth_type=AuthType.OAUTH2,
                rate_limit=500,
                endpoints={
                    "create_order": {
                        "method": "POST",
                        "path": "/checkout/orders",
                        "description": "ایجاد سفارش"
                    }
                }
            ),
            
            # Database APIs
            "firebase": APIConfig(
                name="Firebase API",
                base_url="https://firestore.googleapis.com/v1",
                api_type=APIType.REST,
                auth_type=AuthType.BEARER_TOKEN,
                rate_limit=1000,
                endpoints={
                    "get_document": {
                        "method": "GET",
                        "path": "/projects/{project}/databases/{database}/documents/{collection}/{document}",
                        "description": "دریافت سند"
                    },
                    "set_document": {
                        "method": "PATCH",
                        "path": "/projects/{project}/databases/{database}/documents/{collection}/{document}",
                        "description": "ذخیره سند"
                    }
                }
            ),
            
            "mongodb": APIConfig(
                name="MongoDB Atlas API",
                base_url="https://data.mongodb-api.com/app/{app}/endpoint/data/v1",
                api_type=APIType.REST,
                auth_type=AuthType.API_KEY,
                rate_limit=1000,
                endpoints={
                    "find": {
                        "method": "POST",
                        "path": "/action/find",
                        "description": "جستجو در دیتابیس"
                    },
                    "insert": {
                        "method": "POST",
                        "path": "/action/insertOne",
                        "description": "درج سند"
                    }
                }
            ),
            
            # AI APIs
            "openai": APIConfig(
                name="OpenAI API",
                base_url="https://api.openai.com/v1",
                api_type=APIType.REST,
                auth_type=AuthType.BEARER_TOKEN,
                rate_limit=5000,
                endpoints={
                    "chat_completion": {
                        "method": "POST",
                        "path": "/chat/completions",
                        "description": "تکمیل گفتگو"
                    },
                    "image_generation": {
                        "method": "POST",
                        "path": "/images/generations",
                        "description": "تولید تصویر"
                    }
                }
            ),
            
            "anthropic": APIConfig(
                name="Anthropic API",
                base_url="https://api.anthropic.com/v1",
                api_type=APIType.REST,
                auth_type=AuthType.API_KEY,
                rate_limit=1000,
                endpoints={
                    "complete": {
                        "method": "POST",
                        "path": "/complete",
                        "description": "تکمیل متن"
                    }
                }
            ),
            
            # Weather APIs
            "openweather": APIConfig(
                name="OpenWeather API",
                base_url="https://api.openweathermap.org/data/2.5",
                api_type=APIType.REST,
                auth_type=AuthType.API_KEY,
                rate_limit=1000,
                endpoints={
                    "current_weather": {
                        "method": "GET",
                        "path": "/weather",
                        "description": "آب و هوای فعلی"
                    },
                    "forecast": {
                        "method": "GET",
                        "path": "/forecast",
                        "description": "پیش‌بینی آب و هوا"
                    }
                }
            ),
            
            # News APIs
            "newsapi": APIConfig(
                name="News API",
                base_url="https://newsapi.org/v2",
                api_type=APIType.REST,
                auth_type=AuthType.API_KEY,
                rate_limit=1000,
                endpoints={
                    "top_headlines": {
                        "method": "GET",
                        "path": "/top-headlines",
                        "description": "اخبار برتر"
                    },
                    "everything": {
                        "method": "GET",
                        "path": "/everything",
                        "description": "جستجوی اخبار"
                    }
                }
            )
        }
    
    async def _load_api_configs(self):
        """بارگذاری تنظیمات API ها"""
        config_file = "api_configs.json"
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as f:
                configs_data = json.load(f)
                
            for name, config_data in configs_data.items():
                self.api_configs[name] = APIConfig(
                    name=config_data["name"],
                    base_url=config_data["base_url"],
                    api_type=APIType(config_data["api_type"]),
                    auth_type=AuthType(config_data["auth_type"]),
                    auth_config=config_data.get("auth_config", {}),
                    headers=config_data.get("headers", {}),
                    rate_limit=config_data.get("rate_limit", 100),
                    timeout=config_data.get("timeout", 30),
                    retry_attempts=config_data.get("retry_attempts", 3),
                    endpoints=config_data.get("endpoints", {})
                )
        else:
            # استفاده از API های پیش‌تعریف شده
            self.api_configs = self.predefined_apis.copy()
    
    async def save_api_configs(self):
        """ذخیره تنظیمات API ها"""
        config_file = "api_configs.json"
        configs_data = {}
        
        for name, config in self.api_configs.items():
            configs_data[name] = {
                "name": config.name,
                "base_url": config.base_url,
                "api_type": config.api_type.value,
                "auth_type": config.auth_type.value,
                "auth_config": config.auth_config,
                "headers": config.headers,
                "rate_limit": config.rate_limit,
                "timeout": config.timeout,
                "retry_attempts": config.retry_attempts,
                "endpoints": config.endpoints
            }
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(configs_data, f, ensure_ascii=False, indent=2)
    
    def add_api_config(self, name: str, config: APIConfig):
        """اضافه کردن تنظیمات API جدید"""
        self.api_configs[name] = config
        asyncio.create_task(self.save_api_configs())
    
    def remove_api_config(self, name: str):
        """حذف تنظیمات API"""
        if name in self.api_configs:
            del self.api_configs[name]
            asyncio.create_task(self.save_api_configs())
    
    async def make_request(self, api_name: str, endpoint_name: str, request_data: APIRequest) -> APIResponse:
        """
        ارسال درخواست به API
        
        Args:
            api_name: نام API
            endpoint_name: نام endpoint
            request_data: داده‌های درخواست
            
        Returns:
            پاسخ API
        """
        start_time = datetime.now()
        
        try:
            if api_name not in self.api_configs:
                raise ValueError(f"API '{api_name}' not found")
            
            config = self.api_configs[api_name]
            
            if endpoint_name not in config.endpoints:
                raise ValueError(f"Endpoint '{endpoint_name}' not found in API '{api_name}'")
            
            endpoint_config = config.endpoints[endpoint_name]
            
            # بررسی rate limit
            if not await self._check_rate_limit(api_name):
                raise Exception(f"Rate limit exceeded for API '{api_name}'")
            
            # ساخت URL
            url = self._build_url(config, endpoint_config, request_data)
            
            # ساخت headers
            headers = await self._build_headers(config, request_data)
            
            # ساخت body
            body = self._build_body(request_data, config.api_type)
            
            # ارسال درخواست
            response = await self._send_request(
                method=endpoint_config.get("method", request_data.method),
                url=url,
                headers=headers,
                body=body,
                params=request_data.params,
                timeout=request_data.timeout or config.timeout
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # ذخیره تاریخچه
            self._save_request_history(api_name, endpoint_name, request_data, response, execution_time)
            
            return APIResponse(
                status_code=response.status,
                data=response.data,
                headers=dict(response.headers),
                success=response.status < 400,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"API request failed: {e}")
            
            return APIResponse(
                status_code=500,
                data=None,
                headers={},
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    def _build_url(self, config: APIConfig, endpoint_config: Dict, request_data: APIRequest) -> str:
        """ساخت URL"""
        base_url = config.base_url
        path = endpoint_config.get("path", request_data.endpoint)
        
        # جایگزینی متغیرها در URL
        for key, value in request_data.params.items():
            path = path.replace(f"{{{key}}}", str(value))
        
        # جایگزینی متغیرها در base_url
        for key, value in config.auth_config.items():
            if key in ["token", "api_key", "app_id"]:
                base_url = base_url.replace(f"{{{key}}}", str(value))
        
        return f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    
    async def _build_headers(self, config: APIConfig, request_data: APIRequest) -> Dict[str, str]:
        """ساخت headers"""
        headers = config.headers.copy()
        headers.update(request_data.headers)
        
        # اضافه کردن authentication
        if config.auth_type == AuthType.API_KEY:
            api_key = config.auth_config.get("api_key")
            if api_key:
                key_name = config.auth_config.get("key_name", "X-API-Key")
                headers[key_name] = api_key
        
        elif config.auth_type == AuthType.BEARER_TOKEN:
            token = config.auth_config.get("token")
            if token:
                headers["Authorization"] = f"Bearer {token}"
        
        elif config.auth_type == AuthType.BASIC_AUTH:
            username = config.auth_config.get("username")
            password = config.auth_config.get("password")
            if username and password:
                credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                headers["Authorization"] = f"Basic {credentials}"
        
        elif config.auth_type == AuthType.JWT:
            jwt_token = await self._generate_jwt_token(config)
            if jwt_token:
                headers["Authorization"] = f"Bearer {jwt_token}"
        
        elif config.auth_type == AuthType.HMAC:
            hmac_signature = await self._generate_hmac_signature(config, request_data)
            if hmac_signature:
                headers["X-Signature"] = hmac_signature
        
        return headers
    
    async def _generate_jwt_token(self, config: APIConfig) -> Optional[str]:
        """تولید JWT token"""
        try:
            payload = config.auth_config.get("payload", {})
            secret = config.auth_config.get("secret")
            algorithm = config.auth_config.get("algorithm", "HS256")
            
            if not secret:
                return None
            
            # اضافه کردن زمان انقضا
            if "exp" not in payload:
                payload["exp"] = datetime.utcnow() + timedelta(hours=1)
            
            token = jwt.encode(payload, secret, algorithm=algorithm)
            return token
            
        except Exception as e:
            self.logger.error(f"JWT token generation failed: {e}")
            return None
    
    async def _generate_hmac_signature(self, config: APIConfig, request_data: APIRequest) -> Optional[str]:
        """تولید HMAC signature"""
        try:
            secret = config.auth_config.get("secret")
            if not secret:
                return None
            
            # ساخت message برای signature
            message = f"{request_data.method}\n{request_data.endpoint}\n{json.dumps(request_data.body or {})}"
            
            signature = hmac.new(
                secret.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return signature
            
        except Exception as e:
            self.logger.error(f"HMAC signature generation failed: {e}")
            return None
    
    def _build_body(self, request_data: APIRequest, api_type: APIType) -> Any:
        """ساخت body درخواست"""
        if not request_data.body:
            return None
        
        if api_type == APIType.REST:
            return request_data.body
        elif api_type == APIType.GRAPHQL:
            return {"query": request_data.body}
        elif api_type == APIType.SOAP:
            return request_data.body
        else:
            return request_data.body
    
    async def _send_request(self, method: str, url: str, headers: Dict[str, str], 
                          body: Any, params: Dict[str, Any], timeout: int) -> Any:
        """ارسال درخواست HTTP"""
        try:
            async with self.http_client.request(
                method=method,
                url=url,
                headers=headers,
                json=body if isinstance(body, (dict, list)) else None,
                data=body if isinstance(body, str) else None,
                params=params,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                try:
                    data = await response.json()
                except:
                    data = await response.text()
                
                return type('Response', (), {
                    'status': response.status,
                    'data': data,
                    'headers': response.headers
                })()
                
        except asyncio.TimeoutError:
            raise Exception("Request timeout")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
    
    async def _check_rate_limit(self, api_name: str) -> bool:
        """بررسی rate limit"""
        if api_name not in self.rate_limits:
            self.rate_limits[api_name] = []
        
        config = self.api_configs.get(api_name)
        if not config:
            return True
        
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # حذف درخواست‌های قدیمی
        self.rate_limits[api_name] = [
            req_time for req_time in self.rate_limits[api_name] 
            if req_time > minute_ago
        ]
        
        # بررسی تعداد درخواست‌ها
        if len(self.rate_limits[api_name]) >= config.rate_limit:
            return False
        
        # اضافه کردن درخواست فعلی
        self.rate_limits[api_name].append(now)
        return True
    
    def _save_request_history(self, api_name: str, endpoint_name: str, 
                            request_data: APIRequest, response: Any, execution_time: float):
        """ذخیره تاریخچه درخواست"""
        history_record = {
            "timestamp": datetime.now().isoformat(),
            "api_name": api_name,
            "endpoint_name": endpoint_name,
            "method": request_data.method,
            "endpoint": request_data.endpoint,
            "status_code": response.status,
            "success": response.status < 400,
            "execution_time": execution_time,
            "request_size": len(str(request_data.body or "")),
            "response_size": len(str(response.data or ""))
        }
        
        self.request_history.append(history_record)
        
        # نگه داشتن فقط 1000 رکورد آخر
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-1000:]
    
    def get_api_list(self) -> List[Dict]:
        """دریافت لیست API ها"""
        return [
            {
                "name": name,
                "display_name": config.name,
                "base_url": config.base_url,
                "api_type": config.api_type.value,
                "auth_type": config.auth_type.value,
                "rate_limit": config.rate_limit,
                "endpoints_count": len(config.endpoints)
            }
            for name, config in self.api_configs.items()
        ]
    
    def get_api_endpoints(self, api_name: str) -> List[Dict]:
        """دریافت endpoint های یک API"""
        if api_name not in self.api_configs:
            return []
        
        config = self.api_configs[api_name]
        return [
            {
                "name": name,
                "method": endpoint.get("method", "GET"),
                "path": endpoint.get("path", ""),
                "description": endpoint.get("description", "")
            }
            for name, endpoint in config.endpoints.items()
        ]
    
    def get_request_history(self, limit: int = 50) -> List[Dict]:
        """دریافت تاریخچه درخواست‌ها"""
        return self.request_history[-limit:]
    
    def get_api_stats(self) -> Dict:
        """دریافت آمار API ها"""
        if not self.request_history:
            return {"total_requests": 0}
        
        total_requests = len(self.request_history)
        successful_requests = len([r for r in self.request_history if r["success"]])
        failed_requests = total_requests - successful_requests
        
        avg_execution_time = sum(r["execution_time"] for r in self.request_history) / total_requests
        
        # آمار بر اساس API
        api_stats = {}
        for record in self.request_history:
            api_name = record["api_name"]
            if api_name not in api_stats:
                api_stats[api_name] = {"requests": 0, "successful": 0, "failed": 0}
            
            api_stats[api_name]["requests"] += 1
            if record["success"]:
                api_stats[api_name]["successful"] += 1
            else:
                api_stats[api_name]["failed"] += 1
        
        return {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": (successful_requests / total_requests) * 100,
            "average_execution_time": avg_execution_time,
            "api_stats": api_stats
        }
    
    async def test_api_connection(self, api_name: str) -> Dict:
        """تست اتصال به API"""
        if api_name not in self.api_configs:
            return {"success": False, "error": "API not found"}
        
        config = self.api_configs[api_name]
        
        try:
            # تست ساده با GET request
            test_request = APIRequest(
                method="GET",
                endpoint="/",
                params={}
            )
            
            response = await self.make_request(api_name, list(config.endpoints.keys())[0], test_request)
            
            return {
                "success": response.success,
                "status_code": response.status_code,
                "response_time": response.execution_time,
                "error": response.error
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# مثال استفاده
if __name__ == "__main__":
    async def test_api_integrations():
        integrations = AgentAPIIntegrations()
        await integrations.initialize()
        
        # تست API
        test_request = APIRequest(
            method="GET",
            endpoint="/weather",
            params={"q": "Tehran", "appid": "your_api_key"}
        )
        
        response = await integrations.make_request("openweather", "current_weather", test_request)
        print(f"API Response: {response.status_code}")
        print(f"Data: {response.data}")
        print(f"Success: {response.success}")
        
        # دریافت آمار
        stats = integrations.get_api_stats()
        print(f"API Stats: {stats}")
        
        await integrations.close()
    
    # اجرای تست
    asyncio.run(test_api_integrations())
