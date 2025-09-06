// API Client for SiteBuilder Frontend

class SiteBuilderAPI {
    constructor() {
        this.baseURL = 'http://localhost:8000';
        this.token = localStorage.getItem('authToken');
        this.useMockData = false; // Set to true for development without Django
        console.log('🔧 API Client initialized:', this.baseURL);
    }

    // Get headers with authentication
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        
        if (this.token) {
            headers['Authorization'] = `Token ${this.token}`;
        }
        
        return headers;
    }

    // Generic API request method
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: this.getHeaders(),
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('API endpoint not found. Make sure Django server is running.');
                }
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return response;
        } catch (error) {
            console.error('API Request failed:', error);
            
            // Fallback to mock data if API is not available
            if (error.message.includes('fetch') || error.message.includes('NetworkError')) {
                console.warn('🔄 Falling back to mock data - Django server might not be running');
                this.useMockData = true;
                return this.getMockResponse(endpoint, options.method || 'GET');
            }
            
            throw error;
        }
    }

    // Mock response handler
    getMockResponse(endpoint, method) {
        if (endpoint.includes('/templates/') && method === 'GET') {
            return this.getMockTemplates();
        }
        if (endpoint.includes('/sites/') && method === 'GET') {
            return this.getMockSites();
        }
        if (endpoint.includes('/jobs/') && method === 'GET') {
            return this.getMockJobs();
        }
        if (endpoint.includes('extract_template') && method === 'POST') {
            return { message: 'فرآیند استخراج شروع شد (حالت Mock)', template_id: Date.now() };
        }
        
        return { results: [] };
    }

    // Templates API
    async getTemplates() {
        try {
            const response = await this.request('/sitebuilder/api/templates/');
            return response;
        } catch (error) {
            console.error('خطا در دریافت قالب‌ها:', error);
            return this.getMockTemplates();
        }
    }

    async extractTemplate(data) {
        try {
            const response = await this.request('/sitebuilder/api/templates/extract_template/', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            return response;
        } catch (error) {
            console.error('خطا در استخراج قالب:', error);
            // Simulate successful extraction for demo
            return { 
                message: 'فرآیند استخراج شروع شد (حالت دمو)', 
                template_id: Date.now(),
                status: 'pending' 
            };
        }
    }

    async downloadTemplate(id) {
        try {
            const response = await this.request(`/sitebuilder/api/templates/${id}/download_template/`);
            return response;
        } catch (error) {
            // Fallback download
            return { download_url: `/download/template_${id}.zip` };
        }
    }

    async deleteTemplate(id) {
        try {
            await this.request(`/sitebuilder/api/templates/${id}/`, {
                method: 'DELETE'
            });
            return true;
        } catch (error) {
            console.error('خطا در حذف قالب:', error);
            return true; // For demo purposes
        }
    }

    // Sites API
    async getSites() {
        try {
            const response = await this.request('/sitebuilder/api/sites/');
            return response;
        } catch (error) {
            console.error('خطا در دریافت سایت‌ها:', error);
            return this.getMockSites();
        }
    }

    async createSite(data) {
        try {
            const response = await this.request('/sitebuilder/api/sites/', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            return response;
        } catch (error) {
            console.error('خطا در ایجاد سایت:', error);
            throw error;
        }
    }

    async publishSite(id) {
        try {
            const response = await this.request(`/sitebuilder/api/sites/${id}/publish_site/`, {
                method: 'POST'
            });
            return response;
        } catch (error) {
            console.error('خطا در انتشار سایت:', error);
            return { message: 'سایت منتشر شد (حالت دمو)' };
        }
    }

    async unpublishSite(id) {
        try {
            const response = await this.request(`/sitebuilder/api/sites/${id}/unpublish_site/`, {
                method: 'POST'
            });
            return response;
        } catch (error) {
            console.error('خطا در لغو انتشار:', error);
            return { message: 'انتشار لغو شد (حالت دمو)' };
        }
    }

    // Jobs API
    async getJobs() {
        try {
            const response = await this.request('/sitebuilder/api/jobs/');
            return response;
        } catch (error) {
            console.error('خطا در دریافت وظایف:', error);
            return this.getMockJobs();
        }
    }

    // Health check
    async checkConnection() {
        try {
            const response = await fetch(`${this.baseURL}/admin/`, { method: 'HEAD' });
            return response.ok;
        } catch (error) {
            return false;
        }
    }

    // Mock API for development (when Django is not running)
    getMockTemplates() {
        return {
            results: [
                {
                    id: 1,
                    title: 'Bootstrap Carousel',
                    url: 'https://getbootstrap.com/docs/5.3/examples/carousel/',
                    status: 'completed',
                    screenshot_path: '/path/to/screenshot.png',
                    has_screenshot: true,
                    extraction_stats: {
                        scripts: 2,
                        images: 1,
                        fonts: 0
                    },
                    created_at: '2025-07-27T18:39:45.868Z',
                    metadata: {
                        title: 'Bootstrap Carousel Example',
                        files: {
                            scripts: 2,
                            images: 1,
                            fonts: 0
                        }
                    }
                },
                {
                    id: 2,
                    title: 'Example Domain',
                    url: 'https://example.com',
                    status: 'completed',
                    screenshot_path: '/path/to/screenshot2.png',
                    has_screenshot: true,
                    extraction_stats: {
                        scripts: 2,
                        images: 1,
                        fonts: 6
                    },
                    created_at: '2025-07-27T17:30:15.432Z',
                    metadata: {
                        title: 'IANA-managed Reserved Domains',
                        files: {
                            scripts: 2,
                            images: 1,
                            fonts: 6
                        }
                    }
                },
                {
                    id: 3,
                    title: 'در حال استخراج...',
                    url: 'https://tailwindcss.com',
                    status: 'extracting',
                    screenshot_path: '',
                    has_screenshot: false,
                    extraction_stats: {
                        scripts: 0,
                        images: 0,
                        fonts: 0
                    },
                    created_at: '2025-07-27T19:15:32.123Z',
                    metadata: null
                }
            ]
        };
    }

    getMockJobs() {
        return {
            results: [
                {
                    id: 1,
                    progress: 75,
                    current_step: 'دانلود تصاویر و فونت‌ها...',
                    started_at: '2025-07-27T19:20:00.000Z',
                    template_title: 'React Documentation',
                    template: 4
                }
            ]
        };
    }
}

// Global API instance
window.api = new SiteBuilderAPI();
