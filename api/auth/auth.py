import json
import requests
from .urls import *
from ..api import Api


class Auth:
    def __init__(self):
        self.url = AUTH_URL

    def get(self, user_id):
        return requests.get(f'{self.url}/{user_id}').json()

    def create_new_user(self, data):
        return requests.post(f'{self.url}/create/user', data=json.dumps(data)).json()

    def login_for_access_token(self, data):
        return requests.post(f'{self.url}/login', data=json.dumps(data)).json()

    def get_current_user(self, token):
        return requests.get(f'{self.url}/user/{token}').json()

    def check_user_right(self, token, right):
        data = {"token": token, "right": right}
        return requests.post(f'{self.url}/user/right', data=json.dumps(data)).json()


class UserGroups(Api):
    def __init__(self):
        super().__init__(USER_GROUPS_URL)

    def get_by_group(self, user_id):
        return requests.get(f'{self.url}/groups/{user_id}').json()

    def get_all(self, object_id):
        return requests.get(f'{self.url}/{object_id}').json()


class Rights(Api):
    def __init__(self):
        super().__init__(RIGHTS_URL)


class Groups(Api):
    def __init__(self):
        super().__init__(GROUPS_URL)

    def get_by_name(self, name):
        return requests.get(f'{self.url}/by_name/{name}').json()


class Separations(Api):
    def __init__(self):
        super().__init__(SEPARATIONS_URL)

    def get_on_page(self, start, limit=20):
        return requests.get(f'{self.url}/{start}/{limit}').json()
