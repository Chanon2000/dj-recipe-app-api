"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers
# serializer คือวิธีการในการ convert object เป็นหรือจาก python object โดยเช่นเอาจาก json object ที่ได้จาก api แล้วทำการ check ว่ามัน validation secure correct ตาม rule แล้วหรือยัง จากนั้นก็ convert เป็น python objects หรือเป็น model ก็ได้

# มันมี base class มากมายในการ serialization ที่เราใช้นี้คือ serializers.ModelSerializer
# ModelSerializer จะทำให้เรา automatically validate แล้ว save บางอย่างไปที่ specific model ที่เรากำหนดใน serialization ของเรา
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object.""" # doc string

    class Meta: # ตรงนี้คือจุดที่คุณบอก Django rest framework เกี่ยวกับ models และ field และอื่นๆ เพื่อทำการ serialize
        model = get_user_model() # ใส่ user model
        fields = ['email', 'password', 'name'] # คือ field ที่เราจะ enable for serializers
        # ใส่ field แค่นี้เพราะว่า อย่าง is_staff เราไม่มีทางให้ user กำหนดเองอยู่แล้ว (หมายความว่า field อื่นๆเราจะไม่รับจาก request)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        # ใส่ dict ที่ทำให้คุณเพื่อใส่ extra metadata ให้กับ แต่ละ field ได้ เพื่อบอก Django rest framework ว่า ต้องการให้แต่ละ field มี rule อะไรบ้าง
        # 'write_only': True เพื่อ security ให้เขียน password ได้แต่ดึงส่งออกจาก api ไม่ได้
        # ถ้า user ใส่ value พวกนี้ไม่ตรงตามที่กำหนดไว้เขาจะได้ 400 bad request ซึ่งเป็น result of a validation error

    # override create method เพื่อทำการ custom
    def create(self, validated_data): # method นี้จะถูกเรียกหลังจาก validation successful ถ้า validation ไม่ผ่าน create ก็จะยังไม่ได้ทำงาน
        """Create and return a user with encrypted password."""
        # default create method จะแค่เอา value ที่เราใส่เข้ามา สร้างเป็น objects แล้ว save
        # ซึ่งเนื่องจากเรามี password มันก็จะ save password เราเป็น clear text ในmodel ซึ่งเราไม่ต้องการแบบนั้น เลย override เป็น save ผ่าน create_user method แทน โดยไม่เรียก base create method ให้ทำงานเลย (super().create())
        return get_user_model().objects.create_user(**validated_data)