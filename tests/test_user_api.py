import unittest
from src.sample.user_api import *
from assertpy import assert_that


class TestUserApi(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = UserApi('https://randomuser.me/api/')

    def test_get_api_returns_response_success_code_200(self):
        response = self.temp.get_api(self.temp.main_url)
        self.assertEqual(response.status_code, 200)

    def test_get_api_returns_response_failure_code(self):
        response = self.temp.get_api(self.temp.main_url + 'j')
        self.assertNotEqual(response.status_code, 200)

    def test_get_api_returns_response_not_none(self):
        response = self.temp.get_api(self.temp.main_url)
        assert_that(response).is_not_none()

    def test_get_json_only_results_no_info(self):
        response = self.temp.get_api(self.temp.main_url + '?noinfo')
        json = self.temp.get_json(response)
        assert_that(json["results"]).is_not_empty()

    def test_include_only_parameter(self):
        result = self.temp.get_users_only_with_parameter('name')
        assert_that(result[0]).contains_key('name')



if __name__ == "__main__":
    unittest.main()