// Enhanced Website Building Resource Extractor
// سیستم پیشرفته تکمیل منابع سایت‌سازی

console.log('🚀 شروع سیستم افزایش کیفیت منابع سایت‌سازی...');
console.log('============================================');

const fs = require('fs').promises;
const path = require('path');
const https = require('https');
const DeepWebsiteCloner = require('./deep-cloner');

class EnhancedResourceExtractor {
    constructor() {
        this.outputDir = './extracted_sites';
        this.enhancedDir = './enhanced_resources';
        this.totalProcessed = 0;
        this.errors = [];
        
        // منابع اضافی که باید جمع‌آوری شوند
        this.additionalResources = {
            icons: [
                'https://fontawesome.com/',
                'https://feathericons.com/',
                'https://heroicons.com/',
                'https://lucide.dev/',
                'https://tabler-icons.io/',
                'https://icons8.com/',
                'https://www.flaticon.com/',
                'https://iconify.design/'
            ],
            fonts: [
                'https://fonts.google.com/',
                'https://fontsquirrel.com/',
                'https://fonts.adobe.com/',
                'https://www.dafont.com/',
                'https://www.fontsshop.com/'
            ],
            templates: [
                'https://html5up.net/',
                'https://templated.co/',
                'https://freehtml5.co/',
                'https://www.os-templates.com/',
                'https://www.tooplate.com/',
                'https://templatemo.com/page/1',
                'https://colorlib.com/wp/templates/',
                'https://onepagelove.com/'
            ],
            cssFrameworks: [
                'https://bulma.io/',
                'https://semantic-ui.com/',
                'https://purecss.io/',
                'https://milligram.io/',
                'https://spectre.css/',
                'https://tachyons.io/',
                'https://shoelace.style/'
            ],
            components: [
                'https://headlessui.com/',
                'https://www.radix-ui.com/',
                'https://ui.shadcn.com/',
                'https://daisyui.com/',
                'https://nextui.org/',
                'https://preline.co/',
                'https://flowbite.com/'
            ]
        };
    }

    async init() {
        try {
            // ایجاد پوشه‌های مورد نیاز
            await fs.mkdir(this.enhancedDir, { recursive: true });
            await fs.mkdir(path.join(this.enhancedDir, 'icons'), { recursive: true });
            await fs.mkdir(path.join(this.enhancedDir, 'fonts'), { recursive: true });
            await fs.mkdir(path.join(this.enhancedDir, 'templates'), { recursive: true });
            await fs.mkdir(path.join(this.enhancedDir, 'frameworks'), { recursive: true });
            await fs.mkdir(path.join(this.enhancedDir, 'components'), { recursive: true });
            
            console.log('✅ پوشه‌های بهبودی ایجاد شدند');
        } catch (error) {
            console.error('❌ خطا در ایجاد پوشه‌ها:', error.message);
        }
    }

    async enhanceExistingResources() {
        console.log('\n🔍 بررسی و بهبود منابع موجود...');
        
        try {
            const extractedSites = await fs.readdir(this.outputDir);
            let enhancedCount = 0;
            
            for (const site of extractedSites) {
                if (site.endsWith('.zip')) continue;
                
                const sitePath = path.join(this.outputDir, site);
                const stat = await fs.stat(sitePath);
                
                if (stat.isDirectory()) {
                    await this.analyzeSiteStructure(sitePath, site);
                    enhancedCount++;
                }
            }
            
            console.log(`✅ ${enhancedCount} سایت بررسی و بهبود شد`);
        } catch (error) {
            console.error('❌ خطا در بهبود منابع:', error.message);
        }
    }

