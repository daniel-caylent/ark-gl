def select_by_ledger_id(id):
    """Mock select by ledger id for journal entries"""
    return [
        {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "journalEntryId": "ab72493c-eb7c-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 1,
            "reference": "journal reference",
            "memo": "journal memo",
            "adjustingJournalEntry": True,
            "state": "POSTED",
            "date": "2023-05-05 00:00:00",
            "postDate": "2023-05-05 00:00:00",
            "isHidden": False,
            "attachments": [],
            "lineItems": [],
            "id": 1
        },
        {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "journalEntryId": "33c20245-fb52-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 2,
            "reference": "Reference",
            "memo": "memo",
            "adjustingJournalEntry": False,
            "state": "DRAFT",
            "date": "None",
            "postDate": "None",
            "isHidden": False,
            "attachments": [],
            "lineItems": [],
            "id": 2
        },
    ]

def get_line_items(id, translate=True):
    """Mock select get_line_items for journal entries"""
    return [
        {
            "accountNo": "5555602528",
            "lineItemNo": 1,
            "journal_entry_id": 1,
            "memo": "memo",
            "entityId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
            "type": "CREDIT",
            "amount": 1000
        },
        {
            "accountNo": "5555602528",
            "lineItemNo": 2,
            "journal_entry_id": 1,
            "memo": "memo",
            "entityId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
            "type": "DEBIT",
            "amount": 1000
        }
      ]

def get_attachments(id, translate=True):
    """Mock select get_attachments for journal entries"""
    return [
        {
            "documentId": "This is the id",
            "documentMemo": "Memo",
            "journal_entry_id": 1
        }
    ]

def select_by_id(id, translate=True):
    """Mock select select_by_id for journal entries"""
    if id == "a92bde1e-7825-429d-aaae-909f2d7a8df2":
        return {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "journalEntryId": "33c20245-fb52-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 2,
            "reference": "Reference",
            "memo": "memo",
            "adjustingJournalEntry": False,
            "state": "POSTED",
            "date": "None",
            "postDate": "None",
            "isHidden": False,
            "attachments": [],
            "lineItems": [],
            "id": 2
        }

    return {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "journalEntryId": "33c20245-fb52-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 2,
            "reference": "Reference",
            "memo": "memo",
            "adjustingJournalEntry": False,
            "state": "DRAFT",
            "date": "None",
            "postDate": "None",
            "isHidden": False,
            "attachments": [],
            "lineItems": [],
            "id": 2
        }

def create_new(*args):
    """Mock select create_new for journal entries"""
    return 'a unique id'

def update_by_id(id, input):
    """Mock update for journal entries"""
    return

def delete_by_id(id):
    """Mock delete for journal entries"""
    return

def select_lines_by_journals(id):
    """Mock select line by journals for journal entries"""
    return [
        {
            "id" : 5,
            "uuid" : "de19982b-fc09-11ed-9a6e-0a3efd619f29",
            "account_id" : 67,
            "journal_entry_id" : 12,
            "line_number" : 1,
            "memo" : "memo",
            "entity_id" : "a92bde1e-7825-429d-aaae-909f2d7a8df1",
            "posting_type" : "credit",
            "amount" : 1000.0,
            "created_at" : "2023-05-26 21:11:22",
            "state" : "COMMITED"
	    }
    ]

def select_attachments_by_journals(id):
    """Mock select attachments for journal entries"""
    return [
        {
		    "id" : 2,
		    "uuid" : "This is the id",
		    "journal_entry_id" : 16,
		    "memo" : "Memo",
		    "created_at" : "2023-05-26 22:08:38"
	    }
    ]