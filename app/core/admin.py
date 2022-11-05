"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # เรียก UserAdmin ว่า BaseUserAdmin เพราะมันง่ายกว่าในการเรียก ทำให้ไม่งง
# UserAdmin เป็น class ที่มาจาก Django
from django.utils.translation import gettext_lazy as _ # ที่ไหนที่คุณใช้ _ (translation shortcut) มันจะ automatically translate the text
# ซึ่ง _ เป็น standard ที่ Django อยากให้เราใช้ด้วยนะ
# เนื่องจาก gettext_lazy มันร่วมกับ Django translation system ด้วย
# โดยการทำงานของมันคือ จะทำให้ เมื่อเช่นคุณเปลี่ยนภาษาใน Django settings.py ทุกที่ที่คุณใส่ _ มันก็จะ translate เปลี่ยนภาษาให้คุณด้วยเลย แต่ถ้าคุณไม่เปลี่ยน settings อะไร มันก็จะไม่ translate อะไร

from core import models # import models ใน core app มา

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id'] # ถ้าพิมพ์ key ผิดจาก ordering เป็น order มันก็จะใช้ default ordering ทันที
    list_display = ['email', 'name'] # แสดง field ตามนี้
    # จาก error ที่มันพลายามจะแสดง field ที่อยู่ใน default user model ของ django ซึ่งบาง field นั้น custom user model ของเรามันไม่มี เราเลยต้อง override fieldsets ให้แสดงแค่ field ที่เรามี
    fieldsets = (
        # None คือจะไม่ใส่ title
        # โดยมี 2 field คือ 'email', 'password'
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'), # _ ก็คือจะเรียก gettext_lazy นั้นแหละ
            # ตรงนี้จะเป็น Permissions section ที่จะเป็นอีก section ใน page
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        # Important dates section ที่มี last_login fields แสดงอยู่
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login'] # ทำให้แก้ไม่ได้
    add_fieldsets = (
        # section ที่ไม่มี title
        (None, {
            'classes': ('wide',), # คล้ายๆกับ ใส่ css ให้ admin panel (ไม่ได้มีอะไรมาก)
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }), # อย่าลืม ใส่ , ตรงนี้ด้วย เพราะนี้เป็น tuple
    )

admin.site.register(models.User, UserAdmin) # เพื่อบอกให้ใช้ UserAdmin ใน models.User (ถ้าไม่บอกมันก็จะใช้ default)