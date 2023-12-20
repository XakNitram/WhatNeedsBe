from flask import Blueprint, render_template, request, make_response, jsonify, abort
from sqlalchemy import select

from app.extensions import db
from app.models import Task
from app.utils import is_htmx_request

bp = Blueprint('task', __name__, url_prefix="/task")


@bp.route('/', methods=["GET"])
def get():
    task_list = tuple(db.session.scalars(select(Task).order_by(Task.id.asc())))
    # if not task_list:
    #     return abort(500, "Not implemented.")
    if is_htmx_request():
        return render_template("components/task-list.html.j2", task_list=task_list)
    else:
        return make_response(jsonify({tid: task.id for tid, task in task_list}))


@bp.route('/', methods=["POST"])
def create():
    summary = request.form['summary']
    if not summary:
        return abort(400, message="Missing summary parameter.")
    task = Task(summary=summary)
    db.session.add(task)
    db.session.commit()

    if is_htmx_request():
        response = make_response(f"<p>{summary}</p>", 200)
        response.headers['HX-Trigger'] = "TaskCreated"
        return response
    else:
        return make_response(jsonify({"summary": summary}), 201)
