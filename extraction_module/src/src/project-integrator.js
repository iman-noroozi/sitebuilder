// انتقال فایل‌های مهم به پروژه اصلی
const fs = require('fs-extra');
const path = require('path');

class ProjectIntegrator {
    constructor() {
        this.extractedDir = './extracted_sites';
        this.projectDir = '../';
        this.integratedFiles = [];
    }

    async integrateAll() {
        console.log('🚀 شروع انتقال فایل‌ها به پروژه اصلی...');
        
        // ایجاد ساختار پوشه‌های پروژه
        await this.createProjectStructure();
        
        // انتقال فایل‌های CSS
        await this.transferCSSFiles();
        
        // انتقال فایل‌های JS
        await this.transferJSFiles();
        
        // انتقال کامپوننت‌ها
        await this.transferComponents();
        
        // ایجاد فایل‌های پیکربندی
        await this.createConfigFiles();
        
        console.log('✅ انتقال کامل شد!');
        console.log(`📊 ${this.integratedFiles.length} فایل منتقل شد`);
        
        return this.generateIntegrationReport();
    }

    async createProjectStructure() {
        console.log('📁 ایجاد ساختار پروژه...');
        
        const directories = [
            '../frontend/css/frameworks',
            '../frontend/css/components',
            '../frontend/css/themes',
            '../frontend/js/frameworks',
            '../frontend/js/components',
            '../frontend/assets/images',
            '../frontend/assets/fonts',
            '../backend/templates',
            '../docs/extracted-resources'
        ];

        for (const dir of directories) {
            await fs.ensureDir(dir);
            console.log(`✅ ایجاد شد: ${dir}`);
        }
    }

    async transferCSSFiles() {
        console.log('🎨 انتقال فایل‌های CSS...');
        
        const importantCSS = [
            // Bootstrap
            {
                source: 'getbootstrap_com/docs/5.3/dist/css/bootstrap.min.css',
                dest: '../frontend/css/frameworks/bootstrap.min.css',
                name: 'Bootstrap Framework'
            },
            // Webflow Styles
            {
                source: 'webflow_com/66e88746834b80507cdf7933/css',
                dest: '../frontend/css/frameworks/webflow',
                name: 'Webflow Styles',
                isDirectory: true
            },
            // TailwindCSS
            {
                source: 'tailwindcss_com/_next/static/css',
                dest: '../frontend/css/frameworks/tailwind',
                name: 'TailwindCSS Styles',
                isDirectory: true
            }
        ];

        for (const css of importantCSS) {
            try {
                const sourcePath = path.join(this.extractedDir, css.source);
                
                if (css.isDirectory && await fs.pathExists(sourcePath)) {
                    await fs.copy(sourcePath, css.dest);
                    console.log(`✅ کپی شد: ${css.name} (پوشه)`);
                } else if (await fs.pathExists(sourcePath)) {
                    await fs.copy(sourcePath, css.dest);
                    console.log(`✅ کپی شد: ${css.name}`);
                }
                
                this.integratedFiles.push(css);
                
            } catch (error) {
                console.log(`❌ خطا در کپی ${css.name}:`, error.message);
            }
        }
    }

    async transferJSFiles() {
        console.log('📜 انتقال فایل‌های JS...');
        
        const importantJS = [
            // Webflow Scripts
            {
                source: 'webflow_com/js',
                dest: '../frontend/js/frameworks/webflow',
                name: 'Webflow Scripts',
                isDirectory: true
            },
            // Bootstrap JS
            {
                source: 'getbootstrap_com/docs/5.3/dist/js',
                dest: '../frontend/js/frameworks/bootstrap',
                name: 'Bootstrap Scripts',
                isDirectory: true
            }
        ];

        for (const js of importantJS) {
            try {
                const sourcePath = path.join(this.extractedDir, js.source);
                
                if (await fs.pathExists(sourcePath)) {
                    await fs.copy(sourcePath, js.dest);
                    console.log(`✅ کپی شد: ${js.name}`);
                    this.integratedFiles.push(js);
                }
                
            } catch (error) {
                console.log(`❌ خطا در کپی ${js.name}:`, error.message);
            }
        }
    }

