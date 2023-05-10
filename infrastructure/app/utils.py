import os
from pathlib import Path, PurePath

THIS_DIRECTORY = Path(__file__).parent.absolute()
APP_DIR = str(PurePath(THIS_DIRECTORY.parent.parent, 'app', 'v1'))
ACCOUNTS_DIR = str(PurePath(APP_DIR, 'accounts'))
LEDGERS_DIR = str(PurePath(APP_DIR, 'ledgers'))
ACCOUNTS_ATTR_DIR = str(PurePath(APP_DIR, 'account_attributes'))
LAYERS_DIR = str(PurePath(APP_DIR, 'layers'))
LOCAL_LAYERS_DIR = str(PurePath(THIS_DIRECTORY, 'layers'))


def get_stack_prefix() -> str:
    DEPLOYMENT_ENV = 'DEPLOYMENT_ENV'
    return os.getenv(DEPLOYMENT_ENV) + '-' if os.getenv(DEPLOYMENT_ENV) is not None else ''


def get_stack_id(id : str) -> str:
    return id if id is None else get_stack_prefix() + id