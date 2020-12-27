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

    @patch('src.sample.user_api.requests')
    def test_get_number_of_results(self, mock_requests):
        mock_requests.get.return_value = MockResponse({"results":[{"gender":"female","name":{"title":"Mademoiselle","first":"Adelina","last":"Rey"},"location":{"street":{"number":8495,"name":"Rue des Abbesses"},"city":"Oberbipp","state":"Thurgau","country":"Switzerland","postcode":3804,"coordinates":{"latitude":"-52.1992","longitude":"104.4869"},"timezone":{"offset":"-4:00","description":"Atlantic Time (Canada), Caracas, La Paz"}},"email":"adelina.rey@example.com","login":{"uuid":"0d84db9c-9176-4f5f-9826-2a36b54d9873","username":"happycat685","password":"birdie","salt":"fBy8t9wH","md5":"0aef18a400abb7e4d86db341992fb92f","sha1":"61abee1f76a8cda218ba0f8b3dfb6a9fe1b28680","sha256":"d6859e1b8cbd7bd03d7ba94ed42c4910f8b3e5a5a0b3589f21a4f6cdefa01188"},"dob":{"date":"1956-02-27T19:02:25.043Z","age":64},"registered":{"date":"2009-04-09T07:38:01.861Z","age":11},"phone":"079 654 24 12","cell":"079 556 61 96","id":{"name":"AVS","value":"756.6551.8942.43"},"picture":{"large":"https://randomuser.me/api/portraits/women/69.jpg","medium":"https://randomuser.me/api/portraits/med/women/69.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/women/69.jpg"},"nat":"CH"},{"gender":"female","name":{"title":"Ms","first":"Camille","last":"Kowalski"},"location":{"street":{"number":3801,"name":"Tecumseh Rd"},"city":"New Glasgow","state":"Nova Scotia","country":"Canada","postcode":"Z8E 6B0","coordinates":{"latitude":"-7.1023","longitude":"-135.2649"},"timezone":{"offset":"+5:00","description":"Ekaterinburg, Islamabad, Karachi, Tashkent"}},"email":"camille.kowalski@example.com","login":{"uuid":"3e88ba2e-aa88-42df-a366-2e47ca6e97fa","username":"bluepanda200","password":"hotmail1","salt":"N4Ro2CV4","md5":"aaede229bfc7cb494e98254afa69f078","sha1":"6b327e167300ac9205856462b0246974aafd3ad5","sha256":"19387662a49ced0b590a01bbbd4801c67925a75a05e1f8add4669ab861493125"},"dob":{"date":"1995-07-08T15:13:28.186Z","age":25},"registered":{"date":"2008-09-10T09:54:09.311Z","age":12},"phone":"005-009-7766","cell":"327-300-1753","id":{"name":"","value":None},"picture":{"large":"https://randomuser.me/api/portraits/women/60.jpg","medium":"https://randomuser.me/api/portraits/med/women/60.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/women/60.jpg"},"nat":"CA"}],"info":{"seed":"8f9cbf86e873a257","results":2,"page":1,"version":"1.3"}}, 200)
        results = self.temp.get_number_of_results(2)
        assert_that(results).is_length(2)


if __name__ == "__main__":
    unittest.main()