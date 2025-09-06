// Test script for extracting Duda.co website
const DeepWebsiteCloner = require('./deep-cloner');

async function testDudaExtraction() {
    console.log('🎯 شروع استخراج سایت Duda.co...');
    
    const cloner = new DeepWebsiteCloner({
        outputDir: './extracted_sites',
        maxDepth: 1, // فقط صفحه اصلی برای تست اولیه
        delay: 3000, // 3 ثانیه تاخیر بین درخواست‌ها
        extractCSS: true,
        extractJS: true,
        extractImages: true,
        extractFonts: true,
        extractVideos: true,
        followInternalLinks: false // فعلاً لینک‌ها رو دنبال نکنیم
    });

    try {
        await cloner.init();
        
        const result = await cloner.cloneWebsite('https://www.duda.co/');
        
        console.log('✅ استخراج Duda.co تمام شد!');
        console.log(`📁 فایل‌ها در: ${result}`);
        console.log(`📊 تعداد صفحات: ${cloner.visitedUrls.size}`);
        console.log(`📊 تعداد فایل‌ها: ${cloner.downloadedAssets.size}`);
        
        return result;
        
    } catch (error) {
        console.error('❌ خطا در استخراج Duda:', error);
    } finally {
        await cloner.close();
    }
}

// Run test if called directly
if (require.main === module) {
    testDudaExtraction().catch(console.error);
}

module.exports = testDudaExtraction;
