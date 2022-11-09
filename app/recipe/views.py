"""
Views for the recipe APIs
"""
from rest_framework import ( # import หลายอันให้ใส่เป็น tuple
    viewsets,
    mixins, # คือสิ่งที่สามารถใส่เข้าไปใน view เพื่อเพิ่ม functionality
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
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

# เราจะต้องมี basic CRUD implementation
class TagViewSet(mixins.DestroyModelMixin,
                mixins.UpdateModelMixin,
                mixins.ListModelMixin, # เป็น mixins เพื่อเพิ่ม listing functionality ให้กับการ listing models
                viewsets.GenericViewSet): # viewsets.GenericViewSet ให้คุณสามารถใส่mixinsได้ (เหมือนกับ GenericViewSet มี basic func ต่างๆให้ จากนั้นเอา mixins มาเพิ่มความสามารถให้กับ basic function ต่างๆเหล่านั้น)
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # property พวกนี้ พิมพ์สะกดผิดทีนิหา bug ค่อนข้างยากเลย

    # เพื่อให้ view นี้สามารถ update tag ได้ด้วย
    # mixins ต่างๆต้องกำหนดก่อน GenericViewSet (ใน doc มันบอกเอาไว้)

    # override get_queryset method
    def get_queryset(self): # เพื่อให้ตอน get เอาเฉพาะ tags ของ user ที่ login เท่านั้น
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
