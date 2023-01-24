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
    return jsonify(result)


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
    return jsonify(user)


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
    return jsonify(user)


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
    return jsonify(data)


def insertUser(**params):
    uid = uuid.uuid4().hex
    newUser = Users(
        id=uid,
        email=params['email'],
        password=sha256_crypt.encrypt(params['password']),
    )
    session.add(newUser)
    session.commit()
    return jsonify({"message": "Insert User Succes"})
