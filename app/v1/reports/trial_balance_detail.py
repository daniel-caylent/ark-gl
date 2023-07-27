import json
from datetime import datetime

from arkdb import reports, ledgers, accounts, account_attributes
from shared import endpoint, dataclass_error_to_str

from models import ReportInputs


@endpoint
def handler(event, context) -> tuple[int, dict]:
    """Handler for the trial balance report

    event: dict
    POST event passed in from API gateway. The key 'body' should
    cary the POST request as a JSON string

    context: LambdaContext
    Context about the instance of the lambda function

    """
    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    try:
        valid_input = ReportInputs(**body)
    except Exception as e:
        return 400, {"detail": dataclass_error_to_str(e)}

    if valid_input.ledgerIds:
        for id_ in valid_input.ledgerIds:
            ledger = ledgers.select_by_id(id_)
            if ledger is None:
                return 400, {"detail": f"Invalid ledgerId: {id_}"}

    if valid_input.accountIds:
        for id_ in valid_input.accountIds:
            account = accounts.select_by_id(id_)
            if account is None:
                return 400, {"detail": f"Invalid accountId: {id_}"}

    if valid_input.attributeIds:
        for id_ in valid_input.attributeIds:
            attribute = account_attributes.select_by_id(id_)
            if attribute is None:
                return 400, {"detail": f"Invalid attributeId: {id_}"}

    start_date = (
        datetime.strptime(valid_input.startDate, "%Y-%m-%d").date()
        if valid_input.startDate else None
    )
    valid_input.startDate = None

    lines = reports.get_trial_balance_detail(valid_input.__dict__)

    report = {
        "accounts": [],
    }

    if lines:
        report["decimals"] = lines[0]["decimals"]
        report["currency"] = lines[0]["currency"]
        accounts_ = {}
        for line in lines:
            if not accounts_.get(line["accountId"]):
                accounts_[line["accountId"]] = {
                    "accountId": line["accountId"],
                    "totalAmount": 0,
                    "accountName": line["accountName"],
                    "accountNo": line["accountNo"],
                    "parentAccountId": line["parentAccountId"],
                    "fundId": line["fundId"],
                    "lineItems": [],
                }

            journal_date = line["journalEntryDate"]

            if not start_date or journal_date >= start_date:
                accounts_[line["accountId"]]["totalAmount"] += line["amount"]
                accounts_[line["accountId"]]["lineItems"].append(
                    {
                        "ledgerName": line["ledgerName"],
                        "ledgerId": line["ledgerId"],
                        "accountId": line["accountId"],
                        "entityId": line["entityId"],
                        "journalEntryNum": line["journalEntryNum"],
                        "date": journal_date,
                        "adjustingJournalEntry": bool(line["adjustingJournalEntry"]),
                        "memo": line["memo"],
                        "state": line["journalEntryState"],
                        "amount": line["amount"],
                    }
                )

        all_accounts = get_all_associated_accounts(list(accounts_.values()))

        for account in all_accounts:
            account["startBalance"] = reports.get_start_balance(account["accountId"], str(start_date))
            account["endBalance"] = reports.get_end_balance(account["accountId"], valid_input.endDate)

        report["accounts"] = build_parent_hierarchy(all_accounts, "parentAccountId", "accountId")
    return 200, {"data": report}

def get_all_associated_accounts(accounts_list):
    """Retrieve all parent and child accounts associated with a list"""
    input_ids = [acct["accountId"] for acct in accounts_list]
    parent_accounts = accounts.get_parent_accounts_from_list(input_ids)

    parent_ids = [acct["accountId"] for acct in parent_accounts]
    child_accounts = accounts.get_child_accounts_from_list(parent_ids)

    # add new accounts without duplicates
    for account in parent_accounts + child_accounts:
        if account["accountId"] not in input_ids:
            accounts_list.append(
                {
                    **account,
                    "totalAmount": 0,
                    "lineItems": []
                }
            )

            input_ids.append(account["accountId"])
    return accounts_list


def build_parent_hierarchy(accounts_list, parent_field, child_field):
    """Build a list of accounts with their children in childAccounts attribute"""
    parent_lookup = {}
    for account in accounts_list:
        if not parent_lookup.get(account[parent_field]):
            parent_lookup[account[parent_field]] = [account]
        else:
            parent_lookup[account[parent_field]].append(account)

    def build_hierarchy(id_):
        child_list = parent_lookup.get(id_, [])

        for child in child_list:
            child["childAccounts"] = build_hierarchy(child[child_field])

        return child_list

    return build_hierarchy(None)
