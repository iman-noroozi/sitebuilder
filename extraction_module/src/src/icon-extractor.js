// Icon Resources Mass Extractor
// استخراج کامل منابع آیکون برای سایت‌سازی

const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');
const https = require('https');

console.log('🎯 شروع استخراج کامل منابع آیکون...');
console.log('========================================');

class IconResourceExtractor {
    constructor() {
        this.outputDir = './extracted_sites/icon_resources';
        this.browser = null;
        this.page = null;
        this.extractedSources = [];
        this.errors = [];
        
        // منابع آیکون مختلف
        this.iconSources = [
            {
                name: 'Font Awesome',
                url: 'https://fontawesome.com/',
                type: 'font-icons',
                description: 'محبوب‌ترین مجموعه آیکون وب'
            },
            {
                name: 'Feather Icons',
                url: 'https://feathericons.com/',
                type: 'svg-icons',
                description: 'آیکون‌های ساده و زیبا'
            },
            {
                name: 'Hero Icons',
                url: 'https://heroicons.com/',
                type: 'svg-icons',
                description: 'آیکون‌های مدرن Tailwind'
            },
            {
                name: 'Lucide',
                url: 'https://lucide.dev/',
                type: 'svg-icons',
                description: 'آیکون‌های باکیفیت'
            },
            {
                name: 'Tabler Icons',
                url: 'https://tabler-icons.io/',
                type: 'svg-icons',
                description: 'آیکون‌های رایگان SVG'
            },
            {
                name: 'Phosphor Icons',
                url: 'https://phosphoricons.com/',
                type: 'svg-icons',
                description: 'آیکون‌های انعطاف‌پذیر'
            },
            {
                name: 'Iconify',
                url: 'https://iconify.design/',
                type: 'unified-icons',
                description: 'بزرگترین مجموعه آیکون'
            },
            {
                name: 'Bootstrap Icons',
                url: 'https://icons.getbootstrap.com/',
                type: 'svg-icons',
                description: 'آیکون‌های رسمی Bootstrap'
            }
        ];
    }

    async init() {
        console.log('🚀 راه‌اندازی مرورگر...');
        
        this.browser = await puppeteer.launch({
            headless: 'new',
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage'
            ]
        });

        this.page = await this.browser.newPage();
        await this.page.setViewport({ width: 1920, height: 1080 });
        
        // ایجاد پوشه‌های خروجی
        await fs.mkdir(this.outputDir, { recursive: true });
        await fs.mkdir(path.join(this.outputDir, 'font-awesome'), { recursive: true });
        await fs.mkdir(path.join(this.outputDir, 'svg-icons'), { recursive: true });
        await fs.mkdir(path.join(this.outputDir, 'css-files'), { recursive: true });
        await fs.mkdir(path.join(this.outputDir, 'web-fonts'), { recursive: true });
        
