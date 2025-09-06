// CLI Tool for Deep Website Cloning
// استفاده آسان از خط فرمان

const DeepWebsiteCloner = require('./deep-cloner');
const path = require('path');

class ExtractorCLI {
    constructor() {
        this.cloner = null;
    }

    async run() {
        const args = process.argv.slice(2);
        
        if (args.length === 0) {
            this.showHelp();
            return;
        }

        const command = args[0];
        
        switch (command) {
            case 'extract':
                await this.extractCommand(args.slice(1));
                break;
            case 'help':
                this.showHelp();
                break;
            default:
                console.log('❌ دستور نامعتبر. برای راهنما: node extractor.js help');
        }
    }

    async extractCommand(args) {
        if (args.length === 0) {
            console.log('❌ لطفاً آدرس سایت را وارد کنید');
            console.log('مثال: node extractor.js extract https://example.com');
            return;
        }

        const url = args[0];
        const options = this.parseOptions(args.slice(1));

        console.log('🚀 شروع استخراج کامل سایت...');
        console.log(`🎯 هدف: ${url}`);
        console.log(`⚙️  تنظیمات:`, options);

        try {
            this.cloner = new DeepWebsiteCloner(options);
            await this.cloner.init();
            
            const result = await this.cloner.cloneWebsite(url);
            
            console.log('✅ استخراج با موفقیت تمام شد!');
            console.log(`📁 مسیر فایل‌ها: ${result}`);
            
        } catch (error) {
            console.error('❌ خطا در استخراج:', error.message);
        } finally {
            if (this.cloner) {
                await this.cloner.close();
            }
        }
    }

    parseOptions(args) {
        const options = {
            outputDir: './extracted_sites',
            maxDepth: 3,
            delay: 1000,
            extractCSS: true,
            extractJS: true,
            extractImages: true,
            extractFonts: true,
            extractVideos: true,
            extractDocuments: true,
            extractForms: true,
            extractMetadata: true,
            followInternalLinks: true,
            preserveDirectory: true,
            generateSitemap: true
        };

        for (let i = 0; i < args.length; i += 2) {
            const key = args[i];
            const value = args[i + 1];

            switch (key) {
                case '--output':
                case '-o':
                    options.outputDir = value;
                    break;
                case '--depth':
                case '-d':
                    options.maxDepth = parseInt(value);
                    break;
                case '--delay':
                    options.delay = parseInt(value);
                    break;
                case '--no-css':
                    options.extractCSS = false;
                    i--; // No value for this option
                    break;
                case '--no-js':
                    options.extractJS = false;
                    i--;
                    break;
                case '--no-images':
                    options.extractImages = false;
                    i--;
                    break;
                case '--no-links':
                    options.followInternalLinks = false;
                    i--;
                    break;
            }
        }

        return options;
    }

    showHelp() {
        console.log(`
🌐 Deep Website Cloner - ابزار استخراج کامل سایت‌ها

استفاده:
  node extractor.js extract <URL> [options]

مثال‌ها:
  node extractor.js extract https://example.com
  node extractor.js extract https://example.com --depth 5 --output ./my_sites
  node extractor.js extract https://example.com --no-js --no-css

گزینه‌ها:
  -o, --output <dir>     مسیر ذخیره فایل‌ها (پیش‌فرض: ./extracted_sites)
  -d, --depth <num>      عمق استخراج صفحات (پیش‌فرض: 3)
  --delay <ms>           تاخیر بین درخواست‌ها (پیش‌فرض: 1000)
  --no-css               عدم استخراج فایل‌های CSS
  --no-js                عدم استخراج فایل‌های JavaScript
  --no-images            عدم استخراج تصاویر
  --no-links             عدم دنبال کردن لینک‌های داخلی

ویژگی‌ها:
  ✅ استخراج کامل HTML, CSS, JS
  ✅ دانلود تمام تصاویر و منابع
  ✅ استخراج فونت‌ها و ویدیوها
  ✅ ذخیره ساختار کامل فولدرها
  ✅ تولید sitemap و metadata
  ✅ ایجاد فایل zip از نتیجه
  ✅ دنبال کردن لینک‌های داخلی
  ✅ استخراج فرم‌ها و داده‌ها
        `);
    }
}

// Run CLI if called directly
if (require.main === module) {
    const cli = new ExtractorCLI();
    cli.run().catch(console.error);
}

module.exports = ExtractorCLI;
