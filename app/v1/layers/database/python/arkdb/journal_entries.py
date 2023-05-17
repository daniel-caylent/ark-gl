from database.journal_entry import (
    app_to_db as journal_app_to_db,
    select_by_uuid,
    select_count_with_post_date,
)
from database.line_item import (
    app_to_db as line_app_to_db,
    select_by_multiple_journals,
    select_by_number_journal,
)
from database.db_main import translate_to_app

from .utils import DB_NAME, REGION_NAME, SECRET_NAME


def select_by_id(uuid: str) -> dict:
    result = select_by_uuid(DB_NAME, uuid, REGION_NAME, SECRET_NAME)

    if result is None:
        return result

    translated = translate_to_app(journal_app_to_db, result)
    filtered = {k: translated[k] for k in translated if not k.startswith("missing")}

    return filtered


def select_count_commited_journals() -> str:
    result = select_count_with_post_date(DB_NAME, REGION_NAME, SECRET_NAME)
    return result


def select_lines_by_journals(journal_ids: list) -> list:
    results = select_by_multiple_journals(
        DB_NAME, journal_ids, REGION_NAME, SECRET_NAME
    )

    translated = [translate_to_app(line_app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]
    return filtered


def select_line_by_number_journal(line_number: str, journal_id: str) -> list:
    results = select_by_number_journal(
        DB_NAME, line_number, journal_id, REGION_NAME, SECRET_NAME
    )

    translated = [translate_to_app(line_app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]
    return filtered
