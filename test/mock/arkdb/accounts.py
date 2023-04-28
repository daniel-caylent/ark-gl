def select_by_fund_id(fundId):
    return [
        {
            'id': 1,
            'accountNo': 5,
            'accountName': 'account name',
            'accountId': 'account id',
            'accountDescription': 'account description',
            'state': 'ACTIVE',
            'isHidden': False,
            'isTaxable': True,
            'isVendorCustomerPartnerRequired': False,
            'parrentAccountId': -1,
            'attributeNo': 1,
            'fsName': 'fsName',
            'fsMappingId': 'fsMapping'
        },
        {
            'id': 2,
            'accountNo': 6,
            'accountName': 'account name',
            'accountId': 'account id',
            'accountDescription': 'account description',
            'state': 'ACTIVE',
            'isHidden': False,
            'isTaxable': True,
            'isVendorCustomerPartnerRequired': False,
            'parrentAccountId': -1,
            'attributeId': 1,
            'fsName': 'fsName',
            'fsMappingId': 'fsMapping'
        }
    ]

def select_by_name(name):
    return []

def create_new(account):
    return 'a-unique-account-id'
