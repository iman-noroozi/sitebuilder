// Frontend JavaScript for Website Template Extractor

class ExtractorUI {
    constructor() {
        this.isExtracting = false;
        this.currentJobId = null;
        this.startTime = null;
        
        this.initEventListeners();
    }

    initEventListeners() {
        const form = document.getElementById('extractForm');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.startExtraction();
        });

        const downloadBtn = document.getElementById('downloadBtn');
        downloadBtn.addEventListener('click', () => {
            this.downloadResult();
        });
    }

    async startExtraction() {
        if (this.isExtracting) return;

        this.isExtracting = true;
        this.startTime = Date.now();
        
        const formData = new FormData(document.getElementById('extractForm'));
        const options = this.getExtractionOptions(formData);

        this.showProgress();
        this.updateStatus('شروع فرآیند استخراج...');
        this.addLog('🚀 شروع استخراج سایت...', 'info');

        try {
            // Send extraction request
            const response = await fetch('/api/extract', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(options)
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            this.currentJobId = result.jobId;

            this.addLog(`✅ Job شروع شد: ${this.currentJobId}`, 'success');
            
            // Start polling for progress
            this.pollProgress();

        } catch (error) {
            this.addLog(`❌ خطا: ${error.message}`, 'error');
            this.showError(error.message);
        }
    }

    async pollProgress() {
        if (!this.currentJobId) return;

        try {
            const response = await fetch(`/api/status/${this.currentJobId}`);
            const status = await response.json();

            this.updateProgress(status);

            if (status.status === 'completed') {
                this.showResults(status);
            } else if (status.status === 'failed') {
                this.showError(status.error);
            } else {
                // Continue polling
                setTimeout(() => this.pollProgress(), 2000);
            }

        } catch (error) {
            this.addLog(`❌ خطا در دریافت وضعیت: ${error.message}`, 'error');
            setTimeout(() => this.pollProgress(), 5000);
        }
    }

    getExtractionOptions(formData) {
        return {
            url: formData.get('websiteUrl'),
            maxDepth: parseInt(formData.get('maxDepth')),
            extractCSS: document.getElementById('extractCSS').checked,
            extractJS: document.getElementById('extractJS').checked,
            extractImages: document.getElementById('extractImages').checked,
            extractFonts: document.getElementById('extractFonts').checked,
            extractVideos: document.getElementById('extractVideos').checked,
            followInternalLinks: document.getElementById('followLinks').checked,
            delay: 1000
        };
    }

    showProgress() {
        document.getElementById('progressSection').style.display = 'block';
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('extractBtn').disabled = true;
    }

    updateProgress(status) {
        const progressFill = document.getElementById('progressFill');
        const statusText = document.getElementById('statusText');

        if (status.progress !== undefined) {
            progressFill.style.width = `${status.progress}%`;
        }

        if (status.currentTask) {
            statusText.textContent = status.currentTask;
        }

        if (status.logs && Array.isArray(status.logs)) {
            status.logs.forEach(log => {
                this.addLog(log.message, log.type || 'info');
            });
        }
    }

    updateStatus(message) {
        document.getElementById('statusText').textContent = message;
    }

    addLog(message, type = 'info') {
        const logs = document.getElementById('logs');
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry log-${type}`;
        logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        
        logs.appendChild(logEntry);
        logs.scrollTop = logs.scrollHeight;
    }

    showResults(status) {
        this.isExtracting = false;
        document.getElementById('extractBtn').disabled = false;
        document.getElementById('progressSection').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'block';

        const extractTime = Math.round((Date.now() - this.startTime) / 1000);

        // Update statistics
        document.getElementById('totalPages').textContent = status.stats.totalPages || 0;
        document.getElementById('totalAssets').textContent = status.stats.totalAssets || 0;
        document.getElementById('totalSize').textContent = 
            status.stats.totalSize ? (status.stats.totalSize / (1024 * 1024)).toFixed(2) : '0';
        document.getElementById('extractTime').textContent = extractTime;

        this.addLog('🎉 استخراج با موفقیت تمام شد!', 'success');
    }

    showError(errorMessage) {
        this.isExtracting = false;
        document.getElementById('extractBtn').disabled = false;
        
        this.addLog(`❌ خطا در استخراج: ${errorMessage}`, 'error');
        this.updateStatus('خطا در استخراج');
        
        alert(`خطا در استخراج: ${errorMessage}`);
    }

    async downloadResult() {
        if (!this.currentJobId) return;

        try {
            this.addLog('📥 شروع دانلود فایل...', 'info');
            
            const response = await fetch(`/api/download/${this.currentJobId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = `extracted-website-${this.currentJobId}.zip`;
            document.body.appendChild(a);
            a.click();
            
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            this.addLog('✅ فایل با موفقیت دانلود شد!', 'success');
            
        } catch (error) {
            this.addLog(`❌ خطا در دانلود: ${error.message}`, 'error');
            alert(`خطا در دانلود: ${error.message}`);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.extractorUI = new ExtractorUI();
});

// Handle form validation
document.getElementById('websiteUrl').addEventListener('input', function() {
    const url = this.value;
    const isValid = /^https?:\/\/.+\..+/.test(url);
    
    if (url && !isValid) {
        this.setCustomValidity('لطفاً آدرس معتبر وارد کنید (شامل http:// یا https://)');
    } else {
        this.setCustomValidity('');
    }
});

// Add some nice animations
document.querySelectorAll('.option-item').forEach(item => {
    item.addEventListener('click', function() {
        const checkbox = this.querySelector('input[type="checkbox"]');
        checkbox.checked = !checkbox.checked;
        
        if (checkbox.checked) {
            this.style.background = '#e8f5e8';
        } else {
            this.style.background = '#f8f9fa';
        }
    });
});
