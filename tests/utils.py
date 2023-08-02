from pathlib import Path, PurePath
import sys

THIS_DIRECTORY = Path(__file__).parent.absolute()
TEST_DIR = str(PurePath(THIS_DIRECTORY))
MOCK_DIR = str(PurePath(TEST_DIR, 'mock'))
ROOT_DIR = str(PurePath(THIS_DIRECTORY.parent))

sys.path.append(ROOT_DIR)

APP_DIR = str(PurePath(ROOT_DIR, 'app', 'v1'))
LAYERS_DIR = str(PurePath(ROOT_DIR, 'app', 'layers'))
APP_ARK_QLDB_LAYER = str(PurePath(LAYERS_DIR, "qldb", "python"))
APP_SHARED_LAYER = str(PurePath(LAYERS_DIR, 'shared', 'python'))
APP_JOURNAL_ENTRIES_SHARED_LAYER = str(PurePath(LAYERS_DIR, 'journal_entries_shared', 'python'))
INFRASTRUCTURE_DIR = str(PurePath(ROOT_DIR, 'infrastructure'))

ORIGINAL_PATH = sys.path

def add_to_path(paths):
  for path in paths:
      sys.path.insert(0, path)

def remove_from_path(paths):
   for path in paths:
      sys.path.remove(path)
