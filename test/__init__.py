from pathlib import PurePath
import unittest
import sys

from .app.utils import APP_DIR

from .app.v1.accounts import PATHS as accounts_paths

SHARED_DIR = str(PurePath(APP_DIR, 'layers', 'shared', 'python'))

sys.path.append(APP_DIR)
sys.path.append(SHARED_DIR)

PATHS = [*accounts_paths]

for path in PATHS:
    sys.path.append(path)