def select_by_fund_id(fund_id, translate=True):
    # used for account upload and copy
    if fund_id == "d4b26bbb-e51a-11ed-aede-0247c1ed2ee1":
        return []

    if not translate:
        return [
            {
                'id':1,
                'account_no': '5555',
                'name': 'account name',
                'account_id': 'account-id',
                'uuid': 'a92bde1e-7825-429d-aaae-909f2d7a8df1',
                'accountDescription': 'account description',
                'state': 'ACTIVE',
                'isTaxable': True,
                'is_entity_required': False,
                'parentAccountId': None,
                'attributeId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'fsName': 'fsName',
                'fsMappingId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'fsMappingStatus': "MAPPED",
                'fundId': 'a-unique-fund-id',
                'postDate': None
            },
            {
                'id': 1,
                'account_no': '6',
                'name': 'Miscellaneous Expensesfranco3.',
                'account_id': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'uuid': 'a92bde1e-7825-429d-aaae-909f2d7a8df1',
                'accountDescription': 'account description',
                'state': 'ACTIVE',
                'isTaxable': True,
                'is_entity_required': False,
                'parentAccountId': None,
                'attributeId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'fsName': 'fsName',
                'fsMappingId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'fsMappingStatus': "MAPPED",
                'fundId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'postDate': None
            }
        ]

    return [
        {
            'accountNo': '5555',
            'accountName': 'account name',
            'accountId': 'account-id',
            'accountDescription': 'account description',
            'state': 'ACTIVE',
            'isTaxable': True,
            'isEntityRequired': False,
            'parentAccountId': None,
            'attributeId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
            'fsName': 'fsName',
            'fsMappingId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
            'fsMappingStatus': "MAPPED",
            'fundId': 'a-unique-fund-id',
            'postDate': None
        },
        {
            'accountNo': '6',
            'accountName': 'account name-2',
            'accountId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
            'accountDescription': 'account description',
            'state': 'ACTIVE',
            'isTaxable': True,
            'isEntityRequired': False,
            'parentAccountId': None,
            'attributeId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
            'fsName': 'fsName',
            'fsMappingId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
            'fsMappingStatus': "MAPPED",
            'fundId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
            'postDate': None
        }
    ]

def select_by_name(name):
    return []

def create_new(account):
    return "a92bde1e-7825-429d-aaae-909f2d7a8df1"

def select_by_id(id, translate=True):
    if id == "a92bde1e-7825-429d-aaae-909f2d7a8df1":
        return {
                'accountNo': '5',
                'accountName': 'account name',
                'accountId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'accountDescription': 'account description',
                'state': 'UNUSED',
                'isTaxable': True,
                'isEntityRequired': False,
                'parentAccountId': None,
                'attributeId': 1,
                'fsName': 'fsName',
                'fsMappingId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'fsMappingStatus': "MAPPED",
                'fundId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'postDate': None
            }
    
    if id == "a92bde1e-7825-429d-aaae-909f2d7a8df5":
        return {
                'accountNo': '5',
                'accountName': 'account name',
                'accountId': "a92bde1e-7825-429d-aaae-909f2d7a8df1",
                'accountDescription': 'account description',
                'state': 'POSTED',
                'isTaxable': True,
                'isEntityRequired': False,
                'parentAccountId': None,
                'attributeId': 1,
                'fsName': 'fsName',
                'fsMappingId': None,
                'fsMappingStatus': "SELF-MAPPED",
                'fundId': 'a-unique-fund-id',
                'postDate': None
            }

    return None

def update_by_id(*args):
    return None

def get_line_items(*args):
    return []

def commit_by_id(*args):
    return None

def bulk_insert(accounts_list):
    return ["id", "id2"]

def bulk_update(accounts_list):
    return None

def delete_by_id(id_):
    return None

def bulk_delete(id_list):
    return None

def get_line_items_count(uuid):
    return 0

def get_parent_accounts_from_list(uuid_list):
    return []

def get_child_accounts_from_list(uuid_list):
    return []