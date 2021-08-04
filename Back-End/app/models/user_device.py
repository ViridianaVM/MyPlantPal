from sqlalchemy.orm import backref
from app import db
from flask import current_app
from app.models.device_reading import Device_Reading


class User_Device(db.Model):
    __tablename__='users_devices'
    token_id = db.Column(db.String(500))
    device_id = db.Column(db.String(20), primary_key=True)
    #parent
    device_readings = db.relationship('Device_Reading', lazy=True, backref='User_Device')

    def to_json(self):
        return{
            "token_id": self.token_id,
            "device_id": self.device_id
        }
    
    def device_id_to_json(self):
        return{
            "device_id": self.device_id
        }