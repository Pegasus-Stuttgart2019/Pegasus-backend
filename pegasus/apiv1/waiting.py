from flask import Blueprint, flash, g, redirect, request, session, current_app,Response
from pegasus.apiv1.parking import bp


@bp.route('/waiting')
def ():
    
    headers = {
        'Access-Control-Allow-Origin': '*'
    } 
    return ({ "data": response_data }, headers )
