"""This module adapts specifc methos to access the Aurora MySQL database for journal entries"""

# pylint: disable=import-error; Lambda layer dependency
from database.journal_entry import (
    app_to_db as journal_app_to_db,
    select_by_uuid,
    select_count_with_post_date,
    select_by_ledger_uuid,
    select_by_client_id as __select_by_client_id,
    select_by_fund_id as __select_by_fund_id,
    insert,
    update,
    delete,
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
)

from database.db_main import translate_to_app
# pylint: enable=import-error

from .utils import DB_NAME, REGION_NAME, SECRET_NAME


def select_by_id(uuid: str, translate=True) -> dict:
    """Select a journal entry by uuid"""
    result = select_by_uuid(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    if result is None:
        return result

    if translate:
        translated = translate_to_app(journal_app_to_db, result)
        filtered = {k: translated[k] for k in translated if not k.startswith("missing")}
        return filtered

    return result


def select_by_ledger_id(uuid: str) -> dict:
    """Select a list of journal entries by ledger ID"""
    results = select_by_ledger_uuid(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    if results is None:
        return results

    translated = [translate_to_app(journal_app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]

    return filtered

def select_by_fund_id(uuid: str) -> dict:
    """Select a list of journal entries by fund ID"""
    results = __select_by_fund_id(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    if results is None:
        return results

    translated = [translate_to_app(journal_app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]

    return filtered

def select_by_client_id(uuid: str) -> dict:
    """Select a list of journal entries by client ID"""
    results = __select_by_client_id(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    if results is None:
        return results

    translated = [translate_to_app(journal_app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]

    return filtered


def create_new(journal_entry):
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
        translated = [translate_to_app(line_app_to_db, result) for result in results]
        filtered = [
            {k: each[k] for k in each if not k.startswith("missing")} for each in translated
        ]
        return filtered

    return results


def get_attachments(journal_id, translate=True):
    """Get Attachments for an existing journal entry"""
    results = select_attachments(DB_NAME, journal_id, REGION_NAME, SECRET_NAME)

    if translate:
        translated = [translate_to_app(attachment_app_to_db, result) for result in results]
        filtered = [
            {k: each[k] for k in each if not k.startswith("missing")} for each in translated
        ]
        return filtered

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

    translated = [translate_to_app(line_app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]
    return filtered


def select_line_by_number_journal(line_number: str, journal_id: str) -> list:
    """Select line items by line item number"""
    results = select_by_number_journal(
        DB_NAME, line_number, journal_id, REGION_NAME, SECRET_NAME
    )

    translated = [translate_to_app(line_app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]
    return filtered


def select_attachments_by_journals(journal_ids: list) -> list:
    """Select attachments for multiple journals"""
    results = select_by_multiple_journals_att(
        DB_NAME, journal_ids, REGION_NAME, SECRET_NAME
    )

    translated = [translate_to_app(attachment_app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]
    return filtered
