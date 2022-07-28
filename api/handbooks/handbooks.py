import json

import requests

from .urls import *
from ..api import Api


class Districts(Api):
    def __init__(self):
        super().__init__(DISTRICT_URL)


class Regions(Api):
    def __init__(self):
        super().__init__(REGION_URL)

    def get_on_page(self, start, limit=20):
        return requests.get(f'{self.url}/{start}/{limit}').json()


class Cities(Api):
    def __init__(self):
        super().__init__(CITY_URL)

    def get_on_page(self, start, limit=20):
        return requests.get(f'{self.url}/{start}/{limit}').json()


class CityRegions(Api):
    def __init__(self):
        super().__init__(CITY_REGION_URL)

    def get_on_page(self, start, limit=20):
        return requests.get(f'{self.url}/{start}/{limit}').json()


class Streets(Api):
    def __init__(self):
        super().__init__(STREET_URL)

    def get_on_page(self, start, limit=20):
        return requests.get(f'{self.url}/{start}/{limit}').json()


class Locations:
    def __init__(self):
        self.url = HANDBOOK_URL

    def get_address(self, data):
        return requests.post(f'{self.url}/address', data=json.dumps(data)).json()


class Handbooks(Api):
    def __init__(self):
        super().__init__(HANDBOOK_URL)

    def get(self, handbook_id):
        return requests.get(f'{self.url}/handbook/{handbook_id}').json()

    def get_checked(self, handbook_id, handbook_type):
        return requests.get(f'{self.url}/{handbook_type}/{handbook_id}').json()

    def get_all(self, handbook_type):
        return requests.get(f'{self.url}/{handbook_type}').json()

    def get_on_page(self, handbook_type, start, limit=20):
        return requests.get(f'{self.url}/{handbook_type}/{start}/{limit}').json()


class NewBuildings(Api):
    def __init__(self):
        super().__init__(NEW_BUILDING_URL)

    def get_on_page(self, start, limit=20):
        return requests.get(f'{self.url}/{start}/{limit}').json()


class Clients(Api):
    def __init__(self):
        super().__init__(CLIENT_URL)

    def get_on_page(self, start, limit=20):
        return requests.get(f'{self.url}/{start}/{limit}').json()
