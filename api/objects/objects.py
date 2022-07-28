import requests
from .urls import *
from ..api import Api


class Objects(Api):
    def __init__(self):
        super().__init__(OBJECTS_URL)

    def get_by_category(self, category_id):
        return requests.get(f'{self.url}/type/{category_id}').json()


class Apartments(Api):
    def __init__(self):
        super().__init__(APARTMENTS_URL)

    def get_by_object(self, object_id):
        return requests.get(f'{self.url}/objects/{object_id}').json()


class ObjectTypes(Api):
    def __init__(self):
        super().__init__(OBJECT_TYPES_URL)
