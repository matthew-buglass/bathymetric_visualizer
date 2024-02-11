import json

from channels.generic.websocket import WebsocketConsumer
from django.conf import settings


class NewDataPointConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self):
        data = {
            "flat_vertices": list(settings.GLOBAL_MESH.get_flat_vertices()),
            "flat_faces": list(settings.GLOBAL_MESH.get_flat_faces()),
        }

        self.send(text_data=json.dumps(data))
