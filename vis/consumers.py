import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NewDataPointConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.mesh_name = "global"

        # Connect to the mesh room
        async_to_sync(self.channel_layer.group_add)(
            self.mesh_name, self.channel_name
        )
        logger.info(f"{self.__class__.__name__} connection received for mesh {self.mesh_name}")

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.mesh_name, self.channel_name
        )
        logger.info(f"{self.__class__.__name__} disconnection for mesh {self.mesh_name}: Code {close_code}")
        pass

    def receive_json(self, content: dict, **kwargs):
        """
        Takes the updated list for vertices and faces and sends them along to observers

        Args:
            content: a dictionary with the keys "flat_vertices" and "flat_faces" to send to connections
            **kwargs: Not used

        Returns:
            None
        """
        logger.info(f"{self.__class__.__name__} received json")

        async_to_sync(self.channel_layer.group_send)(
            self.mesh_name, {"type": "new_data", "content": content}
        )

    def new_data(self, event):
        """
        Takes a new_data event and sends updated data
        Args:
            event: The event dictionary

        Returns:
            None
        """
        content = event['content']
        logger.info(f"{self.__class__.__name__} sending new data")

        self.send_json(content=content)
