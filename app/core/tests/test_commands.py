# สำหรับการ test function ใน commands folder
"""
Test custom Django management commands.
"""
from unittest.mock import patch # เอา patch มาเพื่อ mock พฤติกรรมของ database เพื่อ simulate database return response มาให้เรา

from psycopg2 import OperationalError as Psycopg2Error # OperationalError เป็น error ที่คุณอาจเจอเมื่อพลายาม connect กับ database ก่อนที่มันจะพร้อม
 
from django.core.management import call_command # call_command เป็น helper function เพื่อทำการ simulate sinvgiupd function ที่เราต้องการจะทดสอบ
from django.db.utils import OperationalError # OperationalError เป็น error ที่คุณอาจเจอเมื่อพลายาม connect กับ database ก่อนที่มันจะพร้อม เหมือนกับอันบน แต่คนละ stage 
from django.test import SimpleTestCase # เป็น base test class ที่เราจะใช้เพื่อ test นี้

# mock behavior โดยใช้ patch decorator
# และเราจะ mock behavior นี้ในทุก test methods เราเลยเอา patch มาวางที่บนสุดของ CommandTests class
@patch("core.management.commands.wait_for_db.Command.check") # คือ command ที่เราจะทำการ mocking โดยการใส่ path ไปหา command นั้น ซึ่ง check เป็น command หรือ method ที่มาจาก BaseCommand class ที่เรา inherit เข้ามาใน Command class (check method เป็น method ที่ทำให้เราสามารถตรวจสอบ status ของ database ได้)
# เช่น check method สามารถ return exception, authorizing ให้เราได้
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_ready(self, patched_check): # เนื่องจากเราใส่ patch ทำให้เราต้องมารับมันที่ args นี้ โดยเราตั้งชื่อว่า patched_check เป็น object ซึ่งเราใช้มันเพื่อ custom behavior ได้
        """Test waiting for database if database ready."""
        patched_check.return_value = True # custom ให้ check method return True (ทำการเรียก check method จริงๆใน all_command('wait_for_db') ตรงนี้แค่ custom ก่อนเรียกจริง)

        call_command('wait_for_db') # execute code ที่อยู่ใน wait_for_db
        # ซึ่งในนี้ก็จะทำการเรียก check method ด้วย 

        # ทำการ test ว่า check method (ที่ถูกเรียกใน wait_for_db นั้น)ถูกเรียกด้วย parameters คือ database=['default'] หรือป่าว (คือทำการ test ว่า check method มัน calling ถูกที่หรือป่าว)
        patched_check.assert_called_once_with(database=['default']) # check the default database

    # @patch('...') # ถ้ามีอีก patch ตรงนี้ args ที่รับ patch นี้จะไปอยู่ที่ args ที่ 3 ต่อจาก sleep เพราะ sleep อยู่ใกล้กว่า
    @patch('time.sleep') # เพราะเราต้องการ apply patch นี้ให้แค่ test ตัวนี้ (เลยเอามาไว้ที่บนหัว method นี้)
    def test_wait_for_db_delay(self, patched_sleep, patched_check): # ลำดับของ args นั้นสำคัญ คือมันจะ apply args แรกๆ จาก patch ที่อยู่ใกล้ๆ method ก่อน
        # sleep method (เป็น build-in sleep function) จะถูกแทนที่ด้วย mock object ที่เราตั้งชื่อว่า patched_sleep
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
            # เราต้องการให้มัน raise some exceptions (ในความเป็นจริงมันจะ raise เมื่อ database เราไม่พร้อม)
            # ทางที่เราจะทำให้มันสามารถ raise exceptions แทนการ return value คือการใช้ side_effect

            # ถ้าเราใส่ exception มันจะทำการ raise exception นั้น ถ้าคุณใส่ boolean มันก็จะ reture boolean value

            # ค่าที่เราใส่ในที่นี้หมายถึง
            # [Psycopg2Error] * 2 คือ 2 ครั้งแรกที่เราเรียก mocked method เราต้องการให้มัน raise Psycopg2Error
            # \ คือ ใส่เพื่อให้มันไปอยู่อีกบรรทัดนึง
            # [OperationalError] * 3 คือ เราทำการ raise OperationalError ใน 3 ครั้งต่อไป หลังจาก 2 ครั้งแรก
            # [True] คือ database พร้อมต่อ connection กับ app เรา ซึ่ง True เป็น value มันก็จะ return value ไม่ใช่ raise exception
            # คือพฤติกรรมของ postgres ที่คิดว่าจะเกิดขึ้น นั้นคือเมื่อ Postgres ตัวมันยังไม่ started เลย ซึ่งมันก็จะไม่ accept connections ใดๆเราจะได้ error คือ Psycopg2Error จากนั้นเมื่อ database พร้อมที่จะ accept connections แต่ยังไม่ทันได้ setup database ที่เราต้องการจะใช้ case นี้ Django จะ raises OperationalError (ซึ่งเป็น Django's exceptions)
            # ตรวด Psycopg2Error 2 ครั้ง กับ OperationalError 3 ครั้ง เพื่อให้แค่เป็นตัวแรกที่ต่างกันเท่านั้น (เพื่อให้เหมือนใน real situation) ความจริงจะเป็นเลขอะไรก็ได้

        call_command('wait_for_db') # ตรงนี้มันก็จะทำการเรียก check method ตามที่เรา custom ด้านบนด้วย

        self.assertEqual(patched_check.call_count, 6) # test ว่า check method มันเรียกทั้งหมด 6 ครั้งใช่มั้ย
        patched_check.assert_called_with(database=['default']) # เพื่อ test ว่ามันเรียกถูก value หรือป่าว เหมือนอันด้านบน

    # การ sleep
    # เพื่อให้มันรอซักแปปแล้วค่อยไป check อีกทีนั้นแหละ
    # sleep แล้วค่อยไป check อีกที เพราะเราไม่ได้อย่างจะสร้างเป็น 100 request ไปที่ database ในช่วงใดช่วงนึง
    