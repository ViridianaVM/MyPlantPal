from app import db
from flask import current_app


class User(db.Model):
    __tablename__="users"
    token_id = db.Column(db.String(415), primary_key=True)
    device_id = db.Column(db.String(415))


    def to_json(self):
        return{
            "token_id": self.token_id,
            "device_id": self.device_id
        }