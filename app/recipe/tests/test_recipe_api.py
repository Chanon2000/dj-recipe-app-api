"""
Tests for recipe APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer, # เป็น serializer ที่จะแสดง field เพิ่มขึ้นมา (แสดงข้อมูลเพิ่มขึ้น เพิ่ม detail นั้นแหละ เกี่ยวกับ recipe ที่ระบุ)
)

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id): # เราทำเป็น function เพราะเราต้องการจะใส่ id เข้าไปใน url และการทำเป็น function ทำให้เราไม่ต้อง head code reverse บ่อยๆ
    """Create and return a recipe detail URL."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params): # คือ helper function ในการสร้าง recipe
    # params เป็น dictionary ที่จะกลายเป็น parameters ให้กับ func
    # การใส่ ** คือจะทำให้ args ต่างๆที่ใส่เข้ามาต่อจาก user มันเข้ามารวมกันใน params ถ้าไม่ใส่มันก็จะมองว่า params ต้องใส่เข้ามาเป็นก้อน dict เท่านั้น
    """Create and return a sample recipe."""
    defaults = { # เป็น mock default recipe (สำหรับ test ที่ไม่สนว่าข้อมูลใน recipe จะไม่ยังไง)
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params) # เป็นการ update defaults โดยเอา value จาก params ที่มี key เดียวกันมาใส่
    # ถ้าเราไม่ได้ใส่ params มันก็จะใช้ value จาก defaults ที่มีอยู่แล้วนี้แหละ (แต่ถ้าใส่ value ลง params มันก็จะ overwrite)

    recipe = Recipe.objects.create(user=user, **defaults) # ซึ่ง **defaults ก็เหมือนกับการแตกก้อน defaults ให้เป็น key value ต่างๆ เพื่อเอาไปให้ create func
    # ถ้าใส่แค่ defaults มันจะมองเป็นแค่ใส่แค่ field parameters อันเดียว
    return recipe

# แยก test เป็น unauthenticated กับ authenticated เหมือนเดิม

class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient() # เราก็จะได้ test client ที่เราสามารถใช้ได้ใน class นี้

    def test_auth_required(self): # test require auth api เมื่อไม่ทำการ authenticate
        """Test auth is required to call API."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        # สร้าง 2 recipe ที่ใส่แค่ user ซึ่งมีแค่ user field เท่านั้นที่ require ในการสร้าง recipe
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL) # จะได้ recipe ที่เราสร้างเมื่อกี้ทั้งหมด
        # ดึงผ่าน api ซึ่งใน api จะทำ serializer อยู่แล้ว

        # ดึงมาทั้งหมดผ่าน Recipe.objects.all() ตรงๆ แล้วมาทำ serializer ตรงนี้ (เพื่อเอามา check กับการดึงผ่าน api ที่ทำ serializer ใน api)
        recipes = Recipe.objects.all().order_by('-id') # ทำให้ recipe ล่าสุดจะอยู่บนสุด (อันแรกๆ)
        serializer = RecipeSerializer(recipes, many=True) # เอา recipes ผ่านเข้า RecipeSerializer
        # ใส่ many=True เพื่อบอกว่าเราต้องใส่ recipe หลายอัน (ส่งเป็น list)
        self.assertEqual(res.status_code, status.HTTP_200_OK) # check status ก่อน
        self.assertEqual(res.data, serializer.data) # check ว่าที่ serializer return กับที่ยิงไปที่ api ได้ข้อมูลเหมือนกันมั้ย
        # res.data เป็น dictonary

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_recipe(user=other_user) # สร้าง recipe ของ other_user var
        create_recipe(user=self.user) # สร้าง recipe ของ user ที่ auth

        res = self.client.get(RECIPES_URL) # เราต้องการ recipes ที่เป็นของ user ที่ auth เท่านั้นจาก api นี้ เราจึงทำการทดสอบ

        recipes = Recipe.objects.filter(user=self.user) # ไม่ต้อง order เหมือนก่อนหน้านี้เพราะว่า มัน return แค่ single recipe
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data) # check ว่า recipe ที่ได้จาก api กับ ที่ serializer ตรงนี้เลย เหมือนกันหรือป่าว (เพราะใน api ก็ทำ serializer เหมือนกัน)

    def test_create_recipe(self): # เราไม่ต้องใช้ helper func create_recipe ในการ test นี้เพราะเป้าหมายในการ test นี้คือการสร้าง recipe ผ่าน api
        """Test creating a recipe.""" # ทดสอบว่า recipe ที่ถูกสร้างผ่าน api นั้นถูกต้องหรือป่าว
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }
        res = self.client.post(RECIPES_URL, payload) # /api/recipes/recipe

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items(): # check ข้อมูลแต่ละ item
            # k = key ใน dict
                # recipe.k จะได้ value จะ key นั้นๆ
            # v = value ใน dict
            # items() เป็น method ของ dict
            self.assertEqual(getattr(recipe, k), v) # check ข้อมูลแค่ละ attributes
            # getattr() เอา value จาก key ที่ทำหนดใน recipe ที่ใส่มา return
        self.assertEqual(recipe.user, self.user) # check user field ใน recipe