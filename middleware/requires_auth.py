from flask import jsonify
from utils.get_token import get_token

def required_auth():
    def decorator(f):
        @wraps(f)
        def wrapper(*args , **kwargs)
            token = get_token()
            if not token:
                return jsonify({"Not authorized !"}),401
            
            try:
                decoded= jwt.decode(
                    token,
                    os.getenv("JWT_SECRET"),
                )
            except Exception:
                return jsonify({"error": "Invalid token"}), 401
            return f(decoded,*args, **kwargs)
        return wrapper
    return decorator