from os.path import abspath

from flask import Flask
from app.blueprints import register_blueprints
from app.extensions import db


def create_app():
    proto_app = Flask(__name__)
    proto_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wnb.db"
    proto_app.config["APP_PATH"] = abspath(__file__)
    proto_app.jinja_env.trim_blocks = True
    proto_app.jinja_env.lstrip_blocks = True
    # db.app = proto_app
    db.init_app(proto_app)
    register_blueprints(proto_app)
    with proto_app.app_context():
        db.create_all()
    return proto_app
