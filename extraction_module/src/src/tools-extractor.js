// استخراج‌کننده جامع ابزارهای سایت‌سازی
const { extractionPriority, directDownloads } = require('./resources-database');
const DeepWebsiteCloner = require('./deep-cloner');
const fs = require('fs-extra');
const path = require('path');

class ToolsExtractor {
    constructor() {
        this.extractedSites = [];
        this.errors = [];
        this.startTime = Date.now();
    }

    async extractAll() {
        console.log('🚀 شروع استخراج جامع ابزارهای سایت‌سازی...');
        console.log(`📋 ${extractionPriority.length} سایت در لیست استخراج`);
        
        // مرتب‌سازی بر اساس اولویت
        const sortedSites = extractionPriority.sort((a, b) => a.priority - b.priority);
        
        for (const site of sortedSites) {
            try {
                console.log(`\n🎯 در حال استخراج: ${site.name} (اولویت ${site.priority})`);
                await this.extractSite(site);
                
                // استراحت بین استخراج‌ها
                await this.delay(3000);
                
            } catch (error) {
                console.error(`❌ خطا در ${site.name}:`, error.message);
                this.errors.push({
                    site: site.name,
                    url: site.url,
                    error: error.message,
                    timestamp: new Date().toISOString()
                });
            }
        }
        
        await this.generateReport();
        console.log('\n✅ استخراج جامع کامل شد!');
    }

    async extractSite(site) {
        const cloner = new DeepWebsiteCloner({
            outputDir: './extracted_sites',
            maxDepth: 1, // عمق کم برای سرعت بیشتر
            delay: 1500,
            extractCSS: true,
            extractJS: true,
            extractImages: true,
            extractFonts: true,
            extractVideos: false, // غیرفعال برای سرعت
            followInternalLinks: false // فقط صفحه اصلی
        });

        try {
            await cloner.init();
            const result = await cloner.cloneWebsite(site.url);
            
            // اطلاعات استخراج شده
            const info = {
                name: site.name,
                url: site.url,
                extractedPath: result,
                pages: cloner.visitedUrls.size,
                assets: cloner.downloadedAssets.size,
                extractedAt: new Date().toISOString(),
                status: 'موفق'
            };
            
            this.extractedSites.push(info);
            
            console.log(`✅ ${site.name} استخراج شد!`);
            console.log(`   📊 صفحات: ${info.pages}`);
            console.log(`   📊 فایل‌ها: ${info.assets}`);
            
            return result;
            
        } finally {
            await cloner.close();
        }
    }

    async extractPriority1() {
        console.log('🔥 استخراج سایت‌های اولویت 1 (ابزارهای اصلی)...');
        
        const priority1Sites = extractionPriority.filter(site => site.priority === 1);
        
        for (const site of priority1Sites) {
            try {
                await this.extractSite(site);
                await this.delay(2000);
            } catch (error) {
                console.error(`❌ خطا در ${site.name}:`, error.message);
            }
        }
    }

    async extractBootstrapTemplates() {
        console.log('🎨 استخراج قالب‌های Bootstrap رایگان...');
        
        const bootstrapSites = [
            { name: "StartBootstrap", url: "https://startbootstrap.com/" },
            { name: "HTML5UP", url: "https://html5up.net/" },
            { name: "TemplateRealm", url: "https://templatemo.com/" }
        ];

        for (const site of bootstrapSites) {
            try {
                await this.extractSite(site);
                await this.delay(2000);
            } catch (error) {
                console.error(`❌ خطا در ${site.name}:`, error.message);
            }
        }
    }

    async generateReport() {
        const duration = Date.now() - this.startTime;
        const report = {
            summary: {
                totalSites: extractionPriority.length,
                successfulExtractions: this.extractedSites.length,
                errors: this.errors.length,
                duration: `${Math.round(duration / 1000)} ثانیه`,
                generatedAt: new Date().toISOString()
            },
            extractedSites: this.extractedSites,
            errors: this.errors,
            recommendations: this.generateRecommendations()
        };

        const reportPath = './extracted_sites/extraction_report.json';
        await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
        
        console.log(`\n📊 گزارش نهایی:`);
        console.log(`   ✅ موفق: ${this.extractedSites.length}`);
        console.log(`   ❌ خطا: ${this.errors.length}`);
        console.log(`   ⏱️ مدت زمان: ${Math.round(duration / 1000)} ثانیه`);
        console.log(`   📄 گزارش: ${reportPath}`);
        
        return report;
    }

    generateRecommendations() {
        const recommendations = [];
        
        if (this.extractedSites.length > 0) {
            recommendations.push("✅ سایت‌های استخراج شده را بررسی کنید");
            recommendations.push("🔍 فایل‌های CSS و JS را برای ایده‌های جدید مطالعه کنید");
            recommendations.push("🎨 از طراحی‌های استخراج شده الهام بگیرید");
        }
        
        if (this.errors.length > 0) {
            recommendations.push("⚠️ سایت‌های خطادار را مجدداً امتحان کنید");
            recommendations.push("🔧 تنظیمات شبکه را بررسی کنید");
        }
        
        recommendations.push("🚀 از ابزارهای استخراج شده برای پروژه‌های خود استفاده کنید");
        
        return recommendations;
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// اجرای مستقیم
if (require.main === module) {
    const extractor = new ToolsExtractor();
    
    // انتخاب نوع استخراج
    const args = process.argv.slice(2);
    
    if (args.includes('--priority1')) {
        extractor.extractPriority1().catch(console.error);
    } else if (args.includes('--bootstrap')) {
        extractor.extractBootstrapTemplates().catch(console.error);
    } else {
        extractor.extractAll().catch(console.error);
    }
}

module.exports = ToolsExtractor;
