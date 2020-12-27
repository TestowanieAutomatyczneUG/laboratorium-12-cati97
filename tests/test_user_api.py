import unittest
from src.sample.user_api import *


class TestUserApi(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = UserApi()

    def test_get_api_returns_response_success_code_200(self):
        result = self.temp.get_api('https://randomuser.me/api/')
        self.assertEqual(result.status_code, 200)


if __name__ == "__main__":
    unittest.main()