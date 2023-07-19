import json
import pytest

from tests.app.data import (
    LambdaContext
)

from .reports_test_base import ReportsTestBase

class TestTrialBalance(ReportsTestBase):

    def test_accounts_hierarchy(self):
        from app.v1.reports.trial_balance_detail import build_parent_hierarchy
        accounts = [
          {"accountId": 1, "parentAccountId": None},
          {"accountId": 2, "parentAccountId": None},
          {"accountId": 3, "parentAccountId": 1},
          {"accountId": 4, "parentAccountId": 1},
          {"accountId": 5, "parentAccountId": 4},
          {"accountId": 6, "parentAccountId": 2},
        ]

        result = build_parent_hierarchy(accounts, "parentAccountId", "accountId")

        assert len(result) == 2
        assert len(result[0]["childAccounts"]) == 2
        assert len(result[1]["childAccounts"]) == 1
        assert len(result[0]["childAccounts"][0]["childAccounts"]) == 0
        assert len(result[0]["childAccounts"][1]["childAccounts"]) == 1

    def test_get_parent_accounts(self):
        from app.v1.reports.trial_balance_detail import get_all_parent_accounts

        accounts = {
          1: {"accountId": 1, "parentAccountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"},
          2: {"accountId": 2, "parentAccountId": None},
          3: {"accountId": 3, "parentAccountId": 1},
        }

        result = get_all_parent_accounts(accounts, "parentAccountId", "accountId")


        assert len(result.keys()) == 4

    def test_good_get(self):
        from app.v1.reports.trial_balance_detail import handler
        
        event = {
            "body": json.dumps({
              "ledgerIds": ["4e4f2675-146e-4092-aabc-75bbbeaad184"]
            })
        }

        result = handler(event, LambdaContext)

        assert 200 == result["statusCode"]

    def test_good_many_params(self):
        from app.v1.reports.trial_balance_detail import handler
        
        event = {
            "body": json.dumps({
                "attributeIds": ["4e4f2675-146e-4092-aabc-75bbbeaad184"],
                "accountIds": ["a92bde1e-7825-429d-aaae-909f2d7a8df1"],
                "ledgerIds": ["4e4f2675-146e-4092-aabc-75bbbeaad184"],
                "startDate": "1990-10-10",
                "endDate": "1991-10-10",
            })
        }

        result = handler(event, LambdaContext)

        assert 200 == result["statusCode"]

    def test_bad_ledger_id(self):
        from app.v1.reports.trial_balance_detail import handler
        
        event = {
            "body": json.dumps({
              "ledgerIds": ["4e4f2675-146e-4092-aabc-75bbbeaad18"]
            })
        }

        result = handler(event, LambdaContext)

        assert 400 == result["statusCode"]

    def test_no_query_string_params(self):
        from app.v1.reports.trial_balance_detail import handler
        
        event = {
            "body": json.dumps({
            })
        }

        result = handler(event, LambdaContext)

        assert 400 == result["statusCode"]

    def test_no_attribute_id_only(self):
        from app.v1.reports.trial_balance_detail import handler
        
        event = {
            "body": json.dumps({
                "attributeIds": ["attributeId"],
                "ledgerIds": ["4e4f2675-146e-4092-aabc-75bbbeaad184"]
            })
        }

        result = handler(event, LambdaContext)

        assert 400 == result["statusCode"]


