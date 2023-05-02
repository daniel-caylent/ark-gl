def select_by_fund_id(fundId):
    return [
        {
            'accountNo': '5',
            'accountName': 'account name',
            'accountId': 'account-id',
            'accountDescription': 'account description',
            'state': 'ACTIVE',
            'isHidden': False,
            'isTaxable': True,
            'isEntityRequired': False,
            'parentAccountId': -1,
            'attributeId': 1,
            'fsName': 'fsName',
            'fsMappingId': 'fsMapping',
            'fundId': 'a-unique-fund-id'
        },
        {
            'accountNo': '6',
            'accountName': 'account name-2',
            'accountId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
            'accountDescription': 'account description',
            'state': 'ACTIVE',
            'isHidden': False,
            'isTaxable': True,
            'isEntityRequired': False,
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

def select_by_id(id):
    if id == "a92bde1e-7825-429d-aaae-909f2d7a8df1":
        return {
                'accountNo': '5',
                'accountName': 'account name',
                'accountId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'accountDescription': 'account description',
                'state': 'UNUSED',
                'isHidden': False,
                'isTaxable': True,
                'isEntityRequired': False,
                'parentAccountId': -1,
                'attributeId': 1,
                'fsName': 'fsName',
                'fsMappingId': 'fsMapping',
                'fundId': 'a-unique-fund-id'
            }
    
    if id == "a92bde1e-7825-429d-aaae-909f2d7a8df5":
        return {
                'accountNo': '5',
                'accountName': 'account name',
                'accountId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'accountDescription': 'account description',
                'state': 'ACTIVE',
                'isHidden': False,
                'isTaxable': True,
                'isEntityRequired': False,
                'parentAccountId': -1,
                'attributeId': 1,
                'fsName': 'fsName',
                'fsMappingId': 'fsMapping',
                'fundId': 'a-unique-fund-id'
            }

    return None

def update_by_id(*args):
    return None
