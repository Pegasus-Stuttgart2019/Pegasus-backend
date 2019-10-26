from flask import Blueprint, flash, g, redirect, request, session, current_app
import random
import datetime
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
                "name": str(f"P{random.randint(10,20)}"),  #str(alt[0]),
                "value": str(alt[1]),
                "description": "This parkingspcase is an alternativ" ,
            })
        count += 1
    
    headers = {
        'Access-Control-Allow-Origin': '*'
    } 
    return ({ "data": response_data }, headers )

from pegasus.external_services.airport_legacy import Airport


@bp.route('/waiting')
def terminal_waiting():
    
    api = Airport(current_app.config, current_app.logger)

    response = api._send_request('/Apps/AirportSTR/SecurityCheckpoints/GetWaitTimes')

    if response.status_code != 200: 
        output = { "data": [] }
    else:
        output =  response.json()
    
    
    headers = {
        'Access-Control-Allow-Origin': '*'
    } 
    return ( { "data": output }, headers )

from pegasus.external_services.departuers import Departures

@bp.route('/fligthid')
def get_fligth_by_id():
    try:
        fligth_id = int(request.args.get('id'))
    except ValueError:
        fligth_id = request.args.get('id')
    
    print(fligth_id)
    departures = Departures(current_app.config, current_app.logger)

    fligth = departures.getDeparturesById(fligth_id)
    if fligth_id != None:
        return fligth

    
