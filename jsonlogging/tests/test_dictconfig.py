import unittest
import logging
import logging.config


from jsonlogging.formatters import JsonFormatter

class TestJsonFormatterDictconfigFactory(unittest.TestCase):
    def test_dictconfig_factory(self):

        conf = {
            "version": 1,
            "handlers": {
                "test-json-handler": {
                    "class": "logging.StreamHandler",
                    "formatter": "test-json-formatter",
                }
            },
            "formatters": {
                "test-json-formatter": {
                    "()": "jsonlogging.json_formatter_factory",
                    "format": "test: {json}",
                    "json_encoder": {
                        "indent": 2,
                        "separators": [" , ", " : "]
                    }
                }
            },
            "loggers": {
                __name__: {
                    "handlers": ["test-json-handler"]
                }
            }
        }

        logging.config.dictConfig(conf)

        logger = logging.getLogger(__name__)
        handler = logger.handlers[0]
        self.assertEqual("test-json-handler", handler.name)

        formatter = handler.formatter
        self.assertIsInstance(formatter, JsonFormatter)

        self.assertEqual("test: {json}", formatter.get_format())

        self.assertEqual(2, formatter.get_encoder().indent)
        self.assertEqual(" , ", formatter.get_encoder().item_separator)
        self.assertEqual(" : ", formatter.get_encoder().key_separator)

