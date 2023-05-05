from pathlib import PurePath
from ...utils import APP_DIR
MODELS = str(PurePath(APP_DIR, 'ledgers', 'models', 'python'))
PATHS = [MODELS]

from ...test_base import TestBase

LedgersTestBase = TestBase(PATHS)
