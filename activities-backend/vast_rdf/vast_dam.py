## For saving images in DAM...
import requests
import hashlib
from dotenv import dotenv_values
import os
import json
from urllib.parse import urlparse

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
        logger.info(f"DAMStoreVAST: DAM response: {response.text}")
        response.raise_for_status()
        return response

    def create_resource(self, artifact_url, metadata={}, artifact_type='image'):
        json_data = {}
        for k,v in metadata.items():
            match k:
                case 'title':
                    pass
                case 'date':        json_data['12']=v
                case 'description': json_data["8"]=v
        logger.info(f"DAMStoreVAST: metadata: {json.dumps(json_data)}")
        json_data = requests.utils.quote(json.dumps(json_data))
        artifact_absolute_url = self.get_absolute(artifact_url)
        match artifact_type:
            case 'document':
                artifact_type_code = '2'
            case 'video':
                artifact_type_code = '3'
            case 'audio':
                artifact_type_code = '4'
            case _:
                artifact_type_code = '1' # image
        parameters = {
            'param1': artifact_type_code,
            'param2': '0',
            'param3': artifact_absolute_url,
            'param4': '',
            'param5': '',
            'param6': '',
            'param7': json_data,
        }
        logger.info(f"DAMStoreVAST: Saving {artifact_type.title()}: {artifact_absolute_url}")
        response = self.query('create_resource', parameters)
        # We expect an integer...
        if self.is_integer(response.text):
            return int(response.text)
        if response.text.lower() == "false":
            raise Exception(f"{artifact_type.title()} cannot be saved in DAM: {artifact_absolute_url}")
        if response.text.startswith('"'):
            raise Exception(f"{artifact_type.title()} cannot be saved in DAM: {artifact_absolute_url}: {response.text}")
        raise Exception(response.text)

    def get_resource(self, resource_id):
        logger.info(f"DAMStoreVAST: get_resource(): {resource_id}")
        response = self.query('get_resource_all_image_sizes', {'resource': resource_id})
        ## We expect JSON.
        return self.to_json(response)

    def get_resource_data(self, resource_id):
        logger.info(f"DAMStoreVAST: get_resource_data(): {resource_id}")
        response = self.query('get_resource_data', {'resource': resource_id})
        ## We expect JSON.
        return self.to_json(response)

    def delete_resource(self, resource_id):
        logger.info(f"DAMStoreVAST: delete_resource(): {resource_id}")
        response = self.query('delete_resource', {'resource': resource_id})
        ## We expect boolean.
        return self.to_boolean(response)

    def to_json(self, response):
        return json.loads(response.text)

    def json_get_object_matching_property(self, json_data, attr='size_code', value='original'):
        return next(o for o in json_data if o[attr] == value)

    def get_size(self, json_data, size='original'):
        return self.json_get_object_matching_property(json_data, 'size_code', size)

    def is_absolute(self, url):
        return bool(urlparse(url).netloc)

    def get_absolute(self, url):
        if self.is_absolute(url):
            return url
        return self.config.config['DAM_DJANGO_MEDIA_URL_PREFIX']+url

    def is_integer(self, n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

    def to_boolean(self, response):
        if response.text.lower() in ('true', '1', 't', 'y', 'yes',):
            return True
        return False

if __name__ == "__main__":
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    resource_id = 23
    dam = DAMStoreVAST()
    # resource_id = dam.create_resource('https://www.vast-project.eu/wp-content/uploads/2021/01/VAST_LOGO.jpg', {
    #     'title': 'VAST Logo Test',
    #     'description': 'A test image for testing API',
    # })
    # print("ID:", resource_id)
    json_data = dam.get_resource(resource_id)
    print("url:", dam.get_size(json_data)['url'])
    dam.get_resource_data(resource_id)
    #print(response.text)
