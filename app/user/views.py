"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions # เป็น base classes เพื่อให้เรา configure ให้กับ view ของเรา ที่จัดการกับ request
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

# สร้าง ManageUserView โดย base on RetrieveUpdateAPIView จาก drf ซึ่งช่วยเรื่องของ รับและ update object ลง database
# รับ data ก็คือ http Get
# update จะเป็น PATCH, PUT เพื่อ update value ใน object
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer # ใช้ UserSerializer
    authentication_classes = [authentication.TokenAuthentication] # เป็น list
    # กำหนด authentication classes
    # ทำหน้าที่ประมาณว่า เราจะรู้ได้ไงว่า user นี้คือ user ที่เขายืนยันตัวตนจริงๆ
    permission_classes = [permissions.IsAuthenticated]
    # permission class คือประมาณว่า เรารู้ว่า user คนนั้นเป็นใครแล้ว แต่ user คนนั้นสามารถทำอะไรในระบบเราได้บ้าง
    # ในที่นี้ใน list value ใน permission class มีแค่ IsAuthenticated นั้นหมายความว่าจะเข้า api เส้นนี้ได้ user ต้อง authenticated แล้วก่อน

    # เข้าเมื่อมี GET http เข้า api
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
        # return ข้อมูล user ของคนที่ authenticated นี้แหละ จากนั้นมันก็จะเข้า serializer class ก่อน แล้วถึงจะ return response ของ api ออกไป