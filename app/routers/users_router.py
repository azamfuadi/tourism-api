from app import app
from app.controllers import users_controller
from flask import Blueprint, request

users_blueprint = Blueprint("users_router", __name__)


@app.route("/")
def main():
    return "Welcome"


@app.route("/users", methods=["GET"])
def showAllUsers():
    return users_controller.showAllUsers()


@app.route("/user/profile", methods=["GET"])
def showAUserProfile():
    return users_controller.showUserData()


@app.route("/user/update", methods=["POST"])
def editUser():
    params = request.json
    return users_controller.updateUser(**params)


@app.route("/user/<string:userid>", methods=["GET"])
def showUserById(userid):
    return users_controller.showUserById(userid)


@app.route("/user/login", methods=["POST"])
def requestToken():
    params = request.json
    return users_controller.generateToken(**params)


@app.route("/user/insert", methods=["POST"])
def addUser():
    params = request.json
    return users_controller.insertUser(**params)
