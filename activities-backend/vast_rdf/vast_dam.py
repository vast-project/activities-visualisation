## For saving images in DAM...
import requests
import hashlib
from dotenv import dotenv_values
import os

import logging
logger = logging.getLogger('DAMStoreVAST')

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

    def query(self, function, parameters={}):
        query_string = f"user={self.config.config['DAM_USERNAME']}&function={function}&" + '&'.join(f'{k}={v}' for k, v in parameters.items())
        sign = hashlib.sha256((self.config.config["DAM_SECRET_KEY"] + query_string).encode('utf-8')).hexdigest()
        query_url = f"{self.config.config['DAM_HOST']}/?{query_string}&sign={sign}"
        logger.info(f"DAMStoreVAST: query: {query_url}")

        response = requests.get(query_url)
        response.raise_for_status()
        return response

    def create_resource(self, image_url, metadata={}):
        json = {}
        for k,v in metadata.items():
            match k:
                case 'date': json['12']=v
                case 'description': json['8']=v
        json = requests.utils.quote(str(json))
        image_absolute_url = self.config.config['DAM_DJANGO_MEDIA_URL_PREFIX']+image_url
        parameters = {
            'param1': '1',
            'param2': '0',
            'param3': image_absolute_url,
            'param4': '',
            'param5': '',
            'param6': '',
            'param7': json,
        }
        logger.info(f"DAMStoreVAST: Saving Image: {image_absolute_url}")
        response = self.query('create_resource', parameters)
        if response.text.lower() == "false":
            raise Exception(f"Image cannot be saved in DAM: {image_absolute_url}")
        if response.text.startswith('"'):
            raise Exception(f"Image cannot be saved in DAM: {image_absolute_url}: {response.text}")
        logger.info(f"DAMStoreVAST: DAM response: {response.text}")
        return response

# if __name__ == "__main__":
#     dam = DAMStoreVAST()
#     resource = dam.create_resource('https://www.vast-project.eu/wp-content/uploads/2021/01/VAST_LOGO.jpg')
#     print(resource.text)
