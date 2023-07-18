import datetime

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
    if not event.get("queryStringParameters"):
        return 400, {"detail": "Missing query parameters"}

    try:
        valid_input = ReportInputs(**event.get("queryStringParameters"))
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


    lines = reports.get_trial_balance_detail(valid_input.__dict__)

    report = {
        "decimals": None,
        "currencyName": None,
        "accounts": [],
        "lineItems": []
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

            accounts_[line["accountId"]]["totalAmount"] += line["amount"]
            accounts_[line["accountId"]]["lineItems"].append(
                {
                    "ledgerName": line["ledgerName"],
                    "ledgerId": line["ledgerId"],
                    "accountId": line["accountId"],
                    "entityId": line["entityId"],
                    "journalEntryNum": line["journalEntryNum"],
                    "date": line["journalEntryDate"],
                    "adjustingJournalEntry": line["adjustingJournalEntry"],
                    "memo": line["memo"],
                    "state": line["journalEntryState"],
                    "amount": line["amount"],
                }
            )

        all_accounts = list(get_all_parent_accounts(accounts_, "parentAccountId", "accountId").values())

        for account in all_accounts:
            account["startBalance"] = reports.get_start_balance(account["accountId"], valid_input.startDate)
            account["endBalance"] = account["startBalance"] + account["totalAmount"]

        report["accounts"] = build_parent_hierarchy(all_accounts, "parentAccountId", "accountId")
        

    return 200, {"data": report}

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


def get_all_parent_accounts(base_accounts_lookup: dict, parent_field: str, child_field: str):
    """Take a lookup dict of accounts, return a lookup dict including all parents"""
    def get_parent_lookup(account_lookup, parent_field, child_field):

        new_parents = {}
        for account in account_lookup.values():
            if account[parent_field] and account[parent_field] not in account_lookup:
                parent_account = accounts.select_by_id(account[parent_field])
                if parent_account is None:
                    raise Exception(f"Parent account not found: {account[parent_field]}")

                new_parents[account[parent_field]] = {
                    "accountId": parent_account["accountId"],
                    "totalAmount": 0,
                    "accountName": parent_account["accountName"],
                    "accountNo": parent_account["accountNo"],
                    "parentAccountId": parent_account["parentAccountId"],
                }

        if new_parents:
            account_lookup.update(new_parents)
            account_lookup = get_parent_lookup(account_lookup, parent_field, child_field)

        return account_lookup
    return get_parent_lookup(base_accounts_lookup, parent_field, child_field)





    
