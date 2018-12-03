from flask import abort, session


def is_authorized(session_user_id):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if session_user_id in session['user_id']:
                func(*args, **kwargs)
            else:
                abort(403)
        return wrapper
    return decorator
