from flask import Blueprint, flash, g, redirect, request, session, current_app
from pegasus.external_services import airport_legacy
 
bp = Blueprint('parking', __name__, url_prefix='/')

@bp.route('/')
def hello():
    
    test = airport_legacy.Airport_legacy(current_app.config, current_app.logger)
    
    return  test._send_request('/Airlines/Get').json()[1]