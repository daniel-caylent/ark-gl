from shared import endpoint

from models import Account

@endpoint
def handler(event, context):
    fund_id = event['queryStringParameters'].get('fundId', None)
    if fund_id is None:
        return 400, {'detail': "No fund specified."}

    # results = db.get_accounts_by_fund_id(fund_id)
    results = [
        {
            'accountNo': 5,
            'accountName': 'account name',
            'accountId': 'account id',
            'accountDescription': 'account description',
            'state': 'ACTIVE',
            'isHidden': False,
            'isTaxable': True,
            'isVendorCustomerPartnerRequired': False,
            'parrentAccountNo': -1,
            'attributeNo': 1
        },
        {
            'accountNo': 5,
            'accountName': 'account name',
            'accountId': 'account id',
            'accountDescription': 'account description',
            'state': 'ACTIVE',
            'isHidden': False,
            'isTaxable': True,
            'isVendorCustomerPartnerRequired': False,
            'parrentAccountNo': -1,
            'attributeNo': 1
        }
    ]

    accounts = [Account(**acct) for acct in results]

    return 200, {'data': accounts}
