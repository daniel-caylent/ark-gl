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
          "journalEntryDate": "journal_entry_date",
          "amount": 100,
          "entityId": "entity_id",
          "ledgerName": "ledger_name",
        }
    ]

def get_start_balance(uuid, date):
    return 0