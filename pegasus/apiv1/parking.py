from flask import Blueprint, flash, g, redirect, request, session, current_app,Response
import random
import time
from pegasus.models.parking import ParkingData
bp = Blueprint('apv1', __name__, url_prefix='/apiv1')

@bp.route('/parkingfind')
def find_best_parking():
    
    parking_data = ParkingData()

    parkingspace =  parking_data.find_best_parkingspace((10,25),1)
    response_data = []

    best_parking, walktime = parkingspace[0]
    alternatives = parkingspace[1]
    response_data.append({
        "name":str(best_parking),
        "value": str(walktime),
        "description": "This parkingspcase has the shorstest walking time to your Terminal" ,
    })
    count = 0
    for alt in alternatives:
        if count < 3:
            response_data.append({
                "name":str(alt[0]),
                "value": random.randint(0,20), #str(alt[1]),
                "description": "This parkingspcase is an alternativ" ,
            })
        count += 1
    
    headers = {
        'Access-Control-Allow-Origin': '*'
    } 
    return ({ "data": response_data }, headers )
