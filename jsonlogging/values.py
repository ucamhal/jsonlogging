import traceback
from collections import OrderedDict


class RecordValue(object):
    """
    A RecordValue implementation which extracts the value of a named
    attribute from a LogRecord.
    """

    def __init__(self, attr_name):
        self._attr = attr_name

    def get_value(self, message):
        return getattr(message, self._attr, None)


class FormattedMessageRecordValue(object):
    """
    A MessageValue implementation which returns the value of a the
    LogMessage's formatted message.
    """
    def get_value(self, message):
        if isinstance(message.msg, basestring):
            return message.getMessage()
        return None


class BaseExcInfoRecordValue(object):
    def get_value(self, message):
        if message.exc_info is None:
            return None
        return self.exc_info_value(message.exc_info)


class ExceptionTypeRecordValue(BaseExcInfoRecordValue):
    def exc_info_value(self, exc_info):
        exception_type, _, _ = exc_info

        return "{}.{}".format(
            exception_type.__module__, exception_type.__name__)


class ExceptionMessageRecordValue(BaseExcInfoRecordValue):
    def exc_info_value(self, exc_info):
        _, exception, _ = exc_info

        return "{}".format(exception)


class ExceptionTracebackRecordValue(BaseExcInfoRecordValue):
    def exc_info_value(self, exc_info):
        _, _, tb = exc_info

        return [
            self.render_trace_entry(entry)
            for entry in traceback.extract_tb(tb)
        ]

    def render_trace_entry(self, entry):
        filename, line_number, function_name, code_line = entry
        
        json = OrderedDict()
        json["file"] = filename
        json["line"] = line_number
        json["function"] = function_name
        if code_line:
            json["code"] = code_line
        return json
