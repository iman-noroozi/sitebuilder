// SiteBuilder Frontend Application

// Initialize API instance
const api = new SiteBuilderAPI();

class SiteBuilderApp {
    constructor() {
        this.currentPage = 'templates';
        this.templates = [];
        this.sites = [];
        this.jobs = [];
        this.isExtracting = false;
        
        this.init();
    }

    init() {
        console.log('🚀 SiteBuilder App initializing...');
        this.setupEventListeners();
        this.checkAPIConnection();
        this.loadTemplates();
        this.loadSites();
        this.startJobPolling();
    }

    async checkAPIConnection() {
        console.log('🔍 Checking API connection...');
        const isConnected = await api.checkConnection();
        console.log('API Connection status:', isConnected);
        
        const statusEl = document.createElement('div');
        statusEl.style.cssText = `
            position: fixed;
            top: 10px;
            left: 20px;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            font-size: 0.875rem;
            z-index: 1002;
            ${isConnected ? 
                'background: var(--success-color); color: white;' : 
                'background: var(--warning-color); color: white;'
            }
        `;
        statusEl.innerHTML = isConnected ? 
            '<i class="fas fa-check"></i> Django متصل' : 
            '<i class="fas fa-exclamation-triangle"></i> حالت دمو (Django غیرفعال)';
        
        document.body.appendChild(statusEl);
        setTimeout(() => statusEl.remove(), 3000);
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const page = item.dataset.page;
                this.showPage(page);
            });
        });

        // Extraction form
        document.getElementById('extraction-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleExtraction();
        });
    }

    showPage(pageName) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-page="${pageName}"]`).classList.add('active');

        // Update pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        document.getElementById(`${pageName}-page`).classList.add('active');

        this.currentPage = pageName;

        // Load data for the page
        if (pageName === 'templates') {
            this.loadTemplates();
        } else if (pageName === 'sites') {
            this.loadSites();
        }
    }

    async loadTemplates() {
        try {
            // Try to get real data from API
            const response = await api.getTemplates();
            this.templates = response.results || response;
            this.renderTemplates();
            this.updateStats();
        } catch (error) {
            console.error('خطا در بارگذاری قالب‌ها:', error);
            // Fallback to mock data is handled in API class
            this.showError('خطا در بارگذاری قالب‌ها - استفاده از داده‌های نمونه');
        }
    }

    async loadSites() {
        try {
            // Try to get real data from API
            const response = await api.getSites();
            this.sites = response.results || response;
            this.renderSites();
        } catch (error) {
            console.error('خطا در بارگذاری سایت‌ها:', error);
            this.showError('خطا در بارگذاری سایت‌ها - استفاده از داده‌های نمونه');
        }
    }

    async loadJobs() {
        try {
            const response = await api.getJobs();
            this.jobs = response.results || response;
            this.updateJobsProgress();
        } catch (error) {
            console.error('خطا در بارگذاری وظایف:', error);
        }
    }

    renderTemplates() {
        const grid = document.getElementById('templates-grid');
        
        if (this.templates.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-secondary);">
                    <i class="fas fa-layer-group" style="font-size: 3rem; margin-bottom: 1rem; display: block;"></i>
                    <p>هنوز قالبی استخراج نشده است</p>
                    <button class="btn btn-primary" onclick="app.showPage('extract')" style="margin-top: 1rem;">
                        استخراج اولین قالب
                    </button>
                </div>
            `;
            return;
        }

        grid.innerHTML = this.templates.map(template => this.createTemplateCard(template)).join('');
    }

    createTemplateCard(template) {
        const statusClass = `status-${template.status}`;
        const statusText = {
            'completed': 'تکمیل شده',
            'pending': 'در انتظار',
            'extracting': 'در حال استخراج',
            'failed': 'ناموفق'
        }[template.status];

        const statusIcon = {
            'completed': 'fas fa-check-circle',
            'pending': 'fas fa-clock',
            'extracting': 'fas fa-spinner fa-spin',
            'failed': 'fas fa-exclamation-circle'
        }[template.status];

        return `
            <div class="template-card">
                <div class="template-screenshot">
                    ${template.has_screenshot ? 
                        `<img src="/media/screenshots/${template.id}_screenshot.png" alt="Screenshot" onerror="this.parentElement.innerHTML='<i class=\\"fas fa-image\\"></i><span>بدون اسکرین‌شات</span>'">` :
                        `<i class="fas fa-image"></i><span>بدون اسکرین‌شات</span>`
                    }
                </div>
                <div class="template-info">
                    <h3 class="template-title">${template.title}</h3>
                    <p class="template-url">${template.url}</p>
                    
                    <div class="template-status ${statusClass}">
                        <i class="${statusIcon}"></i>
                        ${statusText}
                    </div>
                    
                    ${template.extraction_stats ? `
                        <div class="template-stats">
                            <span><i class="fas fa-code"></i> ${template.extraction_stats.scripts} اسکریپت</span>
                            <span><i class="fas fa-image"></i> ${template.extraction_stats.images} تصویر</span>
                            <span><i class="fas fa-font"></i> ${template.extraction_stats.fonts} فونت</span>
                        </div>
                    ` : ''}
                    
                    <div class="template-actions">
                        ${template.status === 'completed' ? `
                            <button class="btn btn-primary" onclick="app.downloadTemplate(${template.id})">
                                <i class="fas fa-download"></i> دانلود
                            </button>
                            <button class="btn btn-secondary" onclick="app.previewTemplate(${template.id})">
                                <i class="fas fa-eye"></i> پیش‌نمایش
                            </button>
                        ` : ''}
                        <button class="btn btn-error" onclick="app.deleteTemplate(${template.id})">
                            <i class="fas fa-trash"></i> حذف
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    renderSites() {
        const grid = document.getElementById('sites-grid');
        
        if (this.sites.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-secondary);">
                    <i class="fas fa-globe" style="font-size: 3rem; margin-bottom: 1rem; display: block;"></i>
                    <p>هنوز سایتی ایجاد نشده است</p>
                    <button class="btn btn-primary" onclick="app.createNewSite()" style="margin-top: 1rem;">
                        ایجاد اولین سایت
                    </button>
                </div>
            `;
            return;
        }

        grid.innerHTML = this.sites.map(site => this.createSiteCard(site)).join('');
    }

    createSiteCard(site) {
        return `
            <div class="template-card">
                <div class="template-info">
                    <h3 class="template-title">${site.name}</h3>
                    <p class="template-url">${site.domain}</p>
                    
                    <div class="template-status ${site.is_published ? 'status-completed' : 'status-pending'}">
                        <i class="${site.is_published ? 'fas fa-check-circle' : 'fas fa-clock'}"></i>
                        ${site.is_published ? 'منتشر شده' : 'منتشر نشده'}
                    </div>
                    
                    <div class="template-stats">
                        <span><i class="fas fa-layer-group"></i> ${site.template_title}</span>
                        <span><i class="fas fa-calendar"></i> ${new Date(site.created_at).toLocaleDateString('fa-IR')}</span>
                    </div>
                    
                    <div class="template-actions">
                        ${site.is_published ? `
                            <button class="btn btn-success" onclick="window.open('${site.site_url}', '_blank')">
                                <i class="fas fa-external-link-alt"></i> مشاهده
                            </button>
                            <button class="btn btn-warning" onclick="app.unpublishSite(${site.id})">
                                <i class="fas fa-pause"></i> لغو انتشار
                            </button>
                        ` : `
                            <button class="btn btn-primary" onclick="app.publishSite(${site.id})">
                                <i class="fas fa-rocket"></i> انتشار
                            </button>
                        `}
                        <button class="btn btn-secondary" onclick="app.editSite(${site.id})">
                            <i class="fas fa-edit"></i> ویرایش
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    updateStats() {
        const total = this.templates.length;
        const completed = this.templates.filter(t => t.status === 'completed').length;
        const pending = this.templates.filter(t => t.status === 'pending' || t.status === 'extracting').length;

        document.getElementById('total-templates').textContent = total;
        document.getElementById('completed-templates').textContent = completed;
        document.getElementById('pending-templates').textContent = pending;
    }

    async handleExtraction() {
        if (this.isExtracting) return;

        const form = document.getElementById('extraction-form');
        const formData = new FormData(form);
        
        const extractionData = {
            url: formData.get('url'),
            title: formData.get('title') || '',
            take_screenshot: formData.get('take_screenshot') === 'on',
            extract_images: formData.get('extract_images') === 'on',
            extract_fonts: formData.get('extract_fonts') === 'on',
            headless: true,
            timeout: 60000
        };

        try {
            this.isExtracting = true;
            this.showExtractionProgress();
            
            // Try real API first
            const response = await api.extractTemplate(extractionData);
            
            if (response.template_id) {
                // Real API response - start polling for progress
                this.pollExtractionProgress(response.template_id);
            } else {
                // Mock response - simulate extraction
                await this.simulateExtraction(extractionData);
            }
            
            this.showSuccess(response.message || 'استخراج با موفقیت آغاز شد');
            
        } catch (error) {
            console.error('خطا در استخراج:', error);
            this.showError('خطا در شروع استخراج: ' + error.message);
            this.hideExtractionProgress();
        } finally {
            // Don't set isExtracting to false immediately for real API
            if (!response || !response.template_id) {
                setTimeout(() => {
                    this.isExtracting = false;
                    this.hideExtractionProgress();
                    this.loadTemplates();
                    form.reset();
                }, 3000);
            }
        }
    }

    async pollExtractionProgress(templateId) {
        const pollInterval = setInterval(async () => {
            try {
                const jobs = await api.getJobs();
                const currentJob = jobs.results?.find(job => job.template === templateId);
                
                if (currentJob) {
                    // Update progress
                    document.getElementById('progress-fill').style.width = currentJob.progress + '%';
                    document.getElementById('progress-text').textContent = currentJob.current_step;
                    
                    // Add log entry
                    const logsEl = document.getElementById('extraction-logs');
                    const logEntry = document.createElement('div');
                    logEntry.className = 'log-entry log-info';
                    logEntry.textContent = `${currentJob.progress}% - ${currentJob.current_step}`;
                    logsEl.appendChild(logEntry);
                    logsEl.scrollTop = logsEl.scrollHeight;
                    
                } else {
                    // Job completed - check if template is ready
                    await this.loadTemplates();
                    const template = this.templates.find(t => t.id === templateId);
                    
                    if (template && template.status === 'completed') {
                        clearInterval(pollInterval);
                        this.hideExtractionProgress();
                        this.isExtracting = false;
                        this.showSuccess('استخراج با موفقیت تکمیل شد!');
                        document.getElementById('extraction-form').reset();
                    }
                }
                
            } catch (error) {
                console.error('خطا در polling:', error);
            }
        }, 2000); // Poll every 2 seconds
        
        // Stop polling after 5 minutes
        setTimeout(() => {
            clearInterval(pollInterval);
            if (this.isExtracting) {
                this.hideExtractionProgress();
                this.isExtracting = false;
                this.showError('زمان استخراج بیش از حد طولانی شد');
            }
        }, 300000);
    }

    async simulateExtraction(data) {
        const progressEl = document.getElementById('progress-fill');
        const textEl = document.getElementById('progress-text');
        const logsEl = document.getElementById('extraction-logs');
        
        const steps = [
            { progress: 10, text: 'اتصال به سایت...', log: 'ℹ️ شروع استخراج از: ' + data.url },
            { progress: 30, text: 'بارگذاری صفحه...', log: 'ℹ️ در حال بارگذاری صفحه...' },
            { progress: 50, text: 'استخراج HTML و CSS...', log: 'ℹ️ استخراج HTML و CSS...' },
            { progress: 70, text: 'دانلود تصاویر و فونت‌ها...', log: 'ℹ️ دانلود موازی فایل‌ها...' },
            { progress: 90, text: 'ایجاد فایل‌های نهایی...', log: 'ℹ️ ایجاد فایل HTML نهایی...' },
            { progress: 100, text: 'استخراج تکمیل شد', log: '✅ استخراج کامل شد' }
        ];

        for (let step of steps) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            progressEl.style.width = step.progress + '%';
            textEl.textContent = step.text;
            
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry log-info';
            logEntry.textContent = step.log;
            logsEl.appendChild(logEntry);
            logsEl.scrollTop = logsEl.scrollHeight;
        }
    }

    showExtractionProgress() {
        document.getElementById('extraction-progress').style.display = 'block';
        document.getElementById('extract-btn').disabled = true;
        document.getElementById('progress-fill').style.width = '0%';
        document.getElementById('progress-text').textContent = 'شروع فرآیند...';
        document.getElementById('extraction-logs').innerHTML = '';
    }

    hideExtractionProgress() {
        setTimeout(() => {
            document.getElementById('extraction-progress').style.display = 'none';
            document.getElementById('extract-btn').disabled = false;
        }, 2000);
    }

    async downloadTemplate(id) {
        try {
            const response = await api.downloadTemplate(id);
            
            if (response.download_url) {
                // Real API response
                window.open(response.download_url, '_blank');
                this.showSuccess(`فایل آماده دانلود: ${response.filename || 'template.zip'}`);
            } else {
                // Fallback for development
                window.open(`/download/template_${id}.zip`, '_blank');
                this.showSuccess('دانلود آغاز شد (حالت دمو)');
            }
        } catch (error) {
            console.error('خطا در دانلود:', error);
            this.showError('خطا در دانلود قالب: ' + error.message);
        }
    }

    async deleteTemplate(id) {
        if (!confirm('آیا از حذف این قالب مطمئن هستید؟')) return;

        try {
            await api.deleteTemplate(id);
            
            // Remove from local array
            this.templates = this.templates.filter(t => t.id !== id);
            
            this.renderTemplates();
            this.updateStats();
            this.showSuccess('قالب با موفقیت حذف شد');
        } catch (error) {
            console.error('خطا در حذف:', error);
            this.showError('خطا در حذف قالب: ' + error.message);
        }
    }

    async publishSite(id) {
        try {
            const response = await api.publishSite(id);
            
            // Update local data
            const site = this.sites.find(s => s.id === id);
            if (site) {
                site.is_published = true;
                site.site_url = site.site_url || `https://${site.domain}`;
            }
            
            this.renderSites();
            this.showSuccess(response.message || 'سایت با موفقیت منتشر شد');
        } catch (error) {
            console.error('خطا در انتشار:', error);
            this.showError('خطا در انتشار سایت: ' + error.message);
        }
    }

    async unpublishSite(id) {
        try {
            const response = await api.unpublishSite(id);
            
            // Update local data
            const site = this.sites.find(s => s.id === id);
            if (site) {
                site.is_published = false;
                site.site_url = null;
            }
            
            this.renderSites();
            this.showSuccess(response.message || 'انتشار سایت لغو شد');
        } catch (error) {
            console.error('خطا در لغو انتشار:', error);
            this.showError('خطا در لغو انتشار: ' + error.message);
        }
    }

    createNewSite() {
        alert('ساخت سایت جدید - این قابلیت بزودی اضافه خواهد شد');
    }

    editSite(id) {
        alert('ویرایش سایت - این قابلیت بزودی اضافه خواهد شد');
    }

    startJobPolling() {
        // Poll for extraction jobs every 3 seconds
        setInterval(async () => {
            if (this.currentPage === 'templates' && !this.isExtracting) {
                try {
                    await this.loadJobs();
                } catch (error) {
                    // Ignore polling errors
                }
            }
        }, 3000);
    }

    updateJobsProgress() {
        // Show active jobs in the UI
        if (this.jobs && this.jobs.length > 0) {
            // Add job status to templates page
            const activeJobs = this.jobs.filter(job => job.progress < 100);
            if (activeJobs.length > 0) {
                this.showJobsStatus(activeJobs);
            }
        }
    }

    showJobsStatus(jobs) {
        let existingStatus = document.getElementById('jobs-status');
        if (!existingStatus) {
            existingStatus = document.createElement('div');
            existingStatus.id = 'jobs-status';
            existingStatus.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: var(--card-bg);
                border-radius: 0.5rem;
                padding: 1rem;
                box-shadow: var(--shadow-lg);
                max-width: 300px;
                z-index: 1000;
            `;
            document.body.appendChild(existingStatus);
        }

        existingStatus.innerHTML = `
            <h4 style="margin: 0 0 0.5rem 0; color: var(--text-primary);">
                <i class="fas fa-cog fa-spin"></i> استخراج در حال انجام
            </h4>
            ${jobs.map(job => `
                <div style="margin-bottom: 0.5rem;">
                    <div style="font-size: 0.875rem; margin-bottom: 0.25rem;">${job.template_title}</div>
                    <div class="progress-bar" style="height: 4px;">
                        <div class="progress-fill" style="width: ${job.progress}%;"></div>
                    </div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary);">${job.current_step}</div>
                </div>
            `).join('')}
        `;

        // Remove status when all jobs are complete
        if (jobs.every(job => job.progress >= 100)) {
            setTimeout(() => {
                if (existingStatus) existingStatus.remove();
            }, 3000);
        }
    }

    showSuccess(message) {
        // Simple success notification
        const notification = document.createElement('div');
        notification.className = 'notification success';
        notification.innerHTML = `<i class="fas fa-check"></i> ${message}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--success-color);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: var(--shadow-lg);
            z-index: 1001;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        `;
        
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }

    showError(message) {
        // Simple error notification
        const notification = document.createElement('div');
        notification.className = 'notification error';
        notification.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--error-color);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: var(--shadow-lg);
            z-index: 1001;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        `;
        
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 5000);
    }
}

// Global functions for HTML onclick handlers
function showPage(page) {
    app.showPage(page);
}

function closeModal() {
    document.getElementById('preview-modal').classList.remove('active');
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌐 DOM loaded, starting SiteBuilder...');
    window.app = new SiteBuilderApp();
});
