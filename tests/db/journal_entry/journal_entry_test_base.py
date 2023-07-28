from pathlib import PurePath

from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

PATHS = [APP_SHARED_LAYER]
JournalEntryTestBase = TestBase(PATHS)