from flask import jsonify
from functools import wraps


def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(user, *args, **kwargs):
            if user.get("role") != required_role:
                return jsonify({"error": "Forbidden You are not authorized!"}), 403
            return f(user, *args, **kwargs)
        return wrapper
    return decorator