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
    serializer_class = serializers.RecipeDetailSerializer # เปลี่ยนเป็น detail ได้เลย เพราะ detail มัน inherit อันเก่ามาทำให้ไม่ได้เสียความสามารถอะไร
    # เอา detail มาใส่ตรงนี้เลยเพราะว่าเดี๋ยว actions ที่เราจะใช้กันส่วนใหญ่จะอยู่ใน RecipeDetailSerializer ทั้งการ create, update, delete (เพราะมันมี descripion field ด้วย)
    queryset = Recipe.objects.all() # คือคล้ายกับการบอกว่า model ใหนนั้นแหละ
    # บอกว่า นี้คือ queryset ที่เราจะจัดการผ่าน APIs
    authentication_classes = [TokenAuthentication] # ใช้ TokenAuthentication ในการบอกว่า user นั้นๆ ที่ยิงเข้ามาเป็นใคร
    permission_classes = [IsAuthenticated] # user ต้อง IsAuthenticated ถูกจะเข้ามาได้

    def get_queryset(self): # ทำการ override get_queryset method (เป็น method ที่จะถูกเรียกตอนที่ get objects จาก queryset ที่กำหนดที่ property ของ class นั้นแหละ)
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id') # เพื่อให้ recipes ถูกดึงมาเฉพาะ user ที่ auth แล้วเท่านั้น
        # แล้ว order เพื่อให้ recipe อันล่าสุดอยู่บนๆ
        # self.queryset.filter => จะเห็นว่าเรา filter จาก queryset เลย

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list': # มีแค่ list action ที่ต้องใช้ RecipeSerializer
            return serializers.RecipeSerializer # เมื่อ action เป็น list จะ return RecipeSerializer
            # เราจะไม่เรียก constructor ของ RecipeSerializer ซึ่งก็คือการเขียน serializers.RecipeSerializer() เราแค่ return ref แบบนี้แล้ว drf จะจัดการต่อเอง

        return self.serializer_class

    # เป็น method ใน viewsets
    # override drf เมื่อ save model ที่ view
    def perform_create(self, serializer):
        """Create a new recipe."""
        # เราทำการ override เมื่อมันสร้าง recipe ใหม่ขึ้นมา เราจะเรียก method นี้เป็นส่วนหนึ่ง objects creation และรับ 1 parameter คือ serializer (เราเดาได้เลยว่า data ถูก validated โดย serializer ของมันแล้วก่อนที่จะเรียก method นี้)
        serializer.save(user=self.request.user) # และเมื่อ method นี้ถูกเรียกเราก็จะทำการ save โดยกำหนด user field เป็น user ที่ current authenticated