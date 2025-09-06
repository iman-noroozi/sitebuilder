from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.utils import timezone
import subprocess
import json
import os
import threading
import time

from .models import (
    TemplateCategory, 
    SiteTemplate, 
    GeneratedSite, 
    AIExtractionJob, 
    AIResource, 
    UserProject
)

# Views for Template Management
@login_required
def template_management(request):
    """مدیریت قالب‌ها"""
    categories = TemplateCategory.objects.filter(is_active=True)
    templates = SiteTemplate.objects.filter(status='active')
    
    # فیلتر کردن بر اساس دسته‌بندی
    category_id = request.GET.get('category')
    if category_id:
        templates = templates.filter(category_id=category_id)
    
    # جستجو
    search = request.GET.get('search')
    if search:
        templates = templates.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(tags__contains=[search])
        )
    
    # صفحه‌بندی
    paginator = Paginator(templates, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'templates': page_obj,
        'current_category': category_id,
        'search': search,
    }
    return render(request, 'sitebuilder_app/template_management.html', context)

@login_required
def template_detail(request, template_id):
    """جزئیات قالب"""
    template = get_object_or_404(SiteTemplate, id=template_id, status='active')
    context = {
        'template': template,
    }
    return render(request, 'sitebuilder_app/template_detail.html', context)

# Views for Site Builder
@login_required
def site_builder(request):
    """سایت‌ساز"""
    user_sites = GeneratedSite.objects.filter(user=request.user).order_by('-created_at')
    user_projects = UserProject.objects.filter(user=request.user, status='active')
    
    context = {
        'user_sites': user_sites,
        'user_projects': user_projects,
    }
    return render(request, 'sitebuilder_app/site_builder.html', context)

@login_required
def create_site(request):
    """ایجاد سایت جدید"""
    if request.method == 'POST':
        template_id = request.POST.get('template_id')
        site_title = request.POST.get('title')
        site_description = request.POST.get('description')
        
        template = None
        if template_id:
            template = get_object_or_404(SiteTemplate, id=template_id, status='active')
        
        site = GeneratedSite.objects.create(
            user=request.user,
            title=site_title,
            description=site_description,
            template=template,
            html_content=template.html_content if template else '',
            css_content=template.css_content if template else '',
            js_content=template.js_content if template else '',
        )
        
        messages.success(request, f'سایت "{site.title}" با موفقیت ایجاد شد.')
        return redirect('site_editor', site_id=site.id)
    
    templates = SiteTemplate.objects.filter(status='active', is_featured=True)
    context = {
        'templates': templates,
    }
    return render(request, 'sitebuilder_app/create_site.html', context)

@login_required
def site_editor(request, site_id):
    """ویرایشگر سایت"""
    site = get_object_or_404(GeneratedSite, id=site_id, user=request.user)
    
    if request.method == 'POST':
        site.html_content = request.POST.get('html_content', '')
        site.css_content = request.POST.get('css_content', '')
        site.js_content = request.POST.get('js_content', '')
        site.save()
        
        return JsonResponse({'status': 'success'})
    
    context = {
        'site': site,
    }
    return render(request, 'sitebuilder_app/site_editor.html', context)

# Views for AI Tools
@login_required
def ai_tools(request):
    """ابزارهای هوش مصنوعی"""
    ai_resources = AIResource.objects.filter(is_active=True)
    extraction_jobs = AIExtractionJob.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'ai_resources': ai_resources,
        'extraction_jobs': extraction_jobs,
    }
    return render(request, 'sitebuilder_app/ai_tools.html', context)

@login_required
def start_extraction(request):
    """شروع استخراج هوش مصنوعی"""
    if request.method == 'POST':
        job_type = request.POST.get('job_type')
        source_url = request.POST.get('source_url', '')
        source_type = request.POST.get('source_type', 'website')
        
        job = AIExtractionJob.objects.create(
            user=request.user,
            job_type=job_type,
            source_url=source_url,
            source_type=source_type,
            status='pending'
        )
        
        # شروع فرآیند استخراج در پس‌زمینه
        threading.Thread(target=run_extraction_job, args=(job.id,)).start()
        
        messages.success(request, 'فرآیند استخراج شروع شد.')
        return redirect('ai_tools')
    
    return render(request, 'sitebuilder_app/start_extraction.html')

