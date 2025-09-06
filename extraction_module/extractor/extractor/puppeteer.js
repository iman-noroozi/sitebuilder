const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

class TemplateExtractor {
    constructor(options = {}) {
        this.config = this.loadConfig();
        this.logs = [];
        
        // تنظیمات پیش‌فرض برای صورتی که config بارگذاری نشود
        const defaultConfig = {
            extractor: {
                headless: true,
                timeout: 30000,
                screenshot: { enabled: true, fullPage: true, format: 'png' }
            },
            output: { createZip: false },
            advanced: { viewport: { width: 1920, height: 1080 } }
        };
        
        // ادغام config با تنظیمات پیش‌فرض
        this.config = { ...defaultConfig, ...this.config };
        
        this.options = {
            headless: options.headless !== undefined ? options.headless : (this.config.extractor?.headless ?? true),
            timeout: options.timeout || (this.config.extractor?.timeout ?? 30000),
            extractImages: options.extractImages !== undefined ? options.extractImages : true,
            extractFonts: options.extractFonts !== undefined ? options.extractFonts : true,
            screenshotEnabled: options.screenshotEnabled !== undefined ? options.screenshotEnabled : (this.config.extractor?.screenshot?.enabled ?? true),
            screenshotFullPage: options.screenshotFullPage !== undefined ? options.screenshotFullPage : (this.config.extractor?.screenshot?.fullPage ?? true),
            ...options
        };
        
        this.browserInstance = null;
        this.currentBaseURL = '';
    }

    // بارگذاری config.json
    loadConfig() {
        try {
            const configPath = path.join(__dirname, '..', 'config.json');
            if (fs.existsSync(configPath)) {
                return JSON.parse(fs.readFileSync(configPath, 'utf8'));
            } else {
                console.warn('⚠️ فایل config.json یافت نشد، استفاده از تنظیمات پیش‌فرض');
                return {};
            }
        } catch (error) {
            console.warn('⚠️ خطا در بارگذاری config.json:', error.message);
            return {};
        }
    }

    // سیستم لاگ
    addLog(level, message) {
        const timestamp = new Date().toISOString();
        const logEntry = { timestamp, level, message };
        this.logs.push(logEntry);
        
        const emoji = {
            'info': 'ℹ️',
            'success': '✅',
            'warn': '⚠️',
            'error': '❌'
        };
        
        console.log(`${emoji[level] || 'ℹ️'} ${message}`);
    }

    // ذخیره لاگ‌ها
    saveLogs(outputDir) {
        try {
            const logPath = path.join(outputDir, 'extraction.log');
            const logContent = this.logs.map(log => 
                `[${log.timestamp}] ${log.level.toUpperCase()}: ${log.message}`
            ).join('\n');
            
            fs.writeFileSync(logPath, logContent, 'utf8');
            this.addLog('info', `لاگ‌ها ذخیره شد: ${logPath}`);
        } catch (error) {
            console.warn('خطا در ذخیره لاگ‌ها:', error.message);
        }
    }

    // پاک‌سازی HTML
    cleanHTMLContent(html) {
        return html
            .replace(/<!--[\s\S]*?-->/g, '') // حذف کامنت‌ها
            .replace(/\s+/g, ' ') // فشرده‌سازی فضاهای خالی
            .trim();
    }

    // ایجاد HTML نهایی
    createFinalHTML(html, styles) {
        return `<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>قالب استخراج شده</title>
    <style>
        ${styles}
    </style>
</head>
<body>
    ${html.replace(/<html[^>]*>|<\/html>|<head[^>]*>[\s\S]*?<\/head>|<body[^>]*>|<\/body>/gi, '')}
</body>
</html>`;
    }

