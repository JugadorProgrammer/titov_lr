import unittest
from users_api import app, users


class UsersApiTests(unittest.TestCase):
    def setUp(self):
        users.clear()
        self.client = app.test_client()

    def test_get_users_empty(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_user(self):
        data = {"name": "Alex", "email": "alex@example.com", "role": "developer"}
        response = self.client.post("/users", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"id": 1, **data})
