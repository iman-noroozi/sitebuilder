// استخراج منابع اضافی و کامل کردن مجموعه
const DeepWebsiteCloner = require('./deep-cloner');
const fs = require('fs-extra');

class AdditionalResourcesExtractor {
    constructor() {
        this.extractedCount = 0;
        this.errors = [];
    }

    async extractAll() {
        console.log('🔥 شروع استخراج منابع اضافی...');
        
        const additionalSites = [
            // فریمورک‌های CSS مهم
            { name: "TailwindCSS", url: "https://tailwindcss.com/", priority: "فریمورک CSS" },
            { name: "MaterialUI", url: "https://mui.com/", priority: "کامپوننت React" },
            { name: "AntDesign", url: "https://ant.design/", priority: "UI Library" },
            
            // منابع قالب رایگان
            { name: "HTML5UP", url: "https://html5up.net/", priority: "قالب‌های رایگان" },
            { name: "TemplateRealm", url: "https://templatemo.com/", priority: "قالب‌های متنوع" },
            { name: "StartBootstrap", url: "https://startbootstrap.com/", priority: "قالب‌های Bootstrap" },
            
            // ابزارهای طراحی
            { name: "Figma", url: "https://www.figma.com/", priority: "ابزار طراحی" },
            { name: "Dribbble", url: "https://dribbble.com/", priority: "الهام طراحی" },
            
            // منابع کدی
            { name: "CodePen", url: "https://codepen.io/", priority: "نمونه کد" },
            
            // ابزارهای اضافی
            { name: "Elementor", url: "https://elementor.com/", priority: "WordPress Builder" },
            { name: "Notion", url: "https://www.notion.so/", priority: "ابزار مدیریت" }
        ];

        for (const site of additionalSites) {
            try {
                console.log(`\n🎯 در حال استخراج: ${site.name} (${site.priority})`);
                await this.extractSite(site);
                this.extractedCount++;
                
                // استراحت بین استخراج‌ها
                await this.delay(2000);
                
            } catch (error) {
                console.error(`❌ خطا در ${site.name}:`, error.message);
                this.errors.push({
                    site: site.name,
                    error: error.message,
                    timestamp: new Date().toISOString()
                });
            }
        }

        await this.generateFinalReport();
        console.log(`\n🎉 استخراج کامل شد! ${this.extractedCount} سایت جدید اضافه شد.`);
    }

    async extractSite(site) {
        const cloner = new DeepWebsiteCloner({
            outputDir: './extracted_sites',
            maxDepth: 1, // عمق کم برای سرعت
            delay: 1000,
            extractCSS: true,
            extractJS: true,
            extractImages: true,
            extractFonts: true,
            extractVideos: false,
            followInternalLinks: false
        });

        try {
            await cloner.init();
            const result = await cloner.cloneWebsite(site.url);
            
            console.log(`✅ ${site.name} استخراج شد!`);
            console.log(`   📁 مسیر: ${result}`);
            console.log(`   📊 فایل‌ها: ${cloner.downloadedAssets.size}`);
            
            return result;
            
        } finally {
            await cloner.close();
        }
    }

    async generateFinalReport() {
        // خواندن لیست کامل فایل‌های استخراج شده
        const extractedDir = './extracted_sites';
        const extractedSites = await fs.readdir(extractedDir);
        
        const report = {
            extractionSummary: {
                totalExtracted: extractedSites.length,
                newlyAdded: this.extractedCount,
                errors: this.errors.length,
                completedAt: new Date().toISOString()
            },
            extractedSites: extractedSites.filter(item => !item.includes('.')),
            categories: {
                websiteBuilders: ['webflow_com', 'www_wix_com', 'www_squarespace_com', 'www_duda_co'],
                frameworks: ['getbootstrap_com', 'tailwindcss_com', 'mui_com', 'ant_design'],
                templates: ['html5up_net', 'templatemo_com', 'startbootstrap_com'],
                designTools: ['figma_com', 'dribbble_com'],
                codeResources: ['codepen_io'],
                others: ['elementor_com', 'notion_so']
            },
            recommendations: [
                "🎨 از Webflow برای ایجاد سیستم طراحی بصری استفاده کنید",
                "🚀 از Bootstrap و Tailwind برای فریمورک CSS",
                "💎 از Material UI و Ant Design برای کامپوننت‌ها",
                "📚 از قالب‌های HTML5UP برای ایده‌های طراحی",
                "🔧 از CodePen برای نمونه کدهای تعاملی"
            ],
            errors: this.errors
        };

        await fs.writeFile('./extracted_sites/final_extraction_report.json', JSON.stringify(report, null, 2));
        console.log('📄 گزارش نهایی در فایل final_extraction_report.json ذخیره شد');
        
        return report;
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

if (require.main === module) {
    const extractor = new AdditionalResourcesExtractor();
    extractor.extractAll().catch(console.error);
}

module.exports = AdditionalResourcesExtractor;
