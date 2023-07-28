import sys
import os
from .utils import add_to_path, remove_from_path

MODULES = sys.modules

def TestBase(paths: list[str], env={}) -> object:
    class TestBaseClass(object):

        def setup_class(self):
            sys.modules = MODULES
            sys.modules.pop('models', None)
            sys.modules.pop('shared', None)
            sys.modules.pop('ark_qldb', None)
            add_to_path(paths)

            if env:
                for key, value in env.items():
                    os.environ[key] = str(value)

        def teardown_class(self):
            print('base test teardown...')
            remove_from_path(paths)
            sys.modules.pop('models', None)
            sys.modules.pop('shared', None)
            sys.modules.pop('ark_qldb', None)

    return TestBaseClass