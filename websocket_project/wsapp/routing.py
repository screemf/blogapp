from django.urls import path
from wsapp2 import consumers

websocket_urlpatterns = [
    path('ws/posts/', consumers.PostConsumer.as_asgi()),
]