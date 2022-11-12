"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    status, # status นี้ใช้ได้ทั้งใน test และ response จริงๆ
)
from rest_framework.decorators import action
from rest_framework.response import Response
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
        elif self.action == 'upload_image': # action นี้จะเป็น custom action
            # ModelViewSet มี default actions ให้เราใช้เยอะแยะ ที่สามารถได้ศึกษาได้จาก official documentation แต่เราจะเพิ่ม custom action นี้สำหรับ upload image
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    # สร้าง custom action ตรงนี้ โดยใช้ actions decorator จาก Django Rest Framework

    @action(methods=['POST'], detail=True, url_path='upload-image')
    # methods=['POST'] เราสามารถกำหนด http method เพื่อ support custom action
    # detail=True คือ action จะ apply แบบ detail (แบบ detail เช่น get recipe by id ไม่ใช่ get list เป็นต้น)
    # คือต้องส่ง id ของ recipe มาด้วย (เป็น detail endpoint)
    # url_path='upload-image' ก็คือกำหนด url ให้กับ action นั้นแหละ
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object() # เพื่อดึงข้อมูลของ recipe ที่จะ upload file ซึ่งมันจะใช้ pk (primary key) ที่คุณรับมาจาก action parameter
        serializer = self.get_serializer(recipe, data=request.data) # เรียก get_serializer โดย method นี้ก็จะไปรัน get_serializer_class ที่เรากำหนดด้านบนอีกที ซึ่งก็จะได้ instance ของ serializer ซึ่งเราจะได้ image sterilizer

        if serializer.is_valid(): # ถ้า serializer valid
            serializer.save() # ก็ทำการ save หรือก็คือ save image ลง database
            return Response(serializer.data, status=status.HTTP_200_OK) # res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()