# file tests.py จะสร้าง auto เมื่อเราสร้าง app ใน Project
"""
Sample tests
"""
from django.test import SimpleTestCase # import test class ที่จะใช้

from app import calc # impot module ที่ต้องการ test


class CalcTests(SimpleTestCase):
    """Test the calc module."""

    def test_add_numbers(self):
        """Test adding numbers together."""
        res = calc.add(5, 6)
        
        self.assertEqual(res, 11) # เพื่อ check ouput