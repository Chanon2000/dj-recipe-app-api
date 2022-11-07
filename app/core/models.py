"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

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


class Recipe(models.Model): # ใช้ Model เป็น base class ซึ่งเป็น model base class ทั่วไป
    """Recipe object."""
    user = models.ForeignKey( # เป็น field ที่กำหนด user ที่เป็นเจ้าของ Recipe นี้
        settings.AUTH_USER_MODEL, # คือ กำหนดเป็น User model นั้นแหละ เพราะว่าคุณกำหนด core.User ที่ AUTH_USER_MODEL ใน settings.py
        # เราเอามาแจก setting แทนการกำหนด User ด้วยเหตุผลเดียวกับการใช้ get_user_model นั้นคือ ถ้าเปลี่ยน custom user model ทุกทีก็จะเปลี่ยนตามให้เรา (คือเลี่ยงการ hard code)
        on_delete=models.CASCADE,
        # คือถ้า object ที่ relate บถูก delete นั้นที่ recipe นั้นๆก็จะถูก delete ด้วย
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True) # TextField นั้นถูกออกแบบมาให้เก็บ content เยอะๆ แบบหลายๆบรรทัด
    # ถ้าใน mysql TextField นั้นจะโหลดช้ากว่า CharField
    # Django เป็น database agnostic software คือมันไม่สนว่าคุณจะใช้ database engine อะไร คุณสามารถใช้ได้หมด
    time_minutes = models.IntegerField() # เก็บเวลาเป็น นาที
    price = models.DecimalField(max_digits=5, decimal_places=2) # decimal_places กำหนดจำนวนตำแหน่งทศนิยม
    link = models.CharField(max_length=255, blank=True) # เก็บ link url

    def __str__(self):
        return self.title
