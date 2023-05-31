from pathlib import PurePath

from tests.test_base import TestBase
from tests.utils import INFRASTRUCTURE_DIR

MODELS = str(PurePath(INFRASTRUCTURE_DIR, "app", "reconciliation"))
PATHS = [INFRASTRUCTURE_DIR, MODELS]
ReconciliationTestBase = TestBase(PATHS)
