"""Lambda that will perform the GET for JournalEntries"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries, ledgers, funds
from shared import (
    endpoint,
    validate_uuid,
)
# pylint: enable=import-error

from models import JournalEntry


@endpoint
def handler(event, context) -> tuple[int, dict]:  # pylint: disable=unused-argument; Required lambda parameters
    """Get journal entries by ledgerId"""

    if not event.get("queryStringParameters"):
        return 400, {"detail": "Missing query string parameters"}


    client_id = event["queryStringParameters"].get("clientId", None)
    fund_id = event["queryStringParameters"].get("fundId", None)
    ledger_id = event["queryStringParameters"].get("ledgerId", None)

    results = []
    if ledger_id:
        if not validate_uuid(ledger_id):
            return 400, {"detail": "Invalid ledger UUID provided."}

        # validate that the fund exists and client has access to it
        ledger = ledgers.select_by_id(ledger_id)
        if ledger is None:
            return 400, {"detail": "Specified ledger does not exist."}

        # get and format the ledgers
        results = journal_entries.select_by_ledger_id(ledger_id)

    elif fund_id:
        if not validate_uuid(fund_id):
            return 400, {"detail": "Invalid fund UUID provided."}

        # validate that the fund exists and client has access to it
        fund = funds.select_by_uuid(fund_id)
        if fund is None:
            return 400, {"detail": "Specified fund does not exist."}

        # get and format the ledgers
        results = journal_entries.select_by_fund_id(fund_id)

    elif client_id:
        if not validate_uuid(client_id):
            return 400, {"detail": "Invalid client UUID provided."}

        # get and format the ledgers
        results = journal_entries.select_by_client_id(client_id)
    else:
        return 400, {"detail": "No searchable IDs provided."}

    if results:
        id_list = [str(journal["id"]) for journal in results]
        lines_list = journal_entries.select_lines_by_journals(id_list)
        att_list = journal_entries.select_attachments_by_journals(id_list)

        for journal_entry in results:
            journal_entry_id = journal_entry.pop("id")

            journal_entry["lineItems"] = [
                {
                    key: value
                    for key, value in entry.items()
                    if key != "journal_entry_id"
                }
                for entry in list(
                    filter(
                        lambda line: line["journal_entry_id"] == journal_entry_id,
                        lines_list,
                    )
                )
            ]
            journal_entry["attachments"] = [
                {
                    key: value
                    for key, value in entry.items()
                    if key != "journal_entry_id"
                }
                for entry in list(
                    filter(
                        lambda att: att["journal_entry_id"] == journal_entry_id,
                        att_list,
                    )
                )
            ]

    journal_entries_ = [JournalEntry(**result) for result in results]

    return 200, {"data": journal_entries_}
