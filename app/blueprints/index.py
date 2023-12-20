from flask import Blueprint, render_template, make_response

from app.utils import is_htmx_request, render_page

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # HTMX includes headers that can be used to identify its requests.
    # If the request is coming from htmx, we serve only the content inside the <body>.
    # Otherwise, the request is a normal browser request, say from a refresh.
    if is_htmx_request():
        # HTMX takes the new <body> and replaces the current <body>, operating like an SPA.
        response = make_response(
            render_template("pages/index.html.j2")
        )
    else:
        # If the request comes from a refresh or non-htmx request,
        #  we inject the <body> into the includes.html.j2 template
        #  that includes the <html> and <head> tags.
        response = make_response(
            render_page("pages/index.html.j2")
        )

    # Unconfirmed, but I think this allows the browser to cache the
    #  htmx SPA version the same as the non-htmx version of the page.
    response.headers.add("Vary", "HX-Request")

    # See app/templates/pages/index.html.j2 for more info.
    return response
