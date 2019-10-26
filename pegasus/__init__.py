from flask import Flask, g
from configparser import ConfigParser
import os


def create_app():

    # create application
    app = Flask(__name__, instance_relative_config=True)
    # read in config
    print("helo world")

    from pegasus.config import Config
    app.config.from_object(Config)




    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from pegasus.apiv1 import parking

    @app.route('/)')
    def hello_page():
        return 'Hell'

    app.register_blueprint(parking.bp)

    return app