    async analyzeSiteStructure(sitePath, siteName) {
        try {
            const files = await this.getAllFiles(sitePath);
            const analysis = {
                siteName,
                totalFiles: files.length,
                cssFiles: files.filter(f => f.endsWith('.css')).length,
                jsFiles: files.filter(f => f.endsWith('.js')).length,
                htmlFiles: files.filter(f => f.endsWith('.html')).length,
                imageFiles: files.filter(f => /\.(jpg|jpeg|png|gif|svg|webp)$/i.test(f)).length,
                fontFiles: files.filter(f => /\.(woff|woff2|ttf|otf|eot)$/i.test(f)).length,
                hasBootstrap: files.some(f => f.includes('bootstrap')),
                hasTailwind: files.some(f => f.includes('tailwind')),
                hasMaterialUI: files.some(f => f.includes('material') || f.includes('mui')),
                frameworks: this.detectFrameworks(files)
            };
            
            // ذخیره تحلیل
            await fs.writeFile(
                path.join(this.enhancedDir, `${siteName}_analysis.json`),
                JSON.stringify(analysis, null, 2)
            );
            
            console.log(`📊 ${siteName}: ${analysis.totalFiles} فایل، ${analysis.frameworks.length} فریمورک`);
        } catch (error) {
            console.log(`⚠️ ${siteName}: ${error.message}`);
        }
    }

    async getAllFiles(dir) {
        const files = [];
        
        try {
            const entries = await fs.readdir(dir, { withFileTypes: true });
            
            for (const entry of entries) {
                const fullPath = path.join(dir, entry.name);
                
                if (entry.isDirectory()) {
                    const subFiles = await this.getAllFiles(fullPath);
                    files.push(...subFiles);
                } else {
                    files.push(fullPath);
                }
            }
        } catch (error) {
            // پوشه در دسترس نیست
        }
        
        return files;
    }

    detectFrameworks(files) {
        const frameworks = [];
        const fileNames = files.join(' ').toLowerCase();
        
        if (fileNames.includes('bootstrap')) frameworks.push('Bootstrap');
        if (fileNames.includes('tailwind')) frameworks.push('Tailwind CSS');
        if (fileNames.includes('material') || fileNames.includes('mui')) frameworks.push('Material-UI');
        if (fileNames.includes('bulma')) frameworks.push('Bulma');
        if (fileNames.includes('foundation')) frameworks.push('Foundation');
        if (fileNames.includes('semantic')) frameworks.push('Semantic UI');
        if (fileNames.includes('ant-design') || fileNames.includes('antd')) frameworks.push('Ant Design');
        if (fileNames.includes('chakra')) frameworks.push('Chakra UI');
        if (fileNames.includes('mantine')) frameworks.push('Mantine');
        
        return frameworks;
    }

    async extractAdditionalResources() {
        console.log('\n🎯 استخراج منابع اضافی...');
        
        // استخراج آیکون‌ها
        await this.extractResourceCategory('icons', this.additionalResources.icons);
        
        // استخراج فونت‌ها
        await this.extractResourceCategory('fonts', this.additionalResources.fonts);
        
        // استخراج قالب‌های اضافی
        await this.extractResourceCategory('templates', this.additionalResources.templates);
        
        // استخراج فریمورک‌های CSS
        await this.extractResourceCategory('frameworks', this.additionalResources.cssFrameworks);
        
        // استخراج کامپوننت‌ها
        await this.extractResourceCategory('components', this.additionalResources.components);
    }

    async extractResourceCategory(category, urls) {
        console.log(`\n🔥 شروع دسته: ${category} (${urls.length} منبع)`);
        
        const cloner = new DeepWebsiteCloner({
            outputDir: path.join(this.enhancedDir, category),
            maxDepth: 1, // عمق کمتر برای سرعت بیشتر
            delay: 1000,
            extractCSS: true,
            extractJS: category !== 'fonts', // فقط برای فونت‌ها JS نیاز نیست
            extractImages: true,
            extractFonts: true,
            extractVideos: false, // برای سرعت بیشتر
            followInternalLinks: false
        });

        try {
            await cloner.init();
            
            for (let i = 0; i < urls.length; i++) {
                const url = urls[i];
                console.log(`🎯 در حال استخراج: ${this.getUrlName(url)} (${i+1}/${urls.length})`);
                
                try {
                    const result = await cloner.cloneWebsite(url);
                    console.log(`✅ ${this.getUrlName(url)} استخراج شد!`);
                    this.totalProcessed++;
                } catch (error) {
                    console.log(`❌ خطا در ${this.getUrlName(url)}: ${error.message}`);
                    this.errors.push({ url, error: error.message, category });
                }
                
                // کمی استراحت بین درخواست‌ها
                if (i < urls.length - 1) {
                    await new Promise(resolve => setTimeout(resolve, 2000));
                }
            }
        } catch (error) {
            console.error(`❌ خطا در راه‌اندازی ${category}:`, error.message);
        } finally {
            await cloner.close();
        }
    }

