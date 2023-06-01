from pathlib import PurePath

from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'ledgers', 'models', 'python'))
PATHS = [MODELS, APP_SHARED_LAYER]
LedgersTestBase = TestBase(PATHS)