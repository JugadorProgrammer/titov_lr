from flask import Flask, request

app = Flask(__name__)
users = []


@app.get("/users")
def get_users():
    return users


@app.post("/users")
def create_user():
    data = request.get_json()
    if not data.get("name"):
        return {"error": "Name is required"}, 400
    user = {**data, "id": len(users) + 1}
    users.append(user)
    return user, 201


@app.get("/users/<int:user_id>")
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}, 404
