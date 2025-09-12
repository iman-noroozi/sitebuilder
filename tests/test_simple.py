#!/usr/bin/env python3
"""
🧪 تست‌های ساده برای اطمینان از کارکرد CI/CD
"""

import unittest
import sys
import os

class TestSimpleFunctionality(unittest.TestCase):
    """تست‌های ساده برای اطمینان از کارکرد"""

    def test_basic_math(self):
        """تست ریاضی پایه"""
        self.assertEqual(2 + 2, 4)
        self.assertEqual(10 - 5, 5)
        self.assertEqual(3 * 3, 9)
        self.assertEqual(8 / 2, 4)

    def test_string_operations(self):
        """تست عملیات رشته"""
        test_string = "PEY Builder"
        self.assertEqual(len(test_string), 11)
        self.assertIn("PEY", test_string)
        self.assertIn("Builder", test_string)

    def test_list_operations(self):
        """تست عملیات لیست"""
        test_list = [1, 2, 3, 4, 5]
        self.assertEqual(len(test_list), 5)
        self.assertIn(3, test_list)
        self.assertEqual(sum(test_list), 15)

    def test_dictionary_operations(self):
        """تست عملیات دیکشنری"""
        test_dict = {
            'name': 'PEY Builder',
            'version': '1.0.0',
            'language': 'Python'
        }
        self.assertIn('name', test_dict)
        self.assertEqual(test_dict['name'], 'PEY Builder')
        self.assertEqual(len(test_dict), 3)

    def test_boolean_operations(self):
        """تست عملیات بولین"""
        self.assertTrue(True)
        self.assertFalse(False)
        self.assertTrue(1 == 1)
        self.assertFalse(1 == 2)

    def test_none_handling(self):
        """تست مدیریت None"""
        self.assertIsNone(None)
        self.assertIsNotNone("not none")
        self.assertIsNotNone(42)
        self.assertIsNotNone([])

if __name__ == '__main__':
    # راه‌اندازی تست‌ها
    unittest.main(verbosity=2)
