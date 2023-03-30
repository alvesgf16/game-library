import functools
from typing import Optional

from flask import redirect, request, url_for

from flaskr.utils import is_user_logged_in
from flaskr.utils.types import IntConverter, Renderable, Route


def login_required(view: Route) -> Route:
    @functools.wraps(view)
    def wrapped_view(**kwargs: Optional[IntConverter]) -> Renderable:
        return (
            view(**kwargs)
            if is_user_logged_in()
            else redirect(url_for("auth.login", origin=request.path))
        )

    return wrapped_view
