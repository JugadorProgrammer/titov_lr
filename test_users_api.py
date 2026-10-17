import unittest
import users_api
from users_api import app, users


class UsersApiTests(unittest.TestCase):
    def setUp(self):
        users.clear()
        users_api.next_user_id = 1
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

    def test_get_user_by_id(self):
        data = {"name": "Alex", "email": "alex@example.com", "role": "developer"}
        self.client.post("/users", json=data)
        response = self.client.get("/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"id": 1, **data})

    def test_get_unknown_user(self):
        response = self.client.get("/users/999")
        self.assertEqual(response.status_code, 404)

    def test_create_without_name(self):
        data = {"email": "alex@example.com", "role": "developer"}
        response = self.client.post("/users", json=data)
        self.assertEqual(response.status_code, 400)

    def test_create_with_empty_name(self):
        data = {"name": "", "email": "alex@example.com", "role": "developer"}
        response = self.client.post("/users", json=data)
        self.assertEqual(response.status_code, 400)

    def test_create_without_email(self):
        data = {"name": "Alex", "role": "developer"}
        response = self.client.post("/users", json=data)
        self.assertEqual(response.status_code, 400)

    def test_create_with_invalid_email(self):
        data = {"name": "Alex", "email": "wrong-email", "role": "developer"}
        response = self.client.post("/users", json=data)
        self.assertEqual(response.status_code, 400)

    def test_create_with_duplicate_email(self):
        data = {"name": "Alex", "email": "alex@example.com", "role": "developer"}
        self.client.post("/users", json=data)
        response = self.client.post("/users", json=data)
        self.assertEqual(response.status_code, 409)

    def test_update_user_name(self):
        data = {"name": "Alex", "email": "alex@example.com", "role": "developer"}
        self.client.post("/users", json=data)
        response = self.client.patch("/users/1", json={"name": "Alexander"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Alexander")
        self.assertEqual(self.client.get("/users/1").get_json()["name"], "Alexander")

    def test_update_user_role(self):
        data = {"name": "Alex", "email": "alex@example.com", "role": "developer"}
        self.client.post("/users", json=data)
        response = self.client.patch("/users/1", json={"role": "tester"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["role"], "tester")

    def test_update_unknown_user(self):
        response = self.client.patch("/users/999", json={"role": "tester"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "User not found"})

    def test_delete_user(self):
        data = {"name": "Alex", "email": "alex@example.com", "role": "developer"}
        self.client.post("/users", json=data)
        response = self.client.delete("/users/1")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.client.get("/users").get_json(), [])

    def test_delete_unknown_user(self):
        response = self.client.delete("/users/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "User not found"})

    def test_user_id_not_reused_after_deletion(self):
        alex = {"name": "Alex", "email": "alex@example.com", "role": "developer"}
        maria = {"name": "Maria", "email": "maria@example.com", "role": "tester"}
        self.client.post("/users", json=alex)
        self.client.delete("/users/1")
        response = self.client.post("/users", json=maria)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["id"], 2)
