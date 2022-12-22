from flask_restful import Resource

class RootEndPoint(Resource):
    def get(self):
        return {
            'status': 'ok',
            'alive': True
        }
