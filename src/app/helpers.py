# source from aws
import os
import json

from dotenv import load_dotenv


def insert_environment_variables():
    """set up the environment variables for Django settings"""
    "aws_settings is an environment variable from Secret Manager"
    if aws_settings := os.getenv("aws_settings"):
        aws_settings = json.loads(aws_settings)
        for key, value in aws_settings.items():
            os.environ[key] = value
        del os.environ["aws_settings"]
    else:
        load_dotenv()
