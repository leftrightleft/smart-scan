import requests
import logging

class Client:
    def __init__(self, token):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }

    def get_diff(client, compare_url):
        response = requests.get(compare_url, headers=client.headers)
        if response.status_code == 200:
            logging.info("Successfully retrieved diff")
            return response.text
        else:
            e = f"Error retrieving diff.  Response: {response.json()}"
            logging.error(e)
            raise Exception(e)