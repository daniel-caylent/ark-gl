from pathlib import PurePath

from tests.app.data import (
    LambdaContext
)


from tests.test_base import TestBase
from tests.utils import APP_DIR, APP_SHARED_LAYER

MODELS = str(PurePath(APP_DIR, 'accounts', 'post'))
PATHS = [MODELS, APP_SHARED_LAYER]

class TestAccountsPost(TestBase(PATHS)):

    def test_good_post(self):
        from app.v1.accounts.post.post import handler
        request = {
            "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 100,\"accountName\": \"account\", \
                \"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false, \
                \"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\", \
                \"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
        }
        result = handler(request, LambdaContext())
        assert 201 == result['statusCode']

    def test_post_with_parent(self):
        from app.v1.accounts.post.post import handler

        request = {
            "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 100,\"accountName\": \"account\", \
                \"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false, \
                \"parentAccountId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \
                \"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \
                \"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}"
        }
        result = handler(request, LambdaContext())
        assert 201 == result['statusCode']

    def test_post_with_bad_body(self):
        from app.v1.accounts.post.post import handler
        request = {
            "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 555,\"accountName\": \"unique\", \
                \"accountDescription\": \"account description\",\"isTaxable\": True,\"isEntityRequired\": false, \
                \"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\", \
                \"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}"
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_post_with_bad_reqest_data(self):
        from app.v1.accounts.post.post import handler
        request = {
            "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": \"abcd\",\"accountName\": \"unique\", \
                \"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false, \
                \"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\", \
                \"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}"
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_post_without_fund_id(self):
        from app.v1.accounts.post.post import handler
        request = {
            "body": "{\"accountNo\": 105,\"accountName\": \"unique\",\"accountDescription\": \"account description\", \
                \"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null, \
                \"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\", \
                \"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}"
        }

        result = handler(request, LambdaContext())
        assert 400 == result['statusCode']

    def test_post_with_duplicate_name(self):
        from app.v1.accounts.post.post import handler
        request = {
            "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 555,\"accountName\": \"account name\", \
                \"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false, \
                \"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\", \
                \"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}"
        }
        result = handler(request, LambdaContext())
        assert 409 == result['statusCode']

    def test_post_with_duplicate_account_number(self):
        from app.v1.accounts.post.post import handler
        request = {
            "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 5555,\"accountName\": \"unique\", \
                \"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null, \
                \"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\", \
                \"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}"
        }

        result = handler(request, LambdaContext())
        assert 409 == result['statusCode']