"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create') # เพราะเราจะใช้ในหลายๆ test เลยมาวางไว้ตรงนี้
# reverse ทำให้เราได้ url จาก name ของ view
TOKEN_URL = reverse('user:token') # user:token หรือก็คือ  url endpoint ของเรา
ME_URL = reverse('user:me')

# สร้างเป็น helper function เพื่อเอาไปใช้ใน test ต่างๆ
def create_user(**params): # โดย **params เพื่อให้ยืดหยุ่นในการใส่ parameter
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

# Public tests คือ Unauthenticated requests เช่น registering a new user
# เราจะแตก test ของเราเป็น 2 แบบก็คือ แบบ require authenticated กับไม่ require authenticated

class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = { # test payload
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload) # ยิง request ไปที่ url

        self.assertEqual(res.status_code, status.HTTP_201_CREATED) # check ว่า resเป็น 201 code มั้ย
        # HTTP_201_CREATED คือ success response code for creating objects
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password'])) # ดึง user ที่พึงสร้างเอามา check password
        self.assertNotIn('password', res.data) # เพราะ password ไม่ควร return ออกจาก api
        # check ว่ามี key ชื่อ password ใน res.data มั้ย

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload) # คือ **payload เอาทุก key ใส่เป็น parameter
        # คล้ายกับคุณทำ create_user(email="", password="", name="")
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) # มันต้อง return bad request เพราะคุณทำการสร้าง user คนทดลองไปก่อนแล้วโดย create_user จากนั้นก็ยิง post request ไปสร้าง user

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw', # short password
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists() # exists() จะ return bool แล้วเก็บลง user_exists
        self.assertFalse(user_exists) # ต้องไม่มี user ที่ short password คนนี้เก็บอยู่ใน database


    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload) # ยิงไปที่ endpoint ที่สร้าง token

        self.assertIn('token', res.data) # ต้องได้ token มา
        self.assertEqual(res.status_code, status.HTTP_200_OK) # status 200 มั้ย

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'} # ใส่ password ให้ผิด เพื่อทดสอบ
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data) # ต้องไม่ได้ token มา
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) # ต้อง 400 status_code

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': ''} # ไม่ใส่ password เพื่อทดสอบใน method นี้
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED) # เพราะเรายังไม่ได้ authorized


# test ที่จำเป็นต้อง authorized
# เราอยากแยกแบบนี้เพราะว่าเราจะจัดการ authentication ที่ setUp method
class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        # ใช้ force_authenticate ทำให้เราไม่ต้อง authenticate จริงๆในระบบ
        # เราต้องแยก unit test ออกจากระบบจริง (isolate) จึงต้องทำแบบนี้เสมอ

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, { # ได้ data คนเดียวกับคนที่ authenticate อยู่หรือป่าว
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {}) # ตั้งใจใช้ผิด method เป็น POST แทน

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self): # ทดสอบ update ข้อมูล user
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db() # เพื่อให้ user values ใน database ถูก refreshed ให้เป็นค่าใหม่ตามที่ update (เพราะโดย default มันไม่ refreshed automatically เมื่อเรา updated data)
        self.assertEqual(self.user.name, payload['name']) # check ว่าข้อมูลถูกเปลี่ยนตามที่ update มั้ย
        self.assertTrue(self.user.check_password(payload['password'])) # check password ว่าถูกเปลี่ยนแล้วหรือยัง
        self.assertEqual(res.status_code, status.HTTP_200_OK)