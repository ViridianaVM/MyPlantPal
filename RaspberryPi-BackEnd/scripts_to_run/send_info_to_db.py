from datetime import datetime
import requests
import time
import seeed_si114x
import seeed_dht
from grove.grove_moisture_sensor import GroveMoistureSensor


def set_device_reading():
    api_url = "http://52.233.91.25:5000/device_readings"

    #Sunlight Sensor Reading
    sunlight_sensor = seeed_si114x.grove_si114x()
    sunlight_sensor_reading =  sunlight_sensor.ReadVisible

    #Moisture Sensor Reading
    PIN=2
    moisture_sensor = GroveMoistureSensor(PIN)
    moisture_sensor_reading = moisture_sensor.moisture

    #Temperature Sensor Reading
    temperature_sensor = seeed_dht.DHT("11",12)
    humidity, temperature_sensor_reading = temperature_sensor.read()

    while True:
        device_reading_json = {
            "device_id" : "my-plant-pal-001", 
            "moisture_sensor" : int(moisture_sensor_reading),
            "temperature_sensor" : int(temperature_sensor_reading),
            "light_sensor" : int(sunlight_sensor_reading),
            "reading_time" : datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            }
        
        #POST this info to the DB
        requests.post(api_url, json=device_reading_json)

        time.sleep(60)



set_device_reading()
