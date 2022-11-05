# ลบ code ที่มีอยู่เป็น default ทั้งหมด เพื่อจะได้ให้ file ว่างๆ แล้วเริ่มเขียนสิ่งที่ตัวเองต้องการ
"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create user model manager (คือหนึ่งใน Django model manager)
class UserManager(BaseUserManager):
    """Manager for users."""

    # สร้าง create_user method
    def create_user(self, email, password=None, **extra_fields): # โดย **extra_field คือ field อื่นๆที่เหลือที่อาจจะใส่เข้ามาที่ create_user ตอนเรียก
        # เรียกว่า keyword arguments (ให้งานได้ดีเมื่อคุณใส่ extra field เพื่อทำให้การสร้าง user ยืดหยุ่มมากขึ้น) โดยมันจะใส่ทุก value เข้ามาในนี้หลังจาก args อื่นรับ value เสร็จ
        """Create, save and return a new user."""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # normalize_email เป็น method ที่มาจาก BaseUserManager ที่จะทำให้ email คุณ normalize
        # self.model คือเราต้องการสื่อสารกับ model ที่เกี่ยวข้องกับ manager นี้ (นั้นก็คือ user model) # โดยก็จะทำคล้ายๆกับการที่คุณ new object User model (เช่น get_user_model().objects)
        user.set_password(password) # เนื่องจากระบบนี้สามารถสร้าง user ที่ไม่มี password ได้ เลยใส่ password=None ซึ่ง user นั้นก็จะไม่ถูก set_password ตรงนี้
        # set_password จะทำการ set encrypted password (ถ้าเข้าไปดู database จะเห็นเป็น test ที่อ่านไม่รู้เรื่อง)
        user.save(using=self._db) # using=self._db เพื่อให้มัน support adding multiple databases ถ้สคุณต้องการเลือกที่จะเพิ่ม multiple databases ใน project

        return user # return user object ที่พึ่งสร้าง


# ใส่ base class หลายอัน
class User(AbstractBaseUser, PermissionsMixin):
    # AbstractBaseUser จะมี func สำหรับ authentication system แต่ไม่มี field
    # PermissionsMixin จะมี func สำหรับ Permissions feature ของ django และ fields (ที่จำเป็นสำหรับ permissions feature)
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # เอาไว้บอกว่า user คนไหนที่สามารถเข้าไป login ที่ Django admin ได้บ้าง

    objects = UserManager() # ทำการกำหนด manager ให้กับ custom user class นี้

    USERNAME_FIELD = 'email' # เพื่อกำหนดให้ email field เป็น field ที่เอาไว้ authtication (ถ้าไม่กำหนด default จะเป็น username ซึ่งกำหนดโดย default user model ที่คุณเข้ามาเป็น base)


