from functools import wraps
from flask import redirect, session


notes_TO_review_after_You_Are_Done = [
    "details page is retriving data using the buter_name not id(change is to id)",
    ""
]


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
