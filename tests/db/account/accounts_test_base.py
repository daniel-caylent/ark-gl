from pathlib import PurePath

from tests.test_base import TestBase
from tests.utils import APP_SHARED_LAYER, APP_ARK_QLDB_LAYER

PATHS = [APP_SHARED_LAYER, APP_ARK_QLDB_LAYER]

env = {
    "LEDGER_NAME": "TEST"
}
AccountsTestBase = TestBase(PATHS, env)