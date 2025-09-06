// Extract Webflow - The best design-focused website builder
const DeepWebsiteCloner = require('./deep-cloner');

async function extractWebflow() {
    console.log('🎨 شروع استخراج Webflow.com...');
    
    const cloner = new DeepWebsiteCloner({
        outputDir: './extracted_sites',
        maxDepth: 2,
        delay: 2000,
        extractCSS: true,
        extractJS: true,
        extractImages: true,
        extractFonts: true,
        extractVideos: true,
        followInternalLinks: true
    });

    try {
        await cloner.init();
        const result = await cloner.cloneWebsite('https://webflow.com/');
        
        console.log('✅ Webflow استخراج شد!');
        console.log(`📁 مسیر: ${result}`);
        console.log(`📊 صفحات: ${cloner.visitedUrls.size}`);
        console.log(`📊 فایل‌ها: ${cloner.downloadedAssets.size}`);
        
        return result;
    } catch (error) {
        console.error('❌ خطا در Webflow:', error.message);
    } finally {
        await cloner.close();
    }
}

if (require.main === module) {
    extractWebflow().catch(console.error);
}

module.exports = extractWebflow;
