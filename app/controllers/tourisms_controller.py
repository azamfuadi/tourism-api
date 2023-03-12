from app import session
from flask import jsonify, request
from flask_jwt_extended import *
import datetime
import uuid
from app.models.tourisms_model import Tourisms, Plans, UserPlans, TourismPlans
from app.models.users_model import Users


def insertTourism(**params):
    tourisms = session.query(Tourisms).all()
    nameList = []
    for items in tourisms:
        nameList.append(items.name)

    if params['name'] in nameList:
        data = {
            "message": "Tourism name already exist in the database"
        }
    else:
        uid = uuid.uuid4().hex
        newTourism = Tourisms(
            id=uid,
            name=params['name'],
            description=params['description'],
            location=params['location'],
            address=params['address'],
            contact=params['contact'],
            schedule=params['schedule'],
            img_url=params['img_url'],
        )
        session.add(newTourism)
        session.commit()
        data = {
            "message": "Insert New Tourism Success"
        }

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def showAllTourisms():
    tourisms = session.query(Tourisms).all()
    result = []
    for items in tourisms:
        tourism = {
            "id": items.id,
            "name": items.name,
            "description": items.description,
            "location": items.location,
            "address": items.address,
            "contact": items.contact,
            "schedule": items.schedule,
            "img_url": items.img_url,
        }
        result.append(tourism)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def showTourism(tourismid):
    dbresult = session.query(Tourisms).filter(Tourisms.id == tourismid).one()
    tourism = {
        "id": dbresult.id,
        "name": dbresult.name,
        "description": dbresult.description,
        "location": dbresult.location,
        "address": dbresult.address,
        "contact": dbresult.contact,
        "schedule": dbresult.schedule,
        "img_url": dbresult.img_url,
    }
    response = jsonify(tourism)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@jwt_required()
def createPlan(**params):
    current = get_jwt_identity()

    uid = uuid.uuid4().hex
    newPlan = Plans(
        id=uid,
        name=params['name'],
        note=params['note'],
        destination=params['destination'],
        start_date=params['start_date'],
        finish_date=params['finish_date'],
    )
    session.add(newPlan)
    session.commit()

    newUserPlan = UserPlans(
        plan_id=uid,
        user_id=current['id'],
        user_role='Creator',
    )
    session.add(newUserPlan)
    session.commit()

    data = {
        "message": "Insert New Tourism Plan Success"
    }

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def showUserPlan(userid):
    userplans = session.query(UserPlans).filter(
        UserPlans.user_id == userid).all()
    result = []
    if userplans is not None:
        for items in userplans:
            userPlan = {
                "plan_id": items.plans.id,
                "name": items.plans.name,
                "note": items.plans.note,
                "destination": items.plans.destination,
                "start_date": items.plans.start_date,
                "finish_date": items.plans.finish_date,
            }
            result.append(userPlan)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def showPlanById(plan_id):
    dbresult = session.query(Plans).filter(
        Plans.id == plan_id).one()

    # looking for contributor and creator data
    creator = {}
    contributors = []
    cont_users = session.query(UserPlans).filter(
        UserPlans.plan_id == plan_id).all()
    for item in cont_users:
        if item.user_role == "Contributor":
            user_cont = {
                "user_id": item.users.id,
                "email": item.users.email,
                "username": item.users.username,
                "prof_pic": item.users.prof_pic,
                "user_role": item.user_role,
            }
            contributors.append(user_cont)
        else:
            creator["user_id"] = item.users.id
            creator["email"] = item.users.email
            creator["username"] = item.users.username
            creator["prof_pic"] = item.users.prof_pic
            creator["user_role"] = item.user_role

    # looking for tourism data
    tourisms = []
    plan_tour = session.query(TourismPlans).filter(
        TourismPlans.plan_id == plan_id).all()
    for item in plan_tour:
        tour = {
            "tourism_id": item.tourisms.id,
            "name": item.tourisms.name,
            "description": item.tourisms.description,
            "address": item.tourisms.address,
            "location": item.tourisms.location,
            "img_url": item.tourisms.img_url,
            "date": item.date,
        }
        tourisms.append(tour)

    # creating plan data
    plan = {
        "id": dbresult.id,
        "name": dbresult.name,
        "creator": creator,
        "contributors": contributors,
        "note": dbresult.note,
        "destination": dbresult.destination,
        "start_date": dbresult.start_date,
        "finish_date": dbresult.finish_date,
        "tourisms": tourisms,
    }
    response = jsonify(plan)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@jwt_required()
def updateUserPlan(**params):
    dbresult = session.query(Plans).filter(
        Plans.id == params['plan_id']).one()

    if params['name'] != '':
        if isinstance(params['name'], list):
            if len(params['name']) == 0:
                name = dbresult.name
            else:
                name = params['name'][0]
        else:
            name = params['name']
    else:
        note = dbresult.name

    if params['note'] != '':
        if isinstance(params['note'], list):
            if len(params['note']) == 0:
                note = dbresult.note
            else:
                note = params['note'][0]
        else:
            note = params['note']
    else:
        note = dbresult.note

    if params['destination'] != '':
        if isinstance(params['destination'], list):
            if len(params['destination']) == 0:
                destination = dbresult.destination
            else:
                destination = params['destination'][0]
        else:
            destination = params['destination']
    else:
        destination = dbresult.destination

    if params['start_date'] != '':
        if isinstance(params['start_date'], list):
            if len(params['start_date']) == 0:
                start_date = dbresult.start_date
            else:
                start_date = params['start_date'][0]
        else:
            start_date = params['start_date']
    else:
        start_date = dbresult.start_date

    if params['finish_date'] != '':
        if isinstance(params['finish_date'], list):
            if len(params['finish_date']) == 0:
                finish_date = dbresult.finish_date
            else:
                finish_date = params['finish_date'][0]
        else:
            finish_date = params['finish_date']
    else:
        finish_date = dbresult.finish_date

    session.query(Plans).filter(
        Plans.id == params['plan_id']).update({
            "name": name,
            "note": note,
            "destination": destination,
            "start_date": start_date,
            "finish_date": finish_date,
        })
    session.commit()
    data = {
        "message": "Update User Plan Data Success"
    }

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def addContributor(**params):
    plans = session.query(UserPlans, Users).join(Users).filter(
        UserPlans.plan_id == params['plan_id']).all()
    userList = []
    for items in plans:
        userList.append(items.UserPlans.user_id)

    if params['user_id'] in userList:
        data = {
            "message": "User Already Contributing"
        }
    else:
        newUserPlan = UserPlans(
            plan_id=params['plan_id'],
            user_id=params['user_id'],
            user_role='Contributor',
        )
        session.add(newUserPlan)
        session.commit()
        data = {
            "message": "Add New User as Contributor Success"
        }

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def addTourismToPlan(**params):
    plans = session.query(TourismPlans, Tourisms).join(Tourisms).filter(
        TourismPlans.plan_id == params['plan_id']).all()
    tourismList = []
    for items in plans:
        tourismList.append(items.TourismPlans.tourism_id)

    if params['tourism_id'] in tourismList:
        data = {
            "message": "Tourism Already Exist"
        }
    else:
        newTourismPlan = TourismPlans(
            plan_id=params['plan_id'],
            tourism_id=params['tourism_id'],
            date=params['date'],
        )
        session.add(newTourismPlan)
        session.commit()
        data = {
            "message": "Add New Tourism to Plan Success"
        }

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
