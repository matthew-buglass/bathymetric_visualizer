from channels.generic.websocket import JsonWebsocketConsumer


class NewDataPointConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
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
        self.send_json(content=content)
