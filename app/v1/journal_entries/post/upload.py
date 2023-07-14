"""
This Lambda is responsible for serving the journal entries POST request
"""
import json

# pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries, ledgers, accounts
from models import BulkJournalEntryPost, BulkLineItemPost, LineItemPost, AttachmentPost, JournalEntryPost
from validate_new_journal_entry import sum_line_items
from shared import endpoint, dataclass_error_to_str
from shared.bulk import download_from_s3
# pylint: enable=import-error


@endpoint
def handler(
    event, context
) -> tuple[int, dict]:  # pylint: disable=unused-argument; Required lambda parameters
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
    except (
        Exception
    ):  # pylint: disable=broad-exception-caught; Unhandled exception is not allowed
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
        journal_entries_list, ledger_lookup = __add_ledger_ids_to_journals(journal_entries_list)
    except Exception as e:
        return 400, {"detail": str(e)}

    # extract and transform account name to ID
    try:
        journal_entries_list, accounts_lookup = __add_account_ids_to_line_items(journal_entries_list)
    except Exception as e:
        return 400, {"detail": str(e)}

    # ensure journal entry IDs are unique within submission
    valid, reason = __validate_journal_entry_numbers(journal_entries_list)
    if valid is False:
        return 400, {"detail": reason}

    try:
        journal_entries_list = __validate_bulk_line_items(journal_entries_list)
    except Exception as e:
        return 400, {"detail": str(e)}

    post_entries = []
    ledger_journal_entry_num_lookup = {}
    for journal_entry in journal_entries_list:
        journal_entry.pop("fundId")
        journal_entry.pop("decimals")

        # validate the POST contents
        try:
            post = JournalEntryPost(**journal_entry)
        except Exception as e: # pylint: disable=broad-exception-caught; Unhandled exception not allowed
            return 400, {"detail": dataclass_error_to_str(e)}

        if len(post.lineItems) == 0:
            return 400, {"detail": "Journal entry is missing line items."}

        ledger = ledger_lookup.get(post.ledgerId)
        if post.journalEntryNum is not None:
            existing_nums = ledger_journal_entry_num_lookup.get(ledger["uuid"])
            if existing_nums is None:
                ledger_journal_entry_num_lookup[ledger["uuid"]] = journal_entries.select_numbers_in_ledger(ledger["fund_entity_id"])
                existing_nums = ledger_journal_entry_num_lookup.get(ledger["uuid"])

            if post.journalEntryNum in existing_nums:
                return 400, {"detail": f"Journal entry number is not unique: {post.journalEntryNum}"}

        type_safe_line_items = []
        line_item_no = 0
        for item in post.lineItems:
            line_item_no += 1
            try:
                line_item_post = LineItemPost(**item)
                type_safe_line_items.append(
                    {"lineItemNo": line_item_no, **line_item_post.__dict__}
                )
            except Exception as e: # pylint: disable=broad-exception-caught; Unhandled exception not allowed
                return 400, {"detail": dataclass_error_to_str(e)}

        post.lineItems = type_safe_line_items

        type_safe_attachments = []
        for attachment in post.attachments:
            try:
                attachment = AttachmentPost(**attachment)
                type_safe_attachments.append(attachment.__dict__)
            except Exception as e: # pylint: disable=broad-exception-caught; Unhandled exception not allowed
                return 400, {"detail": dataclass_error_to_str(e)}

        post.attachments = type_safe_attachments

        if sum_line_items(type_safe_line_items) != 0:
            return 400, {"detail": f"Line items do not sum to 0 for journal entry number: {post.journalEntryNum}"}

        post_entries.append({"state": "DRAFT", **post.__dict__})

    # insert the new account
    result = journal_entries.bulk_insert(post_entries)

    __update_draft_accounts(accounts_lookup.values())
    __update_draft_ledgers(ledger_lookup.values())
    return 201, {"journalEntryIds": result}



def __update_draft_accounts(accounts_: list):
    """Check to see if line items still exist for old accounts"""
    for acct in accounts_:
        line_items_count = accounts.get_line_items_count(acct["id"])
        if line_items_count > 0 and acct["state"] not in ["POSTED", "DRAFT"]:
            accounts.update_by_id(acct["uuid"], {"state": "DRAFT"})


def __update_draft_ledgers(ledgers_: list):
    """Replace ledger state with UNUSED if no journal entries exist for it"""
    for ledger in ledgers_:
        journal_entries_ = journal_entries.select_by_ledger_id(ledger["id"])
        if len(journal_entries_) > 0 and ledger["state"] not in ["POSTED", "DRAFT"]:
            ledgers.update_by_id(
                ledger["uuid"],
                {"state": "DRAFT"}
            )

def __add_ledger_ids_to_journals(journal_entry_list):
    """Retrieve ledgerIds from db for journal entries"""
    ledgers_dict = {}
    return_ledgers_dict = {}
    new_list = []
    for entry in journal_entry_list:
        fund = entry.get("fundId")
        ledgerName = entry.pop("ledgerName")
        entry.pop("clientId")

        ledger_key = f"{fund}+{ledgerName}"
        ledger = ledgers_dict.get(ledger_key)
        if not ledger:
            ledger = ledgers.select_by_fund_and_name(fund, ledgerName, translate=False)

            if ledger is None:
                raise Exception(
                    f"Cannot find ledger name ({ledgerName}) in fund: {fund}"
                )
            ledgers_dict[ledger_key] = ledger
            return_ledgers_dict[ledger["uuid"]] = ledger

        new_list.append(
            {
                **entry,
                "ledgerId": ledger["uuid"],
                "decimals": ledger["decimals"],
            }
        )
    return new_list, return_ledgers_dict


def __validate_journal_entry_numbers(journal_entry_list):
    """Ensure submitted journal entry IDs are unique in the list"""
    numbers = []
    for entry in journal_entry_list:
        journal_number = entry.get("journalEntryNum")
        if journal_number is None:
            continue

        if journal_number in numbers:
            return (
                False,
                f"Submission includes duplicate journal entry numbers: {entry['journalEntryNum']}",
            )

        numbers.append(journal_number)

    return True, None


def __add_account_ids_to_line_items(journal_entry_list):
    """Add account ids to line items using fundId and account name"""
    funds = []
    accounts_dict = {}
    return_accounts_dict = {}

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
            
            if not return_accounts_dict.get(account["uuid"]):
                return_accounts_dict[account["uuid"]] = account
        new_list.append({**entry, "lineItems": new_line_items})

    return new_list, return_accounts_dict


def __validate_bulk_line_items(journal_entries_list):
    """Line item amounts will come in as floats, but we need ints"""
    modified_journal_entries = []
    for entry in journal_entries_list:
        modified_line_items = []
        for item in entry["lineItems"]:
            try:
                type_safe_line_item = BulkLineItemPost(
                    **item, decimals=entry["decimals"]
                ).__dict__

                type_safe_line_item.pop("decimals")
                modified_line_items.append(type_safe_line_item)
            except Exception as e:
                raise Exception(dataclass_error_to_str(e))
        entry["lineItems"] = modified_line_items
        modified_journal_entries.append(entry)

    return modified_journal_entries
