import os
import sys

import pytest

from tests.test_base import TestBase
from tests.utils import MOCK_DIR

env = {
    "LEDGER_NAME": "test"
}

class TestQldbPost(TestBase([MOCK_DIR], env)):

    def test_account_post(self, monkeypatch):
        import app.layers.qldb.python.ark_qldb.post as post

        post.post("account", {"some": "contents"})


    def test_ledger_post(self):
        import app.layers.qldb.python.ark_qldb.post as post

        post.post("ledger", {"some": "contents"})


    def test_journal_entry_post(self):
        import app.layers.qldb.python.ark_qldb.post as post

        post.post("journal-entry", {"some": "contents"})


    def test_invalid_post(self):
        import app.layers.qldb.python.ark_qldb.post as post
        with pytest.raises(Exception):
            post.post("invalid", {"some": "contents"})
    
    def test_post_many_account(self):
        from app.layers.qldb.python.ark_qldb.post import post_many

        post_many("account", [{"some": "contents"}])
    
    def test_post_many_ledger(self):
        from app.layers.qldb.python.ark_qldb.post import post_many

        post_many("ledger", [{"some": "contents"}])
    
    def test_post_many_ledger(self):
        from app.layers.qldb.python.ark_qldb.post import post_many

        with pytest.raises(Exception):
            post_many("invalid", {"some": "contents"})