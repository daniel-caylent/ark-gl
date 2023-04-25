# TODO: Determine the best way to set the VPC and Subnets for the application
import os

prod = {}

customer_dev = {}

dev = {
    'vpc': "vpc-0fee1c501ecae446b",
    'subnets': ["subnet-0727e6789f058348b", "subnet-007ede16f0c16022f"],
    'deploy': {
      'DB_NAME': 'ARKGL',
      'DB_SECRET_NAME': 'ark/db-password'
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
