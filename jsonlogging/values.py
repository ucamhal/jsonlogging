"""
This module contains a number of Value implementations. These Value classes
have a single method: render(record) which pull out and return a value
from a logging.LogRecord instance.
"""

import datetime
import traceback
from collections import OrderedDict


class OrderedObjectValue(object):
    """
    A Value implementation which is used to create a JSON object literal
    containing other Values.

    This Value is a little different to the rest as it doesn't directly pull
    values out of a record, but instead defers to nested Value instances.

    The `entries` argument is a sequence of (name, value) pairs where name is
    the attribute name for the value in the resulting object and value is a
    Value instance whose render() method will be called to produce the dict
    returned by this instance's render() method.

    The order of `entries` is significant as the returned dict is an OrderedDict
    matching the order that items appear in `entries`.
    """
    def __init__(self, entries):
        self._entries = entries

    def render(self, record):
        entries = (
            (name, value.render(record)) for (name, value) in self._entries
        )

        # Create an ordered dict, dropping any None values
        value = OrderedDict(
            (name, value) for (name, value) in entries if value is not None
        )

        # Return None if our dict is empty
        return value or None


class RecordValue(object):
    """
    A Value implementation which extracts the value of a named
    attribute from a LogRecord.
    """
    def __init__(self, attr_name):
        self._attr = attr_name

    def render(self, record):
        return getattr(record, self._attr, None)


class DateRecordValue(object):
    """
    A Value implementation which renders to a string representation of the
    LogRecord's timestamp.

    This implementation represents the date/time in ISO 8601 format as produced
    by datetime.datetime.isoformat().
    """

    timestamp_attribute = "created"

    def get_datetime(self, record):
        """
        Create a datetime instance from the LogRecord.
        """
        value = RecordValue(self.timestamp_attribute).render(record)
        return datetime.datetime.fromtimestamp(value)

    def render(self, record):
        return self.format_datetime(self.get_datetime(record))

    def format_datetime(self, datetime):
        """
        Converts a datetime instance into a string representation. Subclasses
        can override this method to customise the date string produced by
        render().
        """
        return datetime.isoformat()


class FormattedRecordRecordValue(object):
    """
    A Value implementation which returns the value of a the
    LogRecord's formatted record.
    """
    def render(self, record):
        if isinstance(record.msg, basestring):
            return record.getRecord()
        return None


class BaseExcInfoRecordValue(object):
    """
    A superclass for Value types which deal with a record's exc_info attribute
    which may not be present.
    """
    def render(self, record):
        if record.exc_info is None:
            return None
        return self.exc_info_value(record.exc_info)


class ExceptionTypeRecordValue(BaseExcInfoRecordValue):
    """
    A Value implementation which renders to the record's exception type.
    This type is represented as a string in module.Class notation. None
    is returned if no exception information is present.
    """
    def exc_info_value(self, exc_info):
        exception_type, _, _ = exc_info

        return "{}.{}".format(
            exception_type.__module__, exception_type.__name__)


class ExceptionMessageRecordValue(BaseExcInfoRecordValue):
    """
    A Value implementation which renders to the record's exception message.
    None is returned if no exception information is present.
    """
    def exc_info_value(self, exc_info):
        _, exception, _ = exc_info

        return "{}".format(exception)


class ExceptionTracebackRecordValue(BaseExcInfoRecordValue):
    """
    A Value implementation which renders to the record's exception traceback.
    """
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
