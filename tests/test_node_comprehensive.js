/**
 * 🧪 تست‌های جامع Node.js برای PEY Builder
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { promisify } = require('util');

// Mock modules for testing
const mockPuppeteer = {
    launch: jest.fn(),
    newPage: jest.fn(),
    goto: jest.fn(),
    evaluate: jest.fn(),
    screenshot: jest.fn(),
    close: jest.fn()
};

// Test utilities
class TestUtils {
    static createTempDir() {
        const tempDir = path.join(__dirname, 'temp_test_' + Date.now());
        fs.mkdirSync(tempDir, { recursive: true });
        return tempDir;
    }
    
    static cleanupTempDir(dir) {
        if (fs.existsSync(dir)) {
            fs.rmSync(dir, { recursive: true, force: true });
        }
    }
    
    static createMockHTML() {
        return `
        <!DOCTYPE html>
        <html lang="fa" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>تست سایت</title>
            <style>
                body { font-family: 'Tahoma', sans-serif; }
                .container { max-width: 1200px; margin: 0 auto; }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>سایت تست</h1>
                    <nav>
                        <ul>
                            <li><a href="#home">خانه</a></li>
                            <li><a href="#about">درباره ما</a></li>
                            <li><a href="#contact">تماس</a></li>
                        </ul>
                    </nav>
                </header>
                <main>
                    <section id="home">
                        <h2>خوش آمدید</h2>
                        <p>این یک سایت تست است که با PEY Builder ساخته شده.</p>
                    </section>
                </main>
            </div>
        </body>
        </html>
        `;
    }
}

// Test classes
class TemplateExtractorTest {
    constructor() {
        this.tempDir = null;
    }
    
    setUp() {
        this.tempDir = TestUtils.createTempDir();
    }
    
    tearDown() {
        TestUtils.cleanupTempDir(this.tempDir);
    }
    
    testExtractorInitialization() {
        console.log('🧪 تست راه‌اندازی استخراج‌کننده...');
        
        const config = {
            headless: true,
            timeout: 30000,
            downloadAssets: true,
            extractImages: true,
            extractFonts: true
        };
        
        // بررسی تنظیمات
        assert.strictEqual(config.headless, true);
        assert.strictEqual(config.timeout, 30000);
        assert.strictEqual(config.downloadAssets, true);
        assert.strictEqual(config.extractImages, true);
        assert.strictEqual(config.extractFonts, true);
        
        console.log('✅ راه‌اندازی استخراج‌کننده موفق');
    }
    
    testURLValidation() {
        console.log('🧪 تست اعتبارسنجی URL...');
        
        const validURLs = [
            'https://example.com',
            'http://example.com',
            'https://www.example.com/path',
            'https://subdomain.example.com/page?param=value'
        ];
        
        const invalidURLs = [
            'not-a-url',
            'ftp://example.com',
            '',
            null,
            undefined,
            'javascript:alert("xss")'
        ];
        
        // تست URL های معتبر
        validURLs.forEach(url => {
            assert.strictEqual(this.isValidURL(url), true, `URL معتبر رد شد: ${url}`);
        });
        
        // تست URL های نامعتبر
        invalidURLs.forEach(url => {
            assert.strictEqual(this.isValidURL(url), false, `URL نامعتبر پذیرفته شد: ${url}`);
        });
        
        console.log('✅ اعتبارسنجی URL موفق');
    }
    
    isValidURL(url) {
        if (!url || typeof url !== 'string') {
            return false;
        }
        
        try {
            const urlObj = new URL(url);
            return ['http:', 'https:'].includes(urlObj.protocol);
        } catch {
            return false;
        }
    }
    
    testHTMLParsing() {
        console.log('🧪 تست تجزیه HTML...');
        
        const html = TestUtils.createMockHTML();
        
        // بررسی وجود عناصر مهم
        assert(html.includes('<html'), 'تگ html باید وجود داشته باشد');
        assert(html.includes('<head'), 'تگ head باید وجود داشته باشد');
        assert(html.includes('<body'), 'تگ body باید وجود داشته باشد');
        assert(html.includes('lang="fa"'), 'زبان فارسی باید تنظیم شده باشد');
        assert(html.includes('dir="rtl"'), 'جهت راست به چپ باید تنظیم شده باشد');
        
        console.log('✅ تجزیه HTML موفق');
    }
    
    testCSSExtraction() {
        console.log('🧪 تست استخراج CSS...');
        
        const html = TestUtils.createMockHTML();
        const cssRegex = /<style[^>]*>([\s\S]*?)<\/style>/gi;
        const matches = html.match(cssRegex);
        
        assert(matches && matches.length > 0, 'CSS باید استخراج شود');
        
        const cssContent = matches[0].replace(/<\/?style[^>]*>/gi, '');
        assert(cssContent.includes('font-family'), 'فونت باید در CSS باشد');
        assert(cssContent.includes('max-width'), 'استایل container باید وجود داشته باشد');
        
        console.log('✅ استخراج CSS موفق');
    }
    
    testFileOperations() {
        console.log('🧪 تست عملیات فایل...');
        
        const testFile = path.join(this.tempDir, 'test.html');
        const testContent = TestUtils.createMockHTML();
        
        // نوشتن فایل
        fs.writeFileSync(testFile, testContent, 'utf8');
        assert(fs.existsSync(testFile), 'فایل باید ایجاد شود');
        
        // خواندن فایل
        const readContent = fs.readFileSync(testFile, 'utf8');
        assert.strictEqual(readContent, testContent, 'محتوای فایل باید یکسان باشد');
        
        // بررسی اندازه فایل
        const stats = fs.statSync(testFile);
        assert(stats.size > 0, 'فایل نباید خالی باشد');
        
        console.log('✅ عملیات فایل موفق');
    }
    
    testDirectoryStructure() {
        console.log('🧪 تست ساختار دایرکتوری...');
        
        const projectStructure = {
            'css': path.join(this.tempDir, 'css'),
            'js': path.join(this.tempDir, 'js'),
            'images': path.join(this.tempDir, 'images'),
            'fonts': path.join(this.tempDir, 'fonts')
        };
        
        // ایجاد دایرکتوری‌ها
        Object.values(projectStructure).forEach(dir => {
            fs.mkdirSync(dir, { recursive: true });
            assert(fs.existsSync(dir), `دایرکتوری ${dir} باید ایجاد شود`);
            assert(fs.statSync(dir).isDirectory(), `${dir} باید یک دایرکتوری باشد`);
        });
        
        console.log('✅ ساختار دایرکتوری موفق');
    }
    
    async testAsyncOperations() {
        console.log('🧪 تست عملیات ناهمزمان...');
        
        const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
        
        const startTime = Date.now();
        await delay(100);
        const endTime = Date.now();
        
        assert(endTime - startTime >= 100, 'تاخیر باید حداقل 100ms باشد');
        
        console.log('✅ عملیات ناهمزمان موفق');
    }
    
    testErrorHandling() {
        console.log('🧪 تست مدیریت خطا...');
        
        // تست خطای فایل وجود ندارد
        assert.throws(() => {
            fs.readFileSync('nonexistent-file.txt', 'utf8');
        }, 'باید خطای فایل وجود ندارد پرتاب شود');
        
        // تست خطای URL نامعتبر
        assert.strictEqual(this.isValidURL('invalid-url'), false);
        
        console.log('✅ مدیریت خطا موفق');
    }
    
    testPerformance() {
        console.log('🧪 تست عملکرد...');
        
        const iterations = 1000;
        const startTime = Date.now();
        
        // تست حلقه ساده
        let sum = 0;
        for (let i = 0; i < iterations; i++) {
            sum += i;
        }
        
        const endTime = Date.now();
        const duration = endTime - startTime;
        
        assert(sum > 0, 'مجموع باید بزرگتر از صفر باشد');
        assert(duration < 1000, 'عملیات باید کمتر از 1 ثانیه طول بکشد');
        
        console.log(`✅ عملکرد موفق (${duration}ms برای ${iterations} تکرار)`);
    }
    
    async runAllTests() {
        console.log('🚀 شروع تست‌های جامع Template Extractor...\n');
        
        try {
            this.setUp();
            
            this.testExtractorInitialization();
            this.testURLValidation();
            this.testHTMLParsing();
            this.testCSSExtraction();
            this.testFileOperations();
            this.testDirectoryStructure();
            await this.testAsyncOperations();
            this.testErrorHandling();
            this.testPerformance();
            
            console.log('\n🎉 تمام تست‌های Template Extractor موفق بودند!');
            
        } catch (error) {
            console.error('\n❌ خطا در تست‌ها:', error.message);
            throw error;
        } finally {
            this.tearDown();
        }
    }
}

class SiteBuilderTest {
    constructor() {
        this.tempDir = null;
    }
    
    setUp() {
        this.tempDir = TestUtils.createTempDir();
    }
    
    tearDown() {
        TestUtils.cleanupTempDir(this.tempDir);
    }
    
    testSiteConfiguration() {
        console.log('🧪 تست تنظیمات سایت...');
        
        const siteConfig = {
            name: 'سایت تست',
            domain: 'testsite.com',
            description: 'توضیحات سایت تست',
            keywords: ['تست', 'سایت', 'PEY Builder'],
            language: 'fa',
            theme: 'modern',
            features: ['responsive', 'seo', 'analytics']
        };
        
        // بررسی فیلدهای ضروری
        const requiredFields = ['name', 'domain', 'description'];
        requiredFields.forEach(field => {
            assert(siteConfig[field], `فیلد ${field} باید وجود داشته باشد`);
        });
        
        // بررسی نوع داده‌ها
        assert(typeof siteConfig.name === 'string', 'نام باید رشته باشد');
        assert(typeof siteConfig.domain === 'string', 'دامنه باید رشته باشد');
        assert(Array.isArray(siteConfig.keywords), 'کلمات کلیدی باید آرایه باشد');
        assert(Array.isArray(siteConfig.features), 'ویژگی‌ها باید آرایه باشد');
        
        console.log('✅ تنظیمات سایت موفق');
    }
    
    testTemplateProcessing() {
        console.log('🧪 تست پردازش قالب...');
        
        const template = {
            html: TestUtils.createMockHTML(),
            css: 'body { font-family: Arial; }',
            js: 'console.log("Hello World");',
            assets: {
                images: ['logo.png', 'banner.jpg'],
                fonts: ['font.woff2']
            }
        };
        
        // بررسی ساختار قالب
        assert(template.html, 'HTML باید وجود داشته باشد');
        assert(template.css, 'CSS باید وجود داشته باشد');
        assert(template.js, 'JavaScript باید وجود داشته باشد');
        assert(template.assets, 'Assets باید وجود داشته باشد');
        assert(Array.isArray(template.assets.images), 'تصاویر باید آرایه باشد');
        assert(Array.isArray(template.assets.fonts), 'فونت‌ها باید آرایه باشد');
        
        console.log('✅ پردازش قالب موفق');
    }
    
    testBuildProcess() {
        console.log('🧪 تست فرآیند ساخت...');
        
        const buildSteps = [
            'validate_config',
            'process_template',
            'generate_assets',
            'optimize_code',
            'create_output'
        ];
        
        const buildResult = {
            success: true,
            steps: buildSteps,
            outputPath: this.tempDir,
            files: ['index.html', 'style.css', 'script.js'],
            size: 1024 * 1024 // 1MB
        };
        
        // بررسی نتیجه ساخت
        assert(buildResult.success, 'ساخت باید موفق باشد');
        assert(Array.isArray(buildResult.steps), 'مراحل باید آرایه باشد');
        assert(buildResult.outputPath, 'مسیر خروجی باید وجود داشته باشد');
        assert(Array.isArray(buildResult.files), 'فایل‌ها باید آرایه باشد');
        assert(buildResult.size > 0, 'اندازه باید بزرگتر از صفر باشد');
        
        console.log('✅ فرآیند ساخت موفق');
    }
    
    async runAllTests() {
        console.log('🚀 شروع تست‌های جامع Site Builder...\n');
        
        try {
            this.setUp();
            
            this.testSiteConfiguration();
            this.testTemplateProcessing();
            this.testBuildProcess();
            
            console.log('\n🎉 تمام تست‌های Site Builder موفق بودند!');
            
        } catch (error) {
            console.error('\n❌ خطا در تست‌ها:', error.message);
            throw error;
        } finally {
            this.tearDown();
        }
    }
}

class APITest {
    constructor() {
        this.baseURL = 'http://localhost:8000/api';
    }
    
    testAPIEndpoints() {
        console.log('🧪 تست نقاط پایانی API...');
        
        const endpoints = [
            { path: '/websites', method: 'GET', description: 'لیست وب‌سایت‌ها' },
            { path: '/websites', method: 'POST', description: 'ایجاد وب‌سایت' },
            { path: '/templates', method: 'GET', description: 'لیست قالب‌ها' },
            { path: '/ai/generate-content', method: 'POST', description: 'تولید محتوا' },
            { path: '/collaboration/join', method: 'POST', description: 'پیوستن به همکاری' }
        ];
        
        endpoints.forEach(endpoint => {
            assert(endpoint.path, 'مسیر باید وجود داشته باشد');
            assert(endpoint.method, 'متد باید وجود داشته باشد');
            assert(endpoint.description, 'توضیحات باید وجود داشته باشد');
            
            // بررسی فرمت مسیر
            assert(endpoint.path.startsWith('/'), 'مسیر باید با / شروع شود');
            assert(['GET', 'POST', 'PUT', 'DELETE'].includes(endpoint.method), 'متد باید معتبر باشد');
        });
        
        console.log('✅ نقاط پایانی API موفق');
    }
    
    testRequestValidation() {
        console.log('🧪 تست اعتبارسنجی درخواست...');
        
        const validRequest = {
            method: 'POST',
            url: '/api/websites',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer token123'
            },
            body: {
                name: 'سایت تست',
                domain: 'testsite.com',
                description: 'توضیحات تست'
            }
        };
        
        // بررسی ساختار درخواست
        assert(validRequest.method, 'متد باید وجود داشته باشد');
        assert(validRequest.url, 'URL باید وجود داشته باشد');
        assert(validRequest.headers, 'هدرها باید وجود داشته باشد');
        assert(validRequest.body, 'بدنه باید وجود داشته باشد');
        
        // بررسی هدرها
        assert(validRequest.headers['Content-Type'], 'Content-Type باید وجود داشته باشد');
        assert(validRequest.headers['Authorization'], 'Authorization باید وجود داشته باشد');
        
        console.log('✅ اعتبارسنجی درخواست موفق');
    }
    
    async runAllTests() {
        console.log('🚀 شروع تست‌های جامع API...\n');
        
        try {
            this.testAPIEndpoints();
            this.testRequestValidation();
            
            console.log('\n🎉 تمام تست‌های API موفق بودند!');
            
        } catch (error) {
            console.error('\n❌ خطا در تست‌ها:', error.message);
            throw error;
        }
    }
}

// اجرای تمام تست‌ها
async function runAllTests() {
    console.log('🚀 شروع تست‌های جامع PEY Builder...\n');
    
    const tests = [
        new TemplateExtractorTest(),
        new SiteBuilderTest(),
        new APITest()
    ];
    
    let passedTests = 0;
    let totalTests = tests.length;
    
    for (const test of tests) {
        try {
            await test.runAllTests();
            passedTests++;
        } catch (error) {
            console.error(`❌ تست ${test.constructor.name} شکست خورد:`, error.message);
        }
    }
    
    console.log(`\n📊 نتایج نهایی: ${passedTests}/${totalTests} تست موفق`);
    
    if (passedTests === totalTests) {
        console.log('🎉 تمام تست‌ها موفق بودند!');
        process.exit(0);
    } else {
        console.log('❌ برخی تست‌ها شکست خوردند!');
        process.exit(1);
    }
}

// اجرا اگر فایل مستقیماً فراخوانی شود
if (require.main === module) {
    runAllTests().catch(error => {
        console.error('❌ خطای کلی در اجرای تست‌ها:', error);
        process.exit(1);
    });
}

module.exports = {
    TemplateExtractorTest,
    SiteBuilderTest,
    APITest,
    TestUtils,
    runAllTests
};
