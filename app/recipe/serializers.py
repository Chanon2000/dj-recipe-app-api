"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient # กำหนด model (เนื่องจากเราใช้ ModelSerializer )
        fields = ['id', 'name']
        read_only_fields = ['id'] # กำหนด field ที่เป็น พำ read only


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'price', 'link', 'tags',
            'ingredients', # เอา 'ingredients' element มาไว้บรรทัดที่ 2 ตามที่ Flake-8 ต้องการ
        ]
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe): # เป็น internal method เลยใส่ _ นำหน้า หมายความว่า เราไม่คาดหวังให้ใครที่ใช้ sterilizer นี้ มาเรียก method นี้ตรงๆ (จะเอาไว้ใช้ใน sterilizer นี้เท่านั้น มันจะถูกใช้เฉพาะ methods ที่อยู่ใน recipe sterilizer class นี้เท่านั้น)
        # เป็นแค่หลักการนะ ไม่ใช่ technical คือไม่ควรเรียก method ที่ _ นำหน้า นอก class ของมัน เป็น tip เมื่อเขียน python
        """Handle getting or creating ingredients as needed.""" # ทำเหมือน _get_or_create_tags แค่เปลี่ยนเป็น ingredients
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)


    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])
        # เพิ่มจัดการ ingredients
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
