from flask import Blueprint, render_template, make_response

from app.utils import is_htmx_request, render_page

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    if is_htmx_request():
        response = make_response(
            render_template("pages/index.html.j2")
        )
    else:
        response = make_response(
            render_page("pages/index.html.j2")
        )
    response.headers.add("Vary", "HX-Request")
    return response
