// Test script for extracting a simple website first
const DeepWebsiteCloner = require('./deep-cloner');

async function testSimpleExtraction() {
    console.log('🎯 شروع تست استخراج با سایت ساده...');
    
    const cloner = new DeepWebsiteCloner({
        outputDir: './extracted_sites',
        maxDepth: 1,
        delay: 1000,
        extractCSS: true,
        extractJS: true,
        extractImages: true,
        followInternalLinks: false
    });

    try {
        await cloner.init();
        
        // Test with a simple website first
        const result = await cloner.cloneWebsite('https://example.com/');
        
        console.log('✅ تست اولیه موفق بود!');
        console.log(`📁 فایل‌ها در: ${result}`);
        console.log(`📊 تعداد صفحات: ${cloner.visitedUrls.size}`);
        console.log(`📊 تعداد فایل‌ها: ${cloner.downloadedAssets.size}`);
        
        return result;
        
    } catch (error) {
        console.error('❌ خطا در تست:', error);
    } finally {
        await cloner.close();
    }
}

// Run test if called directly
if (require.main === module) {
    testSimpleExtraction().catch(console.error);
}

module.exports = testSimpleExtraction;
pip uninstall faiss-cpu
pip install faiss-cpu