"""
Tests for models.
"""
from unittest.mock import patch # ทำให้สามารถ mock สิ่งต่างๆ ตามที่ test นั้นๆต้องการ
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)


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

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample receipe description.',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4') # เราใส่ decorator คือ patch เพื่อ patch uuid function
    # โดย func นี้หลักๆ คือ generate a random string
    # ซึ่งใน test นี้เราจะไม่ generate uuid จริงๆ เพราะมันจะดูยากเกินไปว่า uuid เราจะชื่ออะไรใน test  เราเลยจะ mock เอา
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path.""" # test การสร้าง path ไปที่ image
        # เราจะสร้าง path โดยใช้ unique identifier (uuid) เพื่อให้มั้นใจว่าแต่ละ file จะมี unique name ในแต่ละ files ที่ upload
        uuid = 'test-uuid' # นี้แหละ mock uuid
        mock_uuid.return_value = uuid # mock uuid return_value
        file_path = models.recipe_image_file_path(None, 'example.jpg')
        # เป็น func ที่เราจะทำการ test ซึ่งคือ func ที่จะสร้าง path ไปที่ path ที่จะ uploaded image
        # 'example.jpg' คือใส่ original name ของ file นั้น ก่อน upload
        # เราใช้ uuid ใน func นี้ เราเลย  @patch('core.models.uuid.uuid4')
        # None คือแทน Django ImageField

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg') # check path ที่ generate