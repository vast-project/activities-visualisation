## Getting information from WordPress...
import requests
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values
import json
import os

import logging
logger = logging.getLogger('WPStoreVAST')

class WPStoreConfig:

    def __init__(self, env=os.path.dirname(os.path.realpath(__file__))+"/.env"):
        self.config = {
            **dotenv_values(env),  # load sensitive variables from .env file
            **os.environ,          # override loaded values with environment variables
        }

class WPStoreVAST:

    def __init__(self, config=None):
        self.default_config(config)

    def default_config(self, config):
        if not config:
            config = WPStoreConfig()
        self.config = config

    # Function to retrieve blog posts from a specific category
    def get_posts_in_category(self, category_slug='surveys', per_page=100):
        endpoint_url = f"{self.config.config['WORDPRESS_URL']}/wp-json/wp/v2/posts"
        params = {
            "category": category_slug,
            "per_page": per_page,  # Adjust as needed
        }
        # logger.info(f"WPStoreVAST: endpoint: {endpoint_url}, params: {params}")
        response = requests.get(endpoint_url, params=params)
        if response.ok:
            posts = response.json()
            return posts
        return []

    # Function to retrieve pages posts from a specific category
    def get_pages_in_category(self, category_slug='surveys', per_page=100):
        endpoint_url = f"{self.config.config['WORDPRESS_URL']}/wp-json/wp/v2/pages"
        params = {
            "category": category_slug,
            "per_page": per_page,  # Adjust as needed
        }
        # logger.info(f"WPStoreVAST: endpoint: {endpoint_url}, params: {params}")
        response = requests.get(endpoint_url, params=params)
        if response.ok:
            posts = response.json()
            return posts
        return []

    def wpforms_get_form_entries(self, form_id, status=('', 'abandoned', 'partial')):
        if not form_id:
            return None
        endpoint_url = f"{self.config.config['WORDPRESS_URL']}/wp-json/wpforms/v1/responses/{form_id}"
        auth = HTTPBasicAuth(self.config.config['WORDPRESS_WPFORMS_API_USERNAME'], self.config.config['WORDPRESS_WPFORMS_API_PASSWORD'])
        response = requests.get(endpoint_url, auth=auth)
        if response.ok:
            entries = list(filter(lambda entry: entry['status'] in status, response.json()))
            for entry in entries:
                entry['fields'] = json.loads(entry['fields'])
            return entries
        return None
