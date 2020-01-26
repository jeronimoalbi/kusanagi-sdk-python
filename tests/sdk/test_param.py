import pytest
from kusanagi.errors import KusanagiTypeError
from kusanagi.sdk.param import Param
from kusanagi.sdk.param import param_to_payload
from kusanagi.sdk.param import payload_to_param
from kusanagi.sdk.param import TYPE_ARRAY
from kusanagi.sdk.param import TYPE_BINARY
from kusanagi.sdk.param import TYPE_BOOLEAN
from kusanagi.sdk.param import TYPE_INTEGER
from kusanagi.sdk.param import TYPE_FLOAT
from kusanagi.sdk.param import TYPE_NULL
from kusanagi.sdk.param import TYPE_OBJECT
from kusanagi.sdk.param import TYPE_STRING
from kusanagi.payload import FIELD_MAPPINGS


def test_sdk_param_to_payload():
    empty = object()
    values = {
        'value': 'bar',
        'type': TYPE_STRING,
        }
    payload = param_to_payload(Param('foo', **values))
    assert payload is not None
    assert payload.get('name', default=None) == 'foo'

    # Check that payload contains file values
    for name, value in values.items():
        assert payload.get(name, default=empty) == value


def test_sdk_payload_to_param():
    values = {
        'name': 'foo',
        'value': 'bar',
        'type': TYPE_STRING,
        }
    payload = {FIELD_MAPPINGS[name]: value for name, value in values.items()}
    param = payload_to_param(payload)
    assert param is not None
    assert param.exists()

    # Check that file contains payload values
    for name, value in values.items():
        getter = getattr(param, 'get_{}'.format(name), None)
        assert getter is not None
        assert getter() == value


def test_sdk_param():
    # Check empty param creation
    param = Param('foo')
    assert param.get_name() == 'foo'
    assert param.get_value() == ''
    assert param.get_type() == TYPE_STRING
    assert not param.exists()

    # Create a parameter with an unknown type
    param = Param('foo', value='42', type='weird')
    assert param.get_type() == TYPE_STRING

    # Check param creation
    param = Param('foo', value=42, exists=True, type=Param.TYPE_INTEGER)
    assert param.get_name() == 'foo'
    assert param.get_value() == 42
    assert param.get_type() == TYPE_INTEGER
    assert param.exists()


def test_sdk_param_resolve_type():
    class Foo(object):
        pass

    cases = (
        (None, TYPE_NULL),
        (True, TYPE_BOOLEAN),
        (0, TYPE_INTEGER),
        (0.0, TYPE_FLOAT),
        ([], TYPE_ARRAY),
        ((), TYPE_ARRAY),
        (set(), TYPE_ARRAY),
        ('', TYPE_STRING),
        (b'', TYPE_BINARY),
        ({}, TYPE_OBJECT),
        (Foo(), TYPE_OBJECT),
        )

    for value, type_ in cases:
        assert Param.resolve_type(value) == type_


def test_sdk_param_copy():
    param = Param('foo', value=42, type=Param.TYPE_INTEGER)

    # Check copy with methods
    clon = param.copy_with_name('clon')
    assert isinstance(clon, Param)
    assert clon != param
    assert clon.get_name() == 'clon'
    assert clon.get_name() != param.get_name()
    assert clon.get_type() == param.get_type()
    assert clon.get_value() == param.get_value()

    clon = param.copy_with_value(666)
    assert isinstance(clon, Param)
    assert clon != param
    assert clon.get_value() == 666
    assert clon.get_value() != param.get_value()
    assert clon.get_name() == param.get_name()
    assert clon.get_type() == param.get_type()

    with pytest.raises(KusanagiTypeError):
        param.copy_with_type(TYPE_STRING)
