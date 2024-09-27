from django.urls import path
from appss.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:office_name>/', ChatConsumer.as_asgi()),
]
