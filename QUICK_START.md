# 🚀 Site Builder - Quick Start Guide

## ⚡ Get Started in 5 Minutes

### 1. Installation

#### Option A: Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/iman-noroozi/sitebuilder.git
cd sitebuilder

# Start with Docker Compose
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API: http://localhost:8000/api/
```

#### Option B: Local Installation
```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node.js dependencies
npm install

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Run the application
python manage.py runserver
```

### 2. First Steps

#### Extract a Website
```bash
# Using CLI
sitebuilder-cli extract https://example.com ./output

# Using API
curl -X POST http://localhost:8000/api/extract/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

#### Build a Website
```bash
# Using CLI
sitebuilder-cli build ./output ./final_site

# Using API
curl -X POST http://localhost:8000/api/build/ \
  -H "Content-Type: application/json" \
  -d '{"template_id": "template_123"}'
```

### 3. Web Interface

1. **Open Browser**: Navigate to `http://localhost:3000`
2. **Enter URL**: Input the website URL you want to extract
3. **Click Extract**: Watch the magic happen!
4. **Customize**: Modify colors, fonts, and content
5. **Deploy**: Publish your new website

### 4. API Usage

#### Basic Extraction
```python
import requests

response = requests.post('http://localhost:8000/api/extract/', json={
    'url': 'https://example.com'
})

data = response.json()
print(f"Extracted: {data['data']['title']}")
```

#### Performance Analysis
```python
response = requests.post('http://localhost:8000/api/analyze/performance/', json={
    'url': 'https://example.com'
})

performance = response.json()
print(f"Load time: {performance['data']['load_time']}s")
print(f"Performance score: {performance['data']['performance_score']}/100")
```

### 5. CLI Commands

```bash
# Extract website
sitebuilder-cli extract https://example.com ./output --headless --delay 3

# Analyze template
sitebuilder-cli analyze ./output

# Build final site
sitebuilder-cli build ./output ./final_site

# Get help
sitebuilder-cli --help
```

### 6. Configuration

#### Environment Variables
```bash
# .env file
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379/0
```

#### API Configuration
```python
# settings.py
SITEBUILDER_SETTINGS = {
    'MAX_EXTRACTION_SIZE': 50 * 1024 * 1024,  # 50MB
    'SUPPORTED_LANGUAGES': ['en', 'fa', 'ar', 'es', 'fr'],
    'RATE_LIMIT': 100,  # requests per hour
    'CACHE_TTL': 3600,  # 1 hour
}
```

### 7. Examples

#### Extract E-commerce Site
```bash
sitebuilder-cli extract https://shop.example.com ./ecommerce_template \
  --include-assets \
  --analyze-seo \
  --detect-framework
```

#### Build Portfolio Site
```bash
sitebuilder-cli build ./portfolio_template ./my_portfolio \
  --customize-colors \
  --add-content \
  --optimize-images
```

#### Batch Processing
```bash
# Extract multiple sites
sitebuilder-cli batch-extract urls.txt ./output_dir

# URLs file (urls.txt):
# https://example1.com
# https://example2.com
# https://example3.com
```

### 8. Troubleshooting

#### Common Issues

**Docker won't start:**
```bash
# Check Docker status
docker --version
docker-compose --version

# Restart Docker service
sudo systemctl restart docker
```

**Database connection error:**
```bash
# Check database status
docker-compose logs db

# Reset database
docker-compose down
docker-compose up -d db
```

**API not responding:**
```bash
# Check API health
curl http://localhost:8000/health/

# Check logs
docker-compose logs web
```

#### Performance Issues

**Slow extraction:**
```bash
# Increase timeout
export EXTRACTION_TIMEOUT=60

# Use headless mode
sitebuilder-cli extract --headless
```

**High memory usage:**
```bash
# Reduce worker processes
export GUNICORN_WORKERS=2

# Clear cache
docker-compose exec redis redis-cli FLUSHALL
```

### 9. Next Steps

#### Learn More
- 📚 [Full Documentation](README.md)
- 🔧 [API Reference](docs/API_DOCUMENTATION.md)
- 🚀 [Deployment Guide](DEPLOYMENT_GUIDE.md)
- 🎨 [UI Components](frontend/rtl-components.html)

#### Community
- 💬 [GitHub Discussions](https://github.com/iman-noroozi/sitebuilder/discussions)
- 🐛 [Report Issues](https://github.com/iman-noroozi/sitebuilder/issues)
- ⭐ [Star the Project](https://github.com/iman-noroozi/sitebuilder)

#### Support
- 📧 Email: support@sitebuilder.global
- 🌐 Website: https://sitebuilder.global
- 📱 Twitter: @SiteBuilderGlobal

### 10. Pro Tips

1. **Use Docker**: It's the easiest way to get started
2. **Check Logs**: Always check logs when something goes wrong
3. **Monitor Performance**: Use the built-in monitoring tools
4. **Backup Data**: Regular backups are essential
5. **Update Regularly**: Keep your installation up to date

---

**🎉 Congratulations!** You're now ready to build amazing websites with Site Builder!

Need help? Check our [documentation](README.md) or [contact support](mailto:support@sitebuilder.global).
