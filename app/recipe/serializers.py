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