"""
Database models.
"""
import uuid
import os # import os เพราะเราต้องการ some file path management functions

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# จะเป็น func ที่เราเอาไว้ generate path
def recipe_image_file_path(instance, filename):
    # instance ของ object ที่ image จะทำการ uploaded เข้าไป
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1] # เพื่อเอา filename และแยกเอาพวก extension ออกจาก filename นั้น (พวก ext ที่จะเก็บตรงนี้ก็ตือเช่น png jpeg แล้วแต่ว่าเราจะ upload file type ใหน)
    filename = f'{uuid.uuid4()}{ext}' # สร้าง ชื่อ file ใหม่ โดยใช้ uuid แล้วเติม ext ต่อท้าย

    return os.path.join('uploads', 'recipe', filename) # สร้าง path โดยใส่ 3 value
    # เราทำแบบนี้แทนการใส่ string ไปเลยแทน เพื่อให้มั้นใจว่ามันจะสร้าง string ให้เหมาะกับ format ของ operating system ที่เรารัน code นี้ (window, mac, linux)

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    # null=True คือมันสามารถเป็น null ได้
    # เรากำหนด function ที่สามารถ generate path name โดยขึ้นกับ information ที่เราใส่เข้าไป
    # upload_to=recipe_image_file_path คือใส่ ref ไปที่ function เนื่องจากเราไม่ได้จะทำการเรียน func เลยไม่ใส่ ()



    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name