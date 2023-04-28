def select_by_fund_id(fundId):
    return [
        {
            'accountNo': 5,
            'accountName': 'account name',
            'accountId': 'account-id',
            'accountDescription': 'account description',
            'state': 'ACTIVE',
            'isHidden': False,
            'isTaxable': True,
            'isVendorCustomerPartnerRequired': False,
            'parentAccountId': -1,
            'attributeId': 1,
            'fsName': 'fsName',
            'fsMappingId': 'fsMapping',
            'fundId': 'a-unique-fund-id'
        },
        {
            'accountNo': 6,
            'accountName': 'account name',
            'accountId': 'account-id',
            'accountDescription': 'account description',
            'state': 'ACTIVE',
            'isHidden': False,
            'isTaxable': True,
            'isVendorCustomerPartnerRequired': False,
            'parentAccountId': -1,
            'attributeId': 1,
            'fsName': 'fsName',
            'fsMappingId': 'fsMapping',
            'fundId': 'a-unique-fund-id'
        }
    ]

def select_by_name(name):
    return []

def create_new(account):
    return 'a-unique-account-id'
