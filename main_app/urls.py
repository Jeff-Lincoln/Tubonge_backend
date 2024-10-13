# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-room/', views.create_room, name='create_room'),
    path('join-room/', views.join_room, name='join_room'),
    path('end-call/', views.end_call, name='end_call'),
    path('room-info/<str:room_name>/', views.get_room_info, name='get_room_info'),
]
