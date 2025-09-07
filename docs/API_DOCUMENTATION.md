# 🌍 Site Builder API Documentation - Global Edition

## 📋 Overview

The Site Builder API is a comprehensive RESTful API that provides advanced website extraction, analysis, and building capabilities for global use. This API supports multiple languages, frameworks, and deployment scenarios.

## 🔗 Base URL

```
Production: https://api.sitebuilder.global
Development: http://localhost:8000/api
```

## 🔐 Authentication

### API Key Authentication
```http
Authorization: Bearer YOUR_API_KEY
```

### Rate Limiting
- **Free Tier**: 100 requests/hour
- **Pro Tier**: 1,000 requests/hour
- **Enterprise**: 10,000 requests/hour

## 📚 Endpoints

### 1. Health Check

Check API health and status.

```http
GET /health/
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": 1699123456.789,
  "services": {
    "api": "operational",
    "extraction": "operational",
    "analysis": "operational"
  }
}
```

### 2. Extract Website

Extract and analyze a website template.

```http
POST /extract/
```

**Request Body:**
```json
{
  "url": "https://example.com",
  "options": {
    "include_assets": true,
    "extract_images": true,
    "extract_fonts": true,
    "analyze_seo": true,
    "detect_framework": true,
    "performance_analysis": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "url": "https://example.com",
    "timestamp": 1699123456.789,
    "language": "en",
    "framework": "bootstrap",
    "seo": {
      "title": "Example Website",
      "meta_description": "A sample website for demonstration",
      "meta_keywords": "example, website, demo",
      "h1_count": 1,
      "h2_count": 3,
      "images_without_alt": 0,
      "internal_links": 15,
      "external_links": 5,
      "seo_score": 85
    },
    "assets": {
      "css": [
        "https://example.com/css/bootstrap.min.css",
        "https://example.com/css/style.css"
      ],
      "js": [
        "https://example.com/js/jquery.min.js",
        "https://example.com/js/bootstrap.min.js"
      ],
      "images": [
        "https://example.com/images/logo.png",
        "https://example.com/images/hero.jpg"
      ],
      "fonts": [
        "https://fonts.googleapis.com/css?family=Roboto"
      ]
    },
    "performance": {
      "load_time": 2.34,
      "content_size": 156789,
      "status_code": 200,
      "performance_score": 78
    },
    "metadata": {
      "title": "Example Website",
      "description": "A sample website for demonstration",
      "keywords": "example, website, demo",
      "viewport": "width=device-width, initial-scale=1.0",
      "robots": "index, follow"
    }
  },
  "message": "Website extracted successfully"
}
```

### 3. Analyze Performance

Analyze website performance metrics.

```http
POST /analyze/performance/
```

**Request Body:**
```json
{
  "url": "https://example.com",
  "metrics": [
    "load_time",
    "page_size",
    "requests_count",
    "seo_score"
  ]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "url": "https://example.com",
    "load_time": 2.34,
    "status_code": 200,
    "content_size": 156789,
    "headers": {
      "content-type": "text/html; charset=utf-8",
      "server": "nginx/1.18.0"
    },
    "performance_score": 78,
    "recommendations": [
      "Consider optimizing images and reducing file sizes",
      "Enable gzip compression",
      "Minify CSS and JavaScript files"
    ]
  }
}
```

### 4. Get Supported Languages

Get list of supported languages.

```http
GET /languages/
```

**Response:**
```json
{
  "languages": [
    {
      "code": "en",
      "name": "English",
      "flag": "🇺🇸",
      "rtl": false
    },
    {
      "code": "fa",
      "name": "فارسی",
      "flag": "🇮🇷",
      "rtl": true
    },
    {
      "code": "ar",
      "name": "العربية",
      "flag": "🇸🇦",
      "rtl": true
    }
  ],
  "count": 12
}
```

### 5. Get Supported Frameworks

Get list of supported CSS frameworks.

```http
GET /frameworks/
```

**Response:**
```json
{
  "frameworks": [
    {
      "name": "bootstrap",
      "version": "5.3.0",
      "description": "Bootstrap CSS Framework",
      "features": ["responsive", "components", "utilities"]
    },
    {
      "name": "tailwind",
      "version": "3.3.0",
      "description": "Tailwind CSS Framework",
      "features": ["utility-first", "responsive", "customizable"]
    }
  ],
  "count": 8
}
```

### 6. Build Website

Build a website from extracted template.

```http
POST /build/
```

