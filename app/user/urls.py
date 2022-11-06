"""
URL mappings for the user API.
"""
from django.urls import path

from user import views

app_name = 'user' # app_name จะถูกใช้ที่ reverse func เช่นที่ test_user_api.py เป็นต้น
# CREATE_USER_URL = reverse('user:create') คือ user ตรงนี้นี่แหละ ที่อยู่ที่ test_user_api.py file

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    # create/ url ก็จะถูกจัดการโดย CreateUserView view ซึ่งเนื่องจาก Django ต้องการให้เราใส่เป็น function ลง parameter นี้ เราเลยต้องใส่ .as_view() หลัง class เพื่อให้ class เป็น view func
    # .as_view() คือวิธีการที่ Django rest framework แปลง Class base view เป็น Django view
    path('token/', views.CreateTokenView.as_view(), name='token'), # สร้าง url ให้ token (หรือจะเรียกว่า enable token API)
]