// HTML5UP Template Mass Extractor
// استخراج انبوه قالب‌های HTML5UP - بهترین منبع قالب رایگان

const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');
const https = require('https');
const AdmZip = require('adm-zip');

console.log('🎨 شروع استخراج کامل قالب‌های HTML5UP...');
console.log('============================================');

class HTML5UPExtractor {
    constructor() {
        this.baseUrl = 'https://html5up.net';
        this.outputDir = './extracted_sites/html5up_templates';
        this.browser = null;
        this.page = null;
        this.extractedTemplates = [];
        this.errors = [];
    }

    async init() {
        console.log('🚀 راه‌اندازی مرورگر...');
        
        this.browser = await puppeteer.launch({
            headless: 'new',
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        });

        this.page = await this.browser.newPage();
        await this.page.setViewport({ width: 1920, height: 1080 });
        
        // ایجاد پوشه خروجی
        await fs.mkdir(this.outputDir, { recursive: true });
        console.log('✅ راه‌اندازی کامل شد');
    }

    async getAllTemplates() {
        console.log('🔍 جستجوی تمام قالب‌های موجود...');
        
        try {
            await this.page.goto(this.baseUrl, { waitUntil: 'networkidle2' });
            
            // استخراج لینک‌های تمام قالب‌ها
            const templates = await this.page.evaluate(() => {
                const templateLinks = [];
                const links = document.querySelectorAll('section.wrapper.style1 article h3 a');
                
                links.forEach(link => {
                    const href = link.getAttribute('href');
                    const title = link.textContent.trim();
                    if (href && href.startsWith('/')) {
                        templateLinks.push({
                            name: title,
                            path: href,
                            url: 'https://html5up.net' + href
                        });
                    }
                });
                
                return templateLinks;
            });
            
            console.log(`✅ ${templates.length} قالب پیدا شد`);
            return templates;
            
        } catch (error) {
            console.error('❌ خطا در جستجوی قالب‌ها:', error.message);
            return [];
        }
    }

    async extractTemplate(template, index, total) {
        console.log(`🎯 در حال استخراج: ${template.name} (${index + 1}/${total})`);
        
        try {
            // رفتن به صفحه قالب
            await this.page.goto(template.url, { waitUntil: 'networkidle2' });
            
            // پیدا کردن لینک دانلود
            const downloadInfo = await this.page.evaluate(() => {
                const downloadLink = document.querySelector('a[href*=".zip"]');
                if (downloadLink) {
                    return {
                        downloadUrl: downloadLink.href,
                        fileName: downloadLink.href.split('/').pop()
                    };
                }
                return null;
            });
            
            if (!downloadInfo) {
                throw new Error('لینک دانلود پیدا نشد');
            }
            
            // دانلود فایل ZIP
            const templateDir = path.join(this.outputDir, this.sanitizeName(template.name));
            await fs.mkdir(templateDir, { recursive: true });
            
            const zipPath = path.join(templateDir, downloadInfo.fileName);
            await this.downloadFile(downloadInfo.downloadUrl, zipPath);
            
            // استخراج فایل ZIP
            await this.extractZip(zipPath, templateDir);
            
            // ایجاد فایل اطلاعات
            const templateInfo = {
                name: template.name,
                originalUrl: template.url,
                downloadUrl: downloadInfo.downloadUrl,
                extractedAt: new Date().toISOString(),
                files: await this.getDirectoryContents(templateDir)
            };
            
            await fs.writeFile(
                path.join(templateDir, 'template-info.json'),
                JSON.stringify(templateInfo, null, 2)
            );
            
            // حذف فایل ZIP اصلی برای صرفه‌جویی در فضا
            try {
                await fs.unlink(zipPath);
            } catch {}
            
            this.extractedTemplates.push(templateInfo);
            console.log(`✅ ${template.name} استخراج شد!`);
            
        } catch (error) {
            console.log(`❌ خطا در استخراج ${template.name}: ${error.message}`);
            this.errors.push({
                template: template.name,
                url: template.url,
                error: error.message
            });
        }
    }

    async downloadFile(url, filePath) {
        return new Promise((resolve, reject) => {
            const file = require('fs').createWriteStream(filePath);
            
            https.get(url, (response) => {
                if (response.statusCode !== 200) {
                    reject(new Error(`HTTP ${response.statusCode}`));
                    return;
                }
                
                response.pipe(file);
                
                file.on('finish', () => {
                    file.close();
                    resolve();
                });
                
                file.on('error', (err) => {
                    require('fs').unlink(filePath, () => {});
                    reject(err);
                });
                
            }).on('error', (err) => {
                reject(err);
            });
        });
    }

    async extractZip(zipPath, extractPath) {
        try {
            const zip = new AdmZip(zipPath);
            zip.extractAllTo(extractPath, true);
        } catch (error) {
            console.log(`⚠️ خطا در استخراج ZIP: ${error.message}`);
        }
    }

