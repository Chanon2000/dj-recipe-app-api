"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # เรียก UserAdmin ว่า BaseUserAdmin เพราะมันง่ายกว่าในการเรียก ทำให้ไม่งง
# UserAdmin เป็น class ที่มาจาก Django
from core import models # import models ใน core app มา

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id'] # ถ้าพิมพ์ key ผิดจาก ordering เป็น order มันก็จะใช้ default ordering ทันที
    list_display = ['email', 'name'] # แสดง field ตามนี้

admin.site.register(models.User, UserAdmin) # เพื่อบอกให้ใช้ UserAdmin ใน models.User (ถ้าไม่บอกมันก็จะใช้ default)