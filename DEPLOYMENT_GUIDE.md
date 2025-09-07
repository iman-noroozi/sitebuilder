# 🚀 Site Builder - Global Edition Deployment Guide

## 🌍 Production Deployment

### Prerequisites

- Docker & Docker Compose
- Domain name (optional)
- SSL certificate (optional)
- Cloud provider account (AWS, GCP, Azure, DigitalOcean)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/iman-noroozi/sitebuilder.git
cd sitebuilder

# Copy environment file
cp env.example .env

# Edit environment variables
nano .env

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### Environment Configuration

```bash
# .env file
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://sitebuilder:password@db:5432/sitebuilder
REDIS_URL=redis://:password@redis:6379/0

# Email configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Monitoring
GRAFANA_ADMIN_PASSWORD=secure-password
PROMETHEUS_RETENTION=30d
```

### Cloud Deployment Options

#### 1. AWS Deployment

```bash
# Using AWS ECS
aws ecs create-cluster --cluster-name sitebuilder
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs create-service --cluster sitebuilder --service-name sitebuilder-service
```

#### 2. Google Cloud Platform

```bash
# Using Google Cloud Run
gcloud run deploy sitebuilder --source . --platform managed --region us-central1
```

#### 3. DigitalOcean App Platform

```yaml
# .do/app.yaml
name: sitebuilder
services:
- name: web
  source_dir: /
  github:
    repo: iman-noroozi/sitebuilder
    branch: main
  run_command: gunicorn backend.wsgi:application
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  routes:
  - path: /
```

#### 4. Heroku Deployment

```bash
# Create Heroku app
heroku create your-sitebuilder-app

# Add addons
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev

# Deploy
git push heroku main
```

### SSL Configuration

#### Let's Encrypt with Nginx

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Monitoring Setup

#### Prometheus Configuration

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'sitebuilder'
    static_configs:
      - targets: ['web:8000']
```

#### Grafana Dashboards

1. Access Grafana: `http://yourdomain.com:3001`
2. Login: admin / admin123
3. Import dashboards from `monitoring/grafana/dashboards/`

### Performance Optimization

#### Database Optimization

```sql
-- PostgreSQL tuning
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
```

#### Redis Configuration

```conf
# redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

#### Nginx Optimization

```nginx
# nginx.conf
worker_processes auto;
worker_connections 1024;

gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

client_max_body_size 100M;
```

### Scaling

#### Horizontal Scaling

```yaml
# docker-compose.override.yml
version: '3.8'
services:
  web:
    deploy:
      replicas: 3
    environment:
      - GUNICORN_WORKERS=4
      - GUNICORN_WORKER_CONNECTIONS=1000
```

#### Load Balancer

```nginx
upstream sitebuilder {
    server web1:8000;
    server web2:8000;
    server web3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://sitebuilder;
    }
}
```

### Backup Strategy

#### Database Backup

```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h db -U sitebuilder sitebuilder > backup_$DATE.sql
aws s3 cp backup_$DATE.sql s3://your-backup-bucket/
```

#### Media Files Backup

```bash
# Backup media files
tar -czf media_backup_$DATE.tar.gz media/
aws s3 cp media_backup_$DATE.tar.gz s3://your-backup-bucket/
```

### Security Hardening

#### Firewall Configuration

```bash
# UFW setup
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

#### Docker Security

```dockerfile
# Use non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Remove unnecessary packages
RUN apt-get autoremove -y && apt-get clean
```

### Troubleshooting

#### Common Issues

1. **Database Connection Error**
   ```bash
   # Check database status
   docker-compose logs db
   
   # Restart database
   docker-compose restart db
   ```

2. **Redis Connection Error**
   ```bash
   # Check Redis status
   docker-compose logs redis
   
   # Test Redis connection
   docker-compose exec redis redis-cli ping
   ```

3. **Static Files Not Loading**
   ```bash
   # Collect static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

4. **High Memory Usage**
   ```bash
   # Check memory usage
   docker stats
   
   # Optimize worker processes
   export GUNICORN_WORKERS=2
   ```

### Health Checks

#### Application Health

```bash
# Check application health
curl http://localhost:8000/health/

# Check database health
docker-compose exec db pg_isready -U sitebuilder

# Check Redis health
docker-compose exec redis redis-cli ping
```

#### Monitoring Alerts

```yaml
# alertmanager.yml
route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
- name: 'web.hook'
  webhook_configs:
  - url: 'http://your-webhook-url'
```

### Maintenance

#### Regular Maintenance Tasks

```bash
# Weekly maintenance script
#!/bin/bash

# Update system packages
sudo apt update && sudo apt upgrade -y

# Clean Docker images
docker system prune -f

# Backup database
pg_dump -h db -U sitebuilder sitebuilder > weekly_backup_$(date +%Y%m%d).sql

# Check disk space
df -h

# Check logs
docker-compose logs --tail=100
```

### Support

For deployment support:
- 📧 Email: support@sitebuilder.global
- 📚 Documentation: https://docs.sitebuilder.global
- 💬 Community: https://community.sitebuilder.global
- 🐛 Issues: https://github.com/iman-noroozi/sitebuilder/issues
