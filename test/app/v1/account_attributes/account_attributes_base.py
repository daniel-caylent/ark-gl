from pathlib import PurePath
from ...utils import APP_DIR
MODELS = str(PurePath(APP_DIR, 'account_attributes', 'get'))
PATHS = [MODELS]

from ...test_base import TestBase

AccountAttributesTestBase = TestBase(PATHS)
