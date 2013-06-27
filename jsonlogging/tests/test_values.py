import datetime
import logging
import sys
import time
import traceback
import unittest

from jsonlogging import values


class TestRecordValue(unittest.TestCase):
    def setUp(self):
        self.record_params = dict(
            name="testlogger",
            level=logging.DEBUG,
            pathname="/some/path.py",
            lineno=34,
            msg="This is a msg. %s",
            args=[123],
            func="some_func"
        )
        self.record = logging.makeLogRecord(self.record_params)

    def test_record_value_renders_expected_value(self):
        for (name, value) in self.record_params.items():
            record_value = values.RecordValue(name)
            self.assertEqual(value, record_value.render(self.record))


class TestDateRecordValue(unittest.TestCase):
    def test_render(self):
        """
        Verify that DateRecordValue.render() produces the "created" date in
        ISO 8601 format.
        """
        now = 1372241168.878024  # example return val of time.time()
        record = logging.makeLogRecord({"created": now})

        actual = values.DateRecordValue().render(record)
        expected = datetime.datetime.fromtimestamp(now).isoformat()

        self.assertEqual(expected, actual)


class TestFormattedMessageRecordValue(unittest.TestCase):
    def test_render_formats_string(self):
        """
        Verify that FormattedMessageRecordValue.render() produces the formatted
        version of the LogRecord's msg.
        """
        msg = "This is a %s %s."
        args = ("log", "message")
        record = logging.makeLogRecord({"msg": msg, "args": args})

        actual = values.FormattedMessageRecordValue().render(record)
        expected = msg % args

        self.assertEqual(expected, actual)

    def test_render_returns_none_for_non_string_msg(self):
        record = logging.makeLogRecord({"msg": {"foo": "bar"}})
        actual = values.FormattedMessageRecordValue().render(record)
        self.assertEqual(None, actual)


class TestExceptionRelatedRecordValue(unittest.TestCase):
    def setUp(self):
        try:
            something = 1 / 0
            assert False
        except ZeroDivisionError as e:
            self.exc_info = sys.exc_info()

        self.record = logging.makeLogRecord({"exc_info": self.exc_info})

    def test_exception_type_renders_to_none_when_no_exception_present(self):
        """
        ExceptionTypeRecordValue.render() should return None when no exception
        info is present on the record.
        """
        empty_record = logging.makeLogRecord({})
        value = values.ExceptionTypeRecordValue()
        self.assertIsNone(value.render(empty_record))

    def test_exception_message_renders_to_none_when_no_exception_present(self):
        """
        ExceptionMessageRecordValue.render() should return None when no
        exception info is present on the record.
        """
        empty_record = logging.makeLogRecord({})
        value = values.ExceptionMessageRecordValue()
        self.assertIsNone(value.render(empty_record))

    def test_exception_traceback_renders_to_none_when_no_exception_present(self):
        """
        ExceptionTracebackRecordValue.render() should return None when no
        exception info is present on the record.
        """
        empty_record = logging.makeLogRecord({})
        value = values.ExceptionTracebackRecordValue()
        self.assertIsNone(value.render(empty_record))

    def test_exception_type(self):
        self.assertEqual(
            "exceptions.ZeroDivisionError",
            values.ExceptionTypeRecordValue().render(self.record)
        )

    def test_exception_message(self):
        self.assertEqual(
            str(self.exc_info[1]),
            values.ExceptionMessageRecordValue().render(self.record)
        )

    def test_exception_traceback(self):
        trace = values.ExceptionTracebackRecordValue().render(self.record)

        self.assertTrue(trace[-1]["file"].endswith("test_values.py"))
        self.assertEqual("setUp", trace[-1]["function"])
        self.assertEqual("something = 1 / 0", trace[-1]["code"])

        self.assertEqual(
            len(traceback.extract_tb(self.exc_info[2])),
            len(trace)
        )


class TestOrderedObjectValue(unittest.TestCase):

    def test_empty_oov_renders_to_none(self):
        actual = values.OrderedObjectValue([]).render(logging.makeLogRecord({}))
        self.assertEqual(None, actual)

    def test_oov_with_single_none_value_renders_to_none(self):
        record = logging.makeLogRecord({"msg": None})

        oov = values.OrderedObjectValue([
            ("msg", values.RecordValue("msg"))
        ])

        actual = oov.render(record)
        self.assertEqual(None, actual)

    def test_oov_drops_none_values(self):
        message = "Hi"
        record = logging.makeLogRecord({"msg": message, "path": None})

        oov = values.OrderedObjectValue([
            ("msg", values.RecordValue("msg")),
            ("path", values.RecordValue("path")),
        ])

        actual = oov.render(record)

        self.assertEqual(1, len(actual))
        self.assertTrue("msg" in actual)
        self.assertEqual(message, actual["msg"])

    def test_oov_maintains_initial_order(self):
        msg = "This is a msg. foo: %s"
        args = ("bar",)
        now_ts = 1372245551.300383  # time.time() return val
        now_dt = datetime.datetime.fromtimestamp(now_ts)
        path = "/some/path.py",

        record = logging.makeLogRecord({
            "msg": msg,
            "args": args,
            "created": now_ts,
            "pathname": path,
            "lineno": None
        })

        oov = values.OrderedObjectValue([
            ("test_msg", values.RecordValue("msg")),
            ("test_lineno", values.RecordValue("lineno")),
            ("test_path", values.RecordValue("pathname")),
            ("test_args", values.RecordValue("args")),
            ("test_formatted_msg", values.FormattedMessageRecordValue())
        ])

        json = oov.render(record)

        self.assertEqual(
            # Note missing test_lineno as it's None
            ["test_msg", "test_path", "test_args", "test_formatted_msg"],
            json.keys()
        )

    def test_oovs_can_nest(self):
        """
        Verify that nesting OrderedObjectValues produces nested dicts in the
        render() return value.
        """
        oov = values.OrderedObjectValue([
            ("test_msg", values.RecordValue("msg")),
            ("nested", values.OrderedObjectValue([
                ("nested_path", values.RecordValue("pathname"))
            ]))
        ])

        record = logging.makeLogRecord({
            "msg": "Hi",
            "pathname": "/some/path.py"
        })

        json = oov.render(record)

        self.assertEqual(2, len(json))
        self.assertEqual(["test_msg", "nested"], json.keys())

        nested = json["nested"]
        self.assertEqual(1, len(nested))
        self.assertEqual(["nested_path"], nested.keys())