**Request Body:**
```json
{
  "template_id": "template_123",
  "customizations": {
    "colors": {
      "primary": "#6366f1",
      "secondary": "#8b5cf6"
    },
    "fonts": {
      "heading": "Inter",
      "body": "Roboto"
    },
    "content": {
      "title": "My New Website",
      "description": "A beautiful website built with Site Builder"
    }
  },
  "deployment": {
    "platform": "netlify",
    "domain": "mywebsite.com"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "build_id": "build_456",
    "status": "building",
    "estimated_time": 120,
    "deployment_url": "https://build-456.netlify.app",
    "custom_domain": "mywebsite.com"
  },
  "message": "Website build started successfully"
}
```

### 7. Get Build Status

Check the status of a website build.

```http
GET /build/{build_id}/status/
```

**Response:**
```json
{
  "success": true,
  "data": {
    "build_id": "build_456",
    "status": "completed",
    "progress": 100,
    "deployment_url": "https://build-456.netlify.app",
    "custom_domain": "mywebsite.com",
    "build_time": 95,
    "errors": [],
    "warnings": []
  }
}
```

## 🔧 Advanced Features

### Webhook Support

Register webhooks for build completion notifications.

```http
POST /webhooks/
```

**Request Body:**
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["build.completed", "build.failed"],
  "secret": "your-webhook-secret"
}
```

### Batch Processing

Process multiple URLs in a single request.

```http
POST /batch/extract/
```

**Request Body:**
```json
{
  "urls": [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
  ],
  "options": {
    "include_assets": true,
    "analyze_seo": true
  }
}
```

## 📊 Error Handling

### Error Response Format

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": "Additional error details",
  "timestamp": 1699123456.789
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| `INVALID_URL` | Invalid or inaccessible URL |
| `RATE_LIMIT_EXCEEDED` | Rate limit exceeded |
| `EXTRACTION_ERROR` | Error during extraction |
| `ANALYSIS_ERROR` | Error during analysis |
| `BUILD_ERROR` | Error during build process |
| `AUTHENTICATION_ERROR` | Invalid API key |
| `QUOTA_EXCEEDED` | API quota exceeded |

## 🌐 Global Features

### Multi-Language Support

The API automatically detects and supports 12+ languages:

- English (en)
- فارسی (fa) - RTL
- العربية (ar) - RTL
- Español (es)
- Français (fr)
- Deutsch (de)
- 中文 (zh)
- 日本語 (ja)
- 한국어 (ko)
- Русский (ru)
- Português (pt)
- Italiano (it)

### Framework Detection

Automatically detects and supports popular CSS frameworks:

- Bootstrap
- Tailwind CSS
- Bulma
- Foundation
- Materialize
- Semantic UI
- Chakra UI
- Ant Design

### Performance Optimization

Built-in performance analysis and optimization:

- Load time analysis
- Asset optimization
- SEO scoring
- Mobile responsiveness check
- Accessibility compliance

## 🔒 Security

### HTTPS Only
All API endpoints require HTTPS in production.

### CORS Configuration
```json
{
  "allowed_origins": ["https://yourdomain.com"],
  "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
  "allowed_headers": ["Authorization", "Content-Type"]
}
```

### Data Privacy
- No data is stored permanently
- All extractions are processed in memory
- GDPR compliant data handling

## 📈 Monitoring

### Metrics Endpoint
```http
GET /metrics/
```

**Response:**
```json
{
  "requests_total": 12543,
  "requests_per_minute": 45,
  "average_response_time": 1.23,
  "error_rate": 0.02,
  "uptime": 99.9
}
```

## 🚀 SDKs and Libraries

### Python SDK
```bash
pip install sitebuilder-sdk
```

```python
from sitebuilder import SiteBuilder

client = SiteBuilder(api_key="your-api-key")
result = client.extract("https://example.com")
```

### JavaScript SDK
```bash
npm install @sitebuilder/sdk
```

```javascript
import { SiteBuilder } from '@sitebuilder/sdk';

const client = new SiteBuilder('your-api-key');
const result = await client.extract('https://example.com');
```

### PHP SDK
```bash
composer require sitebuilder/sdk
```

```php
use SiteBuilder\Client;

$client = new Client('your-api-key');
$result = $client->extract('https://example.com');
```

## 📞 Support

- **Documentation**: https://docs.sitebuilder.global
- **Support Email**: support@sitebuilder.global
- **Community**: https://community.sitebuilder.global
- **Status Page**: https://status.sitebuilder.global

## 📄 License

This API is licensed under the MIT License. See LICENSE file for details.
