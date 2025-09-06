// Advanced Website Deep Cloner
// استخراج کامل ساختار، محتوا، اسکریپت‌ها و منابع یک سایت

const puppeteer = require('puppeteer');
const fs = require('fs-extra');
const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');
const archiver = require('archiver');

class DeepWebsiteCloner {
    constructor(options = {}) {
        this.baseUrl = null;
        this.domain = null;
        this.outputDir = options.outputDir || './extracted_sites';
        this.maxDepth = options.maxDepth || 3;
        this.delay = options.delay || 1000;
        this.visitedUrls = new Set();
        this.downloadedAssets = new Set();
        this.browser = null;
        this.page = null;

        this.config = {
            extractCSS: true,
            extractJS: true,
            extractImages: true,
            extractFonts: true,
            extractVideos: true,
            extractDocuments: true,
            extractForms: true,
            extractMetadata: true,
            extractAI: true, // 🔥 استخراج هوش مصنوعی
            followInternalLinks: true,
            preserveDirectory: true,
            generateSitemap: true,
            ...options
        };

        // 🤖 الگوهای شناسایی هوش مصنوعی
        this.aiPatterns = {
            chatbots: [
                /chatbot/i, /chat-bot/i, /chat\s*bot/i, /virtual\s*assistant/i,
                /ai\s*assistant/i, /conversational\s*ai/i, /chat\s*interface/i
            ],
            codeGenerators: [
                /code\s*generator/i, /programming\s*assistant/i, /code\s*completion/i,
                /ai\s*coder/i, /code\s*ai/i, /programming\s*ai/i, /github\s*copilot/i
            ],
            contentGenerators: [
                /content\s*generator/i, /writing\s*assistant/i, /text\s*generator/i,
                /ai\s*writer/i, /copywriting\s*ai/i, /content\s*ai/i
            ],
            imageGenerators: [
                /image\s*generator/i, /ai\s*art/i, /dall-e/i, /midjourney/i,
                /stable\s*diffusion/i, /image\s*ai/i, /art\s*generator/i
            ],
            voiceAI: [
                /voice\s*ai/i, /speech\s*recognition/i, /text-to-speech/i,
                /voice\s*assistant/i, /speech\s*ai/i, /tts/i, /stt/i
            ],
            dataAnalysis: [
                /data\s*analysis/i, /predictive\s*analytics/i, /machine\s*learning/i,
                /ml\s*model/i, /ai\s*analytics/i, /predictive\s*ai/i
            ],
            apis: [
                /openai/i, /claude/i, /anthropic/i, /google\s*ai/i, /huggingface/i,
                /azure\s*ai/i, /aws\s*ai/i, /tensorflow/i, /pytorch/i, /langchain/i
            ],
            frameworks: [
                /tensorflow/i, /pytorch/i, /scikit-learn/i, /keras/i, /langchain/i,
                /transformers/i, /spacy/i, /nltk/i, /gensim/i
            ]
        };
    }

    async init() {
        console.log('🚀 راه‌اندازی مرورگر...');

        // Try to find Chrome executable
        const chromePaths = [
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
            process.env.PUPPETEER_EXECUTABLE_PATH
        ].filter(Boolean);

        let executablePath = null;
        const fs = require('fs');

        for (const path of chromePaths) {
            if (fs.existsSync(path)) {
                executablePath = path;
                break;
            }
        }

        console.log('🔍 Chrome path:', executablePath || 'استفاده از Chrome پیش‌فرض');

        this.browser = await puppeteer.launch({
            headless: true,
            executablePath: executablePath,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--ignore-certificate-errors',
                '--ignore-ssl-errors',
                '--disable-blink-features=AutomationControlled',
                '--ignore-certificate-errors-spki-list',
                '--ignore-ssl-errors-spki-list',
                '--disable-extensions',
                '--proxy-server="direct://"',
                '--proxy-bypass-list=*',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
        });

        this.page = await this.browser.newPage();

        // Set better user agent and headers
        await this.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

        // Set extra headers to appear more like a real browser
        await this.page.setExtraHTTPHeaders({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Upgrade-Insecure-Requests': '1'
        });

        // Set viewport
        await this.page.setViewport({ width: 1920, height: 1080 });

        // Set longer timeout
        await this.page.setDefaultNavigationTimeout(60000);
        await this.page.setDefaultTimeout(60000);

        // Enable request interception for asset tracking
        await this.page.setRequestInterception(true);

        this.page.on('request', (request) => {
            // Track all requests
            const url = request.url();
            if (this.isAsset(url)) {
                this.downloadedAssets.add(url);
            }
            request.continue();
        });

        this.page.on('response', (response) => {
            // Track successful responses
            if (response.status() === 200) {
                const url = response.url();
                if (this.isAsset(url)) {
                    this.downloadedAssets.add(url);
                }
            }
        });
    }

