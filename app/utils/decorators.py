# decorators.py v1.0

from flask_login import current_user
from functools import wraps
from flask import redirect, url_for

def coder_required(f):
    """
    Decorator to restrict access to routes to authenticated coders only.
    - f: The function to decorate.
    Redirects to the login page if the user is not authenticated or not a coder.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_coder:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function