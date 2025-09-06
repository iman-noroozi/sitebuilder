from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class TemplateCategory(models.Model):
    """دسته‌بندی قالب‌ها"""
    name = models.CharField(max_length=100, verbose_name="نام دسته")
    name_en = models.CharField(max_length=100, verbose_name="نام انگلیسی")
    description = models.TextField(verbose_name="توضیحات")
    icon = models.CharField(max_length=50, default="fas fa-folder", verbose_name="آیکون")
    color = models.CharField(max_length=7, default="#007bff", verbose_name="رنگ")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "دسته‌بندی قالب"
        verbose_name_plural = "دسته‌بندی‌های قالب"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class SiteTemplate(models.Model):
    """قالب سایت"""
    TEMPLATE_STATUS = (
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
        ('draft', 'پیش‌نویس'),
    )
    
    name = models.CharField(max_length=200, verbose_name="نام قالب")
    description = models.TextField(verbose_name="توضیحات")
    category = models.ForeignKey(TemplateCategory, on_delete=models.CASCADE, verbose_name="دسته‌بندی")
    html_content = models.TextField(verbose_name="محتوای HTML")
    css_content = models.TextField(blank=True, verbose_name="محتوای CSS")
    js_content = models.TextField(blank=True, verbose_name="محتوای JavaScript")
    preview_image = models.ImageField(upload_to='templates/previews/', blank=True, verbose_name="تصویر پیش‌نمایش")
    template_file = models.FileField(upload_to='templates/files/', blank=True, verbose_name="فایل قالب")
    status = models.CharField(max_length=20, choices=TEMPLATE_STATUS, default='active', verbose_name="وضعیت")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    is_free = models.BooleanField(default=True, verbose_name="رایگان")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="قیمت")
    tags = models.JSONField(default=list, verbose_name="برچسب‌ها")
    metadata = models.JSONField(default=dict, verbose_name="متادیتا")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "قالب سایت"
        verbose_name_plural = "قالب‌های سایت"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class GeneratedSite(models.Model):
    """سایت تولید شده"""
    SITE_STATUS = (
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
        ('archived', 'آرشیو شده'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    title = models.CharField(max_length=200, verbose_name="عنوان سایت")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    template = models.ForeignKey(SiteTemplate, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="قالب")
    domain = models.CharField(max_length=255, blank=True, verbose_name="دامنه")
    subdomain = models.CharField(max_length=100, blank=True, verbose_name="زیردامنه")
    html_content = models.TextField(verbose_name="محتوای HTML")
    css_content = models.TextField(blank=True, verbose_name="محتوای CSS")
    js_content = models.TextField(blank=True, verbose_name="محتوای JavaScript")
    assets = models.JSONField(default=dict, verbose_name="فایل‌های ضمیمه")
    settings = models.JSONField(default=dict, verbose_name="تنظیمات")
    status = models.CharField(max_length=20, choices=SITE_STATUS, default='draft', verbose_name="وضعیت")
    is_public = models.BooleanField(default=False, verbose_name="عمومی")
    seo_settings = models.JSONField(default=dict, verbose_name="تنظیمات SEO")
    analytics_code = models.TextField(blank=True, verbose_name="کد آنالیتیکس")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انتشار")
    
    class Meta:
        verbose_name = "سایت تولید شده"
        verbose_name_plural = "سایت‌های تولید شده"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class AIExtractionJob(models.Model):
    """وظیفه استخراج هوش مصنوعی"""
    JOB_STATUS = (
        ('pending', 'در انتظار'),
        ('running', 'در حال اجرا'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
        ('cancelled', 'لغو شده'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    job_type = models.CharField(max_length=50, verbose_name="نوع وظیفه")
    source_url = models.URLField(blank=True, verbose_name="آدرس منبع")
    source_type = models.CharField(max_length=50, verbose_name="نوع منبع")
    configuration = models.JSONField(default=dict, verbose_name="پیکربندی")
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='pending', verbose_name="وضعیت")
    progress = models.IntegerField(default=0, verbose_name="پیشرفت")
    result_data = models.JSONField(default=dict, verbose_name="داده‌های نتیجه")
    error_message = models.TextField(blank=True, verbose_name="پیام خطا")
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ شروع")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ تکمیل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "وظیفه استخراج هوش مصنوعی"
        verbose_name_plural = "وظایف استخراج هوش مصنوعی"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.job_type} - {self.user.username}"

class AIResource(models.Model):
    """منابع هوش مصنوعی"""
    RESOURCE_TYPE = (
        ('dataset', 'مجموعه داده'),
        ('model', 'مدل'),
        ('api', 'API'),
        ('tool', 'ابزار'),
        ('service', 'سرویس'),
        ('template', 'قالب'),
    )
    
    name = models.CharField(max_length=200, verbose_name="نام منبع")
    description = models.TextField(verbose_name="توضیحات")
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE, verbose_name="نوع منبع")
    source_url = models.URLField(blank=True, verbose_name="آدرس منبع")
    local_path = models.CharField(max_length=500, blank=True, verbose_name="مسیر محلی")
    metadata = models.JSONField(default=dict, verbose_name="متادیتا")
    is_offline_available = models.BooleanField(default=False, verbose_name="در دسترس آفلاین")
    file_size = models.BigIntegerField(default=0, verbose_name="حجم فایل")
    version = models.CharField(max_length=20, default="1.0.0", verbose_name="نسخه")
    tags = models.JSONField(default=list, verbose_name="برچسب‌ها")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "منبع هوش مصنوعی"
        verbose_name_plural = "منابع هوش مصنوعی"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class UserProject(models.Model):
    """پروژه کاربر"""
    PROJECT_STATUS = (
        ('active', 'فعال'),
        ('archived', 'آرشیو شده'),
        ('deleted', 'حذف شده'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    name = models.CharField(max_length=200, verbose_name="نام پروژه")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    sites = models.ManyToManyField(GeneratedSite, blank=True, verbose_name="سایت‌ها")
    templates = models.ManyToManyField(SiteTemplate, blank=True, verbose_name="قالب‌ها")
    settings = models.JSONField(default=dict, verbose_name="تنظیمات")
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='active', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "پروژه کاربر"
        verbose_name_plural = "پروژه‌های کاربر"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
