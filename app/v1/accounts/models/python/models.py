from dataclasses import dataclass
from typing import Literal

from shared import validate_uuid    # pylint: disable=import-error


@dataclass
class Account:
    accountNo: str
    accountName: str
    state: Literal["USED", "UNUSED", "ACTIVE"]
    accountDescription: str
    fsMappingId: str
    fsName: str
    isHidden: bool
    isTaxable: bool
    isEntityRequired: bool
    parentAccountId: str
    attributeId: str
    accountId: str
    fundId: str

    def __post_init__(self):
        self.isEntityRequired = bool(self.isEntityRequired)
        self.isHidden = bool(self.isHidden)
        self.isTaxable = bool(self.isTaxable)


@dataclass
class AccountPost:
    fundId: str = None
    attributeId: str = None
    accountNo: str = None
    accountName: str = None
    isTaxable: bool = None
    fsName: str = None

    # optional
    fsMappingId: str = None
    isEntityRequired: bool = False
    accountDescription: str = None
    isDryRun: bool = False
    parentAccountId: str = None
    isHidden: bool = False

    def __post_init__(self):
        # required
        self.accountNo = check_account_no(self.accountNo)
        self.accountName = check_account_name(self.accountName)
        self.fundId = check_uuid(self.fundId, "fundId")
        self.attributeId = check_uuid(self.attributeId, "attributeId")
        self.fsMappingId = (
            None if self.fsMappingId is None else
            check_uuid(self.fsMappingId, "fsMappingId")
        )
        self.isTaxable = check_is_taxable(self.isTaxable)
        self.fsName = check_fs_name(self.fsName)

        # optional
        self.isEntityRequired = bool(self.isEntityRequired)
        self.isHidden = bool(self.isHidden)
        self.parentAccountId = (
            None if self.parentAccountId is None else
            check_uuid(self.parentAccountId, "parentAccountId")
        )


@dataclass
class AccountPut:
    accountNo: str = None
    accountName: str = None
    accountDescription: str = None
    fsMappingId: str = None
    fsName: str = None
    isDryRun: bool = None
    parentAccountId: str = None
    attributeId: str = None
    isEntityRequired: bool = None
    isHidden: bool = None
    isTaxable: bool = None

    def __post_init__(self):
        self.accountName = (
            None if self.accountName is None else
            check_account_name(self.accountName)
        )
        self.isEntityRequired = (
            None if self.isEntityRequired is None
            else bool(self.isEntityRequired)
        )
        self.accountNo = (
            None if self.accountNo is None else check_account_no(self.accountNo)
        )
        self.isHidden = None if self.isHidden is None else bool(self.isHidden)
        self.isTaxable = (
            None if self.isTaxable is None else check_is_taxable(self.isTaxable)
        )
        self.attributeId = (
            None if self.attributeId is None else
            check_uuid(self.attributeId, "attributeId")
        )
        self.parentAccountId = (
            None if self.parentAccountId is None else
            check_uuid(self.parentAccountId, "parentAccountId")
        )
        self.fsMappingId = (
            None if self.fsMappingId is None else
            check_uuid(self.fsMappingId, "fsMappingId")
        )


def check_account_no(account_no):
    if account_no is None:
        raise Exception('Required argument is missing: accountNo')
    try:
        account_no = str(int(account_no))
    except Exception:
        raise Exception('Invalid account number.')
    return account_no


def check_account_name(account_name):
    if account_name is None:
        raise Exception('Required argument is missing: accountName')
    try:
        account_name = account_name.strip()
    except:
        raise Exception('Invalid account name.')

    if len(account_name) == 0:
        raise Exception('Invalid account name.')

    return account_name

def check_is_taxable(is_taxable):
    if is_taxable is None:
        raise Exception("Required argument is missing: isTaxable.")
    try:
        is_taxable = bool(is_taxable)
    except:
        raise Exception("Invalid value for isTaxable.")

    return is_taxable

def check_uuid(uuid, name):
    if uuid is None:
        raise Exception(f'Required argument is missing: {name}')

    try:
        validate_uuid(uuid, throw=True)
    except:
        raise Exception(f'{name} is not a valid UUID')

    return uuid

def check_fs_name(fs_name):
    if fs_name is None:
        raise Exception('Required argument is missing: fsName')
    try:
        fs_name = fs_name.strip()
    except:
        raise Exception('Invalid value for fsName.')

    if len(fs_name) == 0:
        raise Exception('Invalid value for fsName.')

    return fs_name
    