    // دانلود فایل منفرد
    async downloadFile(url, filePath) {
        return new Promise((resolve, reject) => {
            const protocol = url.startsWith('https') ? https : http;
            
            const request = protocol.get(url, (response) => {
                if (response.statusCode === 200) {
                    const fileStream = fs.createWriteStream(filePath);
                    response.pipe(fileStream);
                    
                    fileStream.on('finish', () => {
                        fileStream.close();
                        resolve(filePath);
                    });
                    
                    fileStream.on('error', reject);
                } else {
                    reject(new Error(`HTTP ${response.statusCode}: ${response.statusMessage}`));
                }
            });
            
            request.on('error', reject);
            request.setTimeout(10000, () => {
                request.destroy();
                reject(new Error('Timeout'));
            });
        });
    }

    // دانلود موازی چندین فایل
    async downloadFilesParallel(urls, outputDir, type = 'file') {
        if (!urls || urls.length === 0) return [];
        
        const results = [];
        const maxConcurrent = 5; // حداکثر دانلود همزمان
        
        // ایجاد پوشه‌های مورد نیاز
        const assetsPath = path.join(outputDir, 'assets');
        const imagesPath = path.join(assetsPath, 'images');
        const scriptsPath = path.join(assetsPath, 'scripts');
        const fontsPath = path.join(assetsPath, 'fonts');
        
        [assetsPath, imagesPath, scriptsPath, fontsPath].forEach(dir => {
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
        });

        for (let i = 0; i < urls.length; i += maxConcurrent) {
            const batch = urls.slice(i, i + maxConcurrent);
            
            const batchPromises = batch.map(async (url) => {
                try {
                    // تعیین نوع فایل و مسیر
                    let targetDir, fileType;
                    const urlLower = url.toLowerCase();
                    
                    if (urlLower.includes('.js') || type === 'script') {
                        targetDir = scriptsPath;
                        fileType = 'js';
                    } else if (urlLower.match(/\.(jpg|jpeg|png|gif|svg|webp|ico)/)) {
                        targetDir = imagesPath;
                        fileType = 'image';
                    } else if (urlLower.match(/\.(woff|woff2|ttf|otf|eot)/)) {
                        targetDir = fontsPath;
                        fileType = 'font';
                    } else {
                        targetDir = assetsPath;
                        fileType = 'other';
                    }

                    // تعیین نام فایل
                    const urlParts = new URL(url, this.currentBaseURL);
                    let filename = path.basename(urlParts.pathname);
                    
                    if (!filename || filename === '/') {
                        filename = `file_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
                    }
                    
                    // اضافه کردن پسوند در صورت نیاز
                    if (!path.extname(filename) && fileType === 'js') {
                        filename += '.js';
                    }

                    const filePath = path.join(targetDir, filename);
                    
                    // دانلود فایل
                    await this.downloadFile(url, filePath);
                    
                    return { url, success: true, filename, filePath, type: fileType };
                } catch (error) {
                    this.addLog('warn', `خطا در دانلود ${url}: ${error.message}`);
                    return { url, success: false, error: error.message };
                }
            });
            
            const batchResults = await Promise.allSettled(batchPromises);
            results.push(...batchResults.map(result => 
                result.status === 'fulfilled' ? result.value : { success: false, error: result.reason }
            ));
            
            // نمایش پیشرفت
            this.addLog('info', `پیشرفت: ${Math.min(i + maxConcurrent, urls.length)}/${urls.length} فایل`);
        }
        
        const successful = results.filter(r => r.success);
        this.addLog('success', `دانلود کامل: ${successful.length}/${urls.length} فایل`);
        
        return results;
    }

    async extractTemplate(url, outputDir) {
        this.addLog('info', `شروع استخراج کامل قالب از: ${url}`);
        
        let browser = null;
        let page = null;
        
        try {
            // تنظیمات مرورگر
            const browserOptions = {
                headless: this.config.extractor?.headless ?? this.options.headless,
                args: [
                    '--no-sandbox', 
                    '--disable-setuid-sandbox', 
                    '--disable-web-security',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            };

            // تشخیص Chrome سیستم
            try {
                const { execSync } = require('child_process');
                let chromePath;
                
                try {
                    chromePath = execSync('where chrome', { encoding: 'utf8' }).trim();
                } catch {
                    const possiblePaths = [
                        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
                        process.env.LOCALAPPDATA + '\\Google\\Chrome\\Application\\chrome.exe'
                    ];
                    
                    chromePath = possiblePaths.find(path => fs.existsSync(path));
                }
                
                if (chromePath) {
                    browserOptions.executablePath = chromePath;
                    this.addLog('info', `استفاده از Chrome: ${chromePath}`);
                }
            } catch (error) {
                this.addLog('warn', 'Chrome سیستم یافت نشد، استفاده از Chromium پیش‌فرض');
            }

            browser = await puppeteer.launch(browserOptions);
            page = await browser.newPage();
            
            // تنظیمات صفحه
            const viewport = this.config.advanced?.viewport || { width: 1920, height: 1080 };
            await page.setViewport(viewport);
            
            if (this.config.advanced?.userAgent) {
                await page.setUserAgent(this.config.advanced.userAgent);
            }
            
            // بارگذاری صفحه
            this.addLog('info', 'در حال بارگذاری صفحه...');
            await page.goto(url, { 
                waitUntil: 'networkidle0',
                timeout: this.config.extractor?.timeout ?? this.options.timeout 
            });

            // انتظار اضافی
            if (this.config.advanced?.waitTime) {
                this.addLog('info', `انتظار ${this.config.advanced.waitTime}ms برای بارگذاری کامل...`);
                await page.waitForTimeout(this.config.advanced.waitTime);
            }

            // ایجاد ساختار پوشه‌ها
            if (!fs.existsSync(outputDir)) {
                fs.mkdirSync(outputDir, { recursive: true });
            }

            // گرفتن screenshot
            if (this.config.extractor?.screenshot?.enabled ?? this.options.screenshotEnabled) {
                this.addLog('info', 'گرفتن screenshot...');
                try {
                    const screenshotFormat = this.config.extractor?.screenshot?.format ?? 'png';
                    const screenshotPath = path.join(outputDir, `screenshot.${screenshotFormat}`);
                    await page.screenshot({
                        path: screenshotPath,
                        fullPage: this.config.extractor?.screenshot?.fullPage ?? this.options.screenshotFullPage,
                        type: screenshotFormat
                    });
                    this.addLog('success', `Screenshot ذخیره شد: ${screenshotPath}`);
                } catch (error) {
                    this.addLog('error', `خطا در گرفتن screenshot: ${error.message}`);
                }
            }

            // گرفتن URL پایه
            const baseURL = new URL(url).origin;
            this.currentBaseURL = baseURL;

            // استخراج HTML
            this.addLog('info', 'استخراج HTML...');
            let html = await page.content();
            html = this.cleanHTMLContent(html);
            
            // استخراج CSS
            this.addLog('info', 'استخراج CSS...');
            let styles = await page.evaluate(() => {
                const styleSheets = Array.from(document.styleSheets);
                let allStyles = '';
                
                const inlineStyles = Array.from(document.querySelectorAll('style')).map(style => style.textContent).join('\n');
                allStyles += inlineStyles + '\n';
                
                styleSheets.forEach(styleSheet => {
                    try {
                        const rules = Array.from(styleSheet.cssRules || styleSheet.rules);
                        rules.forEach(rule => {
                            allStyles += rule.cssText + '\n';
                        });
                    } catch (e) {
                        console.warn('Cannot access stylesheet:', e);
                    }
                });
                
                return allStyles;
            });

            // استخراج JavaScript
            this.addLog('info', 'استخراج JavaScript...');
            const scriptSources = await page.evaluate(() => {
                const scriptTags = Array.from(document.querySelectorAll('script[src]'));
                return scriptTags.map(script => script.src).filter(src => src);
            });

            // استخراج تصاویر
            this.addLog('info', 'استخراج تصاویر...');
            const imageUrls = await page.evaluate(() => {
                const imgSrcs = Array.from(document.images).map(img => img.src);
                
                const bgImages = [];
                Array.from(document.querySelectorAll('*')).forEach(el => {
                    const bgImg = getComputedStyle(el).backgroundImage;
                    if (bgImg && bgImg !== 'none' && bgImg.includes('url(')) {
                        const urlMatch = bgImg.match(/url\(['"]?([^'"]+)['"]?\)/);
                        if (urlMatch) {
                            bgImages.push(urlMatch[1]);
                        }
                    }
                });
                
                return [...new Set([...imgSrcs, ...bgImages])];
            });

            // استخراج فونت‌ها
            this.addLog('info', 'استخراج فونت‌ها...');
            const fontUrls = await page.evaluate(() => {
                const fontFaces = [];
                Array.from(document.styleSheets).forEach(styleSheet => {
                    try {
                        Array.from(styleSheet.cssRules || styleSheet.rules).forEach(rule => {
                            if (rule.type === CSSRule.FONT_FACE_RULE) {
                                const src = rule.style.src;
                                if (src) {
                                    const urlMatches = src.match(/url\(['"]?([^'"]+)['"]?\)/g);
                                    if (urlMatches) {
                                        urlMatches.forEach(match => {
                                            const url = match.match(/url\(['"]?([^'"]+)['"]?\)/)[1];
                                            fontFaces.push(url);
                                        });
                                    }
                                }
                            }
                        });
                    } catch (e) {
                        // Ignore cross-origin stylesheet errors
                    }
                });
                return fontFaces;
            });

            // دانلود موازی فایل‌ها
            this.addLog('info', 'دانلود موازی فایل‌ها...');
            let allFiles = [...scriptSources, ...imageUrls, ...fontUrls];
            allFiles = allFiles.filter(url => url && url.startsWith('http'));
            
            await this.downloadFilesParallel(allFiles, outputDir);

            // ایجاد فایل HTML نهایی
            this.addLog('info', 'ایجاد فایل HTML نهایی...');
            const finalHtml = this.createFinalHTML(html, styles);
            const htmlPath = path.join(outputDir, 'index.html');
            fs.writeFileSync(htmlPath, finalHtml, 'utf8');

            // ذخیره metadata
            const metadata = {
                url: url,
                title: await page.title(),
                extractedAt: new Date().toISOString(),
                files: {
                    scripts: scriptSources.length,
                    images: imageUrls.length,
                    fonts: fontUrls.length
                },
                config: this.config.extractor ?? {}
            };
            
            const metadataPath = path.join(outputDir, 'metadata.json');
            fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2));

            // ذخیره لاگ‌ها
            this.saveLogs(outputDir);

            this.addLog('success', `✅ استخراج کامل شد: ${outputDir}`);
            console.log(`✅ استخراج کامل شد: ${outputDir}`);
            
            return outputDir;

        } catch (error) {
            this.addLog('error', `❌ خطا در استخراج: ${error.message}`);
            console.error('❌ خطا در استخراج:', error);
            throw error;
        } finally {
            if (page) await page.close();
            if (browser && !this.browserInstance) await browser.close();
        }
    }

    // استخراج چندین صفحه
    async extractMultiplePages(urls, baseOutputPath) {
        const results = [];
        
        for (let i = 0; i < urls.length; i++) {
            const url = urls[i];
            const outputPath = path.join(baseOutputPath, `template_${i + 1}`);
            
            try {
                const result = await this.extractTemplate(url, outputPath);
                results.push({ url, success: true, data: result });
            } catch (error) {
                results.push({ url, success: false, error: error.message });
            }
        }
        
        return results;
    }
}

// استفاده
if (require.main === module) {
    const extractor = new TemplateExtractor();
    
    const url = process.argv[2] || 'https://example.com';
    const outputPath = process.argv[3] || './extracted_templates';
    
    extractor.extractTemplate(url, outputPath)
        .then(() => console.log('استخراج کامل شد'))
        .catch(error => console.error('خطا:', error));
}

module.exports = TemplateExtractor;
