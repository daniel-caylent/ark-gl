from pathlib import Path, PurePath

THIS_DIRECTORY = Path(__file__).parent.absolute()
TEST_DIR = str(PurePath(THIS_DIRECTORY.parent))
APP_DIR = str(PurePath(THIS_DIRECTORY.parent.parent, 'app', 'v1'))

print(APP_DIR)

