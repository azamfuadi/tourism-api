from app import session
from flask import jsonify, request
from flask_jwt_extended import *
import datetime
import uuid
from app.models.tourisms_model import Tourisms, UserPlans, Plans


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
    # userPlans = session.query(UserPlans).all()
    # result = []
    userplans = session.query(UserPlans, Plans).join(Plans).filter(
        UserPlans.user_id == userid).all()
    result = []
    if userplans is not None:
        for items in userplans:
            userPlan = {
                # "id": items.id,
                # "user_role": items.user_role,
                "name": items.Plans.name,
                "note": items.Plans.note,
                "itinerary": items.Plans.itinerary,
                "start_date": items.Plans.start_date,
                "finish_date": items.Plans.finish_date,
            }
            print(userPlan)
            result.append(userPlan)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
