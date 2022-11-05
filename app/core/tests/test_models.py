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

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        # เพื่อให้มั้นใจว่า ทุก email เรา normalized แล้วก่อนที่จะเข้า database
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'], # email, expected
            ['Test2@Example.com', 'Test2@example.com'], # capitalization in first part (เช่น Test2)ของ email จะ unique ซึ่งเป็น main standard ของทุก email providers
            # first part ก็สามารถมีตัวพิมพ์ใหญ่ได้ แต่ last part (example.com) จะห้ามมี capitalization เราต้องการให้เป็น lowercase เสมอ
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails: # เป็น python syntax ที่จะ loop list ที่มี sub element เป็น list ที่มี 2 item
            # ซึ่งมันก็จะ assign value ที่ email, expected ให้ตามลำดับ
            user = get_user_model().objects.create_user(email, 'sample123') # 'sample123' คือใส่เป็น password mock ไว้เฉยๆ
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError): # เพราะเราจะ raises value error ถ้ามันได้ incorrect value email
            get_user_model().objects.create_user('', 'test123')

