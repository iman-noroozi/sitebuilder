from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # صفحه اصلی - طراحی Duda
    path('', TemplateView.as_view(template_name='index_duda_exact.html'), name='home'),
    
    # پنل ادمین
    path('admin/', admin.site.urls),
    
    # API احراز هویت
    path('api/auth/', include('rest_framework.urls')),
    
    # SiteBuilder App
    path('sitebuilder/', include('sitebuilder_app.urls')),
]

# در حالت DEBUG، فایل‌های استاتیک و مدیا را سرو کن
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
