# TODO: Determine the best way to set the VPC and Subnets for the application
import os

prod = {}

customer_dev = {}

dev = {
    'vpc': "vpc-03f2daf6891ff2ce7",
    'subnets': ["subnet-059b26abb21e13281", "subnet-01f9e2bc3dced4993"],
    'deploy': {
      'DB_NAME': 'ARKGL',
      'DB_SECRET_NAME': '/secret/arkgl_poc'
    }
}

env_name = os.getenv('DEPLOYMENT_TYPE')
ENV = None
if env_name == 'PROD':
    ENV = prod
elif env_name == 'CUSTOMER_DEV':
    ENV = customer_dev
else:
    ENV = dev
