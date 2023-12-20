from dataclasses import dataclass
from datetime import datetime
from mimetypes import guess_type as guess_mimetype
from os.path import splitext
from typing import Optional, Any, TypeVar, Type

from flask import render_template, url_for, request

__all__ = (
    "HTTPError", "NotFound", "BadRequest", "InternalError",
    "value_specified", "page_range",
    "render_page", "is_htmx_request", "is_htmx_redirect",
)

T = TypeVar("T")


class HTTPError(RuntimeError):
    code = 0


class NotFound(HTTPError):
    code = 404


class BadRequest(HTTPError):
    code = 400


class InternalError(HTTPError):
    code = 500


def value_specified(
        name: str, default: Optional[T] = None,
        desired_type: Optional[Type] = None
) -> tuple[Optional[T], bool]:
    try:
        value = request.args[name]
    except KeyError:
        value = default
        return value, False

    if desired_type is not None:
        try:
            return desired_type(value), True
        except ValueError:
            return default, False
    return value, True


def page_range(page_count: int, current: int, max_visible: int = 5):
    half_max = max_visible // 2
    if page_count < max_visible:
        return range(1, page_count + 1)
    if max_visible < 2:
        return range(current, current + 1)
    if current < half_max + 1:
        return range(1, max_visible + 1)
    if current > page_count - half_max:
        return range(page_count - max_visible + 1, page_count + 1)
    return range(current - half_max, current + half_max + (1 if half_max & 0b1 == 0 else 0))


def is_htmx_request() -> bool:
    return request.headers.get("HX-Request", None) is not None


def is_htmx_redirect() -> bool:
    return request.headers.get("HX-Boosted", None) is not None


def render_page(name: str, **context) -> str:
    return render_template(
        "includes.html.j2",
        body_template=name,
        **context
    )
