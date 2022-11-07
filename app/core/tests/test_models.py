"""
Tests for models.
"""
from decimal import Decimal # เป็น class ที่มาจาก Django

from django.test import TestCase
from django.contrib.auth import get_user_model # ที่เราใช้ get_user_model แทน models นั้นเป็นเพราะว่า ถ้าเราเปลี่ยน custom user model เป็น Model อื่น ทุกที่จะเปลี่ยนตามเพราะเราใช้ get_user_model ดึงมาอีกที

from core import models # ก่อนหน้านี้เราใช้ user models จาก get_user_model เราเลยพึงมา import models ตอนนี้

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self): # test การสร้าง recipe ที่ success
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user( # เพราะเราจะใช้ user นี้ให้การ assign recipe ใหม่
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5, # เวลาในการทำอาหาร
            price=Decimal('5.50'), # ถ้าคุณทำพวก real finance application แนะนำให้เก็บพวก currency พวกนี้เป็น integer value แทนการใช้ decimal
            # เราใส่ decimal ตรงนี้เพราะว่าเราแค่จะเอามันไปแสดงเฉยๆ
            # ไม่แนะนำให้ใช้ทั้ง decimal or a float field เพื่อเก็บ prices ใช้ integer ดีกว่า เพราะมันจะทำให้ values ที่เก็บแม่นยำมากขึ้น เพราะถ้าเป็น decimal, float จะมีปัญหาเรื่องการปัดเศษ ขึ้นลง ซึ่งนั้นทำให้ค่าผิดจนเกิดปัญหา
            # เนื่องจาก app เราไม่ได้จะคำนวณอะไรมากขนาดนั้น ดังนั้นเพื่อดึงเอามาแสดงง่ายๆเลยใช้ Decimal
            description='Sample receipe description.',
        )

        self.assertEqual(str(recipe), recipe.title) # check string title ที่จะเอาไปแสดงว่าถูกต้องมั้ย
        # เดี๋ยวเราจะเขียน string ที่แสดงของ models นั้นๆ ซึ่งเราจะเอา title มาแสดง ซึ่ง str(recipe) ก็จะได้ title string นั้นมา
