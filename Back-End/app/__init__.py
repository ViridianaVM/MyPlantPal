from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")
    
    app.url_map.strict_slashes = False

    # Import models here for Alembic setup
    from app.models.user_device import User_Device
    from app.models.device_reading import Device_Reading


    db.init_app(app)
    migrate.init_app(app, db)


    # Register Blueprints here
    from .routes import user_device_bp
    app.register_blueprint(user_device_bp)
    from .routes import device_reading_bp
    app.register_blueprint(device_reading_bp)


    CORS(app)
    return app

