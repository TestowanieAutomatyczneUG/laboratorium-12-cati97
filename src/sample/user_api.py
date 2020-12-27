import requests

class UserApi:
    def __init__(self, main_url):
        self.main_url = main_url

    def get_api(self, url):
        response = requests.get(url)
        return response

    def get_json(self, response):
        return response.json()

    def get_users_only_with_parameter(self, param):  # option can be gender, name, email
        new_url = self.main_url + f"?inc={param}"
        response = self.get_api(new_url)
        return response.json()["results"]

    def get_users_only_with_two_params(self, param1, param2):  # option can be gender, name, email
        new_url = self.main_url + f"?inc={param1},{param2}"
        response = self.get_api(new_url)
        return response.json()["results"]

    def get_users_without_param(self, param):  # e.g. login
        new_url = self.main_url + f"?exc={param}"
        response = self.get_api(new_url)
        return response.json()["results"]

    def get_user_with_nationality(self, nationality):  # e.g. gb - great britain
        new_url = self.main_url + f"?nat={nationality.upper()}"
        response = self.get_api(new_url)
        return response.json()["results"]

    def get_number_of_results(self, length):
        new_url = self.main_url + f"?results={str(length)}"
        response = self.get_api(new_url)
        return response.json()["results"]