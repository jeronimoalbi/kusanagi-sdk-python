import asyncio
import io
import json
import logging
import os

import click.testing
import pytest

import kusanagi.payload
from kusanagi.logging import setup_kusanagi_logging
from kusanagi.schema import SchemaRegistry


@pytest.fixture(scope='session')
def data_path(request):
    """
    Fixture to add full path to test data directory.

    """

    return os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture(scope='function')
def read_json(data_path):
    """
    Fixture to add JSON loading support to tests.

    """

    def deserialize(name):
        if not name[-4:] == 'json':
            name += '.json'

        with open(os.path.join(data_path, name), 'r') as file:
            return json.load(file)

    return deserialize


@pytest.fixture(scope='function')
def registry(request):
    """
    Fixture to add schema registry support to tests.

    """

    def cleanup():
        SchemaRegistry.instance = None

    request.addfinalizer(cleanup)
    return SchemaRegistry()


@pytest.fixture(scope='function')
def cli(request):
    """
    Fixture to add CLI runner support to tests.

    """

    disable_field_mappings = kusanagi.payload.DISABLE_FIELD_MAPPINGS

    def cleanup():
        kusanagi.payload.DISABLE_FIELD_MAPPINGS = disable_field_mappings
        del os.environ['TESTING']

    request.addfinalizer(cleanup)
    os.environ['TESTING'] = '1'
    return click.testing.CliRunner()


@pytest.fixture(scope='function')
def logs(request, mocker):
    """
    Fixture to add logging output support to tests.

    """

    output = io.StringIO()

    def cleanup():
        # Remove root handlers to release sys.stdout
        for handler in logging.root.handlers:
            logging.root.removeHandler(handler)

        # Cleanup kusanagi logger handlers too
        logging.getLogger('kusanagi').handlers = []
        logging.getLogger('kusanagi.sdk').handlers = []

        output.close()

    request.addfinalizer(cleanup)
    mocker.patch('kusanagi.logging.get_output_buffer', return_value=output)
    setup_kusanagi_logging(
        'component', 'name', 'version', 'framework-version', logging.INFO,
        )
    return output


@pytest.fixture(scope='function')
def async_mock(mocker):
    def mock(callback):
        @asyncio.coroutine
        def mocked_coroutine(*args, **kwargs):
            return callback()

        return mocked_coroutine

    return mock
