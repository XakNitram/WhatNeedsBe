from flask import Flask
from app.blueprints import register_blueprints


def create_app():
    proto_app = Flask(__name__)
    register_blueprints(proto_app)
    return proto_app
