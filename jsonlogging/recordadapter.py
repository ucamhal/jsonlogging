"""
RecordAdapter objects are responsible for converting LogMessage's to JSON
values. They have a to_json(LogMessage) method which returns the JSON value
for the provided LogMessage instance.
"""


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
