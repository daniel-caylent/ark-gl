import sys
from .utils import add_to_path, remove_from_path

def TestBase(paths: list[str]) -> object:
    class TestBaseClass(object):

        def setup_class(self):
            print('base test setup ...')
            if sys.modules.get('models'):
                sys.modules.pop('models')
            if sys.modules.get('shared'):
                sys.modules.pop('shared')
            if sys.modules.get('ark_qldb'):
                sys.modules.pop('ark_qldb')
            add_to_path(paths)

        def teardown_class(self):
            print('base test teardown...')
            remove_from_path(paths)
            if sys.modules.get('models'):
                sys.modules.pop('models')
            if sys.modules.get('shared'):
                sys.modules.pop('shared')
            if sys.modules.get('ark_qldb'):
                sys.modules.pop('ark_qldb')

    return TestBaseClass