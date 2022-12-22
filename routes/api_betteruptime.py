from flask import request
from flask_restful import Resource, reqparse

from utils.common import is_not_empty
from utils.slack import incident_message


incident_parser = reqparse.RequestParser()
incident_parser.add_argument('data', type=dict)

def get_body_val(req, key):
    if 'data' in req and is_not_empty(req['data']) and key in req['data'] and is_not_empty(req['data'][key]):
        return str(req['data'][key])
    return None

class BetteruptimeEndPoint(Resource):
    def post(self):
        request.get_json(force=True)
        req = incident_parser.parse_args()

        started_at = get_body_val(req, 'started_at')
        resolved_at = get_body_val(req, 'resolved_at')
        acknowledged_at = get_body_val(req, 'acknowledged_at')
        url = get_body_val(req, 'url')
        cause = get_body_val(req, 'cause')

        if is_not_empty(resolved_at):
            msg = ":smile_cat: [{}] Incident resolved: name = {}, url = {}, cause = {}".format(resolved_at, url, cause)
        elif is_not_empty(acknowledged_at):
            msg = ":crying_cat_face: [{}] Incident acknowledged: name = {}, url = {}, cause = {}".format(acknowledged_at, url, cause)
        else:
            msg = ":scream_cat: [{}] New incident: name = {}, url = {}, cause = {}".format(started_at, url, cause)
        
        incident_message('betteruptime', msg)

        
