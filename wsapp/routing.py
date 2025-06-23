from django.urls import path
from wsapp import consumers

websocket_urlpatterns = [
    path('ws/posts/', consumers.PostConsumer.as_asgi()),
    path('ws/comments/<int:post_id>/', consumers.CommentConsumer.as_asgi()),

]