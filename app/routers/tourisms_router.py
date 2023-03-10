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


@app.route("/plan/insert", methods=["POST"])
def addPlan():
    params = request.json
    return tourisms_controller.createPlan(**params)


@app.route("/tourismplan/update", methods=["POST"])
def updateTourismPlan():
    params = request.json
    return tourisms_controller.updateUserPlan(**params)


@app.route("/tourismplans/<string:userid>", methods=["GET"])
def showTourismPlansbyUserId(userid):
    return tourisms_controller.showUserPlan(userid)


@app.route("/tourismplan/<string:plan_id>", methods=["GET"])
def showTourismPlansbyId(plan_id):
    return tourisms_controller.showPlanById(plan_id)


@app.route("/plancontributor/insert", methods=["POST"])
def addPlanContributor():
    params = request.json
    return tourisms_controller.addContributor(**params)


@app.route("/plantourism/insert", methods=["POST"])
def addPlanTourism():
    params = request.json
    return tourisms_controller.addTourismToPlan(**params)
