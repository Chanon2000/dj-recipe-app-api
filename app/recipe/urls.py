"""
URL mappings for the recipe app.
"""
from django.urls import (
    path, # ใช้เพื่อกำหนด path นั้นแหละ
    include,
)

from rest_framework.routers import DefaultRouter # เราจะสร้าง route โดยใช้ DefaultRouter
# DefaultRouter มาจาก drf โดยสามารถใช้มันใน API view เพื่อ auto สร้าง routes

from recipe import views

router = DefaultRouter() # สร้าง router จาก DefaultRouter
router.register('recipes', views.RecipeViewSet) # แล้วทำการ register RecipeViewSet ลง router โดยใช้ชื่อว่า recipes เป็นชื่อ endpoint (/recipes) และเนื่องจาก RecipeViewSet เรา inherit มาจาก ModelViewSet ทำให้มันสร้างหลาย endpoint เพื่อจัดการ actions ต่างๆที่ ModelViewSet เตรียมมาให้ (CRUD ซึ่งก็แยกเป็น Method ต่างๆได้แค่ get, post, put, patch and delete)

app_name = 'recipe' # คือ name ที่เราจะใช้เอาไว้ identify กับ urls นี้ บน reverse method

urlpatterns = [
    path('', include(router.urls)), # เพื่อ include urls ต่างๆที่ generated auto โดย router
    # นี้แหละคือหน้าที่ของ DefaultRouter คือมันสร้าง urls ให้เราจากการที่เรา register เข้าไป
]