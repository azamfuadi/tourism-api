from app import app
from app.controllers import tourisms_controller
from flask import Blueprint, request

tourisms_blueprint = Blueprint("tourisms_router", __name__)


@app.route("/tourisms", methods=["GET"])
def showAllTourisms():
    return tourisms_controller.showAllTourisms()


@app.route("/tourism/insert", methods=["POST"])
def addTourism():
    params = request.json
    return tourisms_controller.insertTourism(**params)


@app.route("/tourismplan/insert", methods=["POST"])
def addTourismPlan():
    params = request.json
    return tourisms_controller.createPlan(**params)


@app.route("/tourismplans/<string:userid>", methods=["GET"])
def showTourismPlansbyUserId(userid):
    return tourisms_controller.showUserPlan(userid)
