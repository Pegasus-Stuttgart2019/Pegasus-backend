from flask import Blueprint, flash, g, redirect, request, session, current_app
import random
import datetime
from pegasus.models.parking import ParkingData

bp = Blueprint("apv1", __name__, url_prefix="/apiv1")


@bp.route("/parkingfindalex")
def find_best_parking():

    parking_data = ParkingData()

    parkingspace = parking_data.find_best_parkingspace((10, 25), 1)
    response_data = []

    best_parking, walktime = parkingspace[0]
    alternatives = parkingspace[1]
    response_data.append(
        {
            "name": str(best_parking),
            "value": str(walktime),
            "description": "This parkingspcase has the shorstest walking time to your Terminal",
            "topic": "P",
        }
    )
    count = 0
    for alt in alternatives:
        if count < 5:
            response_data.append(
                {
                    "name": str(f"P{random.randint(10,20)}"),  # str(alt[0]),
                    "value": str(alt[1]),
                    "description": "This parkingspcase is an alternativ",
                    "topic": "P",
                }
            )
        count += 1

    return {"data": response_data}


from pegasus.external_services.airport_legacy import Airport


@bp.route("/waiting")
def terminal_waiting():

    api = Airport(current_app.config, current_app.logger)

    response = api._send_request("/Apps/AirportSTR/SecurityCheckpoints/GetWaitTimes")

    if response.status_code != 200:
        output = {"data": []}
    else:
        output = response.json()

    headers = {"Access-Control-Allow-Origin": "*"}
    return ({"data": output}, headers)


from pegasus.external_services.departuers import Departures


@bp.route("/fligthid")
def get_fligth_by_id():
    try:
        fligth_id = int(request.args.get("id"))
    except ValueError:
        fligth_id = request.args.get("id")

    departures = Departures(current_app.config, current_app.logger)

    fligth = departures.getDeparturesById(fligth_id)
    if fligth_id != None:
        return fligth


from pegasus.apiv1.current_fligth import set_current_fligth, remove_current_fligth


@bp.route("/fligthstate", methods=["GET", "DELETE"])
def current_fligth():
    if request.method == "POST":

        return "success"
    if request.method == "GET":
        fligth_id = request.args.get("id")
        try:
            fligth_id = int(fligth_id)
        except ValueError:
            pass
        except TypeError:
            pass
        if fligth_id != None:
            set_current_fligth(fligth_id)
        return {"fligth_id": current_app.fligth_id}

    if request.method == "DELETE":
        print("deleting")
        remove_current_fligth()
        return "success"


from pegasus.external_services.destinations import Destionations


@bp.route("/destinations")
def airlines():
    input = str(request.args.get("input"))
    if input == None:
        return {"Code": ""}

    air = Destionations(current_app.config, current_app.logger)
    if len(input) <= 3:
        data = air.getDestinationCode(input)
    else:
        data = air.getDestinationName(input)

    return {"data": data}


from pegasus.external_services.shops import Shops


@bp.route("/recomend")
def recomend():
    shop = Shops(current_app.config, current_app.logger)

    return {"data": shop.get_recomendation()}


def get_parking_data_and_format(dest):
    parking_data = ParkingData()
    response_data = []

    parkingspace = parking_data.find_best_parkingspace((10, 25), 1)
    best_parking, walktime = parkingspace[0]
    alternatives = parkingspace[1]
    response_data.append(
        {
            "name": str(best_parking),
            "value": f"{str(walktime)} minutes by feet.",
            "description": "This parking lot has the shorstest walking time to your terminal",
            "fligth_dest": dest,
            "topic": "P",
        }
    )
    count = 0
    for alt in alternatives:
        if count < 3:
            response_data.append(
                {
                    "name": str(alt[0]),
                    "value": f"{str(alt[1])} minutes by feet.",
                    "description": "This parking lot is an alternativ",
                    "fligth_dest": dest,
                    "topic": "P",
                }
            )
        count += 1
    return response_data


def format_response(name, value, desc, dest):
    return {
        "name": name,
        "value": value,
        "description": desc,
        "fligth_dest": dest,
        "topic": "P",
    }


@bp.route("/parkingfind")
def find_best_parking2():

    departures = Departures(current_app.config, current_app.logger)
    dest = Destionations(current_app.config, current_app.logger)
    shop = Shops(current_app.config, current_app.logger)

    if departures.getDeparturesById(current_app.fligth_id) != {}:
        fligth = departures.getDeparturesById(current_app.fligth_id)
        dest = dest.getDestinationCode(fligth["Destination"]["Code"])
    else:
        dest = {}

    response_data = []
    try:
        
        dep = departures.getDeparturesById(current_app.fligth_id)
        response_data.append(
            format_response(
                dep["Name"],
                dep["Plan"],
                f"Your Flight to {str(dep['Destination']['Name']).lower().capitalize()  } it will leave at {str(datetime.datetime.strptime(dep['Plan'], '%Y-%m-%dT%H:%M:%S' ).time())[0:5]}.",
                dest,
            )
        )
        recom = shop.get_recomendation()
        response_data.append(
            format_response(
                recom["Name"],
                recom["Terminal"],
                f"Maybe you want to take a look at {recom['Name']} one of your shops",
                dest,
            )
        )
    except Exception as error:
        print(error)
        print(error.with_traceback)

    response_data.extend(get_parking_data_and_format(dest))
        

    return {"data": response_data}


@bp.route("/nextFlight")
def get_test():
    code = request.args.get("destination")
    depa = Departures(current_app.config, current_app.logger)
    if code != None:
        return {"data": depa.nextFlightTo(code)}
    return {}

 