def get_trial_balance_detail(filter):
    return [
        {
          "fundId": "fund_uuid",
          "accountId": "account_uuid",
          "parentAccountId": "parent_uuid",
          "journalEntryNum": "journal_entry_num",
          "accountName": "account_name",
          "accountNo": "account_no",
          "displayName": "account_app_name",
          "attributeId": "attribute_uuid",
          "lineNumber": "line_number",
          "memo": "memo",
          "ledgerId": "ledger_uuid",
          "currency": "currency",
          "decimals": "decimals",
          "journalEntryPostDated": "journal_entry_post_date",
          "adjustingJournalEntry": "adjusting_journal_entry",
          "journalEntryState": "journal_entry_state",
          "journalEntryDate": "journal_entry_date",
          "amount": "amount",
          "entityId": "entity_id",
          "ledgerName": "ledger_name",
        }
    ]