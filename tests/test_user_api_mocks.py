import unittest
from src.sample.user_api import *
from assertpy import assert_that
from unittest.mock import *


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data["results"]


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

    @patch('src.sample.user_api.requests')
    def test_get_json_only_results_no_info(self, mock_requests):
        mock_requests.get.return_value = [{"gender":"female","name":{"title":"Mrs","first":"Lauren","last":"Brooks"},"location":{"street":{"number":3504,"name":"West Street"},"city":"Sligo","state":"Offaly","country":"Ireland","postcode":19283,"coordinates":{"latitude":"17.4256","longitude":"173.3981"},"timezone":{"offset":"+7:00","description":"Bangkok, Hanoi, Jakarta"}},"email":"lauren.brooks@example.com","login":{"uuid":"918c5edb-1f1a-4356-8be8-2b8a93eaae6c","username":"orangedog748","password":"trisha","salt":"0fQlwycR","md5":"ed71e1303fc65b2d48e1e7157ad38215","sha1":"aa6a6686c2c873883592372b01d1c3ff4252c298","sha256":"d45a6f92d5cbb2e164d0e3f6eb03bd5467d64f79cb408c628129ffb6c9cae588"},"dob":{"date":"1973-06-08T00:32:34.887Z","age":47},"registered":{"date":"2013-09-07T02:40:40.583Z","age":7},"phone":"021-966-9371","cell":"081-734-5814","id":{"name":"PPS","value":"5508904T"},"picture":{"large":"https://randomuser.me/api/portraits/women/58.jpg","medium":"https://randomuser.me/api/portraits/med/women/58.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/women/58.jpg"},"nat":"IE"}]
        response = self.temp.get_api(self.temp.main_url + '?noinfo')
        assert_that(response).is_not_empty()

    @patch('src.sample.user_api.requests')
    def test_include_only_parameter_name(self, mock_requests):
        mock_requests.get.return_value = MockResponse({'results': [{'name': {'title': 'Mr', 'first': 'Billy', 'last': 'Morgan'}}], 'info': {'seed': '27be2018e022f702', 'results': 1, 'page': 1, 'version': '1.3'}}, 200)
        result = self.temp.get_users_only_with_parameter('name')
        assert_that(result[0]).contains_key('name')

    @patch('src.sample.user_api.requests')
    def test_include_only_parameter_email(self, mock_requests):
        mock_requests.get.return_value = MockResponse({"results":[{"email":"adriano.lemaire@example.com"}],"info":{"seed":"febadb88cd49f5a4","results":1,"page":1,"version":"1.3"}}, 200)
        result = self.temp.get_users_only_with_parameter('email')
        assert_that(result[0]).contains_key('email')

    @patch('src.sample.user_api.requests')
    def test_include_two_params(self, mock_requests):
        mock_requests.get.return_value = MockResponse({"results":[{"gender":"male","phone":"47910989"}],"info":{"seed":"0fcd53b1bf0c14dc","results":1,"page":1,"version":"1.3"}}, 200)
        result = self.temp.get_users_only_with_two_params('gender', 'phone')
        assert_that(result[0]).does_not_contain_key('name')

    @patch('src.sample.user_api.requests')
    def test_exclude_one_param(self, mock_requests):
        mock_requests.get.return_value = MockResponse({"results":[{"gender":"female","name":{"title":"Ms","first":"Gül","last":"Çörekçi"},"location":{"street":{"number":9117,"name":"Bağdat Cd"},"city":"Kırklareli","state":"Niğde","country":"Turkey","postcode":79578,"coordinates":{"latitude":"69.5480","longitude":"110.0547"},"timezone":{"offset":"+1:00","description":"Brussels, Copenhagen, Madrid, Paris"}},"email":"gul.corekci@example.com","dob":{"date":"1952-12-05T21:15:15.065Z","age":68},"registered":{"date":"2016-02-13T06:29:35.729Z","age":4},"phone":"(733)-000-0193","cell":"(943)-248-8666","id":{"name":"","value":0},"picture":{"large":"https://randomuser.me/api/portraits/women/96.jpg","medium":"https://randomuser.me/api/portraits/med/women/96.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/women/96.jpg"},"nat":"TR"}],"info":{"seed":"66c995cf34cd543d","results":1,"page":1,"version":"1.3"}}, 200)
        result = self.temp.get_users_without_param('login')
        assert_that(result[0]).does_not_contain_key('login')

    @patch('src.sample.user_api.requests')
    def test_get_user_with_nationality(self, mock_requests):
        mock_requests.get.return_value = MockResponse({"results":[{"gender":"male","name":{"title":"Mr","first":"Herbert","last":"Ray"},"location":{"street":{"number":1146,"name":"Kings Road"},"city":"Newcastle upon Tyne","state":"County Fermanagh","country":"United Kingdom","postcode":"H51 0LB","coordinates":{"latitude":"-40.5244","longitude":"-30.4977"},"timezone":{"offset":"-4:00","description":"Atlantic Time (Canada), Caracas, La Paz"}},"email":"herbert.ray@example.com","login":{"uuid":"6b414835-e39c-4e81-a9cb-e6224ced1123","username":"smallpanda901","password":"monica","salt":"6oMV4Ih3","md5":"b7029a76ac2e7841b6e4ac3828fac6cf","sha1":"61bd78a09c930b233e98dc989a11c87c3093cb20","sha256":"59a00168a164df1e0d8dee6d950727a90a034080e2c081e85b09107f4abe9a76"},"dob":{"date":"1966-02-24T14:18:22.822Z","age":54},"registered":{"date":"2004-10-10T16:42:58.118Z","age":16},"phone":"0110443 310 7223","cell":"0767-917-876","id":{"name":"NINO","value":"EP 34 86 92 S"},"picture":{"large":"https://randomuser.me/api/portraits/men/18.jpg","medium":"https://randomuser.me/api/portraits/med/men/18.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/men/18.jpg"},"nat":"GB"}],"info":{"seed":"d15094872502fca6","results":1,"page":1,"version":"1.3"}}, 200)
        result = self.temp.get_user_with_nationality('gb')
        assert_that(result[0]['nat']).is_equal_to('GB')

    def test_get_number_of_results(self):
        results = self.temp.get_number_of_results(50)
        assert_that(results).is_length(50)


if __name__ == "__main__":
    unittest.main()