        console.log('✅ راه‌اندازی کامل شد');
    }

    async extractFontAwesome() {
        console.log('🎯 استخراج Font Awesome...');
        
        try {
            // دانلود مستقیم Font Awesome
            const faUrls = [
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/webfonts/fa-solid-900.woff2',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/webfonts/fa-regular-400.woff2',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/webfonts/fa-brands-400.woff2'
            ];
            
            for (const url of faUrls) {
                const fileName = url.split('/').pop();
                const filePath = path.join(this.outputDir, 'font-awesome', fileName);
                
                try {
                    await this.downloadFile(url, filePath);
                    console.log(`✅ دانلود شد: ${fileName}`);
                } catch (error) {
                    console.log(`❌ خطا در دانلود ${fileName}: ${error.message}`);
                }
            }
            
        } catch (error) {
            console.error('❌ خطا در Font Awesome:', error.message);
        }
    }

    async extractBootstrapIcons() {
        console.log('🎯 استخراج Bootstrap Icons...');
        
        try {
            const bootstrapUrls = [
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css',
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/fonts/bootstrap-icons.woff2',
                'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/fonts/bootstrap-icons.woff'
            ];
            
            for (const url of bootstrapUrls) {
                const fileName = url.split('/').pop();
                const filePath = path.join(this.outputDir, 'bootstrap-icons', fileName);
                
                await fs.mkdir(path.dirname(filePath), { recursive: true });
                
                try {
                    await this.downloadFile(url, filePath);
                    console.log(`✅ دانلود شد: ${fileName}`);
                } catch (error) {
                    console.log(`❌ خطا در دانلود ${fileName}: ${error.message}`);
                }
            }
            
        } catch (error) {
            console.error('❌ خطا در Bootstrap Icons:', error.message);
        }
    }

    async extractIconSource(source) {
        console.log(`🎯 استخراج ${source.name}...`);
        
        try {
            await this.page.goto(source.url, { waitUntil: 'networkidle2', timeout: 60000 });
            
            // استخراج CSS های آیکون
            const cssLinks = await this.page.evaluate(() => {
                const links = [];
                document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
                    const href = link.href;
                    if (href && (href.includes('icon') || href.includes('font'))) {
                        links.push(href);
                    }
                });
                return links;
            });
            
            // دانلود فایل‌های CSS
            for (const cssUrl of cssLinks) {
                try {
                    const fileName = this.sanitizeFileName(cssUrl.split('/').pop() || 'icons.css');
                    const filePath = path.join(this.outputDir, 'css-files', `${source.name.toLowerCase().replace(/\s+/g, '-')}-${fileName}`);
                    
                    await this.downloadFile(cssUrl, filePath);
                    console.log(`✅ CSS دانلود شد: ${fileName}`);
                } catch (error) {
                    console.log(`⚠️ خطا در دانلود CSS: ${error.message}`);
                }
            }
            
            // اسکرین‌شات از صفحه
            const screenshotPath = path.join(this.outputDir, 'screenshots', `${source.name.toLowerCase().replace(/\s+/g, '-')}.png`);
            await fs.mkdir(path.dirname(screenshotPath), { recursive: true });
            await this.page.screenshot({ path: screenshotPath, fullPage: false });
            
            this.extractedSources.push({
                ...source,
                cssFiles: cssLinks.length,
                extractedAt: new Date().toISOString(),
                screenshot: screenshotPath
            });
            
            console.log(`✅ ${source.name} استخراج شد!`);
            
        } catch (error) {
            console.log(`❌ خطا در ${source.name}: ${error.message}`);
            this.errors.push({
                source: source.name,
                url: source.url,
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

    sanitizeFileName(fileName) {
        return fileName.replace(/[<>:"/\\|?*]/g, '_').trim();
    }

    async generateIconGuide() {
        console.log('📚 تولید راهنمای استفاده از آیکون‌ها...');
        
        const guide = `
# 🎯 راهنمای جامع آیکون‌های استخراج شده

## 📂 ساختار پوشه‌ها

### Font Awesome
- **مسیر**: \`font-awesome/\`
- **فایل‌ها**: CSS و WebFont فایل‌های کامل
- **استفاده**: 
  \`\`\`html
  <link rel="stylesheet" href="font-awesome/all.min.css">
  <i class="fas fa-home"></i>
  \`\`\`

### Bootstrap Icons
- **مسیر**: \`bootstrap-icons/\`
- **فایل‌ها**: CSS و WebFont فایل‌های رسمی Bootstrap
- **استفاده**:
  \`\`\`html
  <link rel="stylesheet" href="bootstrap-icons/bootstrap-icons.css">
  <i class="bi bi-house"></i>
  \`\`\`

### CSS Files
- **مسیر**: \`css-files/\`
- **محتوا**: فایل‌های CSS از منابع مختلف آیکون

### Screenshots
- **مسیر**: \`screenshots/\`
- **محتوا**: تصاویر پیش‌نمایش منابع آیکون

## 🎨 منابع آیکون استخراج شده

${this.iconSources.map(source => `
### ${source.name}
- **نوع**: ${source.type}
- **توضیح**: ${source.description}
- **آدرس**: ${source.url}
`).join('')}

## 🚀 نحوه استفاده

### 1. Font-based Icons (Font Awesome, Bootstrap Icons)
\`\`\`html
<!-- اضافه کردن CSS -->
<link rel="stylesheet" href="path/to/icons.css">

<!-- استفاده از آیکون -->
<i class="icon-class-name"></i>
\`\`\`

### 2. SVG Icons
\`\`\`html
<!-- درج مستقیم SVG -->
<svg>...</svg>

<!-- یا استفاده از sprite -->
<svg><use xlink:href="#icon-name"></use></svg>
\`\`\`

### 3. CSS Sprite Icons
\`\`\`css
.icon {
  background-image: url('icons-sprite.png');
  background-position: ...;
}
\`\`\`

## 📝 نکات مهم

1. **کیفیت**: تمام آیکون‌ها با کیفیت بالا و بهینه شده
2. **سازگاری**: با تمام مرورگرهای مدرن سازگار
3. **اندازه**: آیکون‌ها قابل تغییر اندازه هستند
4. **رنگ**: رنگ آیکون‌ها قابل تغییر با CSS
5. **لیسانس**: بررسی لیسانس هر مجموعه قبل از استفاده تجاری

## 🎯 بهترین روش‌ها

- برای پروژه‌های کوچک: Bootstrap Icons
- برای تنوع بالا: Font Awesome
- برای عملکرد بهتر: SVG Icons
- برای سفارشی‌سازی: خام SVG

---
تاریخ ایجاد: ${new Date().toLocaleDateString('fa-IR')}
        `;

        await fs.writeFile(
            path.join(this.outputDir, 'ICON_GUIDE.md'),
            guide
        );

        console.log('✅ راهنما ایجاد شد!');
    }

    async generateReport() {
        console.log('📊 تولید گزارش...');
        
        const report = {
            timestamp: new Date().toISOString(),
            summary: {
                totalSources: this.iconSources.length,
                successfulExtractions: this.extractedSources.length,
                errors: this.errors.length,
                categories: {
                    'font-icons': this.extractedSources.filter(s => s.type === 'font-icons').length,
                    'svg-icons': this.extractedSources.filter(s => s.type === 'svg-icons').length,
                    'unified-icons': this.extractedSources.filter(s => s.type === 'unified-icons').length
                }
            },
            extractedSources: this.extractedSources,
            errors: this.errors
        };

        await fs.writeFile(
            path.join(this.outputDir, 'ICON_REPORT.json'),
            JSON.stringify(report, null, 2)
        );

        const textReport = `
🎯 گزارش استخراج منابع آیکون
===============================

📊 خلاصه:
✅ منابع استخراج شده: ${this.extractedSources.length}/${this.iconSources.length}
❌ خطاها: ${this.errors.length}

📂 دسته‌بندی:
🔤 Font Icons: ${report.summary.categories['font-icons']}
🎨 SVG Icons: ${report.summary.categories['svg-icons']}
🔗 Unified Icons: ${report.summary.categories['unified-icons']}

✅ منابع موفق:
${this.extractedSources.map((source, index) => 
    `${index + 1}. ${source.name} (${source.type})`
).join('\n')}

${this.errors.length > 0 ? `
❌ خطاها:
${this.errors.map(err => `• ${err.source}: ${err.error}`).join('\n')}
` : ''}

📁 مسیر منابع: ${this.outputDir}
📚 راهنما: ICON_GUIDE.md
        `;

        await fs.writeFile(
            path.join(this.outputDir, 'README.md'),
            textReport
        );

        console.log('✅ گزارش ایجاد شد!');
        return report;
    }

    async run() {
        try {
            await this.init();
            
            // استخراج Font Awesome
            await this.extractFontAwesome();
            
            // استخراج Bootstrap Icons
            await this.extractBootstrapIcons();
            
            // استخراج سایر منابع
            for (const source of this.iconSources) {
                await this.extractIconSource(source);
                // استراحت بین درخواست‌ها
                await new Promise(resolve => setTimeout(resolve, 3000));
            }
            
            await this.generateIconGuide();
            const report = await this.generateReport();
            
            console.log('\n🎉 استخراج منابع آیکون تمام شد!');
            console.log(`✅ ${this.extractedSources.length} منبع استخراج شد`);
            console.log(`❌ ${this.errors.length} خطا رخ داد`);
            console.log(`📁 منابع در: ${this.outputDir}`);
            
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
    const extractor = new IconResourceExtractor();
    extractor.run().catch(console.error);
}

module.exports = IconResourceExtractor;