def run_extraction_job(job_id):
    """اجرای وظیفه استخراج در پس‌زمینه"""
    job = AIExtractionJob.objects.get(id=job_id)
    try:
        job.status = 'running'
        job.started_at = timezone.now()
        job.save()
        
        # اینجا کد استخراج واقعی قرار می‌گیرد
        # فعلاً فقط شبیه‌سازی می‌کنیم
        time.sleep(5)  # شبیه‌سازی پردازش
        
        job.status = 'completed'
        job.progress = 100
        job.completed_at = timezone.now()
        job.result_data = {'message': 'استخراج با موفقیت انجام شد'}
        job.save()
        
    except Exception as e:
        job.status = 'failed'
        job.error_message = str(e)
        job.save()

# Views for Extracted Templates Management
@login_required
def extracted_templates_management(request):
    """مدیریت قالب‌های استخراج شده"""
    # بررسی قالب‌های موجود در پوشه templates_library
    templates_library_path = os.path.join(settings.BASE_DIR, '..', '..', '..', 'templates_library', 'site_templates')
    
    extracted_templates = []
    if os.path.exists(templates_library_path):
        for category_folder in os.listdir(templates_library_path):
            category_path = os.path.join(templates_library_path, category_folder)
            if os.path.isdir(category_path):
                for subcategory_folder in os.listdir(category_path):
                    subcategory_path = os.path.join(category_path, subcategory_folder)
                    if os.path.isdir(subcategory_path):
                        for template_folder in os.listdir(subcategory_path):
                            template_path = os.path.join(subcategory_path, template_folder)
                            if os.path.isdir(template_path):
                                # بررسی وجود فایل‌های قالب
                                template_files = {
                                    'index.html': os.path.join(template_path, 'index.html'),
                                    'style.css': os.path.join(template_path, 'style.css'),
                                    'script.js': os.path.join(template_path, 'script.js'),
                                }
                                
                                # بررسی وجود فایل‌ها
                                existing_files = {}
                                for file_type, file_path in template_files.items():
                                    if os.path.exists(file_path):
                                        existing_files[file_type] = file_path
                                
                                if existing_files:
                                    extracted_templates.append({
                                        'name': template_folder,
                                        'category': category_folder,
                                        'subcategory': subcategory_folder,
                                        'path': template_path,
                                        'files': existing_files,
                                        'file_count': len(existing_files),
                                        'size': sum(os.path.getsize(f) for f in existing_files.values() if os.path.exists(f))
                                    })
    
    # فیلتر کردن بر اساس دسته‌بندی
    category_filter = request.GET.get('category')
    if category_filter:
        extracted_templates = [t for t in extracted_templates if t['category'] == category_filter]
    
    # جستجو
    search = request.GET.get('search')
    if search:
        extracted_templates = [t for t in extracted_templates if search.lower() in t['name'].lower()]
    
    # صفحه‌بندی
    paginator = Paginator(extracted_templates, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # دسته‌بندی‌های موجود
    categories = list(set(t['category'] for t in extracted_templates))
    
    context = {
        'extracted_templates': page_obj,
        'categories': categories,
        'current_category': category_filter,
        'search': search,
        'total_templates': len(extracted_templates),
    }
    return render(request, 'sitebuilder_app/extracted_templates_management.html', context)

@login_required
def extracted_template_detail(request, template_path):
    """جزئیات قالب استخراج شده"""
    import urllib.parse
    decoded_path = urllib.parse.unquote(template_path)
    
    template_info = {
        'path': decoded_path,
        'name': os.path.basename(decoded_path),
        'files': {}
    }
    
    if os.path.exists(decoded_path):
        # خواندن فایل‌های قالب
        for file_name in ['index.html', 'style.css', 'script.js', 'README.md']:
            file_path = os.path.join(decoded_path, file_name)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        template_info['files'][file_name] = f.read()
                except:
                    template_info['files'][file_name] = f"خطا در خواندن فایل {file_name}"
        
        # اطلاعات فایل‌ها
        template_info['file_list'] = []
        for file_name in os.listdir(decoded_path):
            file_path = os.path.join(decoded_path, file_name)
            if os.path.isfile(file_path):
                template_info['file_list'].append({
                    'name': file_name,
                    'size': os.path.getsize(file_path),
                    'modified': timezone.datetime.fromtimestamp(os.path.getmtime(file_path))
                })
    
    context = {
        'template': template_info,
    }
    return render(request, 'sitebuilder_app/extracted_template_detail.html', context)

@login_required
def import_template_to_database(request, template_path):
    """وارد کردن قالب استخراج شده به دیتابیس"""
    import urllib.parse
    decoded_path = urllib.parse.unquote(template_path)
    
    if request.method == 'POST':
        try:
            template_name = request.POST.get('name')
            template_description = request.POST.get('description')
            category_id = request.POST.get('category')
            
            # خواندن فایل‌های قالب
            html_content = ""
            css_content = ""
            js_content = ""
            
            html_file = os.path.join(decoded_path, 'index.html')
            css_file = os.path.join(decoded_path, 'style.css')
            js_file = os.path.join(decoded_path, 'script.js')
            
            if os.path.exists(html_file):
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            
            if os.path.exists(css_file):
                with open(css_file, 'r', encoding='utf-8') as f:
                    css_content = f.read()
            
            if os.path.exists(js_file):
                with open(js_file, 'r', encoding='utf-8') as f:
                    js_content = f.read()
            
            # ایجاد قالب در دیتابیس
            category = get_object_or_404(TemplateCategory, id=category_id)
            
            template = SiteTemplate.objects.create(
                name=template_name,
                description=template_description,
                category=category,
                html_content=html_content,
                css_content=css_content,
                js_content=js_content,
                status='active',
                is_free=True,
                tags=['استخراج شده', 'قالب جدید'],
                metadata={
                    'source_path': decoded_path,
                    'imported_at': timezone.now().isoformat(),
                    'imported_by': request.user.username
                }
            )
            
            messages.success(request, f'قالب "{template_name}" با موفقیت وارد دیتابیس شد.')
            return redirect('template_management')
            
        except Exception as e:
            messages.error(request, f'خطا در وارد کردن قالب: {str(e)}')
    
    # نمایش فرم وارد کردن
    categories = TemplateCategory.objects.filter(is_active=True)
    template_name = os.path.basename(decoded_path)
    
    context = {
        'template_path': template_path,
        'template_name': template_name,
        'categories': categories,
    }
    return render(request, 'sitebuilder_app/import_template_form.html', context)

@login_required
def template_analytics(request):
    """آمار و گزارش قالب‌ها"""
    # آمار کلی
    total_templates = SiteTemplate.objects.count()
    active_templates = SiteTemplate.objects.filter(status='active').count()
    featured_templates = SiteTemplate.objects.filter(is_featured=True).count()
    free_templates = SiteTemplate.objects.filter(is_free=True).count()
    
    # آمار بر اساس دسته‌بندی
    category_stats = []
    categories = TemplateCategory.objects.filter(is_active=True)
    for category in categories:
        template_count = SiteTemplate.objects.filter(category=category, status='active').count()
        category_stats.append({
            'category': category,
            'count': template_count,
            'percentage': (template_count / active_templates * 100) if active_templates > 0 else 0
        })
    
    # قالب‌های استخراج شده
    templates_library_path = os.path.join(settings.BASE_DIR, '..', '..', '..', 'templates_library', 'site_templates')
    extracted_count = 0
    if os.path.exists(templates_library_path):
        for root, dirs, files in os.walk(templates_library_path):
            if 'index.html' in files:
                extracted_count += 1
    
    context = {
        'total_templates': total_templates,
        'active_templates': active_templates,
        'featured_templates': featured_templates,
        'free_templates': free_templates,
        'category_stats': category_stats,
        'extracted_count': extracted_count,
    }
    return render(request, 'sitebuilder_app/template_analytics.html', context)

# Views for Business Tools Management
@login_required
def business_tools_dashboard(request):
    """داشبورد ابزارهای کسب‌وکار"""
    try:
        # آمار کلی ابزارها
        tools_stats = {
            'total_tools': 0,
            'by_category': {},
            'by_status': {},
            'recent_additions': []
        }
        
        # بررسی وجود فایل‌های ابزارهای کسب‌وکار
        tools_directories = [
            'template_extractor/tools',
            'template_extractor/business_tools',
            'template_extractor/extracted_data'
        ]
        
        for directory in tools_directories:
            full_path = os.path.join(settings.BASE_DIR, '..', '..', '..', directory)
            if os.path.exists(full_path):
                tools_stats['total_tools'] += len([d for d in os.listdir(full_path) if os.path.isdir(os.path.join(full_path, d))])
        
        context = {
            'tools_stats': tools_stats,
            'tools_directories': tools_directories
        }
        return render(request, 'sitebuilder_app/business_tools_dashboard.html', context)
    except Exception as e:
        messages.error(request, f'خطا در بارگذاری داشبورد ابزارهای کسب‌وکار: {str(e)}')
        return render(request, 'sitebuilder_app/business_tools_dashboard.html', {'tools_stats': {}, 'tools_directories': []})

@login_required
def business_tools_list(request):
    """لیست ابزارهای کسب‌وکار"""
    try:
        tools = []
        tools_base_path = os.path.join(settings.BASE_DIR, '..', '..', '..', 'template_extractor')
        
        # بررسی ابزارهای استخراج شده
        tools_dirs = ['tools', 'business_tools', 'extracted_data']
        
        for dir_name in tools_dirs:
            dir_path = os.path.join(tools_base_path, dir_name)
            if os.path.exists(dir_path):
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    if os.path.isdir(item_path):
                        # خواندن README اگر وجود دارد
                        readme_path = os.path.join(item_path, 'README.md')
                        description = ''
                        if os.path.exists(readme_path):
                            try:
                                with open(readme_path, 'r', encoding='utf-8') as f:
                                    description = f.read()[:200] + '...' if len(f.read()) > 200 else f.read()
                            except:
                                description = 'توضیحات در دسترس نیست'
                        
                        tools.append({
                            'name': item,
                            'category': dir_name,
                            'path': os.path.join(dir_name, item),
                            'description': description,
                            'files': len([f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))]),
                            'created_at': os.path.getctime(item_path)
                        })
        
        # فیلتر کردن بر اساس دسته‌بندی
        category = request.GET.get('category')
        if category:
            tools = [tool for tool in tools if tool['category'] == category]
        
        # جستجو
        search = request.GET.get('search')
        if search:
            tools = [tool for tool in tools if search.lower() in tool['name'].lower() or search.lower() in tool['description'].lower()]
        
        # صفحه‌بندی
        paginator = Paginator(tools, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'tools': page_obj,
            'categories': list(set([tool['category'] for tool in tools])),
            'current_category': category,
            'search': search,
        }
        return render(request, 'sitebuilder_app/business_tools_list.html', context)
            except Exception as e:
        messages.error(request, f'خطا در بارگذاری لیست ابزارها: {str(e)}')
        return render(request, 'sitebuilder_app/business_tools_list.html', {'tools': [], 'categories': [], 'current_category': None, 'search': None})

