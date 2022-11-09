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

    # refract code ให้ดีขึ้นโดยการเขียน _get_or_create_tags เพื่อทำให้ add rela tags field เข้า recipe
    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
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

    # เนื่องจากโดย default แล้ว tags จะกลายเป็น read-only field เราเลยทำการ custom logic create method (override)
    def create(self, validated_data): # validated_data เพราะ data ถูก validate ก่อนจะมาเข้า method นี้
        """Create a recipe."""
        tags = validated_data.pop('tags', []) # .get จะดึง value ขึ้นมาเฉยๆ แต่ถ้า .pop จะถึง value ขึ้นมาแล้วเอา tags key ออกจาก validated_data object เลย
        # .pop(keyname, defaultvalue) defaultvalue คือ value ที่จะ return เมื่อ key นั้นไม่มีใน validated_data
        recipe = Recipe.objects.create(**validated_data) # ตรงนี้คือเหตุผลที่เรา pop ก่อนหน้านี้ เพราะมันจะสนแค่ value จาก Recipe model (นั้นก็คือจะไม่สน tags field)
        # และคาดหวังให้สร้าง tag แยก แล้วเอา relation มาใส่ที่ tags field บน Recipe model
        self._get_or_create_tags(tags, recipe)

        return recipe # ต้อง return เพื่อให้ function ที่เหลือหรือต่อจะ mrthod นี้เอาไปใช้ต่อ

    # ทำการ override update method ที่ จะรันเมื่อ http patch เข้ามา
    def update(self, instance, validated_data): # instance คือ exist data recipe ที่ดึงมาจาก database ของ id ที่ระบุ
        # ส่วน validated_data คือ data ใหม่ที่จะเอาเข้ามา update
        """Update recipe."""
        tags = validated_data.pop('tags', None) # ให้เป็น None ถ้า key tags ใน validated_data ไม่มี value
        if tags is not None: # ถ้า tags ไม่ None
            instance.tags.clear() # clear ทุก tags ที่อยู่ใน instance ก่อน
            self._get_or_create_tags(tags, instance) # แล้วจากนั้นก็ทำการ update tags อันใหม่เข้า tags field ใน recipe

        # คือ update field ที่เหลือ (ที่ไม่ใช่ tags field เพราะจัดการมันได้แล้วด้านบน)
        for attr, value in validated_data.items():
            setattr(instance, attr, value) # object ที่จะ update, attr หรือ key, value ก็คือ ค่าใหม่ที่จะเอามา update

        instance.save() # save update change ต่างๆ ลง database
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
