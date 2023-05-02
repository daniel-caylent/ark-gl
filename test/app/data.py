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
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
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
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df2"
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
  "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 5,\"accountName\": \"account name\",\"accountDescription\": \"account description\",\"state\": \"ACTIVE\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  }
}

post_with_duplicate_account_number = {
  "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 5,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"state\": \"ACTIVE\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  }
}


post_with_bad_body = {
  "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 5,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"state\": \"ACTIVE\",\"isTaxable\": True,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  }
}

good_post = {
  "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 10,\"accountName\": \"account\",\"accountDescription\": \"account description\",\"state\": \"ACTIVE\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  }
}

post_with_parent = {
  "body": "{\"fundId\": \"d4b26dc7-e51a-11ed-aede-0247c1ed2eeb\", \"accountNo\": 10,\"accountName\": \"account\",\"accountDescription\": \"account description\",\"state\": \"ACTIVE\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  }
}

good_put = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  },
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

put_with_parent_id = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  },
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

put_with_committed_account = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  },
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df5"
  },
}

put_with_committed_account_allowed = {
  "body": "{\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\"}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  },
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df5"
  },
}

put_with_bad_uuid = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  },
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df"
  },
}

put_without_account_number = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  },
  "pathParameters": {
    "account": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

put_with_bad_body = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": True,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  },
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

put_with_duplicate_name = {
  "body": "{\"accountNo\": 10,\"accountName\": \"account name\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  },
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

put_with_duplicate_account_number = {
  "body": "{\"accountNo\": \"5\",\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  },
  "pathParameters": {
    "accountId": "a92bde1e-7825-429d-aaae-909f2d7a8df1"
  },
}

post_without_fund_id = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"state\": \"ACTIVE\",\"isTaxable\": true,\"isEntityRequired\": false,\"parentAccountId\": null,\"attributeId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\",\"fsName\": \"fsName\",\"fsMappingId\": \"a92bde1e-7825-429d-aaae-909f2d7a8df1\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  }
}