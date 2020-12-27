import unittest
from src.sample.user_api import *
from assertpy import assert_that
from unittest.mock import *


class TestUserApiMock(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = UserApi('https://randomuser.me/api/')

    @patch('src.sample.user_api.requests')
    def test_get_api_returns_response_success_code_200(self, mock_requests):
        mock_requests.get.return_value = 200
        response = self.temp.get_api(self.temp.main_url)
        self.assertEqual(response, 200)

    @patch('src.sample.user_api.requests')
    def test_get_api_returns_response_failure_code(self, mock_requests):
        mock_requests.get.return_value = 503
        response = self.temp.get_api(self.temp.main_url + 'j')
        self.assertEqual(response, 503)

    @patch('src.sample.user_api.requests')
    def test_get_api_returns_response_not_none(self, mock_requests):
        mock_requests.get.return_value = 200
        response = self.temp.get_api(self.temp.main_url)
        assert_that(response).is_not_none()

    def test_get_json_only_results_no_info(self):
        response = self.temp.get_api(self.temp.main_url + '?noinfo')
        json = self.temp.get_json(response)
        assert_that(json["results"]).is_not_empty()

    def test_include_only_parameter_name(self):
        result = self.temp.get_users_only_with_parameter('name')
        assert_that(result[0]).contains_key('name')

    def test_include_only_parameter_email(self):
        result = self.temp.get_users_only_with_parameter('email')
        assert_that(result[0]).contains_key('email')

    def test_include_two_params(self):
        result = self.temp.get_users_only_with_two_params('gender', 'phone')
        assert_that(result[0]).does_not_contain_key('name')

    def test_exclude_one_param(self):
        result = self.temp.get_users_without_param('login')
        assert_that(result[0]).does_not_contain_key('login')

    def test_get_user_with_nationality(self):
        result = self.temp.get_user_with_nationality('gb')
        assert_that(result[0]['nat']).is_equal_to('GB')

    def test_get_number_of_results(self):
        results = self.temp.get_number_of_results(50)
        assert_that(results).is_length(50)


if __name__ == "__main__":
    unittest.main()