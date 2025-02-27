
from datetime import date
from flask.json import JSONEncoder
from flask_cors import CORS
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_sqlalchemy_session import flask_scoped_session
from flask_jwt_extended import JWTManager
from config import Config
from flask import Flask

# engine = create_engine(
#     'mysql+mysqlconnector://dbmasteruser:oY_w+vBkOJ9wW#qO087d!G>_?7[`X7}]@ls-e43f932a72e8734b573077e2ac603a69c356c1ed.cpobec3ma8he.ap-southeast-1.rds.amazonaws.com:3306', echo=True)
# existing_databases = engine.execute("SHOW DATABASES;")
# # Results are a list of single item tuples, so unpack each tuple
# existing_databases = [d[0] for d in existing_databases]

# # Create database if not exists
# if 'tourism' not in existing_databases:
#     engine.execute("CREATE DATABASE tourism")
#     print("Created database tourism")

url = 'mysql+mysqlconnector://dbmasteruser:oY_w+vBkOJ9wW#qO087d!G>_?7[`X7}]@ls-e43f932a72e8734b573077e2ac603a69c356c1ed.cpobec3ma8he.ap-southeast-1.rds.amazonaws.com:3306/tourism'
Base = declarative_base()
mysql_engine = create_engine(url, echo=True)
session_factory = sessionmaker(bind=mysql_engine)

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.json_encoder = CustomJSONEncoder
session = flask_scoped_session(session_factory, app)
jwt = JWTManager(app)

from app.routers.users_router import *
from app.routers.tourisms_router import *

app.register_blueprint(users_blueprint)
app.register_blueprint(tourisms_blueprint)
