from models import JournalEntryPost, LineItemPost, AttachmentPost
from arkdb import accounts, ledgers
from shared import dataclass_error_to_str

def validate_new_journal_entry(journal_entry):
    # Check for missing details
    if journal_entry.get('ledgerId') is None:
        return 400, "No ledger specified.", None

    # validate the POST contents
    try:
        post = JournalEntryPost(**journal_entry)
    except Exception as e:
        return 400, dataclass_error_to_str(e), None

    if len(post.lineItems) == 0:
        return 400, "Journal entry is missing line items.", None

    # validate that the ledger exists
    ledger = ledgers.select_by_id(post.ledgerId)
    if ledger is None:
        return 400, "Specified ledger does not exist.", None

    accts = accounts.select_by_fund_id(ledger["fundId"])
    acct_numbers = [acct["accountNo"] for acct in accts]

    type_safe_line_items = []
    line_item_no = 0
    for item in post.lineItems:
        line_item_no += 1
        try:
            line_item_post = LineItemPost(**item)
            type_safe_line_items.append({"lineItemNo": line_item_no, **line_item_post.__dict__})
        except Exception as e:
            return 400, dataclass_error_to_str(e), None
        
        if line_item_post.accountNo not in acct_numbers:
            return 400, f"Line item references invalid account: {line_item_post.accountNo}", None
  
    post.lineItems = type_safe_line_items

    type_safe_attachments = []
    for attachment in post.attachments:
        try:
            attachment = AttachmentPost(**attachment)
            type_safe_attachments.append(attachment.__dict__)
        except Exception as e:
            return 400, dataclass_error_to_str(e), None
        
    post.attachments = type_safe_attachments

    if sum_line_items(type_safe_line_items) != 0:
        return 400, "Line items do not sum to 0.", None

    return 201, '', {'state': "DRAFT", **post.__dict__}


def sum_line_items(line_items):
    sum = 0
    for item in line_items:
        if item["type"] == "CREDIT":
            sum += item["amount"]
        else:
            sum -= item["amount"]

    return sum
