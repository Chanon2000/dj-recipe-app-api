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

    # นี้คือ idea ของ TDD คือ เขียน test เพื่อขับเคลื่อน development (คือเขียน test นำ code)
    # ขั้นตอนคือ
    # 1. Write test for behaviour expected to see in code
    # 2. Test fails (เพราะเรายังไม่ได้เขียน code)
    # 3. Write code so test passes

    def test_subtract_numbers(self):
        """Test subtracting numbers."""
        res = calc.subtract(10, 15)

        self.assertEqual(res, 5) # คือเราคาดหวังจะเห็น 5 เป็น result ของ test