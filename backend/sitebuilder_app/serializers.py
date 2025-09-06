from rest_framework import serializers
from .models import ExtractedTemplate, GeneratedSite, ExtractionJob

class ExtractedTemplateSerializer(serializers.ModelSerializer):
    extraction_stats = serializers.ReadOnlyField()
    has_screenshot = serializers.ReadOnlyField()
    
    class Meta:
        model = ExtractedTemplate
        fields = [
            'id', 'title', 'url', 'status', 'output_path', 
            'screenshot_path', 'metadata', 'extraction_log',
            'created_at', 'updated_at', 'extraction_stats', 'has_screenshot'
        ]
        read_only_fields = ['status', 'output_path', 'screenshot_path', 'extraction_log']

class ExtractTemplateRequestSerializer(serializers.Serializer):
    """سریالایزر برای درخواست استخراج قالب"""
    url = serializers.URLField(required=True, help_text="آدرس سایت برای استخراج")
    title = serializers.CharField(max_length=200, required=False, help_text="عنوان قالب (اختیاری)")
    
    # تنظیمات اختیاری
    headless = serializers.BooleanField(default=True, help_text="حالت headless مرورگر")
    take_screenshot = serializers.BooleanField(default=True, help_text="گرفتن اسکرین‌شات")
    extract_images = serializers.BooleanField(default=True, help_text="استخراج تصاویر")
    extract_fonts = serializers.BooleanField(default=True, help_text="استخراج فونت‌ها")
    timeout = serializers.IntegerField(default=30000, help_text="تایم‌اوت (میلی‌ثانیه)")

class GeneratedSiteSerializer(serializers.ModelSerializer):
    site_url = serializers.ReadOnlyField()
    template_title = serializers.CharField(source='template.title', read_only=True)
    
    class Meta:
        model = GeneratedSite
        fields = [
            'id', 'name', 'description', 'domain', 'is_published',
            'publish_path', 'custom_settings', 'created_at', 'updated_at',
            'published_at', 'site_url', 'template_title'
        ]

class ExtractionJobSerializer(serializers.ModelSerializer):
    template_title = serializers.CharField(source='template.title', read_only=True)
    
    class Meta:
        model = ExtractionJob
        fields = [
            'id', 'progress', 'current_step', 'started_at', 
            'estimated_completion', 'template_title'
        ]
        read_only_fields = ['progress', 'current_step', 'started_at']
