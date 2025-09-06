from django.contrib import admin
from .models import (
    TemplateCategory, 
    SiteTemplate, 
    GeneratedSite, 
    AIExtractionJob, 
    AIResource, 
    UserProject
)

@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_en', 'description']
    ordering = ['name']

@admin.register(SiteTemplate)
class SiteTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'status', 'is_featured', 'is_free', 'price', 'created_at']
    list_filter = ['status', 'is_featured', 'is_free', 'category', 'created_at']
    search_fields = ['name', 'description', 'tags']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'description', 'category', 'status')
        }),
        ('محتوای قالب', {
            'fields': ('html_content', 'css_content', 'js_content')
        }),
        ('فایل‌ها', {
            'fields': ('preview_image', 'template_file')
        }),
        ('تنظیمات', {
            'fields': ('is_featured', 'is_free', 'price', 'tags', 'metadata')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(GeneratedSite)
class GeneratedSiteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'template', 'status', 'is_public', 'created_at']
    list_filter = ['status', 'is_public', 'created_at', 'template']
    search_fields = ['title', 'description', 'domain', 'subdomain']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'published_at']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'title', 'description', 'template')
        }),
        ('دامنه و آدرس', {
            'fields': ('domain', 'subdomain')
        }),
        ('محتوای سایت', {
            'fields': ('html_content', 'css_content', 'js_content', 'assets')
        }),
        ('تنظیمات', {
            'fields': ('settings', 'status', 'is_public', 'seo_settings', 'analytics_code')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AIExtractionJob)
class AIExtractionJobAdmin(admin.ModelAdmin):
    list_display = ['job_type', 'user', 'status', 'progress', 'created_at']
    list_filter = ['status', 'job_type', 'source_type', 'created_at']
    search_fields = ['job_type', 'source_url', 'error_message']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'started_at', 'completed_at']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'job_type', 'source_url', 'source_type')
        }),
        ('پیکربندی', {
            'fields': ('configuration',)
        }),
        ('وضعیت', {
            'fields': ('status', 'progress', 'result_data', 'error_message')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AIResource)
class AIResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'resource_type', 'is_offline_available', 'is_active', 'created_at']
    list_filter = ['resource_type', 'is_offline_available', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'tags']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'description', 'resource_type')
        }),
        ('منابع', {
            'fields': ('source_url', 'local_path', 'file_size', 'version')
        }),
        ('تنظیمات', {
            'fields': ('is_offline_available', 'is_active', 'tags', 'metadata')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserProject)
class UserProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['sites', 'templates']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'name', 'description', 'status')
        }),
        ('محتوای پروژه', {
            'fields': ('sites', 'templates', 'settings')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
