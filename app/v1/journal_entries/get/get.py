"""Lambda that will perform the GET for JournalEntries"""
import json

# pylint: disable=import-error; Lambda layer dependency
from arkdb import journal_entries
from shared import (
    endpoint,
    filtering,
    dataclass_error_to_str
)
from journal_entries_shared import utils as je_utils
from models import JournalEntry, SortItem
# pylint: enable=import-error


@endpoint
def handler(event, context) -> tuple[int, dict]:  # pylint: disable=unused-argument; Required lambda parameters
    """Get journal entries by ledgerId"""

    try:
        body = json.loads(event["body"])
    except Exception:
        return 400, {"detail": "Body does not contain valid json."}

    page = int(body.pop("page", 1))
    page_size = int(body.pop("pageSize", 1000))

    default_sort = [
        {"name": "state", "descending": False},
        {"name": "date", "descending": False},
        {"name": "ledgerName", "descending": False},
        {"name": "fundId", "descending": False},
        {"name": "journalEntryNum", "descending": False},
    ]

    sort = body.pop("sort", None) or default_sort
    for item in sort:
        try:
            SortItem(**item)
        except Exception as e:
            return 400, {"detail": dataclass_error_to_str(e)}

    try:
        valid_input = filtering.FilterInput(**body).get_dict()
    except Exception as e:
        return 400, {"detail": dataclass_error_to_str(e)}

    results = journal_entries.select_with_filter_paginated(valid_input, page, page_size, sort)

    data_results = results["data"]
    if data_results:
        id_list = [str(journal["id"]) for journal in data_results]
        lines_list = journal_entries.select_lines_by_journals(id_list)
        att_list = journal_entries.select_attachments_by_journals(id_list)

        for journal_entry in data_results:
            journal_entry_id = journal_entry.pop("id")

            journal_entry["lineItems"] = je_utils.calculate_line_items(lines_list, journal_entry_id)

            journal_entry["attachments"] = je_utils.calculate_attachments(att_list, journal_entry_id)

    journal_entries_ = [JournalEntry(**result) for result in data_results]

    return 200, {
        "data": journal_entries_,
        "totalPages": results["total_pages"],
        "totalItems": results["total_items"],
        "currentPage": results["current_page"],
    }

