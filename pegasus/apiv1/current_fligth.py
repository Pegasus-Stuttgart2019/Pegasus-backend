from flask import current_app

def set_current_fligth(id):
    current_app.fligth_id = id

def remove_current_fligth():
    current_app.fligth_id = False