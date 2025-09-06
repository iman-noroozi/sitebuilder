class TemplateEnhancer {
    constructor(options = {}) {
        this.options = options;
    }

    async enhanceTemplates(templates) {
        console.log('🔍 شروع بهبود قالب‌ها...');

        for (const template of templates) {
            await this.enhanceTemplate(template);
        }

        console.log('✅ بهبود قالب‌ها با موفقیت انجام شد!');
        return templates;
    }
    async extractSite(site) {
        const { name: siteName, url } = site;
        console.log(`\n🔍 استخراج قالب از ${siteName} (${url})...`);

        try {
            const outputDir = path.join(__dirname, 'extracted_sites', siteName);
            await fs.mkdir(outputDir, { recursive: true });

            // رفتن به سایت
            await this.page.goto(url);
            console.log(`🌐 در حال بارگذاری ${siteName}...`);

            // گرفتن HTML
            const html = await this.page.content();
            await fs.writeFile(path.join(outputDir, 'index.html'), html);
            console.log(`✅ HTML ذخیره شد: ${path.join(outputDir, 'index.html')}`);

            // گرفتن CSS ها
            const stylesheets = await this.page.evaluate(() => {
                return Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
                    .map(link => link.href)
                    .slice(0, 5); // فقط 5 فایل CSS اول
            });

            console.log(`📄 ${stylesheets.length} فایل CSS پیدا شد`);

            // دانلود CSS ها (تعداد محدود)
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
                    .map(script => script.src)
                    .slice(0, 5); // فقط 5 فایل JS اول      
            });
        }
        finally {
        }
    }
}
