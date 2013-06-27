import unittest
import logging

from jsonlogging import values, recordadapter


class TestValueRecordAdapter(unittest.TestCase):

    def test_empty_template_converts_to_none(self):
        empty_template = values.OrderedObjectValue([])
        adapter = recordadapter.ValueRecordAdapter(empty_template)
        record = logging.makeLogRecord({})

        self.assertIsNone(adapter.to_json(record))

    def test_to_json_acts_as_value_render(self):
        """
        Assert that the adapter's to_json() method acts the same as the
        value.render() method if value is the adapter's template.
        """
        msg = "This is a msg"
        record = logging.makeLogRecord({"msg": msg})
        template = values.RecordValue("msg")
        adapter = recordadapter.ValueRecordAdapter(template)

        self.assertEqual(msg, adapter.to_json(record))
        self.assertEqual(msg, template.render(record))
