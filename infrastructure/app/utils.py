from pathlib import Path, PurePath

THIS_DIRECTORY = Path(__file__).parent.absolute()
APP_DIR = str(PurePath(THIS_DIRECTORY.parent.parent, 'app'))
ACCOUNTS_DIR = str(PurePath(APP_DIR, 'accounts'))
ACCOUNTS_ATTR_DIR = str(PurePath(APP_DIR, 'account_attributes'))
LAYERS_DIR = str(PurePath(APP_DIR, 'layers'))
