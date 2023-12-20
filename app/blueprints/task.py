from flask import Blueprint, render_template, request, make_response, jsonify, abort
from sqlalchemy import select

from app.extensions import db
from app.models import Task
from app.utils import is_htmx_request

bp = Blueprint('task', __name__, url_prefix="/task")


@bp.route('/', methods=["GET"])
def get():
    task_list = tuple(db.session.scalars(select(Task).order_by(Task.id.asc())))

    # HTMX wants endpoints to return html, so this is a html-api similar to xml apis.
    # We can also use the htmx headers to decide to return data in the traditional json (or xml) format.
    #  Certainly more work and not necessary.
    if is_htmx_request():
        # This template only includes a <div> that can be slotted into a larger template with a htmx request.
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
        # POST requests can also return html that htmx can slot into the page, but the hx-swap="none"
        #  in the index template prevents that swapping from occuring, so this html is never seen.
        #  I only include it now for adherence to POST standards that want a copy of the created resource returned,
        #  but this can change in the future.
        response = make_response(f"<p>{summary}</p>", 201)

        # The HX-Trigger header is read by HTMX, which emits the event in the DOM.
        # Not sure that I'm comfortable with this method, but it works, and it can be a documented feature of the API
        #  used to trigger events client-side.
        response.headers['HX-Trigger'] = "TaskCreated"
        return response
    else:
        return make_response(jsonify({"summary": summary}), 201)
