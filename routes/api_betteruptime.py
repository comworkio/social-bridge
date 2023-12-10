import os

from flask import request
from flask_restful import Resource, reqparse

from utils.common import is_empty, is_not_empty
from utils.logger import log_msg
from utils.notif import incident_message

incident_parser = reqparse.RequestParser()
incident_parser.add_argument('data', type=dict)

def get_body_val(req, key):
    if 'data' in req and is_not_empty(req['data']):
        if 'attributes' in req['data'] and is_not_empty(req['data']['attributes']) and key in req['data']['attributes'] and is_not_empty(req['data']['attributes'][key]):
            return str(req['data']['attributes'][key])
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

        if is_not_empty(BETTERUPTIME_KEY):
            key = request.headers.get('X-Betteruptime-Key')
            if BETTERUPTIME_KEY != key:
                log_msg("WARN", "[betteruptime] try to join the webhook with the wrong header: {}".format(key))
                return {
                    'status': 'authentication_failure',
                    'reason': 'Not the right key passed as header'
                }, 401

        i = 0
        match = False
        while True:
            domain_match = os.getenv("PROD_DOMAIN_MATCH_{}".format(i))
            if is_empty(domain_match):
                if i < 0:
                    continue
                else:
                    break
            match = domain_match.lower() in url.lower()
            if match:
                break
            i = i + 1

        args = "url = {}".format(url)
        for arg in ["http_method", "id", "name", "cause", "response_content", "response_url", "screenshot_url"]:
            val = get_body_val(req, arg)
            if is_not_empty(val):
                args = "{}, {} = {}".format(args, arg, val)

        payload = dict()
        payload['username'] = PROD_USERNAME
        if is_not_empty(resolved_at):
            payload['message'] = "Resolved at {}: {}".format(resolved_at, args)
            payload['color'] = "#10A37F"
            payload['title'] = ":smile_cat: Incident resolved"
        elif is_not_empty(acknowledged_at):
            payload['message'] = "Acknowledged at {}: {}".format(acknowledged_at, args)
            payload['color'] = "#D4D5D7"
            payload['title'] = ":crying_cat_face: Incident acknowledged"
        else:
            payload['message'] = "New incident at {}: {}".format(started_at, args)
            payload['color'] = "#D80020"
            payload['title'] = ":scream_cat: New incident"

        if not match:
            log_msg("INFO", "[betteruptime] not sent : msg = {}".format(payload['message']))
            return {
                'status': 'ok'
            }

        incident_message(payload)
        return {
            'status': 'ok'
        }
