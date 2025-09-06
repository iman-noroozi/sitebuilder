#!/usr/bin/env node
/**
 * 🚀 Site Builder - Template Extractor
 * ابزار استخراج قالب‌های سایت با Puppeteer
 */

const puppeteer = require('puppeteer');
const fs = require('fs-extra');
const path = require('path');
const cheerio = require('cheerio');
const axios = require('axios');

class TemplateExtractor {
    constructor(options = {}) {
        this.options = {
            headless: options.headless !== false,
            timeout: options.timeout || 30000,
            downloadAssets: options.downloadAssets !== false,
            extractImages: options.extractImages !== false,
            extractFonts: options.extractFonts !== false,
            extractScripts: options.extractScripts !== false,
            userAgent: options.userAgent || 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        };
        
        this.browser = null;
        this.page = null;
    }

    async init() {
        if (!this.browser) {
            this.browser = await puppeteer.launch({
                headless: this.options.headless,
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
            await this.page.setUserAgent(this.options.userAgent);
            await this.page.setViewport({ width: 1920, height: 1080 });
        }
    }

    async extractTemplate(url, outputPath) {
        try {
            console.log(`🔍 شروع استخراج از: ${url}`);
            
            await this.init();
            
            // ایجاد دایرکتوری خروجی
            await fs.ensureDir(outputPath);
            
            // بارگذاری صفحه
            await this.page.goto(url, { 
                waitUntil: 'networkidle2',
                timeout: this.options.timeout 
            });
            
            // استخراج HTML
            const html = await this.page.content();
            
            // استخراج CSS
            const styles = await this.extractStyles();
            
            // استخراج JavaScript
            const scripts = await this.extractScripts();
            
            // استخراج تصاویر
            const images = this.options.extractImages ? 
                await this.extractImages(html, outputPath) : [];
            
            // استخراج فونت‌ها
            const fonts = this.options.extractFonts ? 
                await this.extractFonts(html, outputPath) : [];
            
            // ذخیره فایل‌ها
            await this.saveFiles(outputPath, {
                html,
                styles,
                scripts,
                images,
                fonts
            });
            
            console.log(`✅ استخراج کامل شد: ${outputPath}`);
            
            return {
                html,
                styles,
                scripts,
                images,
                fonts,
                outputPath
            };
            
        } catch (error) {
            console.error(`❌ خطا در استخراج: ${error.message}`);
            throw error;
        }
    }

    async extractStyles() {
        const styles = await this.page.evaluate(() => {
            const styleSheets = [];
            
            // استخراج CSS از تگ‌های style
            document.querySelectorAll('style').forEach(style => {
                if (style.textContent.trim()) {
                    styleSheets.push({
                        type: 'inline',
                        content: style.textContent
                    });
                }
            });
            
            // استخراج لینک‌های CSS
            document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
                if (link.href) {
                    styleSheets.push({
                        type: 'external',
                        href: link.href
                    });
                }
            });
            
            return styleSheets;
        });
        
        return styles;
    }

    async extractScripts() {
        const scripts = await this.page.evaluate(() => {
            const scriptList = [];
            
            document.querySelectorAll('script').forEach(script => {
                if (script.src) {
                    scriptList.push({
                        type: 'external',
                        src: script.src
                    });
                } else if (script.textContent.trim()) {
                    scriptList.push({
                        type: 'inline',
                        content: script.textContent
                    });
                }
            });
            
            return scriptList;
        });
        
        return scripts;
    }

    async extractImages(html, outputPath) {
        const $ = cheerio.load(html);
        const images = [];
        const imagesDir = path.join(outputPath, 'images');
        
        await fs.ensureDir(imagesDir);
        
        $('img').each(async (index, element) => {
            const src = $(element).attr('src');
            if (src) {
                try {
                    const imageUrl = new URL(src, this.page.url()).href;
                    const imageName = `image_${index}_${path.basename(src)}`;
                    const imagePath = path.join(imagesDir, imageName);
                    
                    // دانلود تصویر
                    const response = await axios({
                        method: 'GET',
                        url: imageUrl,
                        responseType: 'stream'
                    });
                    
                    const writer = fs.createWriteStream(imagePath);
                    response.data.pipe(writer);
                    
                    images.push({
                        originalSrc: src,
                        downloadedPath: imagePath,
                        name: imageName
                    });
                    
                } catch (error) {
                    console.warn(`⚠️ خطا در دانلود تصویر ${src}: ${error.message}`);
                }
            }
        });
        
        return images;
    }

