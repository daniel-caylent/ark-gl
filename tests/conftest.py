import sys

from pathlib import PurePath

from tests.utils import APP_DIR, TEST_DIR, LAYERS_DIR


def pytest_configure(config):

    shared_dir = str(PurePath(LAYERS_DIR, 'shared', 'python'))
    mock_dir = str(PurePath(TEST_DIR, 'mock'))

    sys.path.append(APP_DIR)
    sys.path.append(shared_dir)
    sys.path.append(mock_dir)
    sys.path.append(LAYERS_DIR)

