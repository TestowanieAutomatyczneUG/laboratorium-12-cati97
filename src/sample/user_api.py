import requests


class UserApi:
    def __init__(self, main_url):
        self.main_url = main_url

    def get_api(self, url):
        response = requests.get(url)
        return response

    def get_json(self, response):
        return response.json()