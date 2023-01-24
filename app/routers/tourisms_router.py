from app import app
from app.controllers import tourisms_controller
from flask import Blueprint, request

tourisms_blueprint = Blueprint("tourisms_router", __name__)