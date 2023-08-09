## For saving images in DAM...
import requests
from dotenv import dotenv_values
import os

class DAMStoreConfig:

    def __init__(self, env=os.path.dirname(os.path.realpath(__file__))+"/.env"):
        self.config = {
            **dotenv_values(env),  # load sensitive variables from .env file
            **os.environ,          # override loaded values with environment variables
        }

class DAMStoreVAST:

    def __init__(self, config=None):
        self.default_config(config)

    def default_config(self, config):
        if not config:
            config = DAMStoreConfig()
        self.config = config

    # POST request to the API
    def post(self, params):
        response = requests.post(self.config.config["DAM_HOST"], files=params)
        response.raise_for_status()

    def create_resource(self, image_path, metadata={}):
        params = metadata
        params.update({
            'userfile': open(image_path, 'rb'),
            'function': 'create_resource',
            'user': self.config.config["DAM_USERNAME"],
            'sign': self.config.config["DAM_SECRET_KEY"],
        })
        print("PARAMS:", params)
        self.post(params)
