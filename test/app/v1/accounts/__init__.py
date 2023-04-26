from pathlib import PurePath

from ...utils import APP_DIR, add_to_path

MODELS = str(PurePath(APP_DIR, 'accounts', 'models', 'python'))
PATHS = [MODELS]

add_to_path(PATHS)