    async cloneWebsite(targetUrl) {
        try {
            console.log(`🎯 شروع استخراج کامل: ${targetUrl}`);

            this.baseUrl = new URL(targetUrl);
            this.domain = this.baseUrl.hostname;

            // Create output directory
            const siteName = this.domain.replace(/[^a-z0-9]/gi, '_');
            const siteDir = path.join(this.outputDir, siteName);
            await fs.ensureDir(siteDir);

            // Start deep extraction
            await this.extractPage(targetUrl, siteDir, 0);

            // Generate sitemap and metadata
            await this.generateSitemap(siteDir);
            await this.generateMetadata(siteDir);

            // Create archive
            await this.createArchive(siteDir);

            console.log('✅ استخراج کامل تمام شد!');
            console.log(`📁 فایل‌ها در: ${siteDir}`);

            return siteDir;

        } catch (error) {
            console.error('❌ خطا در استخراج:', error);
            throw error;
        }
    }

    async extractPage(url, baseDir, depth = 0) {
        if (depth > this.maxDepth || this.visitedUrls.has(url)) {
            return;
        }

        console.log(`📄 استخراج صفحه (عمق ${depth}): ${url}`);
        this.visitedUrls.add(url);

        try {
            await this.page.goto(url, {
                waitUntil: ['networkidle0', 'domcontentloaded'],
                timeout: 60000
            });

            // Wait for dynamic content
            await this.page.waitForTimeout(2000);

            // Extract page data
            const pageData = await this.extractPageData(this.aiPatterns);

            // Save HTML
            const htmlPath = this.getLocalPath(url, baseDir, '.html');
            await fs.ensureDir(path.dirname(htmlPath));
            await fs.writeFile(htmlPath, pageData.html);

            // Download all assets
            await this.downloadAssets(pageData.assets, baseDir);

            // Extract and save CSS
            if (this.config.extractCSS) {
                await this.extractCSS(pageData.css, baseDir);
            }

            // Extract and save JavaScript
            if (this.config.extractJS) {
                await this.extractJS(pageData.js, baseDir);
            }

            // Extract forms data
            if (this.config.extractForms) {
                await this.extractForms(pageData.forms, baseDir);
            }

            // 🤖 استخراج ویژگی‌های هوش مصنوعی
            if (this.config.extractAI && pageData.aiFeatures) {
                await this.extractAIFeatures(pageData.aiFeatures, baseDir);
            }

            // Follow internal links
            if (this.config.followInternalLinks && depth < this.maxDepth) {
                for (const link of pageData.internalLinks) {
                    await this.delay && new Promise(resolve => setTimeout(resolve, this.delay));
                    await this.extractPage(link, baseDir, depth + 1);
                }
            }

        } catch (error) {
            console.error(`❌ خطا در استخراج ${url}:`, error.message);
        }
    }

