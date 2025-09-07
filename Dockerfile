# 🌍 Site Builder - Global Edition Docker Configuration
FROM python:3.11-slim

# تنظیم متغیرهای محیطی
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV NODE_ENV=production
ENV DJANGO_SETTINGS_MODULE=backend.settings

# نصب وابستگی‌های سیستم پیشرفته
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    wget \
    git \
    nodejs \
    npm \
    chromium \
    chromium-driver \
    fonts-liberation \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-roboto \
    fonts-dejavu-core \
    fonts-freefont-ttf \
    imagemagick \
    ffmpeg \
    redis-tools \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# تنظیم مسیر کاری
WORKDIR /app

# کپی فایل‌های requirements
COPY backend/requirements.txt /app/requirements.txt
COPY requirements-test.txt /app/requirements-test.txt

# نصب وابستگی‌های Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn[gevent] \
    && pip install --no-cache-dir -r requirements-test.txt

# کپی package.json و نصب وابستگی‌های Node.js
COPY package.json package-lock.json /app/
RUN npm ci --only=production \
    && npm install -g pm2 \
    && npm cache clean --force

# کپی کد پروژه
COPY . /app/

# ایجاد کاربر غیر root
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# ایجاد دایرکتوری‌های مورد نیاز
RUN mkdir -p /app/staticfiles /app/media /app/logs /app/temp /app/cache

# تنظیم متغیرهای محیطی برای کاربر
ENV HOME=/home/app
ENV PATH=$PATH:/home/app/.local/bin

# جمع‌آوری فایل‌های استاتیک
RUN python manage.py collectstatic --noinput || echo "Static files collection skipped"

# ایجاد فایل‌های پیکربندی
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Wait for database\n\
echo "Waiting for database..."\n\
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do\n\
  sleep 1\n\
done\n\
\n\
# Run migrations\n\
echo "Running migrations..."\n\
python manage.py migrate --noinput\n\
\n\
# Create superuser if not exists\n\
echo "Creating superuser..."\n\
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username=os.environ.get(\"DJANGO_SUPERUSER_USERNAME\", \"admin\")).exists() or User.objects.create_superuser(os.environ.get(\"DJANGO_SUPERUSER_USERNAME\", \"admin\"), os.environ.get(\"DJANGO_SUPERUSER_EMAIL\", \"admin@example.com\"), os.environ.get(\"DJANGO_SUPERUSER_PASSWORD\", \"admin123\"))"\n\
\n\
# Start services\n\
echo "Starting services..."\n\
exec "$@"' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# پورت‌ها
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# دستور راه‌اندازی
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "gevent", "--worker-connections", "1000", "--max-requests", "1000", "--max-requests-jitter", "100", "--timeout", "30", "--keep-alive", "2", "--preload", "backend.wsgi:application"]
