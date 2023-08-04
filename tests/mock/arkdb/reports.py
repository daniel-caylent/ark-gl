import datetime

def get_trial_balance_detail(filter):
    return [
        {
          "fundId": "fund_uuid",
          "accountId": "account_uuid",
          "parentAccountId": None,
          "journalEntryNum": 198,
          "accountName": "account_name",
          "accountNo": "account_no",
          "attributeId": "attribute_uuid",
          "lineNumber": 5,
          "memo": "memo",
          "ledgerId": "ledger_uuid",
          "currency": "USD",
          "decimals": 2,
          "journalEntryPostDated": "journal_entry_post_date",
          "adjustingJournalEntry": "adjusting_journal_entry",
          "journalEntryState": "journal_entry_state",
          "journalEntryDate": datetime.date.today(),
          "amount": 100,
          "entityId": "entity_id",
          "ledgerName": "ledger_name",
          "accountState": "DRAFT",
          "fsMappingId": None,
          "fsName": None,
          "fsMappingStatus": None,
          "isTaxable": False,
          "isEntityRequired": False,
          "accountType": None,
          "detailType": None,
          "accountPostDate": None
        }
    ]

def get_start_balance(uuid, date):
    return 0

def get_end_balance(uuid, date):
    return 0