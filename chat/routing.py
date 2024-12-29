from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:connection_id>/', consumers.ChatConsumer.as_asgi()),
    # re_path(r"ws/chat/(?P<connection_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
]