    getUrlName(url) {
        try {
            const urlObj = new URL(url);
            return urlObj.hostname.replace('www.', '');
        } catch {
            return url;
        }
    }

    async generateEnhancedReport() {
        console.log('\n📊 تولید گزارش کامل...');
        
        const report = {
            timestamp: new Date().toISOString(),
            enhancementSummary: {
                totalResourcesProcessed: this.totalProcessed,
                categoriesEnhanced: Object.keys(this.additionalResources).length,
                totalErrors: this.errors.length
            },
            categories: {},
            errors: this.errors,
            recommendations: [
                'منابع استخراج شده شامل آیکون‌ها، فونت‌ها و قالب‌های اضافی است',
                'فریمورک‌های CSS مدرن برای طراحی سریع اضافه شدند',
                'کامپوننت‌های آماده برای توسعه سریع در دسترس است',
                'برای استفاده بهینه، فایل‌های تحلیلی هر سایت را بررسی کنید'
            ]
        };

        // آمار دسته‌بندی‌ها
        for (const [category, urls] of Object.entries(this.additionalResources)) {
            report.categories[category] = {
                totalUrls: urls.length,
                urls: urls.map(url => ({
                    url,
                    name: this.getUrlName(url),
                    status: this.errors.some(e => e.url === url) ? 'error' : 'success'
                }))
            };
        }

        await fs.writeFile(
            path.join(this.enhancedDir, 'ENHANCEMENT_REPORT.json'),
            JSON.stringify(report, null, 2)
        );

        // گزارش متنی
        const textReport = `
🎯 گزارش تکمیل منابع سایت‌سازی
==========================================

📊 خلاصه:
✅ منابع پردازش شده: ${this.totalProcessed}
🎯 دسته‌های بهبود شده: ${Object.keys(this.additionalResources).length}
❌ خطاهای رخ داده: ${this.errors.length}

📂 دسته‌بندی منابع:
${Object.entries(this.additionalResources).map(([category, urls]) => 
    `🔸 ${category}: ${urls.length} منبع`
).join('\n')}

${this.errors.length > 0 ? `
⚠️ خطاهای رخ داده:
${this.errors.map(err => `❌ ${err.url}: ${err.error}`).join('\n')}
` : '✅ همه منابع با موفقیت استخراج شدند!'}

🎯 نتیجه:
مجموعه کاملتری از ابزارها و منابع سایت‌سازی آماده شد که شامل:
- آیکون‌های متنوع برای UI
- فونت‌های حرفه‌ای
- قالب‌های آماده HTML/CSS
- فریمورک‌های مدرن CSS
- کامپوننت‌های آماده استفاده

📁 مسیر منابع بهبودی: ${this.enhancedDir}
        `;

        await fs.writeFile(
            path.join(this.enhancedDir, 'README.md'),
            textReport
        );

        console.log('✅ گزارش کامل ایجاد شد!');
        return report;
    }

    async run() {
        console.log('🎯 شروع فرآیند تکمیل منابع...');
        
        await this.init();
        await this.enhanceExistingResources();
        await this.extractAdditionalResources();
        const report = await this.generateEnhancedReport();
        
        console.log('\n🎉 فرآیند تکمیل منابع با موفقیت انجام شد!');
        console.log(`📊 نتایج: ${this.totalProcessed} منبع اضافی، ${this.errors.length} خطا`);
        console.log(`📁 منابع بهبودی در: ${this.enhancedDir}`);
        
        return report;
    }
}

// اجرای سیستم
if (require.main === module) {
    const extractor = new EnhancedResourceExtractor();
    extractor.run().catch(console.error);
}

module.exports = EnhancedResourceExtractor;
