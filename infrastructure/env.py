# TODO: Determine the best way to set the VPC and Subnets for the application
import os

MAP_TAG = 'map-migrated'
MAP_MPE_ID = 50399
MAP_VALUE = f'mig{MAP_MPE_ID}'


map_tag = {
    'MAP_TAG': MAP_TAG,
    'MAP_VALUE': MAP_VALUE
}

prod = {
    'vpc': "?",
    'subnets': ["?", "?"],
    'deploy': {
      'DB_NAME': '?',
      'DB_SECRET_NAME': '?'
    },
    **map_tag
}

qa = {
    'vpc': "?",
    'subnets': ["?", "?"],
    'deploy': {
      'DB_NAME': '?',
      'DB_SECRET_NAME': '?'
    },
    **map_tag
}

dev = {
    'vpc': "vpc-03f2daf6891ff2ce7",
    'subnets': ["subnet-059b26abb21e13281", "subnet-01f9e2bc3dced4993"],
    'deploy': {
      'DB_NAME': 'ARKGL',
      'DB_SECRET_NAME': '/secret/arkgl_poc'
    },
    'ledger_name': 'ARKGL',
    'sqs_name': 'ark-sqs-reconciliation',
    'sns_name': 'ark-sns-notifications',
    'reconciliation_trigger_hour': 1,
    'reconciliation_trigger_minute': 0,
    'dr_bucket_name': 'arkgl-dr',
    **map_tag
}

# TODO: remove the caylent configuration
caylent = {
    'vpc': "vpc-0fee1c501ecae446b",
    'subnets': ["subnet-0727e6789f058348b", "subnet-007ede16f0c16022f"],
    'deploy': {
      'DB_NAME': 'ARKGL',
      'DB_SECRET_NAME': 'ark/db-password'
    },
    **map_tag
}

env_name = os.getenv('DEPLOYMENT_TYPE')
ENV = None
if env_name == 'prod':
    ENV = prod
elif env_name == 'qa':
    ENV = qa
elif env_name and env_name.startswith('caylent'):
    ENV = caylent
else:
    ENV = dev
