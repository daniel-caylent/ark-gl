from dataclasses import dataclass

@dataclass
class LambdaContext:
    aws_request_id: str = 'A-unique-lambda-request-id'


get_with_fund_id = {
  "body": "eyJ0ZXN0IjoiYm9keSJ9",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "GET",
  "isBase64Encoded": True,
  "queryStringParameters": {
    "fundId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
  "pathParameters": {
  },
  "path": "/prod/path/to/resource",
  "resourcePath": "/{proxy+}",
  "httpMethod": "GET",
  "apiId": "1234567890",
  "protocol": "HTTP/1.1"
}

get_with_account_id = {
  "body": "eyJ0ZXN0IjoiYm9keSJ9",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "GET",
  "isBase64Encoded": True,
  "path": "/prod/path/to/resource",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1",
    "ledgerId":  "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
  "resourcePath": "/{proxy+}",
  "httpMethod": "GET",
  "apiId": "1234567890",
  "protocol": "HTTP/1.1"
}

get_with_bad_account_id = {
  "body": "eyJ0ZXN0IjoiYm9keSJ9",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "GET",
  "isBase64Encoded": True,
  "path": "/prod/path/to/resource",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df2",
    "ledgerId": "a92bde1e-7825-429d-aaae-909f2d7a8df2"
  },
  "resourcePath": "/{proxy+}",
  "httpMethod": "GET",
  "apiId": "1234567890",
  "protocol": "HTTP/1.1"
}

get_with_non_uuid_account_id = {
  "body": "eyJ0ZXN0IjoiYm9keSJ9",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "GET",
  "isBase64Encoded": True,
  "path": "/prod/path/to/resource",
  "pathParameters": {
    "accountId": "7825-429d-aaae-909f2d7a8df2"
  },
  "resourcePath": "/{proxy+}",
  "httpMethod": "GET",
  "apiId": "1234567890",
  "protocol": "HTTP/1.1"
}

get_without_fund_id = {
  "body": "eyJ0ZXN0IjoiYm9keSJ9",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "pathParameters": {
  },
  "httpMethod": "GET",
  "isBase64Encoded": True,
  "queryStringParameters": {},
  "path": "/prod/path/to/resource",
  "resourcePath": "/{proxy+}",
  "httpMethod": "GET",
  "apiId": "1234567890",
  "protocol": "HTTP/1.1"
}

get_with_non_uuid_fund_id = {
  "body": "eyJ0ZXN0IjoiYm9keSJ9",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "pathParameters": {
    "fundId": 1
  },
  "httpMethod": "GET",
  "isBase64Encoded": True,
  "queryStringParameters": {},
  "path": "/prod/path/to/resource",
  "resourcePath": "/{proxy+}",
  "httpMethod": "GET",
  "apiId": "1234567890",
  "protocol": "HTTP/1.1"
}

post_with_duplicate_name = {
  "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 5,\"accountName\": \"account name\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
}

post_with_duplicate_account_number = {
  "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 5,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
}

post_with_bad_body = {
  "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 5,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": True,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
}

post_with_bad_request = {
  "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": \"abcd\",\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
}

good_post = {
  "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 10,\"accountName\": \"account\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
}

post_with_parent = {
  "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 10,\"accountName\": \"account\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
}

good_put = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

put_with_parent_id = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

commit_account = {
  "body": "{\"state\": \"ACTIVE\"}",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

bad_commit_account = {
  "body": "{\"state\": \"ACTIVE\"}",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df"
  },
}

put_with_committed_account = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df5"
  },
}

put_with_committed_account_allowed = {
  "body": "{\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\"}",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df5"
  },
}

put_with_bad_uuid = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df"
  },
}

put_without_account_number = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "pathParameters": {
    "account": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

put_with_bad_body = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": True,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

put_with_duplicate_name = {
  "body": "{\"accountNo\": 10,\"accountName\": \"account name\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

put_with_duplicate_account_number = {
  "body": "{\"accountNo\": \"5\",\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

post_without_fund_id = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
}

good_upload = {
  "body": "{\"fundId\": \"d4b26bbb-e51a-11ed-aede-0247c1ed2ee1\", \"signedS3Url\": \"https://daniel-ark-test.s3.us-east-2.amazonaws.com/coa_upload.csv?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEM%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMSJIMEYCIQC5jx48%2BWZcbM2GQl6X%2F6KL2YwCybdMR3nO17xEBsnmTgIhALzKpLYi2TgprG5s3FZ3Kj9Sjtvybo0G%2BiOdAJxkM%2B%2FiKvMDCNj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQBRoMMTMxNTc4Mjc2NDYxIgzYjS4dAYdn7URVgKQqxwNC38OLQyob0K1shlKY9sCaMEdFzBe2V99MX3HbHDAJpRIlWLlkUOUGO7Mk2u2qVrGOrOit%2BeOipezu4iv3XivekaIUf1iqMTfLJWrdv8jxcCtfCbRmfvxWb61uxS1eozvYHRd1S%2BJO9iWJH1NUkSb9peAdLg4yxQlxD1TnM4xYnG1Z9WEwzQnToFKzNswcXa%2FqriSXkm2cnWhAY0VdMHqwu1UfGt4YlaIMniS0RdC5USKGC496hxLZDtxw8jcr3R%2BHQS8y0j3xLZpwwhj4AOrwt%2BYH%2BOp8cxDqTRO2yToMS7LbD%2FlbcsXJwuD8BrbW5ev8eYWg3vZIikYbiISakS0AshgZlA%2FU46FOb%2Btu7U8OIqvGJ6%2F8A2zT0yrjiUcYrd%2FJQbP1O%2FEIgJM%2FiXf6eoCHLf%2F6mpb4s%2BT2htkAdyzE336cip2BD17%2B22j%2BAFtJmP0T%2BqJYQLbQh6DZ5pVzRysx59SN6iCB7OjKUlyAeVK%2F5u%2FGG%2BSzDnWDfar8P33AljiLmGsSrHB1SMoodJSwLkRJwikAOBOI3iEjHK0tt48W4fxZCnVfcsyp1a8BDh%2BJGxcZ2iu5JTdphaVslpWvFA3Lv%2BDl6EIZiTCM5cmiBjqTAopey0aIwMjhkZizLI%2Fx6RrjfRajXdh0zbYTIzPT1LGY3P8dW%2FheDqEzIf14tAFMi4qn3eEIjmPpmLJf3i4mqW%2BV9m2osfBDWswBqlbH44Ndz0me3Gz76FLhrXZvuNPKnqKL0pDoWMQ5e1x%2BllFHG9CsBRPeTK4X5QohUGNPlF6jN3je2Om6%2BNgA4OgPI683CFfvU5TJIEabM3VPY99bqvFQeOoa304sZ3Y%2B3EBvJ2pECLvffgSnirGvtjVw6MbPnfQ6bKFE3IbmgdMIHV1naxi9Pddq6FJuACDCobkMwxBYZObWUwFWM3xumWiEGPYFtuFVVN5ygnFdxbTt9hyPpx6cQXezfwbouVoaXvCXFOYEuTcp&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230503T144618Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIAR5IVNFJWVT53LQWM%2F20230503%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Signature=d47a2fd32b54504423370670304a8aef0ae4508a966cea018a7c33b267b66c7a\"}"
}

good_copy = {
  "body": "{\"fundId\": \"d4b26bbb-e51a-11ed-aede-0247c1ed2ee2\"}",
  "pathParameters": {
    "fundId": "d4b26bbb-e51a-11ed-aede-0247c1ed2ee1"
  }
}
