import logging

from kusanagi.logging import KusanagiFormatter
from kusanagi.logging import value_to_log_string


def test_kusanagi_formatter():
    class Record(object):
        pass

    record = Record()
    record.created = 1485622839.2490458  # Non GMT timestamp
    assert KusanagiFormatter().formatTime(record) == '2017-01-28T17:00:39.249'


def test_value_to_los_string():
    # Define a dummy class
    class Dummy(object):
        def __repr__(self):
            return 'DUMMY'

    # Define a dummy function
    def dummy():
        pass

    assert value_to_log_string(None) == 'NULL'
    assert value_to_log_string(True) == 'TRUE'
    assert value_to_log_string(False) == 'FALSE'
    assert value_to_log_string('value') == 'value'
    assert value_to_log_string(b'value') == 'dmFsdWU='
    assert value_to_log_string(lambda: None) == 'anonymous'
    assert value_to_log_string(dummy) == '[function dummy]'

    # Dictionaries and list are serialized as pretty JSON
    assert value_to_log_string({'a': 1}) == '{\n  "a": 1\n}'
    assert value_to_log_string(['1', '2']) == '[\n  "1",\n  "2"\n]'

    # For unknown types 'repr()' is used to get log string
    assert value_to_log_string(Dummy()) == 'DUMMY'

    # Check maximum characters
    max_chars = 100000
    assert len(value_to_log_string('*' * max_chars)) == max_chars
    assert len(value_to_log_string('*' * (max_chars + 10))) == max_chars


def test_setup_kusanagi_logging(logs):
    # Root logger must use KusanagiFormatter
    assert len(logging.root.handlers) == 1
    assert isinstance(logging.root.handlers[0].formatter, KusanagiFormatter)

    # SDK loggers must use KusanagiFormatter
    for name in ('kusanagi', 'kusanagi.sdk'):
        assert len(logging.getLogger(name).handlers) == 1

    logger = logging.getLogger('kusanagi')
    assert logger.level == logging.INFO
    assert isinstance(logger.handlers[0].formatter, KusanagiFormatter)

    logger = logging.getLogger('kusanagi.sdk')
    assert isinstance(logger.handlers[0].formatter, logging.Formatter)

    assert logging.getLogger('asyncio').level == logging.ERROR

    # Basic check for logging format
    message = 'Test message'
    logging.getLogger('kusanagi').info(message)
    out = logs.getvalue()
    assert len(out) > 0
    out_parts = out.split(' ')
    assert out_parts[0].endswith('Z')  # Time
    assert out_parts[1] == 'component'  # Component type
    assert out_parts[2] == 'name/version'  # Component name and version
    assert out_parts[3] == '(framework-version)'
    assert out_parts[4] == '[INFO]'  # Level
    assert out_parts[5] == '[SDK]'  # SDK prefix
    assert ' '.join(out_parts[6:]).strip() == message
