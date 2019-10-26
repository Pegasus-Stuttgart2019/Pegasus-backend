from flask import Flask, g
from configparser import ConfigParser
import os
from flask_cors import CORS


def create_app():

    # create application
    app = Flask(__name__, instance_relative_config=True)
    # read in config
    
    

    from pegasus.config import Config
    app.config.from_object(Config)
    CORS(app)
    app.fligth_id = 2895621


    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from pegasus.apiv1 import parking

    @app.route('/')
    def hello_page():
        return 'Hell'

    app.register_blueprint(parking.bp)

    return app