    async getDirectoryContents(dir) {
        const contents = [];
        
        try {
            const files = await fs.readdir(dir, { withFileTypes: true });
            
            for (const file of files) {
                if (file.name === 'template-info.json') continue;
                
                const filePath = path.join(dir, file.name);
                
                if (file.isDirectory()) {
                    const subContents = await this.getDirectoryContents(filePath);
                    contents.push({
                        name: file.name,
                        type: 'directory',
                        children: subContents
                    });
                } else {
                    const stats = await fs.stat(filePath);
                    contents.push({
                        name: file.name,
                        type: 'file',
                        size: stats.size,
                        extension: path.extname(file.name)
                    });
                }
            }
        } catch (error) {
            console.log(`⚠️ خطا در خواندن محتوای پوشه: ${error.message}`);
        }
        
        return contents;
    }

    sanitizeName(name) {
        return name.replace(/[<>:"/\\|?*]/g, '_').trim();
    }

    async generateReport() {
        console.log('📊 تولید گزارش...');
        
        const report = {
            timestamp: new Date().toISOString(),
            summary: {
                totalTemplatesFound: this.extractedTemplates.length + this.errors.length,
                successfulExtractions: this.extractedTemplates.length,
                errors: this.errors.length,
                successRate: `${Math.round((this.extractedTemplates.length / (this.extractedTemplates.length + this.errors.length)) * 100)}%`
            },
            extractedTemplates: this.extractedTemplates,
            errors: this.errors,
            categories: this.categorizeTemplates()
        };

        // ذخیره گزارش JSON
        await fs.writeFile(
            path.join(this.outputDir, 'HTML5UP_REPORT.json'),
            JSON.stringify(report, null, 2)
        );

        // گزارش متنی
        const textReport = `
🎨 گزارش استخراج قالب‌های HTML5UP
======================================

📊 خلاصه:
✅ قالب‌های استخراج شده: ${this.extractedTemplates.length}
❌ خطاهای رخ داده: ${this.errors.length}
📈 نرخ موفقیت: ${report.summary.successRate}

🎯 قالب‌های استخراج شده:
${this.extractedTemplates.map((template, index) => 
    `${index + 1}. ${template.name}`
).join('\n')}

${this.errors.length > 0 ? `
⚠️ خطاهای رخ داده:
${this.errors.map(err => `❌ ${err.template}: ${err.error}`).join('\n')}
` : ''}

📁 مسیر قالب‌ها: ${this.outputDir}

🎉 تمام قالب‌های HTML5UP آماده استفاده است!
هر قالب شامل HTML، CSS، JS و تصاویر کامل می‌باشد.
        `;

        await fs.writeFile(
            path.join(this.outputDir, 'README.md'),
            textReport
        );

        console.log('✅ گزارش ایجاد شد!');
        return report;
    }

    categorizeTemplates() {
        const categories = {
            business: [],
            portfolio: [],
            landing: [],
            blog: [],
            ecommerce: [],
            creative: [],
            other: []
        };

        this.extractedTemplates.forEach(template => {
            const name = template.name.toLowerCase();
            
            if (name.includes('business') || name.includes('corporate') || name.includes('company')) {
                categories.business.push(template.name);
            } else if (name.includes('portfolio') || name.includes('gallery') || name.includes('showcase')) {
                categories.portfolio.push(template.name);
            } else if (name.includes('landing') || name.includes('intro') || name.includes('home')) {
                categories.landing.push(template.name);
            } else if (name.includes('blog') || name.includes('news') || name.includes('article')) {
                categories.blog.push(template.name);
            } else if (name.includes('shop') || name.includes('store') || name.includes('ecommerce')) {
                categories.ecommerce.push(template.name);
            } else if (name.includes('creative') || name.includes('art') || name.includes('design')) {
                categories.creative.push(template.name);
            } else {
                categories.other.push(template.name);
            }
        });

        return categories;
    }

    async run() {
        try {
            await this.init();
            
            const templates = await this.getAllTemplates();
            
            if (templates.length === 0) {
                console.log('❌ هیچ قالبی پیدا نشد');
                return;
            }
            
            console.log(`🎯 شروع استخراج ${templates.length} قالب...`);
            
            for (let i = 0; i < templates.length; i++) {
                await this.extractTemplate(templates[i], i, templates.length);
                
                // استراحت کوتاه بین استخراج‌ها
                if (i < templates.length - 1) {
                    await new Promise(resolve => setTimeout(resolve, 3000));
                }
            }
            
            const report = await this.generateReport();
            
            console.log('\n🎉 استخراج کامل HTML5UP تمام شد!');
            console.log(`✅ ${this.extractedTemplates.length} قالب استخراج شد`);
            console.log(`❌ ${this.errors.length} خطا رخ داد`);
            console.log(`📁 قالب‌ها در: ${this.outputDir}`);
            
        } catch (error) {
            console.error('❌ خطای کلی:', error.message);
        } finally {
            if (this.browser) {
                await this.browser.close();
            }
        }
    }
}

// اجرای استخراج کننده
if (require.main === module) {
    const extractor = new HTML5UPExtractor();
    extractor.run().catch(console.error);
}

module.exports = HTML5UPExtractor;
