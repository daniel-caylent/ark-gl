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
    if id == "df0f2420-0bbf-11ee-b49c-0a3efd619f29":
        return {
                    "id": 282,
                    "journal_entry_num": 1,
                    "uuid": "df0f2420-0bbf-11ee-b49c-0a3efd619f29",
                    "ledger_id": "9876ce18-0bbe-11ee-b49c-0a3efd619f29",
                    "date": "2023-06-15",
                    "reference": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "memo": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "adjusting_journal_entry": 1,
                    "state": "POSTED",
                    "is_hidden": 0,
                    "post_date": "2023-06-15 21:02:14",
                    "created_at": "2023-06-15 21:02:00",
                    "currency": "EUR",
                    "decimals": 2,
                    "fund_entity_id": "c6bb22f3-e5d5-4192-b19b-1acc0c22a49f"
        }
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

def select_line_by_number_journal(line_number, journal_entry_id):
    
    if line_number == 1:
        return {
                        "id": 2842,
                        "uuid": "df114736-0bbf-11ee-b49c-0a3efd619f29",
                        "account_id": "a16df5a0-0bbe-11ee-b49c-0a3efd619f29",
                        "account_no": "205",
                        "account_name": "If we calculate the microchip, we can get to the SQL array through the wireless PNG transmitter!",
                        "journal_entry_id": 282,
                        "line_number": 1,
                        "memo": "5aeb268f89e4d786d58ac87f1014ada3870276e9c1b235708330353a3b22b9c3",
                        "entity_id": "49dd9637-05da-4eec-98c9-bcbc5cbec2a4",
                        "posting_type": "CREDIT",
                        "amount": 6000,
                        "created_at": "2023-06-15 21:02:00"
                        }
    elif line_number == 2:
        return {
                        "id": 2843,
                        "uuid": "df13e3f1-0bbf-11ee-b49c-0a3efd619f29",
                        "account_id": "a3b52965-0bbe-11ee-b49c-0a3efd619f29",
                        "account_no": "423",
                        "account_name": "The SAS capacitor is down, transmit the cross-platform pixel so we can compress the XML bandwidth!",
                        "journal_entry_id": 282,
                        "line_number": 2,
                        "memo": "b4080d9cefc1bb10af86f0b3715497b987cf93491f05297cabd6d2758b7ddabe",
                        "entity_id": "49dd9637-05da-4eec-98c9-bcbc5cbec2a4",
                        "posting_type": "DEBIT",
                        "amount": 2000,
                        "created_at": "2023-06-15 21:02:00"
                        }
    elif line_number == 3:
        return {
                        "id": 2844,
                        "uuid": "df1591eb-0bbf-11ee-b49c-0a3efd619f29",
                        "account_id": "a3b52965-0bbe-11ee-b49c-0a3efd619f29",
                        "account_no": "423",
                        "account_name": "The SAS capacitor is down, transmit the cross-platform pixel so we can compress the XML bandwidth!",
                        "journal_entry_id": 282,
                        "line_number": 3,
                        "memo": "02e88073eba5e0bdcc2c27718bab05169af40a861f3003fd59415b766f046f91",
                        "entity_id": "49dd9637-05da-4eec-98c9-bcbc5cbec2a4",
                        "posting_type": "DEBIT",
                        "amount": 4000,
                        "created_at": "2023-06-15 21:02:00"
                        }

def select_attachment_by_uuid_journal(doc_id, current_row_id):
    return {
        "id": 252,
        "uuid": "This is the id",
        "journal_entry_id": 282,
        "memo": "3533550468585acb059f7fd8336d9f27e4a6ced3214dec3a5fd34d149c498c5d",
        "created_at": "2023-06-15 21:02:00"
    }

def select_count_commited_journals():
    return {"count(*)": 1}
