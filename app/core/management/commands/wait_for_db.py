# ชื่อ file เอาตาม command ที่จะสร้าง
"""
Django command to wait for the database to be available.
"""
import time
from psycopg2 import OperationalError as Psycopg2Error # Error Postgres throes when it is not ready
from django.db.utils import OperationalError # Error Django throws when database is not ready
from django.core.management.base import BaseCommand

# นี้คือ simple empty (minimum code) ที่เราจะเอาไว้เขียนสร้าง command ต่อ
# class Command(BaseCommand):
#     """Django command to wait for database."""

#     def handle(self, *args, **options):
#         pass

class Command(BaseCommand):
    """Django command to wait for database."""

    # เมื่อเราทำการรัน command นี้ มันจะเข้าที่ handle method
    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for database...") # stdout => standard output เพื่อทำการ log สิ่งต่างๆบนหน้าเจอได้
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default']) # databases=['default'] คือ parameter เดียวกับที่ test ใน test นั้นแหละ 
                db_up = True # เป็น True เมื่อ เรียก check method แล้วไม่เกิด error
            except (Psycopg2Error, OperationalError): # ถ้า self.check แล้ว database ไม่พร้อมมันจะ throw except ซึ่งเราก็มาดักตรงนี้
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('Database available!'))