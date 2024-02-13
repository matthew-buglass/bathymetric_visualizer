from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"dynamic_mesh/$", consumers.NewDataPointConsumer.as_asgi()),
]
