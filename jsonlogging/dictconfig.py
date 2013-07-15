import json

from .formatters import WrapedJsonFormatter
from .recordadapter import default_record_adapter


def json_formatter_factory(json_encoder={}, format="{json}"):
    """
    A factory to create JsonFormatter instances from dictconfig logging
    configurations.

    formatters:
      json:
        (): jsonlogging.json_formatter_factory
        format: my-app: {json}
        json_encoder:
          indent: 0
          separators: [", ", ": "]

    Customising the record template is not yet supported through this
    dictconfig factory.
    """
    encoder = json_encoder_factory(**json_encoder)

    return WrapedJsonFormatter(format, encoder, default_record_adapter())


def json_encoder_factory(
        skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True,
        sort_keys=False, indent=None, separators=[",", ":"], encoding="utf-8"):

    # pass a tuple rather than a list to JSONEncoder for separators
    separators = tuple(separators)

    return json.JSONEncoder(**locals())
