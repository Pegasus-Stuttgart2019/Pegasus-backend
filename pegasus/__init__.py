from flask import Flask, g
from configparser import ConfigParser
from flask_sqlalchemy import SQLAlchemy
import os


def create_app():

    # create application
    app = Flask(__name__, instance_relative_config=True)
    # read in config
    config = ConfigParser()

    config.read("./config.cfg")
    app_config = config["Server"]
    air_config = config["Airport"]
    app.config.from_mapping(
        SECRET_KEY=app_config["SECRET_KEY"],
        SQLALCHEMY_DATABASE_URI=app_config["DATABASE"],
        APIKEY=air_config["apikey"],
        LEGACYURL=air_config["legacyUrl"],
        FLIGTHSTATEURL=air_config["fligthStateUrl"],
        WEATHERURL=air_config["weatherUrl"],
    )
    # connect to db
    db = SQLAlchemy()
    db.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from pegasus.apiv1 import parking

    app.register_blueprint(parking.bp)

    return app
