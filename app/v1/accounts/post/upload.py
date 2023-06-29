"""
This Lambda is responsible for serving the journal entries POST request
"""
import json

 # pylint: disable=import-error; Lambda layer dependency
from arkdb import account_attributes, accounts
from models import BulkAccountPost
from validate_new_account import validate_new_account
from shared import endpoint, dataclass_error_to_str
from shared.bulk import download_from_s3
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]: # pylint: disable=unused-argument; Required lambda parameters 
    """Handler for the journal entries upload request

    event: dict
    POST event passed in from API gateway. The key 'body' should
    cary the POST request as a JSON string

    context: LambdaContext
    Context about the instance of the lambda function
    """

    # validate the request body
    try:
        body = json.loads(event["body"])
    except Exception: # pylint: disable=broad-exception-caught; Unhandled exception is not allowed
        return 400, {"detail": "Body does not contain valid json."}

    s3_url = body.get("signedS3Url")
    if not s3_url:
        return 400, {"detail": "Missing s3 URL."}
    
    # download from s3
    try:
        download = download_from_s3(s3_url)
        if download is None:
            return 400, {"detail": "Unable to download from S3."}
    except:
        return 400, {"detail": "Unable to download from S3."}
  
    # validate json from file
    try:
        json_dict = json.loads(download)
    except:
        return 400, {"detail": "File contains invalid JSON."}

    accounts_list = json_dict.get("accounts")
    if not accounts_list:
        return 400, {"detail": "No accounts submitted."}

    # validate journal entry bodies
    type_safe_accounts = []
    for account in accounts_list:
        try:
            type_safe_accounts.append(BulkAccountPost(**account).__dict__)
        except Exception as e:
            return 400, {"detail": dataclass_error_to_str(e)}

    account_attributes_list = account_attributes.select_all()

    # extract and replace account attribute name with ID
    try:
        accounts_list = __add_attributes_to_accounts(accounts_list, account_attributes_list)
    except Exception as e:
        return 400, {"detail": str(e)}

    # ensure journal entry IDs are unique within submission
    valid, reason = __validate_account_names_and_numbers(accounts_list)
    if valid is False:
        return 400, {"detail": reason}

    post_entries = []
    for account in accounts_list:
        parent = account.pop("parentAccountNo")
        fs_mapping = account.pop("fsMappingNo")

        code, detail, post = validate_new_account(account)

        if code != 201:
            return code, {"detail": detail}
        
        post_entries.append({**post, "parentAccountNo": parent, "fsMappingNo": fs_mapping})

    # insert the new account
    result = accounts.bulk_insert(post_entries)
    return code, {"accountIds": result}

def __add_attributes_to_accounts(accounts_list: list, account_attributes_list: list):
    """Convert account attribute names in IDs"""
    attribute_lookup = {}
    for attribute in account_attributes_list:
        attribute_lookup[attribute["accountType"]] = attribute

    new_list = []
    for account in accounts_list:
        attribute_type = account.pop("attributeType")

        attribute = attribute_lookup.get(attribute_type)
        if not attribute:
            raise Exception(f"Cannot find attribute by type: {attribute_type}")

        new_list.append({**account, "attributeId": attribute["attributeId"]})

    print(f"NEW LIST: {new_list}")
    return new_list

def __validate_account_names_and_numbers(accounts_list):
    """Ensure submitted journal entry IDs are unique in the list"""
    fund_lookup = {}

    for account in accounts_list:
        if account["fundId"] not in fund_lookup:
            fund_lookup[account["fundId"]] = accounts.select_by_fund_id(account["fundId"])
        
        fund_lookup[account["fundId"]] += [account]
    
    for fund in fund_lookup.values():
        name_list = []
        number_list = []
        for account in fund:
            if account["accountName"] not in name_list:
                name_list.append([account["accountName"]])
            else:
                return False, f"Duplicate account name: {account['accountName']}"
            
            if account["accountNo"] not in number_list:
                number_list.append([account["accountNo"]])
            else:
                return False, f"Duplicate account number: {account['accountNo']}"

    return True, None
