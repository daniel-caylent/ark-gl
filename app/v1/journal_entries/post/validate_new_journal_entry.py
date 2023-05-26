from models import JournalEntryPost, LineItemPost, AttachmentPost
from arkdb import accounts, journal_entries, ledgers
def validate_new_journal_entry(journal_entry):
    # Check for missing details
    if journal_entry.get('ledgerId') is None:
        return 400, "No ledger specified.", None

    # validate the POST contents
    try:
        post = JournalEntryPost(**journal_entry)
    except Exception as e:
        remove_str = "__init__() got an "
        error_str = str(e).replace(remove_str, '')
        return 400, error_str[0].upper() + error_str[1:], None

    # validate that the ledger exists
    ledger = ledgers.select_by_id(post.ledgerId)
    if ledger is None:
        return 400, "Specified ledger does not exist.", None

    # check uniqueness of journal entry
    journal_entries_ = journal_entries.select_by_ledger_id(post.ledgerId)
    unique = validate_unique_journal_entry(post, journal_entries_)
    if unique is False:
        return 409, "journalEntryNo already exists in this fund.", None

    accts = accounts.select_by_fund_id(ledger["fundId"])
    acct_numbers = [acct["accountNo"] for acct in accts]

    type_safe_line_items = []
    for item in post.lineItems:
        try:
            line_item_post = LineItemPost(**item)
            type_safe_line_items.append(line_item_post.__dict__)
        except Exception as e:
            remove_str = "__init__() got an "
            error_str = str(e).replace(remove_str, '')
            return 400, error_str[0].upper() + error_str[1:], None
        
        if line_item_post.accountNo not in acct_numbers:
            return 400, f"Line item references invalid account. Line item number: {line_item_post.lineItemNo}", None
  
    type_safe_attachments = []
    for attachment in post.attachments:
        try:
            attachment = AttachmentPost(**attachment)
            type_safe_attachments.append(attachment.__dict__)
        except Exception as e:
            remove_str = "__init__() got an "
            error_str = str(e).replace(remove_str, '')
            return 400, error_str[0].upper() + error_str[1:], None
        

    if sum_line_items(type_safe_line_items) != 0:
        return 400, "Line items do not sum to 0.", None

    type_safe_post = post.__dict__
    type_safe_post["attachments"] = type_safe_attachments
    type_safe_post["lineItems"] = type_safe_line_items

    return 201, '', {'state': "DRAFT", **type_safe_post}


def validate_unique_journal_entry(post, existing_journal_entries):
    for entry in existing_journal_entries:
        if entry['journalEntryNo'] == post.journalEntryNo:
            return False

def sum_line_items(line_items):
    sum = 0
    for item in line_items:
        if item["type"] == "CREDIT":
            sum += item["amount"]
        else:
            sum -= item["amount"]

    return sum
