/**
 * 🧪 تنظیمات اولیه برای تست‌های Jest
 */

// تنظیم متغیرهای محیطی تست
process.env.NODE_ENV = 'test';
process.env.TEST_DATABASE_URL = 'sqlite://:memory:';
process.env.SECRET_KEY = 'test-secret-key';
process.env.DEBUG = 'false';

// تنظیم timeout برای تست‌ها
jest.setTimeout(30000);

// Mock console برای تست‌ها
global.console = {
    ...console,
    // غیرفعال کردن console.log در تست‌ها (اختیاری)
    // log: jest.fn(),
    // debug: jest.fn(),
    // info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
};

// Mock modules
jest.mock('puppeteer', () => ({
    launch: jest.fn(() => Promise.resolve({
        newPage: jest.fn(() => Promise.resolve({
            goto: jest.fn(() => Promise.resolve()),
            evaluate: jest.fn(() => Promise.resolve()),
            screenshot: jest.fn(() => Promise.resolve(Buffer.from('fake-image'))),
            close: jest.fn(() => Promise.resolve())
        })),
        close: jest.fn(() => Promise.resolve())
    }))
}));

// Mock fs برای تست‌ها
jest.mock('fs', () => {
    const actualFs = jest.requireActual('fs');
    return {
        ...actualFs,
        promises: {
            ...actualFs.promises,
            writeFile: jest.fn(() => Promise.resolve()),
            readFile: jest.fn(() => Promise.resolve('mock content')),
            mkdir: jest.fn(() => Promise.resolve()),
            rmdir: jest.fn(() => Promise.resolve()),
            unlink: jest.fn(() => Promise.resolve())
        }
    };
});

// Mock path
jest.mock('path', () => {
    const actualPath = jest.requireActual('path');
    return {
        ...actualPath,
        join: jest.fn((...args) => args.join('/')),
        resolve: jest.fn((...args) => args.join('/'))
    };
});

// Mock axios
jest.mock('axios', () => ({
    get: jest.fn(() => Promise.resolve({
        data: { success: true },
        status: 200,
        statusText: 'OK'
    })),
    post: jest.fn(() => Promise.resolve({
        data: { success: true },
        status: 200,
        statusText: 'OK'
    }))
}));

// Mock cheerio
jest.mock('cheerio', () => ({
    load: jest.fn(() => ({
        html: jest.fn(() => '<html>mock</html>'),
        text: jest.fn(() => 'mock text'),
        find: jest.fn(() => ({
            each: jest.fn(),
            attr: jest.fn(() => 'mock-attr'),
            text: jest.fn(() => 'mock-text')
        }))
    }))
}));

// تنظیمات قبل از هر تست
beforeEach(() => {
    // پاک کردن تمام mock ها
    jest.clearAllMocks();

    // تنظیم console
    console.log('🧪 شروع تست جدید...');
});

// تنظیمات بعد از هر تست
afterEach(() => {
    // پاکسازی
    console.log('✅ تست تمام شد');
});

// تنظیمات قبل از تمام تست‌ها
beforeAll(() => {
    console.log('🚀 شروع تست‌های PEY Builder...');
});

// تنظیمات بعد از تمام تست‌ها
afterAll(() => {
    console.log('🎉 تمام تست‌ها تمام شدند!');
});

// تابع کمکی برای ایجاد mock data
global.createMockData = {
    website: () => ({
        id: 'test-website-1',
        name: 'سایت تست',
        domain: 'testsite.com',
        description: 'توضیحات تست',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
    }),

    template: () => ({
        id: 'test-template-1',
        name: 'قالب تست',
        category: 'business',
        html: '<html><body>Test</body></html>',
        css: 'body { margin: 0; }',
        js: 'console.log("test");'
    }),

    user: () => ({
        id: 'test-user-1',
        username: 'testuser',
        email: 'test@example.com',
        role: 'user',
        created_at: new Date().toISOString()
    })
};

// تابع کمکی برای انتظار
global.waitFor = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// تابع کمکی برای ایجاد فایل موقت
global.createTempFile = (content = 'test content') => {
    const fs = require('fs');
    const path = require('path');
    const tempDir = require('os').tmpdir();
    const tempFile = path.join(tempDir, `test-${Date.now()}.txt`);

    fs.writeFileSync(tempFile, content);
    return tempFile;
};

// تابع کمکی برای حذف فایل موقت
global.cleanupTempFile = (filePath) => {
    const fs = require('fs');
    if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
    }
};

// تنظیمات error handling
process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
});

// Export برای استفاده در تست‌ها
module.exports = {
    setupTests: true
};
