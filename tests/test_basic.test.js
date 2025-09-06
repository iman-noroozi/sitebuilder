/**
 * 🧪 تست‌های پایه JavaScript
 */

const fs = require('fs');
const path = require('path');

describe('Basic Functionality Tests', () => {
    let tempDir;

    beforeAll(() => {
        // ایجاد دایرکتوری موقت
        tempDir = fs.mkdtempSync('/tmp/test-');
    });

    afterAll(() => {
        // پاکسازی دایرکتوری موقت
        if (fs.existsSync(tempDir)) {
            fs.rmSync(tempDir, { recursive: true, force: true });
        }
    });

    test('should validate project structure', () => {
        const projectRoot = path.join(__dirname, '..');
        
        const requiredFiles = [
            'package.json',
            'README.md',
            'Dockerfile',
            'docker-compose.yml'
        ];

        requiredFiles.forEach(fileName => {
            const filePath = path.join(projectRoot, fileName);
            expect(fs.existsSync(filePath)).toBe(true);
        });
    });

    test('should validate directory structure', () => {
        const projectRoot = path.join(__dirname, '..');
        
        const requiredDirs = [
            'backend',
            'extractor',
            'frontend',
            'tests'
        ];

        requiredDirs.forEach(dirName => {
            const dirPath = path.join(projectRoot, dirName);
            const stats = fs.statSync(dirPath);
            expect(stats.isDirectory()).toBe(true);
        });
    });

    test('should validate URL format', () => {
        const isValidUrl = (url) => {
            if (!url) return false;
            return url.startsWith('http://') || url.startsWith('https://');
        };

        // تست URL های معتبر
        const validUrls = [
            'https://example.com',
            'http://example.com',
            'https://www.example.com/path'
        ];

        validUrls.forEach(url => {
            expect(isValidUrl(url)).toBe(true);
        });

        // تست URL های نامعتبر
        const invalidUrls = [
            'not-a-url',
            'ftp://example.com',
            '',
            null,
            undefined
        ];

        invalidUrls.forEach(url => {
            expect(isValidUrl(url)).toBe(false);
        });
    });

    test('should handle file operations', () => {
        const testFile = path.join(tempDir, 'test.txt');
        const testContent = 'تست محتوای فارسی';

        // نوشتن فایل
        fs.writeFileSync(testFile, testContent, 'utf8');

        // بررسی وجود فایل
        expect(fs.existsSync(testFile)).toBe(true);

        // خواندن فایل
        const content = fs.readFileSync(testFile, 'utf8');
        expect(content).toBe(testContent);
    });

    test('should handle JSON operations', () => {
        const testData = {
            name: 'تست',
            version: '1.0.0',
            features: ['استخراج', 'ساخت', 'ویرایش']
        };

        const jsonFile = path.join(tempDir, 'test.json');

        // نوشتن JSON
        fs.writeFileSync(jsonFile, JSON.stringify(testData, null, 2), 'utf8');

        // خواندن JSON
        const loadedData = JSON.parse(fs.readFileSync(jsonFile, 'utf8'));
        expect(loadedData).toEqual(testData);
    });

    test('should validate package.json', () => {
        const packageJsonPath = path.join(__dirname, '..', 'package.json');
        const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));

        // بررسی فیلدهای ضروری
        expect(packageJson.name).toBeDefined();
        expect(packageJson.version).toBeDefined();
        expect(packageJson.description).toBeDefined();
        expect(packageJson.scripts).toBeDefined();
        expect(packageJson.dependencies).toBeDefined();
    });

    test('should validate extractor module', () => {
        const extractorPath = path.join(__dirname, '..', 'extractor', 'puppeteer.js');
        
        // بررسی وجود فایل extractor
        expect(fs.existsSync(extractorPath)).toBe(true);

        // بررسی محتوای فایل
        const content = fs.readFileSync(extractorPath, 'utf8');
        expect(content).toContain('TemplateExtractor');
        expect(content).toContain('class');
    });
});

describe('TemplateExtractor Tests', () => {
    test('should create TemplateExtractor instance', () => {
        const TemplateExtractor = require('../extractor/puppeteer.js');
        
        const extractor = new TemplateExtractor({
            headless: true,
            timeout: 30000
        });

        expect(extractor).toBeDefined();
        expect(extractor.options).toBeDefined();
        expect(extractor.options.headless).toBe(true);
        expect(extractor.options.timeout).toBe(30000);
    });

    test('should have required methods', () => {
        const TemplateExtractor = require('../extractor/puppeteer.js');
        const extractor = new TemplateExtractor();

        expect(typeof extractor.init).toBe('function');
        expect(typeof extractor.extractTemplate).toBe('function');
        expect(typeof extractor.close).toBe('function');
    });
});
