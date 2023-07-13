"""This module adapts specifc methos to access the Aurora MySQL database for journal entries"""

# pylint: disable=import-error; Lambda layer dependency
from database.journal_entry import (
    app_to_db as journal_app_to_db,
    select_by_uuid,
    select_count_with_post_date,
    select_by_ledger_uuid,
    select_by_ledger_uuid_paginated,
    select_by_client_id as __select_by_client_id,
    select_by_fund_id as __select_by_fund_id,
    select_by_fund_id as __select_by_fund_id,
    select_by_fund_id_paginated as __get_select_by_fund_id_query_paginated,
    select_by_client_id_paginated as __select_by_client_id_paginated,
    bulk_insert as __bulk_insert,
    bulk_delete as __bulk_delete,
    select_with_filter_paginated as __select_with_filter_paginated,
    insert,
    update,
    delete,
    commit,
)
from database.line_item import (
    app_to_db as line_app_to_db,
    select_by_multiple_journals,
    select_by_number_journal,
    select_by_journal as select_line_items,
)

from database.attachment import (
    app_to_db as attachment_app_to_db,
    select_by_journal as select_attachments,
    select_by_multiple_journals as select_by_multiple_journals_att,
    select_by_uuid_journal,
)

# pylint: enable=import-error

from .utils import (
    DB_NAME,
    REGION_NAME,
    SECRET_NAME,
    translate_result,
    translate_results,
)


def select_by_id(uuid: str, translate=True) -> dict:
    """Select a journal entry by uuid"""
    result = select_by_uuid(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    if translate:
        result = translate_result(result, journal_app_to_db)

    return result


def select_by_ledger_id(uuid: str) -> dict:
    """Select a list of journal entries by ledger ID"""
    results = select_by_ledger_uuid(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    results = translate_results(results, journal_app_to_db)

    return results


def select_by_ledger_id_paginated(uuid: str, page: int, page_size: int) -> dict:
    """Select a list of journal entries by ledger ID paginated"""
    results = select_by_ledger_uuid_paginated(DB_NAME, uuid, REGION_NAME, SECRET_NAME, page, page_size)

    results = {
        "data": translate_results(results[0], journal_app_to_db),
        "total_pages": results[1]
    }

    return results


def select_by_fund_id(uuid: str) -> dict:
    """Select a list of journal entries by fund ID"""
    results = __select_by_fund_id(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    results = translate_results(results, journal_app_to_db)

    return results


def select_by_fund_id_paginated(uuid: str, page: int, page_size: int) -> dict:
    """Select a list of journal entries by fund ID paginated"""
    results = __get_select_by_fund_id_query_paginated(DB_NAME, uuid, REGION_NAME, SECRET_NAME, page, page_size)

    results = {
        "data": translate_results(results[0], journal_app_to_db),
        "total_pages": results[1]
    }

    return results


def select_by_client_id(uuid: str) -> dict:
    """Select a list of journal entries by client ID"""
    results = __select_by_client_id(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    results = translate_results(results, journal_app_to_db)
    return results


def select_by_client_id_paginated(uuid: str, page: int, page_size: int) -> dict:
    """Select a list of journal entries by client ID paginated"""
    results = __select_by_client_id_paginated(DB_NAME, uuid, REGION_NAME, SECRET_NAME, page, page_size)

    results = {
        "data": translate_results(results[0], journal_app_to_db),
        "total_pages": results[1]
    }

    return results


def bulk_insert(journal_entries: list):
    """Insert a list of multiple journal entries"""
    result = __bulk_insert(DB_NAME, journal_entries, REGION_NAME, SECRET_NAME)
    return result

def create_new(journal_entry: dict):
    """Create a new journal entry"""
    id_ = insert(DB_NAME, journal_entry, REGION_NAME, SECRET_NAME)
    return id_


def update_by_id(id_, updated):
    """Update a journal entry by ID"""
    update(DB_NAME, id_, updated, REGION_NAME, SECRET_NAME)


def delete_by_id(id_):
    """Delete a journal entry by ID"""
    delete(DB_NAME, id_, REGION_NAME, SECRET_NAME)


def get_line_items(journal_id, translate=True):
    """Get line items for an existing Journal Entry"""
    results = select_line_items(DB_NAME, journal_id, REGION_NAME, SECRET_NAME)

    if translate:
        results = translate_results(results, line_app_to_db)
    return results


def get_attachments(journal_id, translate=True):
    """Get Attachments for an existing journal entry"""
    results = select_attachments(DB_NAME, journal_id, REGION_NAME, SECRET_NAME)

    if translate:
        results = translate_results(results, attachment_app_to_db)
    return results


def select_count_commited_journals() -> str:
    """Count committed journals"""
    result = select_count_with_post_date(DB_NAME, REGION_NAME, SECRET_NAME)
    return result


def select_lines_by_journals(journal_ids: list) -> list:
    """Select line items from multiple journals"""
    results = select_by_multiple_journals(
        DB_NAME, journal_ids, REGION_NAME, SECRET_NAME
    )

    results = translate_results(results, line_app_to_db)
    return results


def select_line_by_number_journal(line_number: str, journal_id: str) -> list:
    """Select line items by line item number"""
    results = select_by_number_journal(
        DB_NAME, line_number, journal_id, REGION_NAME, SECRET_NAME
    )

    results = translate_results(results, line_app_to_db)
    return results


def select_attachments_by_journals(journal_ids: list) -> list:
    """Select attachments for multiple journals"""
    results = select_by_multiple_journals_att(
        DB_NAME, journal_ids, REGION_NAME, SECRET_NAME
    )
    results = translate_results(results, attachment_app_to_db)
    return results


def select_attachment_by_uuid_journal(attachment_uuid: str, journal_id: str) -> list:
    """Select line items by line item number"""
    results = select_by_uuid_journal(
        DB_NAME, attachment_uuid, journal_id, REGION_NAME, SECRET_NAME
    )

    results = translate_results(results, line_app_to_db)
    return results


def commit_by_id(journal_uuid) -> None:
    """Commit an existing journal"""
    commit(DB_NAME, journal_uuid, REGION_NAME, SECRET_NAME)


def select_with_filter_paginated(filter, page=None, page_size=None):
    results = __select_with_filter_paginated(DB_NAME, filter, REGION_NAME, SECRET_NAME, page, page_size)

    results = {
        "data": translate_results(results[0], journal_app_to_db),
        "total_pages": results[1]
    }

    return results


def bulk_delete(ids):
    __bulk_delete(DB_NAME, ids, REGION_NAME, SECRET_NAME)
