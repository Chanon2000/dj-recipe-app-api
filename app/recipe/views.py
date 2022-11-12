"""
Views for the recipe APIs
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import (
    viewsets,
    mixins,
    status,
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


@extend_schema_view( # คือ decorator ที่ทำให้คุณ extend auto generated schema ที่สร้างโดย drf-spectacular
    list=extend_schema( # กำหนด list = extend_schema ก็เพราะเราจะ extend schema นั้นแหละ โดย extend ให้กับ endpoint ที่เป็น list
        parameters=[ # กำหนด parameters ที่สามารถใส่เข้าไปได้ ใน list api
            OpenApiParameter( # เราใช้ OpenApiParameter ซึ่งมาจาก drf-spectacular เพื่อกำหนด detail ต่างๆ เกี่ยวกับ parameter ที่สามารถ accepted ใน API request
                'tags', # name ของ parameter
                OpenApiTypes.STR, # typr ของ value ซึ่ง STR นั้นก็คือ string (ไม่ int เพราะว่าเราจะให้มันสามารถใส่ , ได้ไง)
                description='Comma separated list of tag IDs to filter', # เป็นคำอธิบาย บน docs
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            ),
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # เริ่มจากเขียน func ที่สามารถดึง list of parameters มาใช้ filter
    # accepting our filter arguments as a list of IDs แล้วเปลี่ยนเป็น int
    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]
        # เช่น "1,2,3" เก็บใน qs แล้ว split โดย , เป็น str_id แล้วก็เอามา convert เป็น int โดย int()

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        # return self.queryset.filter(user=self.request.user).order_by('-id')
        tags = self.request.query_params.get('tags') # ดึง tags params มา
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags: # ถ้ามันไม่ได้ใส่ tag อะไรมา ก็ไม่ต้อง filter มัน (ซึ่งทำให้มันเป็ย optional คือจะใส่ param หรือ ไม่ใส่ก็ได้)
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
            # filter tags field by id ถ้า tag_ids อยู่ใน list ของ recipe อันไหน มันก็จะเป็น true
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct() # distinct เพราะเราอาจจะได้ duplicate recipe ได้ การใส่ distinct ก็จะไม่ทำให้ result ไม่ duplicate

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

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