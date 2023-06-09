from database import report

from .utils import DB_NAME, SECRET_NAME, REGION_NAME

def get_trial_balance(ledger_ids, state, start_date, end_date, hide_zero_balance):
    results = report.select_trial_balance(
        DB_NAME,
        {
            "journalEntryState": state,
            "hideZeroBalance": hide_zero_balance,
            "ledgerId": ledger_ids,
            "startDay": start_day,
            "endDay": end_day
        },
        REGION_NAME,
        SECRET_NAME
    )

    return results