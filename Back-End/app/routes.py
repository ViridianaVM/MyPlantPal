from flask import Blueprint, request, jsonify, make_response
from dotenv import load_dotenv

import os
import requests

from app import db
from app.models.user import User


user_bp = Blueprint("user", __name__, url_prefix="/users")
load_dotenv()

"""
CRUD FOR USER
"""
@user_bp.route("", methods=["POST"], strict_slashes=False)
def create_user():
    #Reads the HTTP request boby with:
    request_body = request.get_json()

    if len(request_body) == 2:
        new_user = User(token_id = request_body["token_id"], device_id = request_body["device_id"])
        db.session.add(new_user)
        db.session.commit()
        response = {
            "device_id" : new_user.device_id,
            "status" : 201 
        }
        return make_response(response,201)
    
    elif ("token_id" not in request_body) or ("device_id" not in request_body):
        response = {
            "error": "Invalid data"
        }
        return make_response(response,400)

