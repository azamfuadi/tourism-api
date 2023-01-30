from app import session
from flask import jsonify, request
from flask_jwt_extended import *
import datetime
import uuid
from app.models.tourisms_model import Tourisms, UserPlans, Plans
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
            "img_url": items.img_url,
        }
        result.append(tourism)
    response = jsonify(result)
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
        itinerary=params['itinerary'],
        start_date=params['start_date'],
        finish_date=params['finish_date'],
        tourism_id=params['tourism_id'],
    )
    session.add(newPlan)
    session.commit()

    uid2 = uuid.uuid4().hex
    newUserPlan = UserPlans(
        id=uid2,
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
    userplans = session.query(UserPlans, Plans).join(Plans).filter(
        UserPlans.user_id == userid).all()
    result = []
    if userplans is not None:
        for items in userplans:
            userPlan = {
                "plan_id": items.Plans.id,
                "name": items.Plans.name,
                "creator_email": items.Plans.creator_email,
                "note": items.Plans.note,
                "itinerary": items.Plans.itinerary,
                "start_date": items.Plans.start_date,
                "finish_date": items.Plans.finish_date,
            }
            result.append(userPlan)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def showPlanById(plan_id):
    dbresult = session.query(Plans).filter(
        Plans.id == plan_id).one()

    # looking for creator data
    cresult = session.query(Users).filter(
        Users.email == dbresult.creator_email).one()
    creator = {
        "user_id": cresult.id,
        "email": cresult.email,
        "username": cresult.username,
        "prof_pic": cresult.prof_pic,
    }

    # looking for contributor data
    cont_users = session.query(UserPlans, Users).join(Users).filter(
        UserPlans.plan_id == plan_id).all()
    contributors = []
    if cont_users is not None:
        for items in cont_users:
            if items.Users.email != dbresult.creator_email:
                user_cont = {
                    "user_id": items.Users.id,
                    "email": items.Users.email,
                    "username": items.Users.username,
                    "prof_pic": items.Users.prof_pic,
                }
                contributors.append(user_cont)

    # creating plan data
    plan = {
        "id": dbresult.id,
        "name": dbresult.name,
        "creator": creator,
        "contributor": contributors,
        "note": dbresult.note,
        "itinerary": dbresult.itinerary,
        "start_date": dbresult.start_date,
        "finish_date": dbresult.finish_date,
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

    if params['itinerary'] != '':
        if isinstance(params['itinerary'], list):
            if len(params['itinerary']) == 0:
                itinerary = dbresult.itinerary
            else:
                itinerary = params['itinerary'][0]
        else:
            itinerary = params['itinerary']
    else:
        itinerary = dbresult.itinerary

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
            "itinerary": itinerary,
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
        )
        session.add(newUserPlan)
        session.commit()
        data = {
            "message": "Add New User as Contributor Success"
        }

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
