from pathlib import PurePath

from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER, MOCK_DIR

MODELS = str(PurePath(APP_DIR, 'accounts'))
PATHS = [MODELS, APP_SHARED_LAYER, MOCK_DIR]
AccountsTestBase = TestBase(PATHS)