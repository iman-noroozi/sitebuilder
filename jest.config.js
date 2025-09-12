/**
 * 🧪 تنظیمات Jest برای PEY Builder
 */

module.exports = {
    // محیط تست
    testEnvironment: 'node',

    // مسیرهای تست
    testMatch: [
        '**/tests/**/*.test.js',
        '**/tests/**/*.spec.js',
        '**/test/**/*.test.js',
        '**/test/**/*.spec.js'
    ],

    // مسیرهای نادیده گرفته شده
    testPathIgnorePatterns: [
        '/node_modules/',
        '/dist/',
        '/build/',
        '/coverage/'
    ],

    // پوشش کد
    collectCoverage: false,

    // تنظیمات timeout
    testTimeout: 30000,

    // تنظیمات verbose
    verbose: true,

    // تنظیمات setup
    setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],

    // تنظیمات module
    moduleFileExtensions: ['js', 'json', 'node'],

    // تنظیمات transform
    transform: {
        '^.+\\.js$': 'babel-jest'
    },

    // تنظیمات globals
    globals: {
        'process.env.NODE_ENV': 'test'
    },

    // تنظیمات reporters
    reporters: ['default'],

    // تنظیمات watch
    watchman: false,

    // تنظیمات clearMocks
    clearMocks: true,
    restoreMocks: true,

    // تنظیمات errorOnDeprecated
    errorOnDeprecated: true
};