    async transferComponents() {
        console.log('🧩 استخراج کامپوننت‌ها...');
        
        // ایجاد کتابخانه کامپوننت‌ها
        const componentsHTML = `
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>کتابخانه کامپوننت‌های استخراج شده</title>
    <link rel="stylesheet" href="css/frameworks/bootstrap.min.css">
    <link rel="stylesheet" href="css/frameworks/webflow/webflow-styles.css">
</head>
<body>
    <div class="container">
        <h1>🧩 کتابخانه کامپوننت‌های استخراج شده</h1>
        
        <div class="row">
            <div class="col-md-6">
                <h2>🔹 کامپوننت‌های Bootstrap</h2>
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">نمونه کارت</h5>
                        <p class="card-text">این یک کامپوننت نمونه از Bootstrap است.</p>
                        <button class="btn btn-primary">دکمه اصلی</button>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <h2>🔹 استایل‌های Webflow</h2>
                <div class="webflow-container">
                    <div class="webflow-card">
                        <h5>کامپوننت Webflow</h5>
                        <p>طراحی زیبا و مدرن با استایل‌های Webflow</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="js/frameworks/bootstrap/bootstrap.bundle.min.js"></script>
    <script src="js/frameworks/webflow/webflow-scripts.js"></script>
</body>
</html>`;

        await fs.writeFile('../frontend/components.html', componentsHTML);
        console.log('✅ کتابخانه کامپوننت‌ها ایجاد شد');
    }

    async createConfigFiles() {
        console.log('⚙️ ایجاد فایل‌های پیکربندی...');
        
        // فایل پیکربندی CSS
        const cssConfig = {
            frameworks: {
                bootstrap: {
                    path: "css/frameworks/bootstrap.min.css",
                    version: "5.3",
                    description: "فریمورک CSS محبوب"
                },
                webflow: {
                    path: "css/frameworks/webflow/",
                    description: "استایل‌های Webflow"
                },
                tailwind: {
                    path: "css/frameworks/tailwind/",
                    description: "TailwindCSS Framework"
                }
            },
            components: {
                cards: "css/components/cards.css",
                buttons: "css/components/buttons.css",
                forms: "css/components/forms.css"
            },
            usage: {
                development: "همه فریمورک‌ها برای توسعه",
                production: "فقط فریمورک‌های ضروری"
            }
        };

        await fs.writeFile('../frontend/css/config.json', JSON.stringify(cssConfig, null, 2));
        
        // فایل راهنمای استفاده
        const usageGuide = `# 🚀 راهنمای استفاده از منابع انتقال یافته

## 📂 ساختار فایل‌ها:

### CSS:
- \`css/frameworks/bootstrap.min.css\` - فریمورک Bootstrap
- \`css/frameworks/webflow/\` - استایل‌های Webflow
- \`css/frameworks/tailwind/\` - TailwindCSS

### JavaScript:
- \`js/frameworks/bootstrap/\` - اسکریپت‌های Bootstrap
- \`js/frameworks/webflow/\` - اسکریپت‌های Webflow

## 🔧 نحوه استفاده:

### در HTML:
\`\`\`html
<link rel="stylesheet" href="css/frameworks/bootstrap.min.css">
<link rel="stylesheet" href="css/frameworks/webflow/main.css">
<script src="js/frameworks/bootstrap/bootstrap.bundle.min.js"></script>
\`\`\`

### در پروژه Node.js:
\`\`\`javascript
// وارد کردن استایل‌ها
import 'css/frameworks/bootstrap.min.css';
import 'css/frameworks/webflow/main.css';
\`\`\`

## 🎯 توصیه‌ها:
1. برای پروژه‌های سریع از Bootstrap استفاده کنید
2. برای طراحی‌های سفارشی از Webflow styles استفاده کنید
3. برای کنترل دقیق از TailwindCSS استفاده کنید

---
*تاریخ انتقال: ${new Date().toLocaleDateString('fa-IR')}*
`;

        await fs.writeFile('../docs/extracted-resources/INTEGRATION_GUIDE.md', usageGuide);
        console.log('✅ فایل‌های پیکربندی ایجاد شد');
    }

    async generateIntegrationReport() {
        const report = {
            integration: {
                completedAt: new Date().toISOString(),
                totalFiles: this.integratedFiles.length,
                status: 'موفق'
            },
            integratedFiles: this.integratedFiles,
            projectStructure: {
                frontend: {
                    css: ['frameworks', 'components', 'themes'],
                    js: ['frameworks', 'components'],
                    assets: ['images', 'fonts']
                },
                backend: {
                    templates: 'قالب‌های HTML'
                },
                docs: {
                    'extracted-resources': 'مستندات منابع استخراج شده'
                }
            },
            nextSteps: [
                "1. بررسی فایل‌های منتقل شده",
                "2. تست عملکرد در پروژه",
                "3. سفارشی‌سازی بر اساس نیاز",
                "4. بهینه‌سازی برای production"
            ]
        };

        await fs.writeFile('./integration_report.json', JSON.stringify(report, null, 2));
        
        console.log('\n📊 گزارش انتقال:');
        console.log(`   📁 ${this.integratedFiles.length} فایل منتقل شد`);
        console.log('   📄 گزارش در integration_report.json ذخیره شد');
        
        return report;
    }
}

if (require.main === module) {
    const integrator = new ProjectIntegrator();
    integrator.integrateAll().catch(console.error);
}

module.exports = ProjectIntegrator;
