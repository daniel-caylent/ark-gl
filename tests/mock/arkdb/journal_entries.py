import datetime

def select_by_ledger_id(id):
    """Mock select by ledger id for journal entries"""
    return [
        {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "fundId": 1,
            "journalEntryId": "ab72493c-eb7c-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 1,
            "reference": "journal reference",
            "memo": "journal memo",
            "adjustingJournalEntry": True,
            "state": "POSTED",
            "date": datetime.date.today(),
            "postDate": datetime.datetime.now(),
            "attachments": [],
            "lineItems": [],
            "id": 1,
            "currencyName": "USD",
            "currencyDecimal": 2
        },
        {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "fundId": 1,
            "journalEntryId": "33c20245-fb52-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 2,
            "reference": "Reference",
            "memo": "memo",
            "adjustingJournalEntry": False,
            "state": "DRAFT",
            "date": datetime.date.today(),
            "postDate": None,
            "attachments": [],
            "lineItems": [],
            "id": 2,
            "currencyName": "USD",
            "currencyDecimal": 2
        },
    ]


def select_by_ledger_id_paginated(*args, **kwargs):
    return {
        "total_items": 2,
        "total_pages": 1,
        "current_page": 1,
        "data": select_by_ledger_id(None)
    }

def select_by_fund_id(id):
    """Mock select by ledger id for journal entries"""
    return [
        {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "fundId": 1,
            "journalEntryId": "ab72493c-eb7c-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 1,
            "reference": "journal reference",
            "memo": "journal memo",
            "adjustingJournalEntry": True,
            "state": "POSTED",
            "date": datetime.date.today(),
            "postDate": datetime.datetime.now(),
            "attachments": [],
            "lineItems": [],
            "id": 1,
            "currencyName": "USD",
            "currencyDecimal": 2
        },
        {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "fundId": 1,
            "journalEntryId": "33c20245-fb52-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 2,
            "reference": "Reference",
            "memo": "memo",
            "adjustingJournalEntry": False,
            "state": "DRAFT",
            "date": datetime.date.today(),
            "postDate": None,
            "attachments": [],
            "lineItems": [],
            "id": 2,
            "currencyName": "USD",
            "currencyDecimal": 2
        },
    ]

def get_line_items(id, translate=True):
    """Mock select get_line_items for journal entries"""
    return [
        {
            "accountNo": "5555602528",
            "accountId": 1,
            "lineItemNo": 1,
            "journal_entry_id": 1,
            "memo": "memo",
            "entityId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
            "type": "CREDIT",
            "amount": 1000
        },
        {
            "accountNo": "5555602528",
            "accountId": 1,
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
    if not translate:
        if id == "a92bde1e-7825-429d-aaae-909f2d7a8df2":
            return {
                "ledger_id": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
                "fund_id": 1,
                "uuid": "33c20245-fb52-11ed-9a6e-0a3efd619f29",
                "journal_entry_num": 2,
                "reference": "Reference",
                "memo": "memo",
                "adjusting_journal_entry": False,
                "state": "POSTED",
                "date": datetime.date.today(),
                "post_date": None,
                "attachments": [],
                "line_items": [],
                "id": 2,
                "currency": "USD",
                "decimals": 2
            }
        return {
                "ledger_id": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
                "fund_id": 1,
                "uuid": "33c20245-fb52-11ed-9a6e-0a3efd619f29",
                "journal_entry_num": 2,
                "reference": "Reference",
                "memo": "memo",
                "adjusting_journal_entry": False,
                "state": "DRAFT",
                "date": datetime.date.today(),
                "post_date": None,
                "attachments": [],
                "line_items": [],
                "id": 2,
                "currency": "USD",
                "decimals": 2
            }
    if id == "a92bde1e-7825-429d-aaae-909f2d7a8df2":
        return {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "fundId": 1,
            "journalEntryId": "33c20245-fb52-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 2,
            "reference": "Reference",
            "memo": "memo",
            "adjustingJournalEntry": False,
            "state": "POSTED",
            "date": datetime.date.today(),
            "postDate": None,
            "attachments": [],
            "lineItems": [],
            "id": 2,
            "currencyName": "USD",
            "currencyDecimal": 2
        }

    return {
            "ledgerId": "ab353519-eb7c-11ed-9a6e-0a3efd619f29",
            "fundId": 1,
            "journalEntryId": "33c20245-fb52-11ed-9a6e-0a3efd619f29",
            "journalEntryNum": 2,
            "reference": "Reference",
            "memo": "memo",
            "adjustingJournalEntry": False,
            "state": "DRAFT",
            "date": datetime.date.today(),
            "postDate": None,
            "attachments": [],
            "lineItems": [],
            "id": 2,
            "currencyName": "USD",
            "currencyDecimal": 2
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

def bulk_insert(journal_entries):
    return None

def commit_by_id(*args):
    return None

def select_with_filter_paginated(filter, page=None, page_size=None, sort=None):
    return {
        "data": [
            {
                'id': 48654,
                'journalEntryNum': 1462,
                'journalEntryId':
                '3b184ece-a05b-4caf-8bd9-1607281b9fb4',
                'ledgerId': 'a4c789c6-219b-11ee-b49c-0a3efd619f29',
                'date': datetime.date.today(),
                'reference': '',
                'memo': 'This is a memo',
                'adjustingJournalEntry': 0,
                'state': 'DRAFT',
                'postDate': None,
                'currencyName': 'USD',
                'currencyDecimal': 2,
                'fundId': 'a7e61775-9d15-4ebf-b88d-24dcc3cfffc3'
            }
        ],
        "total_pages": 10,
        "total_items": 10,
        "current_page": 1
    }