from .urls import OBJECT_IMAGES_URL
import requests
from ..api import Api


class ObjectImages(Api):
    def __init__(self):
        super().__init__(OBJECT_IMAGES_URL)

    def get_image(self, file):
        return f"{self.url}/{file}"

    def add(self, object_id, files):
        return requests.post(f'{self.url}/{object_id}', files=files)

    def get_by_object(self, object_id):
        return requests.get(f'{self.url}/by_object/{object_id}').json()

    def get_all_by_object(self, object_id):
        return requests.get(f'{self.url}/all/by_object/{object_id}').json()
