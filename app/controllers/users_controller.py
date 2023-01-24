from flask import jsonify, request
from app import session
from app.models.users_model import Users
from flask_jwt_extended import *
from passlib.hash import sha256_crypt
import datetime
import uuid


# @jwt_required()
def showAllUsers():
    users = session.query(Users).all()
    result = []
    for items in users:
        user = {
            "id": items.id,
            "username": items.username,
            "email": items.email,
            "password": items.password,
            "prof_pic": items.prof_pic,
            "birth_date": items.birth_date,
            "gender": items.gender,
        }
        result.append(user)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def showUserById(userid):
    dbresult = session.query(Users).filter(
        Users.id == userid).one()
    user = {
        "id": dbresult.id,
        "username": dbresult.username,
        "email": dbresult.email,
        "password": dbresult.password,
        "prof_pic": dbresult.prof_pic,
        "birth_date": dbresult.birth_date,
        "gender": dbresult.gender,
    }
    response = jsonify(user)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@jwt_required()
def showUserData():
    current = get_jwt_identity()
    dbresult = session.query(Users).filter(
        Users.id == current['id']).one()
    user = {
        "id": dbresult.id,
        "username": dbresult.username,
        "email": dbresult.email,
        "password": dbresult.password,
        "prof_pic": dbresult.prof_pic,
        "birth_date": dbresult.birth_date,
        "gender": dbresult.gender,
    }
    response = jsonify(user)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def generateToken(**param):
    dbresult = session.query(Users).filter(
        Users.email == param['email']).first()
    if dbresult is not None:
        authenticated = sha256_crypt.verify(
            param['password'], dbresult.password)
        if authenticated:
            user = {
                "id": dbresult.id,
                "username": dbresult.username,
                "email": dbresult.email,
                "prof_pic": dbresult.prof_pic,
                "birth_date": dbresult.birth_date,
                "gender": dbresult.gender,
            }
            expires = datetime.timedelta(days=1)
            expires_refresh = datetime.timedelta(days=3)
            access_token = create_access_token(
                user, fresh=True, expires_delta=expires)

            data = {
                "data": user,
                "token_access": access_token
            }
        else:
            data = {
                "message": "Password salah"
            }
    else:
        data = {
            "message": "Email tidak terdaftar"
        }
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def insertUser(**params):
    users = session.query(Users).all()
    emailList = []
    for items in users:
        emailList.append(items.email)

    if params['email'] in emailList:
        data = {
            "message": "Email already exist in the database"
        }
    else:
        uid = uuid.uuid4().hex
        newUser = Users(
            userid=uid,
            email=params['email'],
            password=sha256_crypt.encrypt(params['password']),
        )
        session.add(newUser)
        session.commit()
        data = {
            "message": "Insert user success"
        }

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
