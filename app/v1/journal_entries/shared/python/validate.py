from models import JournalEntryPost
from arkdb import journal_entries
def validate_new_journal_entry(journal_entry):
    from arkdb import accounts, account_attributes, ledgers

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

    # validate that the fund exists and client has access to it
    ledger = ledgers.select_by_id(post.ledgerId)
    if ledger is None:
        return 400, "Specified ledger does not exist.", None

    # check uniqueness of journal entry
    journal_entries_ = journal_entries.select_by_ledger_id(post.ledgerId)
    unique = validate_unique_journal_entry(post, journal_entries_)
    if unique is False:
        return 409, "Account number or name already exists in this fund.", None

    if not validate_line_items(post.lineItems):
        return 400, "Line items are invalid.", None   
  
    if not validate_attachments(post.attachments):
        return 400, "Attachments are invalid.", None     

    return 201, '', {'state': "DRAFT", **post.__dict__}


def validate_unique_journal_entry(post, existing_journal_entries):
    for entry in existing_journal_entries:
        if entry['journalEntryNo'] == post.journalEntryNo:
            return False

def validate_attachments(attachments):
    return True

def validate_line_items(line_items):
    return True
