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
    if not data.get("email"):
        return {"error": "Email is required"}, 400
    email = data["email"]
    if not isinstance(email, str) or email.count("@") != 1:
        return {"error": "Invalid email"}, 400
    local, domain = email.split("@")
    if not local or "." not in domain or domain.startswith(".") or domain.endswith("."):
        return {"error": "Invalid email"}, 400
    if any(user["email"] == email for user in users):
        return {"error": "Email already exists"}, 409
    user = {**data, "id": len(users) + 1}
    users.append(user)
    return user, 201


@app.get("/users/<int:user_id>")
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}, 404


@app.patch("/users/<int:user_id>")
def update_user(user_id):
    user = next(user for user in users if user["id"] == user_id)
    data = request.get_json()
    if "name" in data:
        user["name"] = data["name"]
    if "role" in data:
        user["role"] = data["role"]
    return user
