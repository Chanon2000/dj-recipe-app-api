"""
Views for the recipe APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet): # ModelViewSet คือ viewsets ที่เราจะใช้ (ซึ่งมันมี class อื่นมากมายให้ใช้)
    # ModelViewSet จะ setup ให้เราทำงานตรงๆกับ model (ทำให้เราไม่ต้องเขียน crud เอง)
    """View for manage recipe APIs.""" # APIs เติม s เลย เพื่อ View นี้จาก generate มาหลาย endpoints ได้แก่เช่น list endpoint, ID endpoint(detail endpoint) และจัดการกลาย methods เป็น actions ต่างๆ บน recipes ให้กับเรา
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all() # คือคล้ายกับการบอกว่า model ใหนนั้นแหละ
    # บอกว่า นี้คือ queryset ที่เราจะจัดการผ่าน APIs
    authentication_classes = [TokenAuthentication] # ใช้ TokenAuthentication ในการบอกว่า user นั้นๆ ที่ยิงเข้ามาเป็นใคร
    permission_classes = [IsAuthenticated] # user ต้อง IsAuthenticated ถูกจะเข้ามาได้

    def get_queryset(self): # ทำการ override get_queryset method (เป็น method ที่จะถูกเรียกตอนที่ get objects จาก queryset ที่กำหนดที่ property ของ class นั้นแหละ)
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id') # เพื่อให้ recipes ถูกดึงมาเฉพาะ user ที่ auth แล้วเท่านั้น
        # แล้ว order เพื่อให้ recipe อันล่าสุดอยู่บนๆ
        # self.queryset.filter => จะเห็นว่าเรา filter จาก queryset เลย
