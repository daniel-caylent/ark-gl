from pathlib import PurePath

from tests.test_base import TestBase
from tests.utils import APP_DIR

MODELS = str(PurePath(APP_DIR, 'account_attributes', 'get'))
PATHS = [MODELS]
AccountAttributeTestBase = TestBase(PATHS)