from flask import Flask

from app.blueprints.index import bp as bp_index
from app.blueprints.task import bp as bp_task


def register_blueprints(app: Flask):
    app.register_blueprint(bp_index)
    app.register_blueprint(bp_task)
