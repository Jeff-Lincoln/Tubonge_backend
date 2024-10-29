# main_app/routing.py
from django.urls import re_path
from .views import create_user

urlpatterns = [
    re_path(r'^api/create-user/$', create_user, name='create_user'),
    # You can add more routes here as needed
]
