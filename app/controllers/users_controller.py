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
def updateUser(**params):
    current = get_jwt_identity()

    if params['username'] != '':
        if isinstance(params['username'], list):
            if len(params['username']) == 0:
                username = current['username']
            else:
                username = params['username'][0]
        else:
            username = params['username']
    else:
        username = current['username']

    if params['prof_pic'] != '':
        if isinstance(params['prof_pic'], list):
            if len(params['prof_pic']) == 0:
                prof_pic = current['prof_pic']
            else:
                prof_pic = params['prof_pic'][0]
        else:
            prof_pic = params['prof_pic']
    else:
        prof_pic = current['prof_pic']

    if params['birth_date'] != '':
        if isinstance(params['birth_date'], list):
            if len(params['birth_date']) == 0:
                birth_date = current['birth_date']
            else:
                birth_date = params['birth_date'][0]
        else:
            birth_date = params['birth_date']
    else:
        birth_date = current['birth_date']

    if params['gender'] != '':
        if isinstance(params['gender'], list):
            if len(params['gender']) == 0:
                gender = current['gender']
            else:
                gender = params['gender'][0]
        else:
            gender = params['gender']
    else:
        gender = current['gender']

    if params['passwordnew'] != '':
        authenticated = sha256_crypt.verify(
            params['password'], current['password'])
        if authenticated:
            passwordnew = params['passwordnew']
            session.query(Users).filter(
                Users.id == current['id']).update({
                    "username": username,
                    "password": sha256_crypt.encrypt(passwordnew),
                    "prof_pic": prof_pic,
                    "birth_date": birth_date,
                    "gender": gender,
                })
            session.commit()
            data = {
                "message": "Update User Data Success"
            }
        else:
            data = {
                "message": "Wrong Password Verification for Password Changing"
            }
    else:
        session.query(Users).filter(
            Users.id == current['id']).update({
                "username": username,
                "prof_pic": prof_pic,
                "birth_date": birth_date,
                "gender": gender,
            })
        session.commit()
        data = {
            "message": "Update User Data Success"
        }

    response = jsonify(data)
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
                "password": dbresult.password,
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
            id=uid,
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
