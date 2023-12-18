from flask import Flask

from app.blueprints.index import bp as bp_index


def register_blueprints(app: Flask):
    app.register_blueprint(bp_index)
