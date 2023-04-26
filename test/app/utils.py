from pathlib import Path, PurePath
import sys

THIS_DIRECTORY = Path(__file__).parent.absolute()
TEST_DIR = str(PurePath(THIS_DIRECTORY.parent))
APP_DIR = str(PurePath(THIS_DIRECTORY.parent.parent, 'app', 'v1'))
ORIGINAL_PATH = sys.path

def add_to_path(paths):
  for path in paths:
      sys.path.append(path)
