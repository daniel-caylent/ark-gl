"""Lambda that will perform the GET for JournalEntries"""

# pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries, ledgers, funds
from shared import (
    endpoint,
    validate_uuid,
)
from models import JournalEntry
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]:  # pylint: disable=unused-argument; Required lambda parameters
    """Get journal entries by ledgerId"""

    if not event.get("queryStringParameters"):
        return 400, {"detail": "Missing query string parameters"}

    client_id = event["queryStringParameters"].get("clientId", None)
    fund_id = event["queryStringParameters"].get("fundId", None)
    ledger_id = event["queryStringParameters"].get("ledgerId", None)
    page = int(event["queryStringParameters"].get("page", 1))
    page_size = int(event["queryStringParameters"].get("pageSize", 1000))

    results = []
    if ledger_id:
        if not validate_uuid(ledger_id):
            return 400, {"detail": "Invalid ledger UUID provided."}

        # validate that the fund exists and client has access to it
        ledger = ledgers.select_by_id(ledger_id)
        if ledger is None:
            return 400, {"detail": "Specified ledger does not exist."}

        # get and format the ledgers
        results = journal_entries.select_by_ledger_id_paginated(ledger_id, page, page_size)

    elif fund_id:
        if not validate_uuid(fund_id):
            return 400, {"detail": "Invalid fund UUID provided."}

        # validate that the fund exists and client has access to it
        fund = funds.select_by_uuid(fund_id)
        if fund is None:
            return 400, {"detail": "Specified fund does not exist."}

        # get and format the ledgers
        results = journal_entries.select_by_fund_id_paginated(fund_id, page, page_size)

    elif client_id:
        if not validate_uuid(client_id):
            return 400, {"detail": "Invalid client UUID provided."}

        # get and format the ledgers
        results = journal_entries.select_by_client_id_paginated(client_id, page, page_size)
    else:
        return 400, {"detail": "No searchable IDs provided."}

    data_results = results["data"]

    if data_results:
        id_list = [str(journal["id"]) for journal in data_results]
        lines_list = journal_entries.select_lines_by_journals(id_list)
        att_list = journal_entries.select_attachments_by_journals(id_list)

        for journal_entry in data_results:
            journal_entry_id = journal_entry.pop("id")

            journal_entry["lineItems"] = __calculate_line_items(lines_list, journal_entry_id)

            journal_entry["attachments"] = __calculate_attachments(att_list, journal_entry_id)

    journal_entries_ = [JournalEntry(**result) for result in data_results]

    return 200, {
        "data": journal_entries_,
        "totalPages": results["total_pages"],
        "totalItems": results["total_items"],
        "currentPage": results["current_page"],
    }


def __calculate_attachments(att_list, journal_entry_id):
    return [
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


def __calculate_line_items(lines_list, journal_entry_id):
    return [
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
