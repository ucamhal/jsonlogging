class JsonFormatter(object):

    def __init__(self, json_encoder, message_adapter):
        self._encoder = json_encoder
        self._adapter = message_adapter

    def get_encoder(self):
        return self._encoder

    def get_adapter(self):
        return self._adapter

    def format(self, message):
        json = self.get_adapter().to_json(message)
        return self.get_encoder().encode(json)
