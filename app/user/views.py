"""
Views for the user API.
"""

from rest_framework import generics # เป็น base classes เพื่อให้เรา configure ให้กับ view ของเรา ที่จัดการกับ request
# ในที่นี้เราใช้ generics module
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer, # import serializers ที่เราสร้าง
    AuthTokenSerializer,
)

class CreateUserView(generics.CreateAPIView): # base on CreateAPIView ซึ่งเป็น class ส่วนหนึ่งใน generics
    # CreateAPIView จัดการ POST request เพื่อสร้าง objects ลง database
    # จัดการ logic ให้เราหมดเลย
    """Create a new user in the system."""
    serializer_class = UserSerializer # สิ่งที่เราต้องทำคือกำหนด serializer_class
    # มันรู้ว่าเราจะสร้าง model อะไรจาก UserSerializer แหละ

    # เมื่อเราสร้าง http request มันก็จะไปที่ url ที่เรา map กับ view นี้ แล้วมันจะผ่านเข้า CreateAPIView class ที่จะเรียก UserSerializer แล้วก็สร้าง objects แล้วก็ return response ที่เหมาะสมมาให้

class CreateTokenView(ObtainAuthToken): # drf มี view ที่ช่วยลดงานคุณให้แล้ว ทำให้คุณไม่ต้องเขียน creaeting token เอง นั้นก็คือ ObtainAuthToken
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer # จะสังเกตว่าที่เราต้อง custom serializer โดยเราสร้างเป็น AuthTokenSerializer เพราะว่า ObtainAuthToken ใช้ username and password เราเลยต้อง custom ให้เป็น email, password ใน Serializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES # เป็น option ใส่หรือไม่ใส่ก็ได้
    # ที่เราต้องกำหนดนั้นเป็นเพราะว่า ObtainAuthToken โดย default นั้น view นี้จะไม่แสดงที่ browser ที่เป็น doc ซึ่งติดว่าหน้าจะเป็นissueของ framework ทำให้เราต้องมา override เพื่อให้มันกลับมาแสดง (แต่ APIs ตัวอื่นไม่มีปัญหานี้)