    async extractPageData(aiPatterns) {
        return await this.page.evaluate((aiPatterns) => {
            const data = {
                html: '',
                assets: [],
                css: [],
                js: [],
                forms: [],
                internalLinks: [],
                metadata: {},
                aiFeatures: {
                    chatbots: [],
                    codeGenerators: [],
                    contentGenerators: [],
                    imageGenerators: [],
                    voiceAI: [],
                    dataAnalysis: [],
                    apis: [],
                    frameworks: [],
                    aiElements: [],
                    aiScripts: [],
                    aiAPIs: []
                }
            };

            // Get full HTML
            data.html = document.documentElement.outerHTML;

            // Extract all assets
            const assetSelectors = [
                'img[src]',
                'link[href]',
                'script[src]',
                'source[src]',
                'video[src]',
                'audio[src]',
                'iframe[src]',
                'embed[src]',
                'object[data]'
            ];

            assetSelectors.forEach(selector => {
                document.querySelectorAll(selector).forEach(el => {
                    const attr = el.tagName === 'OBJECT' ? 'data' :
                        el.tagName === 'LINK' ? 'href' : 'src';
                    const url = el.getAttribute(attr);
                    if (url) {
                        data.assets.push({
                            url: url,
                            type: el.tagName.toLowerCase(),
                            element: el.outerHTML
                        });
                    }
                });
            });

            // Extract CSS
            document.querySelectorAll('style').forEach(style => {
                data.css.push({
                    content: style.textContent,
                    type: 'inline'
                });
            });

            document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
                data.css.push({
                    url: link.href,
                    type: 'external'
                });
            });

            // Extract JavaScript
            document.querySelectorAll('script').forEach(script => {
                if (script.src) {
                    data.js.push({
                        url: script.src,
                        type: 'external'
                    });
                } else if (script.textContent.trim()) {
                    data.js.push({
                        content: script.textContent,
                        type: 'inline'
                    });
                }
            });

            // Extract forms
            document.querySelectorAll('form').forEach(form => {
                const formData = {
                    action: form.action,
                    method: form.method,
                    html: form.outerHTML,
                    fields: []
                };

                form.querySelectorAll('input, select, textarea').forEach(field => {
                    formData.fields.push({
                        name: field.name,
                        type: field.type || field.tagName.toLowerCase(),
                        value: field.value,
                        required: field.required
                    });
                });

                data.forms.push(formData);
            });

            // Extract internal links
            const currentDomain = window.location.hostname;
            document.querySelectorAll('a[href]').forEach(link => {
                try {
                    const url = new URL(link.href);
                    if (url.hostname === currentDomain) {
                        data.internalLinks.push(link.href);
                    }
                } catch (e) {
                    // Relative links
                    if (link.href.startsWith('/') || !link.href.includes('://')) {
                        data.internalLinks.push(new URL(link.href, window.location.href).href);
                    }
                }
            });

            // Extract metadata
            data.metadata = {
                title: document.title,
                description: document.querySelector('meta[name="description"]')?.content || '',
                keywords: document.querySelector('meta[name="keywords"]')?.content || '',
                viewport: document.querySelector('meta[name="viewport"]')?.content || '',
                author: document.querySelector('meta[name="author"]')?.content || '',
                charset: document.characterSet,
                lang: document.documentElement.lang,
                url: window.location.href,
                timestamp: new Date().toISOString()
            };

            // 🤖 استخراج ویژگی‌های هوش مصنوعی
            const pageText = document.body.innerText.toLowerCase();
            const pageHTML = document.documentElement.outerHTML.toLowerCase();

            // بررسی چت‌بات‌ها
            if (aiPatterns && aiPatterns.chatbots) {
                aiPatterns.chatbots.forEach(pattern => {
                    if (pattern.test(pageText) || pattern.test(pageHTML)) {
                        data.aiFeatures.chatbots.push({
                            pattern: pattern.source,
                            foundIn: pattern.test(pageText) ? 'text' : 'html'
                        });
                    }
                });
            }

            // بررسی تولیدکنندگان کد
            if (aiPatterns && aiPatterns.codeGenerators) {
                aiPatterns.codeGenerators.forEach(pattern => {
                    if (pattern.test(pageText) || pattern.test(pageHTML)) {
                        data.aiFeatures.codeGenerators.push({
                            pattern: pattern.source,
                            foundIn: pattern.test(pageText) ? 'text' : 'html'
                        });
                    }
                });
            }

            // بررسی تولیدکنندگان محتوا
            if (aiPatterns && aiPatterns.contentGenerators) {
                aiPatterns.contentGenerators.forEach(pattern => {
                    if (pattern.test(pageText) || pattern.test(pageHTML)) {
                        data.aiFeatures.contentGenerators.push({
                            pattern: pattern.source,
                            foundIn: pattern.test(pageText) ? 'text' : 'html'
                        });
                    }
                });
            }

            // بررسی تولیدکنندگان تصویر
            if (aiPatterns && aiPatterns.imageGenerators) {
                aiPatterns.imageGenerators.forEach(pattern => {
                    if (pattern.test(pageText) || pattern.test(pageHTML)) {
                        data.aiFeatures.imageGenerators.push({
                            pattern: pattern.source,
                            foundIn: pattern.test(pageText) ? 'text' : 'html'
                        });
                    }
                });
            }

            // بررسی هوش مصنوعی صوتی
            if (aiPatterns && aiPatterns.voiceAI) {
                aiPatterns.voiceAI.forEach(pattern => {
                    if (pattern.test(pageText) || pattern.test(pageHTML)) {
                        data.aiFeatures.voiceAI.push({
                            pattern: pattern.source,
                            foundIn: pattern.test(pageText) ? 'text' : 'html'
                        });
                    }
                });
            }

            // بررسی تحلیل داده‌ها
            if (aiPatterns && aiPatterns.dataAnalysis) {
                aiPatterns.dataAnalysis.forEach(pattern => {
                    if (pattern.test(pageText) || pattern.test(pageHTML)) {
                        data.aiFeatures.dataAnalysis.push({
                            pattern: pattern.source,
                            foundIn: pattern.test(pageText) ? 'text' : 'html'
                        });
                    }
                });
            }

            // بررسی API های هوش مصنوعی
            if (aiPatterns && aiPatterns.apis) {
                aiPatterns.apis.forEach(pattern => {
                    if (pattern.test(pageText) || pattern.test(pageHTML)) {
                        data.aiFeatures.apis.push({
                            pattern: pattern.source,
                            foundIn: pattern.test(pageText) ? 'text' : 'html'
                        });
                    }
                });
            }

            // بررسی فریم‌ورک‌های هوش مصنوعی
            if (aiPatterns && aiPatterns.frameworks) {
                aiPatterns.frameworks.forEach(pattern => {
                    if (pattern.test(pageText) || pattern.test(pageHTML)) {
                        data.aiFeatures.frameworks.push({
                            pattern: pattern.source,
                            foundIn: pattern.test(pageText) ? 'text' : 'html'
                        });
                    }
                });
            }

            // بررسی عناصر HTML مرتبط با AI
            document.querySelectorAll('[class*="ai"], [id*="ai"], [class*="chat"], [id*="chat"], [class*="bot"], [id*="bot"]').forEach(el => {
                data.aiFeatures.aiElements.push({
                    tag: el.tagName,
                    className: el.className,
                    id: el.id,
                    text: el.textContent.substring(0, 100)
                });
            });

            // بررسی اسکریپت‌های مرتبط با AI
            document.querySelectorAll('script').forEach(script => {
                const scriptContent = script.textContent.toLowerCase();
                if (scriptContent.includes('openai') || scriptContent.includes('claude') ||
                    scriptContent.includes('anthropic') || scriptContent.includes('ai') ||
                    scriptContent.includes('chatbot') || scriptContent.includes('machine learning')) {
                    data.aiFeatures.aiScripts.push({
                        src: script.src || 'inline',
                        content: script.textContent.substring(0, 200)
                    });
                }
            });

            return data;
        });
    }

    async downloadAssets(assets, baseDir) {
        // فیلتر کردن URL های data: و سایر موارد غیرقابل دانلود
        const downloadableAssets = assets.filter(asset => {
            // نادیده گرفتن data URI ها
            if (asset.url.startsWith('data:')) {
                return false;
            }

            // نادیده گرفتن blob URL ها
            if (asset.url.startsWith('blob:')) {
                return false;
            }

            // نادیده گرفتن javascript: URL ها
            if (asset.url.startsWith('javascript:')) {
                return false;
            }

            // نادیده گرفتن about:blank
            if (asset.url === 'about:blank') {
                return false;
            }

            // نادیده گرفتن URL های خالی یا نامعتبر
            if (!asset.url || asset.url.trim() === '') {
                return false;
            }

            // نادیده گرفتن URL هایی که فقط / دارند
            if (asset.url === '/' || asset.url === '//') {
                return false;
            }

            return true;
        });

        console.log(`📥 دانلود ${downloadableAssets.length} منبع (${assets.length - downloadableAssets.length} مورد فیلتر شد)...`);

        for (const asset of downloadableAssets) {
            try {
                const fullUrl = this.resolveUrl(asset.url);

                // نادیده گرفتن URL های null
                if (!fullUrl) {
                    continue;
                }

                const localPath = this.getLocalPath(fullUrl, baseDir);

                if (!await fs.pathExists(localPath)) {
                    await this.downloadFile(fullUrl, localPath);
                    console.log(`✅ دانلود شد: ${asset.url}`);
                }
            } catch (error) {
                // Only show errors for important files, skip tracking/analytics URLs
                if (!this.isIgnorableError(asset.url, error.message)) {
                    console.error(`❌ خطا در دانلود ${asset.url}:`, error.message);
                }
            }
        }
    }

    async extractCSS(cssAssets, baseDir) {
        const cssDir = path.join(baseDir, 'css');
        await fs.ensureDir(cssDir);

        for (let i = 0; i < cssAssets.length; i++) {
            const css = cssAssets[i];

            if (css.type === 'inline') {
                const filePath = path.join(cssDir, `inline-${i}.css`);
                await fs.writeFile(filePath, css.content);
            } else if (css.type === 'external') {
                try {
                    await this.downloadFile(css.url, this.getLocalPath(css.url, baseDir));
                } catch (error) {
                    if (!this.isIgnorableError(css.url, error.message)) {
                        console.error(`❌ خطا در دانلود CSS ${css.url}:`, error.message);
                    }
                }
            }
        }
    }

    async extractJS(jsAssets, baseDir) {
        const jsDir = path.join(baseDir, 'js');
        await fs.ensureDir(jsDir);

        for (let i = 0; i < jsAssets.length; i++) {
            const js = jsAssets[i];

            if (js.type === 'inline') {
                const filePath = path.join(jsDir, `inline-${i}.js`);
                await fs.writeFile(filePath, js.content);
            } else if (js.type === 'external') {
                try {
                    await this.downloadFile(js.url, this.getLocalPath(js.url, baseDir));
                } catch (error) {
                    if (!this.isIgnorableError(js.url, error.message)) {
                        console.error(`❌ خطا در دانلود JS ${js.url}:`, error.message);
                    }
                }
            }
        }
    }

    async extractForms(forms, baseDir) {
        if (forms.length === 0) return;

        const formsDir = path.join(baseDir, 'forms');
        await fs.ensureDir(formsDir);

        const formsData = {
            timestamp: new Date().toISOString(),
            forms: forms
        };

        await fs.writeFile(
            path.join(formsDir, 'forms-data.json'),
            JSON.stringify(formsData, null, 2)
        );
    }

    async extractAIFeatures(aiFeatures, baseDir) {
        const aiDir = path.join(baseDir, 'ai_features');
        await fs.ensureDir(aiDir);

        // محاسبه آمار کلی
        const totalFeatures = Object.values(aiFeatures).reduce((sum, features) => {
            return sum + (Array.isArray(features) ? features.length : 0);
        }, 0);

        if (totalFeatures === 0) {
            console.log('🤖 هیچ ویژگی هوش مصنوعی شناسایی نشد');
            return;
        }

        // ذخیره تمام ویژگی‌های AI
        const aiData = {
            timestamp: new Date().toISOString(),
            summary: {
                totalFeatures: totalFeatures,
                chatbots: aiFeatures.chatbots.length,
                codeGenerators: aiFeatures.codeGenerators.length,
                contentGenerators: aiFeatures.contentGenerators.length,
                imageGenerators: aiFeatures.imageGenerators.length,
                voiceAI: aiFeatures.voiceAI.length,
                dataAnalysis: aiFeatures.dataAnalysis.length,
                apis: aiFeatures.apis.length,
                frameworks: aiFeatures.frameworks.length,
                aiElements: aiFeatures.aiElements.length,
                aiScripts: aiFeatures.aiScripts.length
            },
            features: aiFeatures
        };

        // ذخیره فایل اصلی
        await fs.writeFile(
            path.join(aiDir, 'ai_features.json'),
            JSON.stringify(aiData, null, 2)
        );

        // ایجاد گزارش خلاصه
        const summaryReport = this.generateAISummaryReport(aiData);
        await fs.writeFile(
            path.join(aiDir, 'ai_summary_report.md'),
            summaryReport
        );

        // ذخیره اسکریپت‌های AI جداگانه
        if (aiFeatures.aiScripts.length > 0) {
            const scriptsDir = path.join(aiDir, 'scripts');
            await fs.ensureDir(scriptsDir);

            aiFeatures.aiScripts.forEach((script, index) => {
                const scriptPath = path.join(scriptsDir, `ai_script_${index + 1}.js`);
                fs.writeFileSync(scriptPath, script.content);
            });
        }

        console.log(`🤖 ${totalFeatures} ویژگی هوش مصنوعی استخراج شد`);
    }

    generateAISummaryReport(aiData) {
        const { summary, features } = aiData;

        let report = `# 🤖 گزارش ویژگی‌های هوش مصنوعی\n\n`;
        report += `**تاریخ استخراج:** ${new Date(aiData.timestamp).toLocaleString('fa-IR')}\n\n`;

        report += `## 📊 خلاصه آماری\n\n`;
        report += `- **کل ویژگی‌ها:** ${summary.totalFeatures}\n`;
        report += `- **چت‌بات‌ها:** ${summary.chatbots}\n`;
        report += `- **تولیدکنندگان کد:** ${summary.codeGenerators}\n`;
        report += `- **تولیدکنندگان محتوا:** ${summary.contentGenerators}\n`;
        report += `- **تولیدکنندگان تصویر:** ${summary.imageGenerators}\n`;
        report += `- **هوش مصنوعی صوتی:** ${summary.voiceAI}\n`;
        report += `- **تحلیل داده‌ها:** ${summary.dataAnalysis}\n`;
        report += `- **API های AI:** ${summary.apis}\n`;
        report += `- **فریم‌ورک‌های AI:** ${summary.frameworks}\n`;
        report += `- **عناصر HTML AI:** ${summary.aiElements}\n`;
        report += `- **اسکریپت‌های AI:** ${summary.aiScripts}\n\n`;

        // جزئیات هر بخش
        Object.entries(features).forEach(([category, items]) => {
            if (items.length > 0) {
                report += `## ${this.getCategoryTitle(category)}\n\n`;

                if (Array.isArray(items)) {
                    items.forEach((item, index) => {
                        if (item.pattern) {
                            report += `${index + 1}. **الگو:** \`${item.pattern}\`\n`;
                            report += `   - **مکان:** ${item.foundIn}\n\n`;
                        } else if (item.tag) {
                            report += `${index + 1}. **عنصر:** \`<${item.tag}>\`\n`;
                            report += `   - **کلاس:** ${item.className || 'بدون کلاس'}\n`;
                            report += `   - **ID:** ${item.id || 'بدون ID'}\n`;
                            report += `   - **متن:** ${item.text}\n\n`;
                        } else if (item.src) {
                            report += `${index + 1}. **اسکریپت:** ${item.src}\n`;
                            report += `   - **محتوای نمونه:** \`\`\`js\n${item.content}\n\`\`\`\n\n`;
                        }
                    });
                }
            }
        });

        return report;
    }

    getCategoryTitle(category) {
        const titles = {
            chatbots: '💬 چت‌بات‌ها',
            codeGenerators: '💻 تولیدکنندگان کد',
            contentGenerators: '📝 تولیدکنندگان محتوا',
            imageGenerators: '🎨 تولیدکنندگان تصویر',
            voiceAI: '🎤 هوش مصنوعی صوتی',
            dataAnalysis: '📊 تحلیل داده‌ها',
            apis: '🔌 API های هوش مصنوعی',
            frameworks: '🏗️ فریم‌ورک‌های AI',
            aiElements: '🏷️ عناصر HTML مرتبط با AI',
            aiScripts: '📜 اسکریپت‌های AI'
        };
        return titles[category] || category;
    }

    async downloadFile(url, localPath) {
        // بررسی URL قبل از دانلود
        if (!url || url.startsWith('data:') || url.startsWith('blob:') || url.startsWith('javascript:')) {
            throw new Error('URL نامعتبر یا غیرقابل دانلود');
        }

        return new Promise((resolve, reject) => {
            const client = url.startsWith('https:') ? https : http;

            // تنظیم timeout برای جلوگیری از hang شدن
            const request = client.get(url, { timeout: 10000 }, (response) => {
                if (response.statusCode === 200) {
                    // Ensure the directory exists and the path is safe
                    const dir = path.dirname(localPath);
                    fs.ensureDir(dir).then(() => {
                        // Make sure localPath doesn't conflict with existing directories
                        fs.pathExists(localPath).then(exists => {
                            if (exists) {
                                // If path exists as directory, add .html extension
                                localPath = localPath + '.html';
                            }

                            const file = fs.createWriteStream(localPath);
                            response.pipe(file);
                            file.on('finish', () => {
                                file.close();
                                resolve();
                            });
                            file.on('error', reject);
                        }).catch(reject);
                    }).catch(reject);
                } else {
                    reject(new Error(`HTTP ${response.statusCode}`));
                }
            });

            // اضافه کردن timeout و error handling
            request.on('error', (error) => {
                // اگر خطای timeout یا connection است، نادیده بگیر
                if (error.code === 'ECONNRESET' || error.code === 'ETIMEDOUT' || 
                    error.message.includes('socket disconnected')) {
                    reject(new Error('Network error - ignored'));
                } else {
                    reject(error);
                }
            });

            request.setTimeout(10000, () => {
                request.destroy();
                reject(new Error('Request timeout'));
            });
        });
    }

    resolveUrl(url) {
        // نادیده گرفتن data URI ها و سایر پروتکل‌های غیر HTTP
        if (url.startsWith('data:') || url.startsWith('blob:') || url.startsWith('javascript:')) {
            return null;
        }

        // نادیده گرفتن about:blank
        if (url === 'about:blank') {
            return null;
        }

        // نادیده گرفتن URL های خالی یا نامعتبر
        if (!url || url.trim() === '') {
            return null;
        }

        if (url.startsWith('http')) {
            return url;
        }

        try {
            return new URL(url, this.baseUrl.href).href;
        } catch (error) {
            // اگر URL نامعتبر است، null برگردان
            return null;
        }
    }

    getLocalPath(url, baseDir, defaultExt = '') {
        try {
            const urlObj = new URL(url);
            let pathname = urlObj.pathname;

            // Handle root path
            if (pathname === '/' || pathname === '') {
                pathname = '/index' + defaultExt;
            }

            // Handle empty or problematic paths
            if (!pathname || pathname === '/') {
                pathname = '/index' + defaultExt;
            }

            // Check if this is an API endpoint or similar (no file extension)
            if (!path.extname(pathname) && defaultExt) {
                // If it's an API endpoint like /wp-json, treat it as a file
                if (pathname.includes('/wp-json') || pathname.includes('/api/')) {
                    // Replace slashes with underscores for file names
                    const filename = pathname.replace(/\//g, '_').replace(/^_/, '') + '.json';
                    return path.join(baseDir, 'api', filename);
                }

                // Handle paths that end with / (like /v1/)
                if (pathname.endsWith('/')) {
                    // برای مسیرهایی مثل /v1/ که ممکنه فایل باشن
                    if (pathname.includes('/v1/') || pathname.includes('/api/')) {
                        pathname = pathname.slice(0, -1) + '.js';
                    } else {
                        pathname = pathname.slice(0, -1) + '/index' + defaultExt;
                    }
                } else {
                    pathname += defaultExt;
                }
            }

            // Sanitize path separators for Windows and handle problematic characters
            let sanitizedPath = pathname.replace(/\//g, path.sep);

            // Remove or replace problematic characters
            sanitizedPath = sanitizedPath.replace(/[<>:"|?*]/g, '_');

            // Ensure the path doesn't end with a separator (except for root)
            if (sanitizedPath.endsWith(path.sep) && sanitizedPath !== path.sep) {
                sanitizedPath = sanitizedPath.slice(0, -1);
            }

            // Handle paths that might conflict with existing directories
            const fullPath = path.join(baseDir, sanitizedPath);

            // If the path would create a directory conflict, add a suffix
            if (sanitizedPath.endsWith(path.sep) || !path.extname(sanitizedPath)) {
                return fullPath + defaultExt;
            }

            return fullPath;
        } catch (error) {
            // Fallback for invalid URLs
            const filename = url.replace(/[^a-z0-9]/gi, '_') + defaultExt;
            return path.join(baseDir, 'assets', filename);
        }
    }

    isAsset(url) {
        const assetExtensions = [
            '.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp',
            '.mp4', '.webm', '.mp3', '.wav', '.pdf', '.doc', '.docx',
            '.woff', '.woff2', '.ttf', '.eot', '.ico'
        ];

        return assetExtensions.some(ext => url.toLowerCase().includes(ext));
    }

    isIgnorableError(url, errorMessage) {
        // URLs that typically fail and are not important for site cloning
        const ignorablePatterns = [
            'bat.bing.com',
            'google-analytics.com',
            'googletagmanager.com',
            'facebook.com/tr',
            'segment.com',
            'segment.prod.bidr.io',
            'accounts.google.com/gsi',
            'doubleclick.net',
            'googleadservices.com',
            'google.com/ads',
            'hotjar.com',
            'drift.com',
            'intercom.io',
            'clerk.openrouter.ai',
            'datadoghq.com',
            'us5.datadoghq.com',
            'cdn.getkoala.com',
            'js.partnerstack.com'
        ];

        // Error codes that are acceptable
        const ignorableErrors = [
            'HTTP 302', 'HTTP 303', 'HTTP 204', 'HTTP 403', 'HTTP 301', 'HTTP 404', 'HTTP 307'
        ];

        // Data URI errors (base64 encoded images)
        const dataUriErrors = [
            'protocol "data:" not supported',
            'data:image',
            'data:application',
            'data:text',
            'protocol "about:" not supported',
            'about:blank'
        ];

        // Network connection errors
        const networkErrors = [
            'ECONNRESET',
            'Client network socket disconnected',
            'socket hang up',
            'ENOTFOUND',
            'ETIMEDOUT',
            'ECONNREFUSED'
        ];

        const urlLower = url.toLowerCase();
        const errorLower = errorMessage.toLowerCase();

        // Check for data URI patterns
        if (url.startsWith('data:') || dataUriErrors.some(pattern => errorLower.includes(pattern))) {
            return true;
        }

        // Check for network errors
        if (networkErrors.some(pattern => errorLower.includes(pattern))) {
            return true;
        }

        return ignorablePatterns.some(pattern => urlLower.includes(pattern)) ||
            ignorableErrors.some(error => errorLower.includes(error.toLowerCase()));
    }

    async generateSitemap(siteDir) {
        const sitemap = {
            baseUrl: this.baseUrl.href,
            domain: this.domain,
            extractedAt: new Date().toISOString(),
            totalPages: this.visitedUrls.size,
            totalAssets: this.downloadedAssets.size,
            pages: Array.from(this.visitedUrls),
            assets: Array.from(this.downloadedAssets)
        };

        await fs.writeFile(
            path.join(siteDir, 'sitemap.json'),
            JSON.stringify(sitemap, null, 2)
        );
    }

    async generateMetadata(siteDir) {
        const metadata = {
            extractor: 'DeepWebsiteCloner v1.0',
            extractedAt: new Date().toISOString(),
            baseUrl: this.baseUrl.href,
            domain: this.domain,
            config: this.config,
            statistics: {
                totalPages: this.visitedUrls.size,
                totalAssets: this.downloadedAssets.size,
                maxDepth: this.maxDepth
            }
        };

        await fs.writeFile(
            path.join(siteDir, 'metadata.json'),
            JSON.stringify(metadata, null, 2)
        );
    }

    async createArchive(siteDir) {
        const archiver = require('archiver');
        const archivePath = `${siteDir}.zip`;
        const output = fs.createWriteStream(archivePath);
        const archive = archiver('zip', { zlib: { level: 9 } });

        return new Promise((resolve, reject) => {
            output.on('close', () => {
                console.log(`📦 آرشیو ایجاد شد: ${archivePath} (${archive.pointer()} bytes)`);
                resolve(archivePath);
            });

            archive.on('error', (err) => {
                reject(err);
            });

            archive.pipe(output);
            archive.directory(siteDir, false);
            archive.finalize();
        });
    }

    async close() {
        if (this.browser) {
            await this.browser.close();
        }
    }
}

module.exports = DeepWebsiteCloner;
