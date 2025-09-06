const TemplateExtractor = require('../extractor/puppeteer.js');
const path = require('path');

async function testExtractor() {
    console.log('🧪 شروع تست ابزار استخراج...\n');
    
    const extractor = new TemplateExtractor({
        headless: false, // برای مشاهده فرآیند
        timeout: 45000,
        downloadAssets: true,
        extractImages: true,
        extractFonts: true
    });

    // سایت‌های تست
    const testUrls = [
        'https://example.com',
        'https://getbootstrap.com/docs/5.3/examples/carousel/',
        'https://tailwindui.com/preview', // اگر در دسترس باشد
    ];

    const outputBasePath = path.join(__dirname, '..', 'test_outputs');

    try {
        console.log('📋 شروع استخراج چندین سایت...\n');
        
        for (let i = 0; i < testUrls.length; i++) {
            const url = testUrls[i];
            const outputPath = path.join(outputBasePath, `test_site_${i + 1}`);
            
            console.log(`\n🔍 در حال استخراج: ${url}`);
            console.log(`📁 مسیر خروجی: ${outputPath}\n`);
            
            try {
                const result = await extractor.extractTemplate(url, outputPath);
                
                console.log(`✅ استخراج موفق: ${url}`);
                console.log(`📊 آمار:
                - HTML: ${result.html.length} کاراکتر
                - CSS: ${result.styles.length} کاراکتر  
                - تصاویر: ${result.images?.length || 0} فایل
                - اسکریپت‌ها: ${result.scripts?.length || 0} فایل
                - فونت‌ها: ${result.fonts?.length || 0} فایل
                `);
                
            } catch (error) {
                console.error(`❌ خطا در استخراج ${url}:`, error.message);
            }
            
            // وقفه بین درخواست‌ها
            if (i < testUrls.length - 1) {
                console.log('\n⏳ انتظار 3 ثانیه...\n');
                await new Promise(resolve => setTimeout(resolve, 3000));
            }
        }
        
        console.log('\n🎉 تست‌ها تمام شد!');
        console.log(`📁 نتایج در: ${outputBasePath}`);
        
    } catch (error) {
        console.error('❌ خطای کلی:', error);
    }
}

// تست تک سایت
async function testSingleSite() {
    console.log('🧪 تست تک سایت...\n');
    
    const extractor = new TemplateExtractor({
        headless: false,
        downloadAssets: true,
        extractImages: true,
        extractFonts: true
    });

    const url = process.argv[3] || 'https://example.com'; // آرگومان سوم برای URL
    const outputPath = path.join(__dirname, '..', 'single_test_output');

    console.log(`🔍 استخراج از: ${url}`);
    console.log(`📁 ذخیره در: ${outputPath}\n`);

    try {
        const result = await extractor.extractTemplate(url, outputPath);
        
        console.log('\n✅ استخراج کامل شد!');
        console.log('📂 فایل‌های ایجاد شده:');
        
        const fs = require('fs');
        const files = fs.readdirSync(outputPath);
        files.forEach(file => {
            const stats = fs.statSync(path.join(outputPath, file));
            console.log(`  - ${file} (${stats.isDirectory() ? 'پوشه' : Math.round(stats.size/1024) + ' KB'})`);
        });
        
    } catch (error) {
        console.error('❌ خطا:', error.message);
    }
}

// اجرای تست‌ها
if (require.main === module) {
    const testType = process.argv[2];
    
    if (testType === 'single') {
        testSingleSite();
    } else if (testType === 'multi') {
        testExtractor();
    } else {
        console.log(`
🧪 راهنمای تست ابزار استخراج

استفاده:
  node test/test.js single [URL]     - تست تک سایت
  node test/test.js multi            - تست چند سایت
  
مثال‌ها:
  node test/test.js single https://example.com
  node test/test.js multi
        `);
    }
}

module.exports = { testExtractor, testSingleSite };
