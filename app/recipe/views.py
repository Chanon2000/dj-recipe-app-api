"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient
)
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

# Refactor ให้TagViewSet กับ IngredientViewSet มัน base BaseRecipeAttrViewSet เพราะ login ทั้ง 2 อันมันซำ้
# Base เพราะว่าเราจะใช้ class นี้เป็น base class มันจะไม่ใช้ view ที่เราจะใช้ตรงๆ
# RecipeAttr เพราะทั้ง Tag และ Ingredient ก็เป็นเหมือน attributes ของ Recipe
# ViewSet ก็เพราะมัน base มาจาก viewsets อีกที ซึ่งในที่นี้เราใช้ GenericViewSet
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """Filter queryset to authenticated user."""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')

class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer # กำหนด Serializer class
    queryset = Ingredient.objects.all()
    # authentication_classes = [TokenAuthentication] # ใช้ TokenAuthentication ในการ authentication
    # permission_classes = [IsAuthenticated] # user ต้อง authenticated เพื่อใช้ endpoint นี้

    # def get_queryset(self):
    #     """Filter queryset to authenticated user."""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')