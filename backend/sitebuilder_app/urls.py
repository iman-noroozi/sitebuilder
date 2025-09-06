from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# تنظیمات Router برای API
router = DefaultRouter()
router.register(r'templates', views.TemplateViewSet)
router.register(r'sites', views.SiteViewSet, basename='site')

# URL patterns برای صفحات
urlpatterns = [
    # صفحات اصلی
    path('', views.site_builder, name='site_builder'),
    path('templates/', views.template_management, name='template_management'),
    path('templates/<int:template_id>/', views.template_detail, name='template_detail'),
    
    # مدیریت قالب‌های استخراج شده
    path('extracted-templates/', views.extracted_templates_management, name='extracted_templates_management'),
    path('extracted-templates/<path:template_path>/', views.extracted_template_detail, name='extracted_template_detail'),
    path('extracted-templates/<path:template_path>/import/', views.import_template_to_database, name='import_template_to_database'),
    path('template-analytics/', views.template_analytics, name='template_analytics'),
    
    # مدیریت ابزارهای کسب‌وکار
    path('business-tools/', views.business_tools_dashboard, name='business_tools_dashboard'),
    path('business-tools/list/', views.business_tools_list, name='business_tools_list'),
    path('business-tools/<path:tool_path>/', views.business_tool_detail, name='business_tool_detail'),
    path('business-tools/analytics/', views.business_tools_analytics, name='business_tools_analytics'),
    
    # سایت‌ساز
    path('create/', views.create_site, name='create_site'),
    path('editor/<int:site_id>/', views.site_editor, name='site_editor'),
    
    # ابزارهای هوش مصنوعی
    path('ai-tools/', views.ai_tools, name='ai_tools'),
    path('extraction/', views.start_extraction, name='start_extraction'),
    
    # API
    path('api/', include(router.urls)),
    
    # ابزارها
    path('health/', views.health_check, name='health_check'),
    path('webhook/', views.webhook_handler, name='webhook_handler'),
]
