from flask import Blueprint, render_template, request, make_response, jsonify, abort
from jinja2_fragments.flask import render_block
from sqlalchemy import select

from app.extensions import db
from app.models import Task
from app.utils import is_htmx_request

bp = Blueprint('task', __name__, url_prefix="/task")


@bp.route('/', methods=["GET"])
def get():
    task_list = tuple(db.session.scalars(select(Task).order_by(Task.summary.asc())))

    # HTMX wants endpoints to return html, so this is a html-api similar to xml apis.
    # We can also use the htmx headers to decide to return data in the traditional json (or xml) format.
    #  Certainly more work and not necessary.
    if is_htmx_request():
        # This template only includes a <div> that can be slotted into a larger template with a htmx request.
        return render_template("components/task-list.html.j2", task_list=task_list)
    else:
        return make_response(jsonify({tid: task.id for tid, task in task_list}))


@bp.route('/', methods=["POST", "PUT"])
def create():
    summary = request.form['summary']
    if not summary:
        return abort(400, message="Missing summary parameter.")
    task = Task(summary=summary)  # TODO: Allow passing other parameters
    db.session.add(task)
    db.session.commit()

    if is_htmx_request():
        # POST requests can also return html that htmx can slot into the page, but the hx-swap="none"
        #  in the index template prevents that swapping from occuring, so this html is never seen.
        #  I only include it now for adherence to POST standards that want a copy of the created resource returned,
        #  but this can change in the future.
        response = make_response(f"<p>{summary}</p>", 201)

        # HTMX includes HX-Trigger in the request headers indicating the ID of the element that triggered the request.
        # The HX-Trigger response header is read by HTMX, which emits an event under that name in the DOM.
        # If we return the content of the HX-Trigger request header in the HX-Trigger response header,
        #  we can use the ID of the element that triggered the request as an event name to listen for in the DOM.
        # Watching multiple elements for requests can be achieved with:
        #  hx-trigger="task-create from:body,task-delete from:body"
        response.headers['HX-Trigger'] = request.headers.get('HX-Trigger')
        return response
    return make_response(jsonify(task.as_dict()), 201)


@bp.route('/detail/<int:task_id>', methods=["GET"])
def detail(task_id: int):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(400, message="Invalid task ID parameter.")
    task = db.session.scalar(select(Task).filter(Task.id == task_id))

    if not task:
        return abort(400, message=f"No task found for id {task_id}.")
    if is_htmx_request():
        element = request.headers.get("HX-Trigger", "")
        if element == "description":
            return render_template("components/task-description-edit.html.j2", task=task)
        if element == "description-edit":
            return render_template("components/task-description.html.j2", task=task)
        return render_template("components/task-details.html.j2", task=task)
    return make_response(jsonify(task.as_dict()), 200)


@bp.route('/detail/<int:task_id>', methods=["PATCH"])
def patch(task_id: int):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(400, message="Invalid task ID parameter.")

    task = db.session.scalar(select(Task).filter(Task.id == task_id))
    if not task:
        return abort(400, message=f"No task found for id {task_id}.")

    description = request.form.get("description", "")
    if description:
        task.description = description
        db.session.commit()

    if is_htmx_request():
        return render_template("components/task-description.html.j2", task=task)
    return make_response(jsonify({"description": task.description}), 200)
