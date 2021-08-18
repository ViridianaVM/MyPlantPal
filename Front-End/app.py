from flask import Flask, Response, flash, redirect, render_template, request, session, abort
import os
import json
import requests
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
api_url = "http://52.233.91.25:5000/device_readings/"

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('landing_page.html', username = "Viri")

@app.route('/login', methods=['POST'])
def do_admin_login():
    print("ESTOY POR IMPRIMIR")
    if request.form['password'] != 'password' and request.form['username'] != 'admin':
        error = 'Invalid Credentials'
        return render_template('login.html', error=error)
        # session['logged_in'] = True
    else:
        flash('You were successfully logged in!')
        session['logged_in'] = True
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/dashboard/<device_id>/<place>")
def dashboard(device_id, place):
    moisture_readings=[]
    light_readings=[]
    temperature_readings=[]
    dates_readings=[]
    database_response = requests.get(api_url+device_id+"/plots")
    sensors_readings = database_response.json()
    # print("ESTOY IMPRIMIENDO MIS DATOS: ", database_response.json())
    for reading in sensors_readings:
        moisture_readings.append(reading["moisture_sensor"])
        light_readings.append(reading["light_sensor"])
        temperature_readings.append(reading["temperature_sensor"])
        dates_readings.append(reading["reading_time"])
    return render_template("dashboard.html", moisture_data = json.dumps(moisture_readings),
        light_data = json.dumps(light_readings),
        temperature_data = json.dumps(temperature_readings),
        dates = json.dumps(dates_readings),
        place_name = place)

if __name__ == "__main__":
    # app.run(debug=True,host='0.0.0.0', port=5050)
    app.run()
