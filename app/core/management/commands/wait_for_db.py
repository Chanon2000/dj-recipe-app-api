# ชื่อ file เอาตาม command ที่จะสร้าง
"""
Django command to wait for the database to be available.
"""
from django.core.management.base import BaseCommand

# นี้คือ simple empty (minimum code) ที่เราจะเอาไว้เขียนสร้าง command ต่อ
# class Command(BaseCommand):
#     """Django command to wait for database."""

#     def handle(self, *args, **options):
#         pass

class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        pass