"""
Core views for app.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET']) # api_view decorator สามารถใช้สร้าง simple API ซึ่งทำให้คุณสามารถสร้าง function ที่ทำหน้าที่เป็น views ให้เราได้
def health_check(request):
    """Returns successful response."""
    return Response({'healthy': True})
