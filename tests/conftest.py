import sys


from tests.utils import APP_DIR, TEST_DIR, LAYERS_DIR, MOCK_DIR


def pytest_configure(config):


    sys.path.append(APP_DIR)
    sys.path.append(MOCK_DIR)
    sys.path.append(LAYERS_DIR)
