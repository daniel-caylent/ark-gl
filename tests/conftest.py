import sys

from pathlib import PurePath

from tests.utils import APP_DIR, TEST_DIR


def pytest_configure(config):

    shared_dir = str(PurePath(APP_DIR, 'layers', 'shared', 'python'))
    mock_dir = str(PurePath(TEST_DIR, 'mock'))

    sys.path.append(APP_DIR)
    sys.path.append(shared_dir)
    sys.path.append(mock_dir)

