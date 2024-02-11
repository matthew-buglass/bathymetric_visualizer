import logging

from channels.generic.websocket import JsonWebsocketConsumer

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NewDataPointConsumer(JsonWebsocketConsumer):
    def connect(self):
        logger.info(f"{self.__class__.__name__} connection received")
        self.accept()

    def disconnect(self, close_code):
        logger.info(f"{self.__class__.__name__} disconnection {close_code}")
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
        self.send_json(content=content)
