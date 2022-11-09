"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
)


# เนื่องจากเราจะทำหนด TagSerializer เป็น nested Serializer ของ RecipeSerializer เราเลยต้องกำหนดมันไว้ข้างบน RecipeSerializer (เพราะถาไม่ทำมันจะไม่รู้จัก TagSerializer แล้ว error)
class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)
    # many=True คือสามารถมี tag ได้มากกว่า 1 (หรือบอกว่าตรงนี้จะเป็น list ของ item)
    # required=False คือ tags field ไม่จำเป็นต้องใส่

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags'] # เติม tags field ด้วย
        read_only_fields = ['id']

    # เนื่องจากโดย default แล้ว tags จะกลายเป็น read-only field เราเลยทำการ custom logic create method (override)
    def create(self, validated_data): # validated_data เพราะ data ถูก validate ก่อนจะมาเข้า method นี้
        """Create a recipe."""
        tags = validated_data.pop('tags', []) # .get จะดึง value ขึ้นมาเฉยๆ แต่ถ้า .pop จะถึง value ขึ้นมาแล้วเอา tags key ออกจาก validated_data object เลย
        # .pop(keyname, defaultvalue) defaultvalue คือ value ที่จะ return เมื่อ key นั้นไม่มีใน validated_data
        recipe = Recipe.objects.create(**validated_data) # ตรงนี้คือเหตุผลที่เรา pop ก่อนหน้านี้ เพราะมันจะสนแค่ value จาก Recipe model (นั้นก็คือจะไม่สน tags field)
        # และคาดหวังให้สร้าง tag แยก แล้วเอา relation มาใส่ที่ tags field บน Recipe model
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create( # get_or_create คือ helper method ที่มีในทุก model manager
            # ทำงานตามชื่อเลยคือ ถ้ามี value นี้อยู่แล้วมันจะแค่ดึง แต่ถ้าไม่มี value นี้มันจะสร้างแทน
            # check ทั้ง 2 value (user, name)เลย ว่ามีซำ้ทั้งคู่มั้ย
            # get_or_create doc: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#get-or-create
                user=auth_user,
                **tag, # เราสามารถทำเป็ย name=tag['name'] ได้ แค่เราใส่ **tag เพราะเราจะใส่ทุก value จาก tag # เผื่อในอนาคตมี field ใหม่เข้ามา เวลาสร้างมันก็จะเอา field นั้นเข้ามาตรงนี้เลยโดยที่เราไม่ต้องแก้ code ตรงนี้ใดๆ
            )
            recipe.tags.add(tag_obj)

        return recipe # ต้อง return เพื่อให้ function ที่เหลือหรือต่อจะ mrthod นี้เอาไปใช้ต่อ

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
