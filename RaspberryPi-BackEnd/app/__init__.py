from flask import Flask, request
from flask import jsonify
from datetime import datetime
import requests
app = Flask(__name__)

api_url = "http://52.233.91.25:5000/device_readings"

@app.route("/raspberry_reading", methods=['GET'])
def get_device_reading():
    device_reading_json = {
        "device_id" : "my-plant-pal-001", 
        "moisture_sensor" : 2300,
        "temperature_sensor" : 1000,
        "light_sensor" : 100,
        "reading_time" : datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }
    
    #POST this info to the DB
    requests.post(api_url, json=device_reading_json)

    return jsonify(device_reading_json)

if __name__ == "__main__":
    app.run()