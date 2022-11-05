"""
Tests for the Django admin modifications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    # สร้าง setup method เข้า class ซึ่ง setUp จะรันทุกครั้งในทุก test method ใน class นี้
    def setUp(self): # ใน unittest lib นี้ เขาหน้าจะพลาดตอนตั้งชื่อแล้วไม่ได้แก้ เพราะเอาจริงๆชื่อว่า set_up ดีกว่า
        """Create user and client."""
        self.client = Client() # คือ django test client เพื่อทำ http request
        # docs: https://docs.djangoproject.com/en/3.2/topics/testing/tools/#overview-and-a-quick-example
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user) # force the authentication ด้วย self.admin_user คนนี้
        # ทำให้ทุก request ที่ทำจาก self.client จะ authenticated เป็น self.admin_user คนนี้
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    # สร้าง test method ชื่อ test_users_lists (หรือก็คือ unittest ของเรา)
    def test_users_lists(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist') # reverse เพื่อเอา url
        # 'admin:core_user_changelist' คือ syntax เพื่อกำหนดว่าเราจะเอา url อะไรจาก django admin ซึ่งในที่นี้คือเราจะเอา page ที่แสดง list ของ users ในระบบเรา
        # docs: https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls
        res = self.client.get(url) # call http request
        # ซึ่ง request ถูก authenticated แล้ว โดย user ที่อยู่ใน setUp method

        self.assertContains(res, self.user.name) # check ว่า page มี name ของ user อยู่มั้ย (เพราะหน้านั้นต้อง list users ทั้งหมดในระบบ)
        self.assertContains(res, self.user.email) # เช่นเดียวกับ name

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id]) # เนื่องจากเราเข้าหน้า edit เลยต้องระบุ id ของ user ที่จะเข้าด้วย (ดู url จาก docs)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200) # check ว่า page load success ด้วย status_code=200