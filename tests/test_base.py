import sys
from .utils import add_to_path, remove_from_path

def TestBase(paths: list[str]) -> object:
    class TestBaseClass(object):

        def setup_class(self):
            print('base test setup ...')
            add_to_path(paths)

        def teardown_class(self):
            print('base test teardown...')
            remove_from_path(paths)
            if sys.modules.get('models'):
                sys.modules.pop('models')

    return TestBaseClass