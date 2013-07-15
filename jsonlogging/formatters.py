import json

from .recordadapter import default_record_adapter


def get_json_formatter(json_encoder=None, record_adapter=None):
    return JsonFormatter(
        json_encoder or default_json_encoder(),
        record_adapter or default_record_adapter()
    )


def default_json_encoder():
    return json.JSONEncoder(
        indent=None,  # We want to ensure a single line of output
        ensure_ascii=True,  # escape all non-ascii chars
        separators=(',', ':')  # Eliminate all whitespace
    )


class JsonFormatter(object):

    def __init__(self, json_encoder, record_adapter):
        self._encoder = json_encoder
        self._adapter = record_adapter

    def get_encoder(self):
        return self._encoder

    def get_adapter(self):
        return self._adapter

    def format(self, record):
        json = self.get_adapter().to_json(record)
        return self.get_encoder().encode(json)


class WrapedJsonFormatter(JsonFormatter):
    """
    A JsonFormatter whose JSON output is itself formatted into a format
    string, allowing the JSON log entry to be surrounded in arbitary text.
    """

    def __init__(self, format, json_encoder, record_adapter):
        super(WrapedJsonFormatter, self).__init__(
            json_encoder, record_adapter)

        self._format = format

    def get_format(self):
        return self._format

    def format(self, record):
        json = super(WrapedJsonFormatter, self).format(record)

        return self.get_format().format(json=json)
