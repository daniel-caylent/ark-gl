"""This module provides values to perform the database connection"""

import os

from database.db_main import translate_to_app

DB_NAME = os.getenv("DB_NAME")
SECRET_NAME = os.getenv("DB_SECRET_NAME")
REGION_NAME = os.getenv("AWS_REGION")


def translate_result(result: dict, app_to_db: dict):
    """Translate a single dict from db column names to app parameter names"""
    if result is None:
        return result

    translated = translate_to_app(app_to_db, result)
    filtered = {k: translated[k] for k in translated if not k.startswith("missing")}
    return filtered


def translate_results(results: list, app_to_db: dict):
    """Translate a list of dicts from db column names to app parameter names"""
    translated = [translate_to_app(app_to_db, result) for result in results]
    filtered = [
        {k: each[k] for k in each if not k.startswith("missing")} for each in translated
    ]

    return filtered
