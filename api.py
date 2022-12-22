from flask import Flask
from flask_restful import Api
from multiprocessing import Process

from routes.api_root import RootEndPoint
from routes.api_manifest import ManifestEndPoint
from utils.bridge import bridge

app = Flask(__name__)
api = Api(app)

health_check_routes = ['/', '/health', '/health/', '/v1/health', '/v1/health/']
manifest_routes = ['/manifest', '/manifest/', '/v1/manifest', '/v1/manifest/']

api.add_resource(RootEndPoint, *health_check_routes)
api.add_resource(ManifestEndPoint, *manifest_routes)

async_process = Process( 
    target=bridge,
    daemon=True
)
async_process.start()

if __name__ == '__main__':
    app.run()
