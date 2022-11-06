"""
Views for the user API.
"""

from rest_framework import generics # เป็น base classes เพื่อให้เรา configure ให้กับ view ของเรา ที่จัดการกับ request
# ในที่นี้เราใช้ generics module

from user.serializers import UserSerializer # import serializers ที่เราสร้าง

class CreateUserView(generics.CreateAPIView): # base on CreateAPIView ซึ่งเป็น class ส่วนหนึ่งใน generics
    # CreateAPIView จัดการ POST request เพื่อสร้าง objects ลง database
    # จัดการ logic ให้เราหมดเลย
    """Create a new user in the system."""
    serializer_class = UserSerializer # สิ่งที่เราต้องทำคือกำหนด serializer_class
    # มันรู้ว่าเราจะสร้าง model อะไรจาก UserSerializer แหละ

    # เมื่อเราสร้าง http request มันก็จะไปที่ url ที่เรา map กับ view นี้ แล้วมันจะผ่านเข้า CreateAPIView class ที่จะเรียก UserSerializer แล้วก็สร้าง objects แล้วก็ return response ที่เหมาะสมมาให้