    async extractFonts(html, outputPath) {
        const $ = cheerio.load(html);
        const fonts = [];
        const fontsDir = path.join(outputPath, 'fonts');
        
        await fs.ensureDir(fontsDir);
        
        // استخراج فونت‌ها از CSS
        const cssText = await this.page.evaluate(() => {
            let css = '';
            document.querySelectorAll('style, link[rel="stylesheet"]').forEach(element => {
                if (element.textContent) {
                    css += element.textContent;
                }
            });
            return css;
        });
        
        // استخراج URL های فونت
        const fontUrlRegex = /url\(['"]?([^'")]+\.(woff2?|ttf|otf|eot))['"]?\)/gi;
        let match;
        
        while ((match = fontUrlRegex.exec(cssText)) !== null) {
            const fontUrl = match[1];
            try {
                const fullUrl = new URL(fontUrl, this.page.url()).href;
                const fontName = path.basename(fontUrl);
                const fontPath = path.join(fontsDir, fontName);
                
                const response = await axios({
                    method: 'GET',
                    url: fullUrl,
                    responseType: 'stream'
                });
                
                const writer = fs.createWriteStream(fontPath);
                response.data.pipe(writer);
                
                fonts.push({
                    originalUrl: fontUrl,
                    downloadedPath: fontPath,
                    name: fontName
                });
                
            } catch (error) {
                console.warn(`⚠️ خطا در دانلود فونت ${fontUrl}: ${error.message}`);
            }
        }
        
        return fonts;
    }

    async saveFiles(outputPath, data) {
        // ذخیره HTML
        await fs.writeFile(
            path.join(outputPath, 'index.html'), 
            data.html, 
            'utf8'
        );
        
        // ذخیره CSS
        const cssContent = data.styles
            .filter(style => style.type === 'inline')
            .map(style => style.content)
            .join('\n\n');
        
        if (cssContent.trim()) {
            await fs.writeFile(
                path.join(outputPath, 'styles.css'), 
                cssContent, 
                'utf8'
            );
        }
        
        // ذخیره JavaScript
        const jsContent = data.scripts
            .filter(script => script.type === 'inline')
            .map(script => script.content)
            .join('\n\n');
        
        if (jsContent.trim()) {
            await fs.writeFile(
                path.join(outputPath, 'scripts.js'), 
                jsContent, 
                'utf8'
            );
        }
        
        // ذخیره metadata
        const metadata = {
            extractedAt: new Date().toISOString(),
            url: this.page.url(),
            title: await this.page.title(),
            styles: data.styles.length,
            scripts: data.scripts.length,
            images: data.images.length,
            fonts: data.fonts.length
        };
        
        await fs.writeFile(
            path.join(outputPath, 'metadata.json'), 
            JSON.stringify(metadata, null, 2), 
            'utf8'
        );
    }

    async close() {
        if (this.browser) {
            await this.browser.close();
            this.browser = null;
            this.page = null;
        }
    }
}

// اجرای مستقیم
if (require.main === module) {
    async function main() {
        const args = process.argv.slice(2);
        
        if (args.length < 2) {
            console.log(`
🚀 Site Builder - Template Extractor

استفاده:
  node puppeteer.js <URL> <OUTPUT_PATH> [OPTIONS]

مثال‌ها:
  node puppeteer.js https://example.com ./output
  node puppeteer.js https://getbootstrap.com ./bootstrap_template --headless
            `);
            process.exit(1);
        }
        
        const url = args[0];
        const outputPath = args[1];
        const options = {
            headless: args.includes('--headless')
        };
        
        const extractor = new TemplateExtractor(options);
        
        try {
            await extractor.extractTemplate(url, outputPath);
            console.log('🎉 استخراج با موفقیت انجام شد!');
        } catch (error) {
            console.error('❌ خطا:', error.message);
            process.exit(1);
        } finally {
            await extractor.close();
        }
    }
    
    main();
}

module.exports = TemplateExtractor;