@login_required
def business_tool_detail(request, tool_path):
    """جزئیات ابزار کسب‌وکار"""
    try:
        # رمزگشایی مسیر
        decoded_path = tool_path.replace('_', '/')
        full_path = os.path.join(settings.BASE_DIR, '..', '..', '..', 'template_extractor', decoded_path)
        
        if not os.path.exists(full_path):
            messages.error(request, 'ابزار مورد نظر یافت نشد')
            return redirect('business_tools_list')
        
        # اطلاعات ابزار
        tool_info = {
            'name': os.path.basename(full_path),
            'path': decoded_path,
            'category': os.path.basename(os.path.dirname(full_path)),
            'files': [],
            'readme_content': '',
            'created_at': os.path.getctime(full_path)
        }
        
        # لیست فایل‌ها
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            if os.path.isfile(item_path):
                tool_info['files'].append({
                    'name': item,
                    'size': os.path.getsize(item_path),
                    'extension': os.path.splitext(item)[1]
                })
        
        # خواندن README
        readme_path = os.path.join(full_path, 'README.md')
        if os.path.exists(readme_path):
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    tool_info['readme_content'] = f.read()
            except:
                tool_info['readme_content'] = 'خطا در خواندن فایل README'
        
        context = {
            'tool': tool_info
        }
        return render(request, 'sitebuilder_app/business_tool_detail.html', context)
    except Exception as e:
        messages.error(request, f'خطا در بارگذاری جزئیات ابزار: {str(e)}')
        return redirect('business_tools_list')

