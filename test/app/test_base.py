import unittest
import sys
from .utils import add_to_path, remove_from_path

def TestBase(paths: list[str]) -> unittest.TestCase:
    class TestBaseClass(unittest.TestCase):

        def setUp(self):
            add_to_path(paths)

        def tearDown(self):
            remove_from_path(paths)
            if sys.modules.get('models'):
                sys.modules.pop('models')

    return TestBaseClass