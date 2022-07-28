import json
import requests


class Api:
    def __init__(self, url):
        self.url = url

    def get_all(self):
        return requests.get(self.url).json()

    def get(self, object_id):
        return requests.get(f'{self.url}/{object_id}').json()

    def add(self, data):
        return requests.post(self.url, data=json.dumps(data)).json()

    def refactor(self, object_id, data):
        return requests.put(f'{self.url}/{object_id}', data=json.dumps(data)).json()

    def delete(self, object_id):
        return requests.delete(f'{self.url}/{object_id}').json()
