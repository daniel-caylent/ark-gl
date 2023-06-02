from pathlib import PurePath

from tests.test_base import TestBase
from tests.utils import LAYERS_DIR

MODELS = str(PurePath(LAYERS_DIR, "qldb", "python", "ark_qldb", "qldb"))
PATHS = [MODELS]
QldbTestBase = TestBase(PATHS)
