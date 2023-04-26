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
    "fundId": "unique-fund-id"
  },
  "path": "/prod/path/to/resource",
  "pathParameters": {
    "fundId": 1
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
  "body": "{\"fundId\": 1, \"accountNo\": 5,\"accountName\": \"account name\",\"accountDescription\": \"account description\",\"state\": \"ACTIVE\",\"isTaxable\": true,\"isVendorCustomerPartnerRequired\": false,\"parentAccountNo\": -1,\"attributeId\": 1,\"fsName\": \"fsName\",\"fsMappingId\": \"fsMapping\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  }
}

post_with_duplicate_account_number = {
  "body": "{\"fundId\": 1, \"accountNo\": 5,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"state\": \"ACTIVE\",\"isTaxable\": true,\"isVendorCustomerPartnerRequired\": false,\"parentAccountNo\": -1,\"attributeId\": 1,\"fsName\": \"fsName\",\"fsMappingId\": \"fsMapping\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  }
}


post_with_bad_body = {
  "body": "{\"fundId\": 1, \"accountNo\": 5,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"state\": \"ACTIVE\",\"isTaxable\": True,\"isVendorCustomerPartnerRequired\": false,\"parentAccountNo\": -1,\"attributeId\": 1,\"fsName\": \"fsName\",\"fsMappingId\": \"fsMapping\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  }
}


good_post = {
  "body": "{\"fundId\": 1, \"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"state\": \"ACTIVE\",\"isTaxable\": true,\"isVendorCustomerPartnerRequired\": false,\"parentAccountNo\": -1,\"attributeId\": 1,\"fsName\": \"fsName\",\"fsMappingId\": \"fsMapping\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  }
}

post_without_fund_id = {
  "body": "{\"accountNo\": 10,\"accountName\": \"unique\",\"accountDescription\": \"account description\",\"state\": \"ACTIVE\",\"isTaxable\": true,\"isVendorCustomerPartnerRequired\": false,\"parentAccountNo\": -1,\"attributeId\": 1,\"fsName\": \"fsName\",\"fsMappingId\": \"fsMapping\", \"isDryRun\": false}",
  "resource": "/{proxy+}",
  "path": "/path/to/resource",
  "httpMethod": "POST",
  "queryStringParameters": {
    "foo": "bar"
  }
}