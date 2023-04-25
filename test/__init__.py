from pathlib import PurePath
import sys

from .app.utils import APP_DIR, TEST_DIR

from .app.v1.accounts import PATHS as accounts_paths

SHARED_DIR = str(PurePath(APP_DIR, 'layers', 'shared', 'python'))
MOCK_DIR = str(PurePath(TEST_DIR, 'mock'))

sys.path.append(APP_DIR)
sys.path.append(SHARED_DIR)
sys.path.append(MOCK_DIR)

PATHS = [*accounts_paths]

for path in PATHS:
    sys.path.append(path)