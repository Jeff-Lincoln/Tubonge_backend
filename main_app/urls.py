# main_app/urls.py

from django.urls import path
from .views import generate_user_token

urlpatterns = [
    path('generate-user-token/', generate_user_token, name='generate_user_token'),
]
