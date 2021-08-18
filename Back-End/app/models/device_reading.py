from app import db
from datetime import datetime


class Device_Reading(db.Model):
    __tablename__="device_readings"
    reading_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    moisture_sensor = db.Column(db.Integer, default=0)
    temperature_sensor = db.Column(db.Integer, default=0)
    light_sensor = db.Column(db.Integer, default=0)
    reading_time = db.Column(db.DateTime)
    received_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    #child
    device_id = db.Column(db.String(20), db.ForeignKey('users_devices.device_id'))

    def to_json(self):
        return{
            "moisture_sensor": self.moisture_sensor,
            "temperature_sensor": self.temperature_sensor,
            "light_sensor": self.light_sensor,
            "reading_time": self.reading_time,
            "received_time": self.received_time 
        }
    
    #Usefult to give a cleaner format to dates
    def to_graph_json(self):
        return{
            "moisture_sensor": self.moisture_sensor,
            "temperature_sensor": self.temperature_sensor,
            "light_sensor": self.light_sensor,
            "reading_time": self.reading_time.strftime('%d/%m/%y')
        }