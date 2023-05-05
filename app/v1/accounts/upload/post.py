import json

from arkdb import accounts, account_attributes, funds  # pylint: disable=import-error
from shared import (
    endpoint
)
from shared.accounts.csv import download_from_s3, convert_csv_to_dicts  # pylint: disable=import-error
from shared.accounts import sort_accounts_for_insert, validate_new_account  # pylint: disable=import-error
from shared import validate_uuid  # pylint: disable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]:
    """Handler for the accounts upload request

    event: dict
    POST event passed in from API gateway. The key 'body' should
    cary the POST request as a JSON string

    context: LambdaContext
    Context about the instance of the lambda function
    """

    # validate the request body
    try:
        body = json.loads(event['body'])
    except:
        return 400, {'detail': "Body does not contain valid json."}

    # validate the url is present
    url = body.get("signedS3Url")
    if not url:
        return 400, {'detail': "Body does not contain a signedS3Url."}

    # validate the fundId is present
    fund_id = body.get("fundId")
    if not fund_id:
        return 400, {'detail': "Body does not contain a fund ID."}

    # check that the fundId is a valid uuid
    if not validate_uuid(fund_id):
        return 400, {'detail': "Invalid UUID."}

    # check that the fund exists in the database
    fund = funds.select_by_uuid(fund_id)
    if not fund:
        return 404, {'detail': "Fund does not exist."}

    # check that accounts don't already exist in target fund
    accts = accounts.select_by_fund_id(fund_id)
    if len(accts) > 0:
        return 409, {'detail': "Accounts already exist in destination fund."}

    # try to download contents of the csv
    try:
        contents = download_from_s3(url)
    except:
        return 400, {'detail': "Could not reach url."}

    if not contents:
        return 400, {'detail': "No access to content"}

    # transform accountType fields into attributeIds
    account_dicts = convert_csv_to_dicts(contents)
    attributes = account_attributes.select_all()
    linked_accounts = link_attributes(account_dicts, attributes)

    # sort accounts for correct insertion order
    sorted_accounts = sort_accounts_for_insert(
        linked_accounts,
        parent_id_field="parentAccountNo",
        child_id_field="accountNo"
    )
 
    # post one account at a time, tracking UUIDs as they're recorded
    # for child accounts
    uuid_lookup = {}
    for acct in sorted_accounts:
        parent_no = acct.pop('parentAccountNo')
        acct.pop('arkTransaction')

        acct['fundId'] = fund_id

        if parent_no in uuid_lookup.keys():
            acct['parentAccountId'] = uuid_lookup[parent_no]

        code, detail, post = validate_new_account(acct)
        if code != 201:
            return code, {'detail': detail}

        # insert the new account and retain accountId mapping
        uuid_lookup[post['accountNo']] = accounts.create_new(post)

    return code, {'accountIds': list(uuid_lookup.values())}


def link_attributes(account_dicts: list[dict], attributes: list[dict]) -> list[dict]:
    """
    Input CSV files will use accountType instead of attributeId. Match
    attribute IDs to the accounts which are attempting to use them and
    return dicts with valid attributeIds and without accountType fields
    """
    attribute_lookup = {}
    for att in attributes:
        attribute_lookup[att['accountType']] = att['attributeId']

    for account in account_dicts:
        accountType = account.pop('accountType')
        account['attributeId'] = attribute_lookup[accountType]

    return account_dicts
