from pathlib import Path, PurePath
import sys

THIS_DIRECTORY = Path(__file__).parent.absolute()
TEST_DIR = str(PurePath(THIS_DIRECTORY))
ROOT_DIR = str(PurePath(THIS_DIRECTORY.parent))

sys.path.append(ROOT_DIR)

APP_DIR = str(PurePath(ROOT_DIR, 'app', 'v1'))
LAYERS_DIR = str(PurePath(ROOT_DIR, 'app', 'layers'))
INFRASTRUCTURE_DIR = str(PurePath(ROOT_DIR, 'infrastructure'))
INFRASTRUCTURE_APP_DIR = str(PurePath(ROOT_DIR, 'infrastructure', 'app'))

sys.path.insert(0, INFRASTRUCTURE_APP_DIR)

ORIGINAL_PATH = sys.path

def add_to_path(paths):
  for path in paths:
      sys.path.insert(0, path)

def remove_from_path(paths):
   for path in paths:
      sys.path.remove(path)
