"""
Tests for models.
"""

from django.test import TestCase # จะเป็น base class for tests
from django.contrib.auth import get_user_model # เป็น helper function จาก django เพื่อ get default user model ทำให้คุณสามารถอ้างถึง model จาก models.py ได้ด้วย
# ใช้ get_user_model() เพื่อรับ custom user model (เมื่อเราใช้ django user model)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with is successful."""
        email = 'test@example.com' # แนะนำให้ลงด้วย example.com เพราะว่าเป็น domain name ที่มีไว้เพื่อสำหรับ testing (เพื่อไม่ให้บังเอินส่ง email จริงๆ)
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        # ได้ model object จากการเรียก get_user_model()
        # .objects เพื่ออ้างถึง manager ที่เราจะสร้าง
        # create_user เรียก create_user เพื่อสร้าง user

        self.assertEqual(user.email, email) # check ว่า email ที่เก็บลง user ตรงกับ email ที่ใส่มามั้ย
        self.assertTrue(user.check_password(password)) # check password ว่าถูกต้องตามที่กรอกมามั้ย ใช้ check_password() เพราะเป็นการ check ผ่าน hashing system นะ
        # check_password เป็น method ที่มีมาให้ใน default model manager (base user manager) ที่เข้า add เข้า project