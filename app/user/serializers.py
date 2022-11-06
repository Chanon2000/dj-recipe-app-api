"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate, # import หลายอันต้องใส่เป็น tuple
    # authenticate เป็น func ที่มาจาก django ที่ทำ authenticate ด้วย authentication system ให้กับคุณ
)
from django.utils.translation import gettext as _ # _ เป็น common use syntax สำหรับ translation ใน django

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

    # เราจะสร้าง serializer สำหรับ token
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    # เราทำการกำหนด serializer 2 fields
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, # เรา style ตรงนี้ เพราะเมื่อเรายิงบน browser นั้น ตัวinput ควรจะเป็น password (เหมือน type password บน html)
        trim_whitespace=False, # เพราะโดย default drf จะเป็น True คือ trim whitespace ให้เราใน CharField
        # ซึ่งครั้งนี้เราอนุญาติให้มี whitespace ใน password ได้
    )

    # เรากำหนด validate method ให้กับ auth token sterilizer
    # โดย validate method จะถูกเรียนตอน validation stage โดย view ของเรา
    # คือตอนที่ data POST เข้า view มา view ก็จะใส่ value เข้า Serializer แล้วมันก็ check แต่ละ field ตาม rule ด้านบนก่อน แล้วมันก็จะเรียก validate นี้
    # validate ก็เหมือน create method ของ ModelSerializer นั้นแหละ ในเรื่องเวลาในการถูกเรียกใช้งาน
    def validate(self, attrs): # attrs = attributes
        """Validate and authenticate the user."""
        # ตรงนี้เราจะใส่ logic ในการ authenticates user ที่ logging in

        # โดยใส่ส่วนของ validation ก็จะเรื่มจากรับ email, password
        email = attrs.get('email')
        password = attrs.get('password')
        # เรียก authenticate func ซึ่งมาจาก Django build-in โดยมันจะ accept 3 อย่าง
        user = authenticate(
            request=self.context.get('request'), # คือ request context (ซึ่งมีเช่น header ของ request เป็นต้น)
            # เอาจริงในกรณีที่เราใช้ตรงนี้ มันไม่หน้าจะใช้ request ที่เราใส่มาแต่เราใส่เพราะมันเป็น require field
            username=email, # เราใช้ email เป็น username ในการ auth
            password=password,
        ) # ถ้าข้อมูลถูกต้องมันก็จะ return user แต่ถ้าไม่ผ่านก็จะได้เป็น empty object
        if not user: # ถ้า user ไม่ถูก set (ไม่มีค่า)
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
            # นี้คือ standard way to raise errors ด้วย Serialize ซึ่งเมื่อ view ได้ raise นี้มาก็จะ raise เป็น http 400 bad request และใส่ message ที่เรากำหนดมาให้ด้วย

        attrs['user'] = user # กำหนด user attributes แล้วใส่ user หรือข้อมูลของคนที่ auth แล้วเข้าไป
        return attrs # return ไปให้ view ใช้ต่อ