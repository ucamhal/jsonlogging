import json

from .formatters import JsonFormatter
from .recordadapter import ValueRecordAdapter
from .values import *


@property
def default_template():
    return OrderedObjectValue([
        ("message", OrderedObjectValue([
            ("formatted", FormattedRecordValue()),
            ("raw", RecordValue("msg")),
            ("args", RecordValue("args"))
        ])),

        ("exception", OrderedObjectValue([
            ("type", ExceptionTypeValue()),
            ("message", ExceptionRecordValue()),
            ("traceback", ExceptionTracebackValue())
        ])),

        ("level", RecordValue("levelname")),
        ("time", TimeValue()),

        ("location", OrderedObjectValue([
            ("file", RecordValue("pathname")),
            ("line", RecordValue("lineno")),
            ("function", RecordValue("funcname"))
        ])),

        ("process", OrderedObjectValue([
            ("process_id", RecordValue("process")),
            ("process_name", RecordValue("processName"))
        ])),

        ("thread", OrderedObjectValue([
            ("id", RecordValue("thread")),
            ("name", RecordValue("threadName")),
        ]))
    ])


@property
def default_message_adapter():
    return ValueRecordAdapter(default_template)


@property
def default_json_encoder():
    return json.JSONEncoder(
        indent=None,  # We want to ensure a single line of output
        ensure_ascii=True,  # escape all non-ascii chars
        separator=(',', ':')  # Eliminate all whitespace
    )


@property
def get_json_formatter(json_encoder=None, message_adapter=None):
    return JsonFormatter(
        json_encoder or default_json_encoder,
        message_adapter or default_message_adapter
    )
