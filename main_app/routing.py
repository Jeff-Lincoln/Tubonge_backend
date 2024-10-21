# main_app/routing.py
from django.urls import re_path
from .consumers import VideoCallConsumer

# Define WebSocket URL patterns
websocket_urlpatterns = [
    re_path(r'^ws/videocall/(?P<room_name>\w+)/$', VideoCallConsumer.as_asgi()),  # WebSocket URL with dynamic room_name
]
