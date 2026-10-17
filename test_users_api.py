import unittest
from users_api import app


class UsersApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_users_empty(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])


if __name__ == "__main__":
    unittest.main()
