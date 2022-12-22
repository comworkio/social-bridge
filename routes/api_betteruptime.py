import os

from flask import request
from flask_restful import Resource, reqparse

from utils.common import is_empty, is_not_empty
from utils.logger import log_msg
from utils.slack import incident_message

incident_parser = reqparse.RequestParser()
incident_parser.add_argument('data', type=dict)

def get_body_val(req, key):
    if 'data' in req and is_not_empty(req['data']):
        if 'attributes' in req['data'] and is_not_empty(req['data']['attributes']) and key in req['data']['attributes'] and is_not_empty(req['data']['attributes'][key]):
            return str(req['data']['attribute'][key])
        elif key in req['data'] and is_not_empty(req['data'][key]):
            return str(req['data'][key])
    
    if key in req and is_not_empty(req[key]):
        return str(req[key])
    return ""

PROD_USERNAME = os.getenv('PROD_USERNAME')
if is_empty(PROD_USERNAME):
    PROD_USERNAME = 'betteruptime'

BETTERUPTIME_KEY = os.getenv('BETTERUPTIME_KEY')

class BetteruptimeEndPoint(Resource):
    def post(self):
        request.get_json(force=True)
        req = incident_parser.parse_args()

        started_at = get_body_val(req, 'started_at')
        resolved_at = get_body_val(req, 'resolved_at')
        acknowledged_at = get_body_val(req, 'acknowledged_at')
        url = get_body_val(req, 'url')
        cause = get_body_val(req, 'cause')
        name = get_body_val(req, 'name')

        if is_not_empty(BETTERUPTIME_KEY):
            key = request.headers.get('X-Betteruptime-Key')
            if BETTERUPTIME_KEY != key:
                return {
                    'status': 'authentication_failure',
                    'reason': 'Not the right key passed as header'
                }, 401

        i = 1
        match = False
        while True:
            domain_match = os.getenv("PROD_DOMAIN_MATCH_{}".format(i))
            if is_empty(domain_match):
                break
            match = domain_match.lower() in url.lower() or domain_match.lower() in name.lower()
            if match:
                break
            i = i + 1

        if is_not_empty(resolved_at):
            msg = ":smile_cat: [{}] Incident resolved: name = {}, url = {}, cause = {}".format(resolved_at, name, url, cause)
        elif is_not_empty(acknowledged_at):
            msg = ":crying_cat_face: [{}] Incident acknowledged: name = {}, url = {}, cause = {}".format(acknowledged_at, name, url, cause)
        else:
            msg = ":scream_cat: [{}] New incident: name = {}, url = {}, cause = {}".format(started_at, name, url, cause)
        
        if not match:
            log_msg("INFO", "[betteruptime] not sent : msg = {}, req = {}".format(msg, req))
            return {
                'status': 'ok'
            }

        incident_message(PROD_USERNAME, msg)
        return {
            'status': 'ok'
        }
