// تجزیه و تحلیل فایل‌های استخراج شده و آماده‌سازی برای پروژه
const fs = require('fs-extra');
const path = require('path');

class ExtractedFilesAnalyzer {
    constructor() {
        this.extractedDir = './extracted_sites';
        this.analysis = {
            cssFiles: [],
            jsFiles: [],
            components: [],
            frameworks: [],
            designSystems: []
        };
    }

    async analyzeAll() {
        console.log('🔍 شروع تجزیه و تحلیل فایل‌های استخراج شده...');
        
        const sites = await fs.readdir(this.extractedDir);
        const siteFolders = sites.filter(item => !item.includes('.'));
        
        console.log(`📁 تعداد سایت‌های استخراج شده: ${siteFolders.length}`);
        
        for (const siteFolder of siteFolders) {
            await this.analyzeSite(siteFolder);
        }
        
        await this.generateUsefulResources();
        console.log('✅ تجزیه و تحلیل کامل شد!');
    }

    async analyzeSite(siteFolder) {
        const sitePath = path.join(this.extractedDir, siteFolder);
        
        try {
            console.log(`🔍 تجزیه و تحلیل: ${siteFolder}`);
            
            // پیدا کردن فایل‌های CSS
            await this.findFiles(sitePath, '.css', this.analysis.cssFiles, siteFolder);
            
            // پیدا کردن فایل‌های JS
            await this.findFiles(sitePath, '.js', this.analysis.jsFiles, siteFolder);
            
            // تشخیص نوع سایت
            this.categorizeWebsite(siteFolder);
            
        } catch (error) {
            console.log(`❌ خطا در تجزیه و تحلیل ${siteFolder}:`, error.message);
        }
    }

    async findFiles(dirPath, extension, targetArray, siteName) {
        try {
            const items = await fs.readdir(dirPath);
            
            for (const item of items) {
                const itemPath = path.join(dirPath, item);
                const stat = await fs.stat(itemPath);
                
                if (stat.isDirectory()) {
                    await this.findFiles(itemPath, extension, targetArray, siteName);
                } else if (item.endsWith(extension)) {
                    const size = stat.size;
                    if (size > 1024) { // فقط فایل‌های بزرگتر از 1KB
                        targetArray.push({
                            file: item,
                            path: itemPath,
                            site: siteName,
                            size: this.formatFileSize(size)
                        });
                    }
                }
            }
        } catch (error) {
            // پوشه موجود نیست یا قابل دسترسی نیست
        }
    }

    categorizeWebsite(siteFolder) {
        if (siteFolder.includes('webflow')) {
            this.analysis.designSystems.push('Webflow Visual Designer');
        } else if (siteFolder.includes('bootstrap')) {
            this.analysis.frameworks.push('Bootstrap CSS Framework');
        } else if (siteFolder.includes('tailwind')) {
            this.analysis.frameworks.push('Tailwind CSS Framework');
        } else if (siteFolder.includes('mui') || siteFolder.includes('material')) {
            this.analysis.components.push('Material-UI Components');
        } else if (siteFolder.includes('ant')) {
            this.analysis.components.push('Ant Design Components');
        }
    }

    async generateUsefulResources() {
        console.log('\n📊 خلاصه تجزیه و تحلیل:');
        console.log(`🎨 فایل‌های CSS: ${this.analysis.cssFiles.length}`);
        console.log(`📜 فایل‌های JS: ${this.analysis.jsFiles.length}`);
        console.log(`🔧 فریمورک‌ها: ${this.analysis.frameworks.length}`);
        console.log(`🎯 کامپوننت‌ها: ${this.analysis.components.length}`);
        
        // ایجاد فهرست بهترین فایل‌ها
        const bestResources = {
            topCSSFiles: this.analysis.cssFiles
                .sort((a, b) => parseInt(b.size) - parseInt(a.size))
                .slice(0, 10),
            topJSFiles: this.analysis.jsFiles
                .sort((a, b) => parseInt(b.size) - parseInt(a.size))
                .slice(0, 10),
            frameworks: [...new Set(this.analysis.frameworks)],
            components: [...new Set(this.analysis.components)],
            designSystems: [...new Set(this.analysis.designSystems)],
            recommendations: [
                "🎨 از فایل‌های CSS Webflow برای سیستم طراحی استفاده کنید",
                "🚀 از Bootstrap برای responsive design",
                "💎 از Material-UI برای کامپوننت‌های آماده",
                "🔧 از فایل‌های JS برای تعاملات پیشرفته",
                "📱 از طراحی‌های موجود الهام بگیرید"
            ],
            nextSteps: [
                "1. فایل‌های CSS اصلی را به پروژه اضافه کنید",
                "2. کامپوننت‌های مفید را استخراج کنید", 
                "3. سیستم طراحی یکپارچه ایجاد کنید",
                "4. فایل‌های JS را برای قابلیت‌های تعاملی استفاده کنید",
                "5. از الگوهای طراحی موجود الهام بگیرید"
            ]
        };

        await fs.writeFile('./extracted_sites/resources_analysis.json', JSON.stringify(bestResources, null, 2));
        
        // ایجاد فایل راهنمای استفاده
        const guide = `# 🚀 راهنمای استفاده از منابع استخراج شده

## 📁 فایل‌های مهم استخراج شده:

### 🎨 بهترین فایل‌های CSS:
${bestResources.topCSSFiles.map(f => `- ${f.file} (${f.site}) - ${f.size}`).join('\n')}

### 📜 بهترین فایل‌های JS:
${bestResources.topJSFiles.map(f => `- ${f.file} (${f.site}) - ${f.size}`).join('\n')}

### 🔧 فریمورک‌های موجود:
${bestResources.frameworks.map(f => `- ${f}`).join('\n')}

### 🎯 کامپوننت‌های موجود:
${bestResources.components.map(c => `- ${c}`).join('\n')}

## 🏗️ نحوه استفاده در پروژه:

1. **کپی فایل‌های مهم:**
   \`\`\`bash
   cp extracted_sites/webflow_com/css/* ../frontend/css/
   cp extracted_sites/getbootstrap_com/css/* ../frontend/frameworks/
   \`\`\`

2. **ادغام در پروژه اصلی:**
   \`\`\`html
   <link rel="stylesheet" href="css/webflow-styles.css">
   <link rel="stylesheet" href="frameworks/bootstrap.css">
   \`\`\`

3. **استفاده از کامپوننت‌ها:**
   \`\`\`javascript
   // استفاده از کدهای JS استخراج شده
   // ایجاد کامپوننت‌های مشابه
   \`\`\`

## ✅ توصیه‌ها:
${bestResources.recommendations.map(r => `${r}`).join('\n')}

## 🔄 مراحل بعدی:
${bestResources.nextSteps.map(s => `${s}`).join('\n')}

---
*تاریخ تولید: ${new Date().toLocaleDateString('fa-IR')}*
`;

        await fs.writeFile('./extracted_sites/USAGE_GUIDE.md', guide);
        
        console.log('\n📄 فایل‌های تجزیه و تحلیل ایجاد شد:');
        console.log('   📊 resources_analysis.json');
        console.log('   📚 USAGE_GUIDE.md');
        
        return bestResources;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }
}

if (require.main === module) {
    const analyzer = new ExtractedFilesAnalyzer();
    analyzer.analyzeAll().catch(console.error);
}

module.exports = ExtractedFilesAnalyzer;
