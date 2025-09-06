// استخراج ساده و سریع وب‌سایت‌ها
const puppeteer = require('puppeteer');
const fs = require('fs-extra');
const path = require('path');

class SimpleExtractor {
    constructor() {
        this.browser = null;
        this.page = null;
    }

    async init() {
        console.log('🚀 راه‌اندازی مرورگر ساده...');
        
        // پیدا کردن Chrome
        const chromePaths = [
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        ];
        
        let executablePath = null;
        for (const chromePath of chromePaths) {
            if (fs.existsSync(chromePath)) {
                executablePath = chromePath;
                break;
            }
        }

        this.browser = await puppeteer.launch({
            headless: true,
            executablePath: executablePath,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--ignore-certificate-errors',
                '--disable-web-security',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
        });

        this.page = await this.browser.newPage();
        
        // تنظیمات بهتر
        await this.page.setViewport({ width: 1920, height: 1080 });
        await this.page.setDefaultNavigationTimeout(30000);
        
        console.log('✅ مرورگر آماده شد');
    }

    async extractSite(url, siteName) {
        try {
            console.log(`🎯 شروع استخراج ${siteName}: ${url}`);
            
            // رفتن به سایت
            const response = await this.page.goto(url, { 
                waitUntil: 'networkidle2',
                timeout: 30000 
            });
            
            if (!response.ok()) {
                throw new Error(`HTTP ${response.status()}: ${response.statusText()}`);
            }

            console.log('✅ سایت لود شد');

            // گرفتن HTML
            const html = await this.page.content();
            
            // ایجاد پوشه
            const outputDir = path.join('./extracted_sites', siteName);
            await fs.ensureDir(outputDir);
            
            // ذخیره HTML
            await fs.writeFile(path.join(outputDir, 'index.html'), html);
            
            // گرفتن CSS ها
            const stylesheets = await this.page.evaluate(() => {
                return Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
                    .map(link => link.href);
            });

            console.log(`📄 ${stylesheets.length} فایل CSS پیدا شد`);

            // دانلود CSS ها
            for (const cssUrl of stylesheets) {
                try {
                    const cssResponse = await this.page.goto(cssUrl);
                    if (cssResponse.ok()) {
                        const css = await cssResponse.text();
                        const fileName = path.basename(new URL(cssUrl).pathname) || 'style.css';
                        await fs.writeFile(path.join(outputDir, fileName), css);
                        console.log(`✅ دانلود شد: ${fileName}`);
                    }
                } catch (error) {
                    console.log(`❌ خطا در دانلود CSS: ${cssUrl}`);
                }
            }

            // گرفتن JS ها
            const scripts = await this.page.evaluate(() => {
                return Array.from(document.querySelectorAll('script[src]'))
                    .map(script => script.src);
            });

            console.log(`📜 ${scripts.length} فایل JS پیدا شد`);

            // دانلود JS ها (تعداد محدود)
            for (const jsUrl of scripts.slice(0, 5)) {
                try {
                    const jsResponse = await this.page.goto(jsUrl);
                    if (jsResponse.ok()) {
                        const js = await jsResponse.text();
                        const fileName = path.basename(new URL(jsUrl).pathname) || 'script.js';
                        await fs.writeFile(path.join(outputDir, fileName), js);
                        console.log(`✅ دانلود شد: ${fileName}`);
                    }
                } catch (error) {
                    console.log(`❌ خطا در دانلود JS: ${jsUrl}`);
                }
            }

            // گرفتن تصاویر
            const images = await this.page.evaluate(() => {
                return Array.from(document.querySelectorAll('img[src]'))
                    .map(img => img.src)
                    .slice(0, 10); // فقط 10 تصویر اول
            });

            console.log(`🖼️ ${images.length} تصویر پیدا شد`);

            // ایجاد گزارش
            const report = {
                siteName: siteName,
                url: url,
                extractedAt: new Date().toISOString(),
                files: {
                    html: 1,
                    css: stylesheets.length,
                    js: scripts.length,
                    images: images.length
                },
                status: 'موفق'
            };

            await fs.writeFile(
                path.join(outputDir, 'report.json'), 
                JSON.stringify(report, null, 2)
            );

            console.log(`✅ ${siteName} با موفقیت استخراج شد!`);
            console.log(`📁 مسیر: ${outputDir}`);
            
            return outputDir;

        } catch (error) {
            console.error(`❌ خطا در استخراج ${siteName}:`, error.message);
            throw error;
        }
    }

    async close() {
        if (this.browser) {
            await this.browser.close();
            console.log('🔒 مرورگر بسته شد');
        }
    }
}

module.exports = SimpleExtractor;
