"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer): # เราจะใช้ ModelSerializer เพื่อให้มัน serializer ข้อมูลใน model ที่กำหนด
    """Serializer for recipes."""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id'] # เพื่อไม่ให้ id field ถูกเปลี่ยนได้

# เอา RecipeSerializer มาเพิ่ม fields
class RecipeDetailSerializer(RecipeSerializer): # extend จาก RecipeSerializer เพราะ detail serialize จะเห็นเหมือน extension ของ RecipeSerializer
    # สิ่งที่เราทำคือเอาทุก function จาก RecipeSerializer มา แล้วเพิ่มบาง field ที่เราต้องการเข้าไป
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta): # เอา Meta จากที่ inherit มามาใส่ตรงนี้
        fields = RecipeSerializer.Meta.fields + ['description'] # เอา inherit Meta fields มาใส่ แล้วเติม description field เข้าไปแค่นั้น