# 🏗️ Site Builder - Docker Configuration
FROM python:3.11-slim

# تنظیم متغیرهای محیطی
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# نصب وابستگی‌های سیستم
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
    && rm -rf /var/lib/apt/lists/*

# تنظیم مسیر کاری
WORKDIR /app

# کپی فایل‌های requirements
COPY backend/requirements.txt /app/requirements.txt

# نصب وابستگی‌های Python
RUN pip install --no-cache-dir -r requirements.txt

# کپی package.json و نصب وابستگی‌های Node.js
COPY package.json package-lock.json /app/
RUN npm install

# کپی کد پروژه
COPY . /app/

# ایجاد کاربر غیر root
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# ایجاد دایرکتوری‌های مورد نیاز
RUN mkdir -p /app/staticfiles /app/media /app/logs

# جمع‌آوری فایل‌های استاتیک
RUN python manage.py collectstatic --noinput

# پورت
EXPOSE 8000

# دستور راه‌اندازی
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
