from flask import Flask

app = Flask(__name__)
users = []


@app.get("/users")
def get_users():
    return users
