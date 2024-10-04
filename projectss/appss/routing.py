from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:office>/', consumers.ChatConsumer.as_asgi()),
]
