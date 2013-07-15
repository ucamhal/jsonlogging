import json

from .dictconfig import json_formatter_factory
from .formatters import (
    default_json_encoder,
    get_json_formatter,
    JsonFormatter,
    WrapedJsonFormatter
)
from .recordadapter import (
    default_record_adapter,
    default_template,
    ValueRecordAdapter
)


__version__ = "0.0.3"
__version_info__ = tuple(int(n) for n in __version__.split("."))
