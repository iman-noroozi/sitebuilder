// Test script for extracting Bootstrap website
const DeepWebsiteCloner = require('./deep-cloner');

async function testBootstrapExtraction() {
    console.log('🎯 شروع استخراج سایت Bootstrap...');
    
    const cloner = new DeepWebsiteCloner({
        outputDir: './extracted_sites',
        maxDepth: 2,
        delay: 2000,
        extractCSS: true,
        extractJS: true,
        extractImages: true,
        extractFonts: true,
        followInternalLinks: true
    });

    try {
        await cloner.init();
        
        const result = await cloner.cloneWebsite('https://getbootstrap.com/');
        
        console.log('✅ استخراج Bootstrap تمام شد!');
        console.log(`📁 فایل‌ها در: ${result}`);
        console.log(`📊 تعداد صفحات: ${cloner.visitedUrls.size}`);
        console.log(`📊 تعداد فایل‌ها: ${cloner.downloadedAssets.size}`);
        
        return result;
        
    } catch (error) {
        console.error('❌ خطا در استخراج Bootstrap:', error);
    } finally {
        await cloner.close();
    }
}

// Run test if called directly
if (require.main === module) {
    testBootstrapExtraction().catch(console.error);
}

module.exports = testBootstrapExtraction;
