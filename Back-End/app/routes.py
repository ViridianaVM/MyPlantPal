
from datetime import datetime
from datetime import timedelta
from sqlalchemy import desc
from flask import Blueprint, request, jsonify, make_response
from app import db
from dotenv import load_dotenv
from .models.user_device import User_Device
from .models.device_reading import Device_Reading
# import requests


user_device_bp = Blueprint("users_devices", __name__, url_prefix="/user_devices")
device_reading_bp = Blueprint("device_readings", __name__, url_prefix="/device_readings")
load_dotenv()

"""
CRUD FOR USER
"""
@user_device_bp.route("", methods=["POST"])
def create_user():
    request_body = request.get_json()

    if invalid_user_post_request_body(request_body):
        return make_response({"error": "Missing required data"}, 400)

    new_user = User_Device(token_id = request_body["token_id"], device_id = request_body["device_id"])
    db.session.add(new_user)
    db.session.commit()
    return make_response(f"New device with id: {new_user.device_id} successfully created", 201)


def invalid_user_post_request_body(request_body):
    if ("token_id" not in request_body) or ("device_id" not in request_body):
        return True
    return False


@user_device_bp.route("", methods=["GET"])
def get_users_list():
    users_devices_list = [user.to_json() for user in User_Device.query.all()]
    return jsonify(users_devices_list), 200


@user_device_bp.route("/<string:token_id>", methods=["GET"])
def get_user_by_id(token_id):
    #returns a list of device_ids with a JSON format fro that token_id
    users_devices_list = [user_device.device_id_to_json() for user_device in User_Device.query.filter_by(token_id=token_id).all()]

    return jsonify(users_devices_list), 200




"""
CRUD FOR DEVICE_READING
"""
@device_reading_bp.route("", methods=["POST"])
def create_device_reading():
    #Validate if user device exists otherwise bail.
    request_body = request.get_json()
    user_device = User_Device.query.get_or_404(request_body["device_id"], "Invalid device id")

    if invalid_device_reading_post_request_body(request_body):
        return make_response({"details": "Missing required data"}, 400)

    #received_time is equal to datime.now() because flask is doing weird stuff with the date when sending it to the database, which already has a default value in the model.
    device_reading = Device_Reading(device_id=request_body["device_id"], moisture_sensor=request_body["moisture_sensor"], temperature_sensor=request_body["temperature_sensor"], light_sensor=request_body["light_sensor"], reading_time = request_body["reading_time"], received_time = datetime.now() )

    db.session.add(device_reading)
    db.session.commit()

    return make_response(f"New reading for device: {device_reading.device_id} successfully created", 201)


def invalid_device_reading_post_request_body(request_body):
    if ("device_id" not in request_body) or ("moisture_sensor" not in request_body) or ("temperature_sensor" not in request_body) or ("light_sensor" not in request_body) or ("reading_time" not in request_body):
        return True
    return False


@device_reading_bp.route("/<string:device_id>/all", methods=["GET"])
def get_all_device_readings(device_id):
    # device_reading = Device_Reading.query.get_or_404(device_id, "Incorrect device id")
    device_reading_list = [device_reading.to_json() for device_reading in Device_Reading.query.filter_by(device_id=device_id).all()]
    if device_reading_list:
        return jsonify(device_reading_list), 200
    else:
        #Device_id may not exist
        return make_response({"error": "incorrect device_id or no readings for this device"}, 400)



@device_reading_bp.route("/<string:device_id>/last", methods=["GET"])
def get_last_device_reading(device_id):
    current_time = datetime.now()
    twentyfour_hours_ago = current_time - timedelta(days=1)

    device_reading_list = [device_reading.to_json() for device_reading in Device_Reading.query.filter(device_id==device_id, Device_Reading.reading_time >= twentyfour_hours_ago).order_by(desc(Device_Reading.reading_time)).limit(1)]
    if device_reading_list:
        return jsonify(device_reading_list), 200
    else:
        #TODO: Call the raspberry pi to access real time data
        real_time_reading = get_real_time_device_reading()
        if real_time_reading:
            return jsonify(real_time_reading), 200
        else:
            # If the device cannot be reached, get the last record from the database 
            return get_last_reading_stored(device_id)


def get_real_time_device_reading():
    return ""


def get_last_reading_stored(device_id):
    device_reading_list = [device_reading.to_json() for device_reading in Device_Reading.query.filter_by(device_id=device_id).order_by(desc(Device_Reading.reading_time)).limit(1)]
    if device_reading_list:
        return jsonify(device_reading_list), 200
    else:
        #TODO check how to send this to Alexa_Lambda
        return make_response({"error": "incorrect device_id or no readings for this device. Check how to send this message to Alexa"}, 400)