@login_required
def business_tools_analytics(request):
    """تحلیل و آمار ابزارهای کسب‌وکار"""
    try:
        analytics = {
            'total_tools': 0,
            'by_category': {},
            'by_type': {},
            'recent_activity': [],
            'popular_tools': []
        }
        
        tools_base_path = os.path.join(settings.BASE_DIR, '..', '..', '..', 'template_extractor')
        
        # بررسی تمام ابزارها
        for root, dirs, files in os.walk(tools_base_path):
            for dir_name in dirs:
                if dir_name not in ['__pycache__', '.git', 'node_modules']:
                    dir_path = os.path.join(root, dir_name)
                    category = os.path.basename(os.path.dirname(dir_path))
                    
                    analytics['total_tools'] += 1
                    analytics['by_category'][category] = analytics['by_category'].get(category, 0) + 1
                    
                    # بررسی نوع ابزار
                    if 'ai' in dir_name.lower() or 'chatbot' in dir_name.lower():
                        tool_type = 'AI Tools'
                    elif 'payment' in dir_name.lower() or 'financial' in dir_name.lower():
                        tool_type = 'Financial Tools'
                    elif 'analytics' in dir_name.lower() or 'data' in dir_name.lower():
                        tool_type = 'Analytics Tools'
                    else:
                        tool_type = 'Business Tools'
                    
                    analytics['by_type'][tool_type] = analytics['by_type'].get(tool_type, 0) + 1
        
        context = {
            'analytics': analytics
        }
        return render(request, 'sitebuilder_app/business_tools_analytics.html', context)
            except Exception as e:
        messages.error(request, f'خطا در بارگذاری آمار: {str(e)}')
        return render(request, 'sitebuilder_app/business_tools_analytics.html', {'analytics': {}})

# API Views
class TemplateViewSet(viewsets.ModelViewSet):
    """API برای مدیریت قالب‌ها"""
    queryset = SiteTemplate.objects.filter(status='active')
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = SiteTemplate.objects.filter(status='active')
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset
    
    @action(detail=True, methods=['post'])
    def preview(self, request, pk=None):
        """پیش‌نمایش قالب"""
        template = self.get_object()
        return Response({
            'html': template.html_content,
            'css': template.css_content,
            'js': template.js_content,
        })

class SiteViewSet(viewsets.ModelViewSet):
    """API برای مدیریت سایت‌ها"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GeneratedSite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """انتشار سایت"""
        site = self.get_object()
        site.status = 'published'
        site.published_at = timezone.now()
        site.save()
        return Response({'status': 'published'})

# Utility Views
def health_check(request):
    """بررسی سلامت سیستم"""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0'
    })

@csrf_exempt
def webhook_handler(request):
    """پردازش webhook ها"""
    if request.method == 'POST':
        data = json.loads(request.body)
        # پردازش webhook
        return JsonResponse({'status': 'received'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
