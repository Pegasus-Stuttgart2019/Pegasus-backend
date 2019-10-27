from flask import current_app
from pegasus.external_services.departuers import Departures
def set_current_fligth(id):
    current_app.fligth_id = id

def remove_current_fligth():
    current_app.fligth_id = False



