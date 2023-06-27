import os

MAP_TAG = "map-migrated"
MAP_MPE_ID = 50399
MAP_VALUE = f"mig{MAP_MPE_ID}"


map_tag = {"MAP_TAG": MAP_TAG, "MAP_VALUE": MAP_VALUE}


prod = {
    "environment": "prod",
    "vpc": "vpc-001397989d8bec005",
    "subnets": [
        "subnet-0f8f35e61c4ffb9f2",
        "subnet-0d8d9b13ae14bbed8",
        "subnet-009f1a60270f8ecab",
    ],
    "deploy": {
        "DB_NAME": "ARKGL",
        "DB_SECRET_NAME": "/secret/arkgl_prd",
        "LEDGER_NAME": "ARKGL",
        "ROLE_ARN": "arn:aws:iam::466731580695:role/ark-caylent-prd-cross-account-policy",
    },
    "sqs_name": "ark-sqs-reconciliation",
    "sns_name": "ark-sns-notifications",
    "reconciliation_trigger_hour": 1,
    "reconciliation_trigger_minute": 0,
    "QLDB_EXPORT_TRIGGER_HOUR": "1",
    "DR_BUCKET_NAME": "arkgl-dr",
    "SQS_RECOVERY_PROCESS": "ark-sqs-dr-recovery-process",
    "ACCOUNT_ID": "466731580695",
    "enable_profiling": False,
    **map_tag,
}

qa = {
    "environment": "qa",
    "vpc": "vpc-0e608aa288e0cf3e8",
    "subnets": [
        "subnet-071c18bb851ebb13b",
        "subnet-0bdceb2901ff0e01c",
        "subnet-040de6a76f50175f6",
    ],
    "deploy": {
        "DB_NAME": "ARKGL",
        "DB_SECRET_NAME": "/secret/arkgl_qa",
        "LEDGER_NAME": "ARKGL",
        "ROLE_ARN": "arn:aws:iam::057034653783:role/ark-caylent-qa-cross-account-policy",
    },
    "sqs_name": "ark-sqs-reconciliation",
    "sns_name": "ark-sns-notifications",
    "reconciliation_trigger_hour": 1,
    "reconciliation_trigger_minute": 0,
    "QLDB_EXPORT_TRIGGER_HOUR": "1",
    "DR_BUCKET_NAME": "arkgl-dr",
    "SQS_RECOVERY_PROCESS": "ark-sqs-dr-recovery-process",
    "ACCOUNT_ID": "057034653783",
    "enable_profiling": True,
    **map_tag,
}

dev = {
    "environment": "dev",
    "vpc": "vpc-03f2daf6891ff2ce7",
    "subnets": ["subnet-059b26abb21e13281", "subnet-01f9e2bc3dced4993"],
    "deploy": {
        "DB_NAME": "ARKGL",
        "DB_SECRET_NAME": "/secret/arkgl_poc",
        "LEDGER_NAME": "ARKGL",
    },
    "sqs_name": "ark-sqs-reconciliation",
    "sns_name": "ark-sns-notifications",
    "reconciliation_trigger_hour": 1,
    "reconciliation_trigger_minute": 0,
    "QLDB_EXPORT_TRIGGER_HOUR": "1",
    "DR_BUCKET_NAME": "arkgl-disaster-recovery",
    "SQS_RECOVERY_PROCESS": "ark-sqs-dr-recovery-process",
    "ACCOUNT_ID": "319244063014",
    "enable_profiling": True,
    "replication_configuration": {
        "region": "us-east-2",
        # 'compliance_duration_days': 2,
        "vpc": "vpc-0acbf36a4d1313153",
        "subnets": [
            "subnet-025f3e7ea356535b6",
            "subnet-095fbe87b18fc2192",
        ],
    },
    **map_tag,
}


env_name = os.getenv("DEPLOYMENT_ENV")
ENV = None
if env_name == "prod":
    ENV = prod
elif env_name == "qa":
    ENV = qa
else:
    ENV = dev
