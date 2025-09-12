/**
 * 🧪 تست‌های ساده برای اطمینان از کارکرد CI/CD
 */

describe('Simple Functionality Tests', () => {
    test('basic math operations', () => {
        expect(2 + 2).toBe(4);
        expect(10 - 5).toBe(5);
        expect(3 * 3).toBe(9);
        expect(8 / 2).toBe(4);
    });

    test('string operations', () => {
        const testString = 'PEY Builder';
        expect(testString.length).toBe(11);
        expect(testString).toContain('PEY');
        expect(testString).toContain('Builder');
    });

    test('array operations', () => {
        const testArray = [1, 2, 3, 4, 5];
        expect(testArray.length).toBe(5);
        expect(testArray).toContain(3);
        expect(testArray.reduce((sum, num) => sum + num, 0)).toBe(15);
    });

    test('object operations', () => {
        const testObject = {
            name: 'PEY Builder',
            version: '1.0.0',
            language: 'JavaScript'
        };
        expect(testObject).toHaveProperty('name');
        expect(testObject.name).toBe('PEY Builder');
        expect(Object.keys(testObject).length).toBe(3);
    });

    test('boolean operations', () => {
        expect(true).toBe(true);
        expect(false).toBe(false);
        expect(1 === 1).toBe(true);
        expect(1 === 2).toBe(false);
    });

    test('null and undefined handling', () => {
        expect(null).toBeNull();
        expect(undefined).toBeUndefined();
        expect('not null').not.toBeNull();
        expect(42).not.toBeUndefined();
    });

    test('async operations', async () => {
        const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

        const startTime = Date.now();
        await delay(10);
        const endTime = Date.now();

        expect(endTime - startTime).toBeGreaterThanOrEqual(10);
    });
});
