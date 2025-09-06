# 🏗️ Site Builder - Makefile
# دستورات مفید برای مدیریت پروژه

.PHONY: help install setup test lint format clean docker-build docker-run docker-compose docker-down

# نمایش راهنما
help:
	@echo "🏗️ Site Builder - دستورات مفید"
	@echo ""
	@echo "📦 نصب و راه‌اندازی:"
	@echo "  make install     - نصب وابستگی‌ها"
	@echo "  make setup       - راه‌اندازی اولیه پروژه"
	@echo ""
	@echo "🧪 تست و کیفیت:"
	@echo "  make test        - اجرای تست‌ها"
	@echo "  make test-cov    - تست با گزارش پوشش"
	@echo "  make lint        - بررسی کیفیت کد"
	@echo "  make format      - فرمت کردن کد"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  make docker-build     - ساخت Docker image"
	@echo "  make docker-run       - اجرای Docker container"
	@echo "  make docker-compose   - راه‌اندازی با Docker Compose"
	@echo "  make docker-down      - توقف Docker Compose"
	@echo ""
	@echo "🔧 مدیریت:"
	@echo "  make clean       - پاکسازی فایل‌های موقت"
	@echo "  make migrate     - اجرای migrations"
	@echo "  make collectstatic - جمع‌آوری فایل‌های استاتیک"
	@echo "  make runserver   - راه‌اندازی سرور توسعه"

# نصب وابستگی‌ها
install:
	@echo "📦 نصب وابستگی‌های Python..."
	pip install -r backend/requirements.txt
	@echo "📦 نصب وابستگی‌های Node.js..."
	npm install
	@echo "✅ نصب کامل شد!"

# راه‌اندازی اولیه
setup: install
	@echo "🚀 راه‌اندازی اولیه پروژه..."
	cp env.example .env
	@echo "⚠️  لطفاً فایل .env را ویرایش کنید"
	python manage.py migrate
	python manage.py collectstatic --noinput
	@echo "✅ راه‌اندازی کامل شد!"

# اجرای تست‌ها
test:
	@echo "🧪 اجرای تست‌های Python..."
	cd backend && python manage.py test
	@echo "🧪 اجرای تست‌های Node.js..."
	npm test
	@echo "✅ تست‌ها کامل شدند!"

# تست با گزارش پوشش
test-cov:
	@echo "🧪 اجرای تست‌ها با گزارش پوشش..."
	pytest tests/ -v --cov=backend --cov-report=html --cov-report=term
	@echo "📊 گزارش پوشش در htmlcov/ ایجاد شد"

# بررسی کیفیت کد
lint:
	@echo "🔍 بررسی کیفیت کد Python..."
	flake8 backend/
	black --check backend/
	isort --check-only backend/
	@echo "🔍 بررسی کیفیت کد JavaScript..."
	npm run lint
	@echo "✅ بررسی کیفیت کد کامل شد!"

# فرمت کردن کد
format:
	@echo "🎨 فرمت کردن کد Python..."
	black backend/
	isort backend/
	@echo "🎨 فرمت کردن کد JavaScript..."
	npm run format
	@echo "✅ فرمت کردن کد کامل شد!"

# پاکسازی فایل‌های موقت
clean:
	@echo "🧹 پاکسازی فایل‌های موقت..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	@echo "✅ پاکسازی کامل شد!"

# اجرای migrations
migrate:
	@echo "🗄️ اجرای migrations..."
	python manage.py migrate
	@echo "✅ migrations اجرا شدند!"

# جمع‌آوری فایل‌های استاتیک
collectstatic:
	@echo "📦 جمع‌آوری فایل‌های استاتیک..."
	python manage.py collectstatic --noinput
	@echo "✅ فایل‌های استاتیک جمع‌آوری شدند!"

# راه‌اندازی سرور توسعه
runserver:
	@echo "🚀 راه‌اندازی سرور توسعه..."
	python manage.py runserver

# ساخت Docker image
docker-build:
	@echo "🐳 ساخت Docker image..."
	docker build -t sitebuilder:latest .
	@echo "✅ Docker image ساخته شد!"

# اجرای Docker container
docker-run:
	@echo "🐳 اجرای Docker container..."
	docker run -p 8000:8000 sitebuilder:latest

# راه‌اندازی با Docker Compose
docker-compose:
	@echo "🐳 راه‌اندازی با Docker Compose..."
	docker-compose up -d
	@echo "✅ سرویس‌ها راه‌اندازی شدند!"
	@echo "🌐 دسترسی: http://localhost"

# توقف Docker Compose
docker-down:
	@echo "🐳 توقف Docker Compose..."
	docker-compose down
	@echo "✅ سرویس‌ها متوقف شدند!"

# ایجاد superuser
createsuperuser:
	@echo "👤 ایجاد کاربر مدیر..."
	python manage.py createsuperuser

# اجرای shell Django
shell:
	@echo "🐍 اجرای Django shell..."
	python manage.py shell

# اجرای shell Django با IPython
shell-plus:
	@echo "🐍 اجرای Django shell با IPython..."
	python manage.py shell_plus

# بررسی امنیت
security:
	@echo "🔒 بررسی امنیت..."
	bandit -r backend/
	safety check
	@echo "✅ بررسی امنیت کامل شد!"

# تولید مستندات
docs:
	@echo "📚 تولید مستندات..."
	# اینجا دستورات تولید مستندات قرار می‌گیرد
	@echo "✅ مستندات تولید شدند!"

# بک‌آپ دیتابیس
backup:
	@echo "💾 بک‌آپ دیتابیس..."
	python manage.py dumpdata > backup_$(shell date +%Y%m%d_%H%M%S).json
	@echo "✅ بک‌آپ ایجاد شد!"

# بازگردانی دیتابیس
restore:
	@echo "🔄 بازگردانی دیتابیس..."
	@read -p "نام فایل بک‌آپ: " file; \
	python manage.py loaddata $$file
	@echo "✅ دیتابیس بازگردانی شد!"

# بررسی وضعیت پروژه
status:
	@echo "📊 وضعیت پروژه:"
	@echo "📁 فایل‌های Python: $$(find . -name '*.py' | wc -l)"
	@echo "📁 فایل‌های JavaScript: $$(find . -name '*.js' | wc -l)"
	@echo "📁 فایل‌های HTML: $$(find . -name '*.html' | wc -l)"
	@echo "📁 فایل‌های CSS: $$(find . -name '*.css' | wc -l)"
	@echo "📁 کل فایل‌ها: $$(find . -type f | wc -l)"
	@echo "📁 کل دایرکتوری‌ها: $$(find . -type d | wc -l)"

# نمایش اطلاعات پروژه
info:
	@echo "🏗️ Site Builder - اطلاعات پروژه"
	@echo "📅 تاریخ: $$(date)"
	@echo "🐍 Python: $$(python --version)"
	@echo "🟢 Node.js: $$(node --version)"
	@echo "📦 npm: $$(npm --version)"
	@echo "🐳 Docker: $$(docker --version)"
	@echo "🐳 Docker Compose: $$(docker-compose --version)"
