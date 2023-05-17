from tests.app.data import (
    good_post,
    post_with_bad_body,
    post_with_duplicate_name,
    post_with_duplicate_account_number,
    post_without_fund_id,
    post_with_parent,
    post_with_bad_request,
    LambdaContext
)

from .accounts_test_base import AccountsTestBase

class TestAccountsPost(AccountsTestBase):

    def test_good_post(self):
        from app.v1.accounts.post.post import handler
        result = handler(good_post, LambdaContext())
        assert 201 == result['statusCode']

    def test_post_with_parent(self):
        from app.v1.accounts.post.post import handler
        result = handler(post_with_parent, LambdaContext())
        assert 201 == result['statusCode']

    def test_post_with_bad_body(self):
        from app.v1.accounts.post.post import handler
        result = handler(post_with_bad_body, LambdaContext())
        assert 400 == result['statusCode']

    def test_post_with_bad_reqest_data(self):
        from app.v1.accounts.post.post import handler
        result = handler(post_with_bad_request, LambdaContext())
        assert 400 == result['statusCode']

    def test_post_without_fund_id(self):
        from app.v1.accounts.post.post import handler
        result = handler(post_without_fund_id, LambdaContext())
        assert 400 == result['statusCode']

    def test_post_with_duplicate_name(self):
        from app.v1.accounts.post.post import handler
        result = handler(post_with_duplicate_name, LambdaContext())
        assert 409 == result['statusCode']

    def test_post_with_duplicate_account_number(self):
        from app.v1.accounts.post.post import handler
        result = handler(post_with_duplicate_account_number, LambdaContext())
        assert 409 == result['statusCode']