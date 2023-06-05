def select_by_ledger_id(id):
    return [
        {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "journalEntryId": "ab72493c-eb7c-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 1,
            "reference": "journal reference",
            "memo": "journal memo",
            "adjustingJournalEntry": True,
            "state": "COMMITTED",
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

def get_line_items(id):
    return [
        {
            "accountNo": "5555602528",
            "lineItemNo": 1,
            "memo": "memo",
            "entityId": "1234123",
            "type": "CREDIT",
            "amount": 1000
        },
        {
            "accountNo": "5555602528",
            "lineItemNo": 2,
            "memo": "memo",
            "entityId": "1234123",
            "type": "DEBIT",
            "amount": 1000
        }
      ]

def get_attachments(id):
    return [
        {
            "documentId": "This is the id",
            "documentMemo": "Memo"
        }
    ]

def select_by_id(id):
    if id == "a92bde1e-7825-429d-aaae-909f2d7a8df2":
        return {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "journalEntryId": "33c20245-fb52-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 2,
            "reference": "Reference",
            "memo": "memo",
            "adjustingJournalEntry": False,
            "state": "COMMITTED",
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
    return 'a unique id'

def update_by_id(id, input):
    return

def delete_by_id(id):
    return

def select_lines_by_journals(id):
    return [
        {
            "id" : 5,
            "uuid" : "de19982b-fc09-11ed-9a6e-0a3efd619f29",
            "account_id" : 67,
            "journal_entry_id" : 12,
            "line_number" : 1,
            "memo" : "memo",
            "entity_id" : "1234123",
            "posting_type" : "credit",
            "amount" : 1000.0,
            "created_at" : "2023-05-26 21:11:22",
            "state" : "COMMITED"
	    }
    ]

def select_attachments_by_journals(id):
    return [
        {
		    "id" : 2,
		    "uuid" : "This is the id",
		    "journal_entry_id" : 16,
		    "memo" : "Memo",
		    "created_at" : "2023-05-26 22:08:38"
	    }
    ]