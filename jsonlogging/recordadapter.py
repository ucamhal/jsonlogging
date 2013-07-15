"""
RecordAdapter objects are responsible for converting LogMessage's to JSON
values. They have a to_json(LogRecord) method which returns the JSON value
for the provided LogMessage instance.
"""

from .values import *


def default_record_adapter():
    return ValueRecordAdapter(default_template())


def default_template():
    return OrderedObjectValue([
        ("message", OrderedObjectValue([
            ("formatted", FormattedMessageRecordValue()),
            ("raw", RecordValue("msg")),
            ("args", RecordValue("args"))
        ])),

        ("exception", OrderedObjectValue([
            ("type", ExceptionTypeRecordValue()),
            ("message", ExceptionMessageRecordValue()),
            ("traceback", ExceptionTracebackRecordValue())
        ])),

        ("name", RecordValue("name")),
        ("level", RecordValue("levelname")),
        ("time", DateRecordValue()),

        ("location", OrderedObjectValue([
            ("file", RecordValue("pathname")),
            ("line", RecordValue("lineno")),
            ("function", RecordValue("funcName"))
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


class ValueRecordAdapter(object):
    """
    Adapts LogRecord instances into a JSON structure.

    This implementation uses a Value heirachy as a template to render a JSON
    value from a LogMessage.
    """

    def __init__(self, value_template):
        self._value_template = value_template

    def to_json(self, record):
        return self._value_template.render(record)
