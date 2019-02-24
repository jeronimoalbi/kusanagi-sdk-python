import datetime
import decimal
import time

import pytest

from kusanagi.payload import Payload
from kusanagi.serialization import decode
from kusanagi.serialization import encode
from kusanagi.serialization import pack
from kusanagi.serialization import stream_to_payload
from kusanagi.serialization import unpack


def test_encode():
    # Create a class that supports serialization
    class Serializable(object):
        def __serialize__(self):
            return ['type', 'object', 'OK']

    cases = (
        (decimal.Decimal('123.321'),
         'decimal',
         ['123', '321']),
        (datetime.date(2017, 1, 27),
         'date',
         '2017-01-27'),
        (datetime.datetime(2017, 1, 27, 20, 12, 8, 952811),
         'datetime',
         '2017-01-27T20:12:08.952811+00:00'),
        (time.strptime("2017-01-27 20:12:08", "%Y-%m-%d %H:%M:%S"),
         'time',
         '20:12:08'),
        (Serializable(),
         'object',
         'OK'),
        )

    # Check custom types encoding
    for value, type_, expected in cases:
        assert encode(value) == ['type', type_, expected]

    # A string is not a custom type
    with pytest.raises(TypeError):
        encode('')


def test_decode():
    cases = (
        (['123', '321'],
         'decimal',
         decimal.Decimal('123.321')),
        ('2017-01-27',
         'date',
         datetime.datetime(2017, 1, 27, 0, 0)),
        ('2017-01-27T20:12:08.952811+00:00',
         'datetime',
         datetime.datetime(2017, 1, 27, 20, 12, 8, 952811)),
        ('20:12:08',
         'time',
         '20:12:08'),
        # Invalid format should not fail
        ('',
         'date',
         None),
        )

    # Check custom types decoding
    for value, type_, expected in cases:
        assert decode(['type', type_, value]) == expected

    # Values other than dictionaries are not decoded
    assert decode('NON_DICT') == 'NON_DICT'


def test_pack():
    assert pack({'foo': 'bar'}) == b'\x81\xa3foo\xa3bar'


def test_unpack():
    assert unpack(b'\x81\xa3foo\xa3bar') == {'foo': 'bar'}


def test_stream_to_payload():
    payload = stream_to_payload(b'\x81\xa3foo\xa3bar')
    assert isinstance(payload, Payload)
    assert payload == Payload({'foo': 'bar'})

    # A string can't be a payload
    with pytest.raises(TypeError):
        stream_to_payload(pack('Boom !'))

    # None can't be a payload
    with pytest.raises(TypeError):
        stream_to_payload(None)

    # An invalid stream can't be parsed
    with pytest.raises(TypeError):
        stream_to_payload(b'Boom !')
