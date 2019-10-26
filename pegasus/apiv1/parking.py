from flask import Blueprint, flash, g, redirect, request, session, current_app
import time
bp = Blueprint('parking', __name__, url_prefix='/')

@bp.route('/')
def hello():
    
    from pegasus.models.parking import ParkingData
    print("geting csv data")
    test = ParkingData()
    
    return str(test.keys)