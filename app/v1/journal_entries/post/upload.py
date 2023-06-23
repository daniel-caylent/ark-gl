"""
This Lambda is responsible for serving the journal entries POST request
"""
import json

 # pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries, ledgers, accounts
from models import BulkJournalEntryPost
from validate_new_journal_entry import validate_new_journal_entry
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

    journal_entries_list = json_dict.get("journalEntries")
    if not journal_entries_list:
        return 400, {"detail": "No journal entries submitted."}

    # validate journal entry bodies
    for entry in journal_entries_list:
        try:
            BulkJournalEntryPost(**entry)
        except Exception as e:
            return 400, {"detail": dataclass_error_to_str(e)}

    # extract and replace ledger name with ID
    try:
        journal_entries_list = __add_ledger_ids_to_journals(journal_entries_list)
    except Exception as e:
        return 400, {"detail": str(e)}
  
    # extract and transform account name to ID
    try:
        journal_entries_list = __add_account_ids_to_line_items(journal_entries_list)
    except Exception as e:
        return 400, {"detail": str(e)}

    # ensure journal entry IDs are unique within submission
    valid, reason = __validate_journal_entry_ids(journal_entries_list)
    if valid is False:
        return 400, {"detail": reason}

    post_entries = []
    for journal_entry in journal_entries_list:
        journal_entry.pop("fundId")

        code, detail, post = validate_new_journal_entry(journal_entry)

        if code != 201:
            return code, {"detail": detail}
        
        post_entries.append(post)

    # insert the new account
    result = journal_entries.bulk_insert(post_entries)
    return code, {"journalEntryIds": result}

def __add_ledger_ids_to_journals(journal_entry_list):
    """Retrieve ledgerIds from db for journal entries"""
    ledgers_dict = {}
    new_list = []
    for entry in journal_entry_list:
        fund = entry.get("fundId")
        ledgerName = entry.pop("ledgerName")
        entry.pop("clientId")

        ledger_key = f"{fund}+{ledgerName}"
        ledger = ledgers_dict.get(ledger_key)
        if not ledger:
            ledger = ledgers.select_by_fund_and_name(fund, ledgerName)

            if ledger is None:
                raise Exception(f"Cannot associate with ledger: {ledger_key}")
            ledgers_dict[ledger_key] = ledger

        new_list.append({**entry, "ledgerId": ledger["ledgerId"]})
    return new_list

def __validate_journal_entry_ids(journal_entry_list):
    """Ensure submitted journal entry IDs are unique in the list"""
    numbers = []
    for entry in journal_entry_list:
        journal_number = entry.get("journalEntryNum")
        if journal_number is None:
            continue

        if journal_number in numbers:
            return False, f"Submission includes duplicate journal entry numbers: {entry['journalEntryNum']}"

        numbers.append(journal_number)

    return True, None

def __add_account_ids_to_line_items(journal_entry_list):
    """Add account ids to line items using fundId and account name"""
    funds = []
    accounts_dict = {}

    new_list = []
    for entry in journal_entry_list:
        if entry["fundId"] not in funds:
            funds.append(entry["fundId"])
            accounts_list = accounts.select_by_fund_id(entry["fundId"], translate=False)
            for account in accounts_list:
                account_key = f"{entry['fundId']}+{account['name']}"
                accounts_dict[account_key] = account
        
        new_line_items = []
        for item in entry.pop("lineItems"):
            account_name = item.pop("accountName")
            account_key = f"{entry['fundId']}+{account_name}"
            account = accounts_dict.get(account_key)
            
            if account is None:
                raise Exception(f"Unable to locate account by name: {account_name}")
            new_line_items.append({**item, "accountId": account["uuid"]})
        new_list.append({**entry, "lineItems": new_line_items})
    
    return new_list