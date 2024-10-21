"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from main_app.consumers import VideoCallConsumer  # Import the custom WebSocket consumer
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Get the default ASGI application for HTTP handling
django_asgi_app = get_asgi_application()

# Define the WebSocket URL patterns for the application
websocket_urlpatterns = [
    path('ws/videocall/<str:room_name>/', VideoCallConsumer.as_asgi()),  # WebSocket URL for video call signaling
]

# Create the ASGI application with both HTTP and WebSocket handling
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # HTTP handling for standard requests
    "websocket": AuthMiddlewareStack(  # Authenticated WebSocket handling
        URLRouter(
            websocket_urlpatterns  # WebSocket URL routing for video call rooms
        )
    ),
})



# """
# ASGI config for core project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
# """

# import os
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from main_app.consumers import VideoCallConsumer  # Import the custom WebSocket consumer
# from django.urls import path

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# # Get the default ASGI application for HTTP handling
# django_asgi_app = get_asgi_application()

# # Define the WebSocket URL patterns for the application
# websocket_urlpatterns = [
#     path('ws/videocall/<str:room_name>/', VideoCallConsumer.as_asgi()),  # WebSocket URL for video call signaling
# ]

# # Create the ASGI application with both HTTP and WebSocket handling
# application = ProtocolTypeRouter({
#     "http": django_asgi_app,  # HTTP handling
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns  # WebSocket URL routing
#         )
#     ),
# })
