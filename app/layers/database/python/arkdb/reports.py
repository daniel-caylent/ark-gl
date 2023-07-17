"""Trial balance report methods"""

# pylint: disable=import-error; Lambda layer dependency
from database import report
from .utils import DB_NAME, SECRET_NAME, REGION_NAME, translate_results
# pylint: enable=import-error

def get_trial_balance(input_dict):
    """Retrieve a trial balance report based on input dict

    input_dict:
    EXAMPLE: {
      "journalEntryState": "POSTED",
      "hideZeroBalance": true,
      "ledgerId": [
        "32fd629e-bc96-11ed-8a31-0ed8d524c7fe",
        "3fa85f64-5717-4562-b3fc-2c963f66afa6"
      ],
      "startDay": "2017-01-01",
      "endDay": "2017-05-31"
    }
    """
    results = report.select_trial_balance(DB_NAME, input_dict, REGION_NAME, SECRET_NAME)

    return results

def get_trial_balance_detail(input_dict):
    """Retrieve a trial balance detail report"""
    results = report.select_trial_balance_detail(DB_NAME, input_dict, REGION_NAME, SECRET_NAME)

    results = translate_results(results, report.app_to_db)
    return results

def get_start_balance(account_id, start_date):
    result = report.select_start_balance(DB_NAME, account_id, start_date, REGION_NAME, SECRET_NAME)
    return result
