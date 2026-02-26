from flask import jsonify
import jwt
import os
from utils.get_token import get_token
from functools import wraps

def requires_auth():
    def decorator(f):
        @wraps(f)
        def wrapper(*args , **kwargs):
            print("ASSSSSSSSSSSSSSSSSSSSS")
            token = get_token()
            print("token",token)
            if not token:
                return jsonify({"error":"Not authorized !"}),401
            try:
                decoded= jwt.decode(
                    token,
                    os.getenv("JWT_SECRET"),
                    algorithms=["HS256"]
                )
                
            except Exception as e:
                return jsonify({"error": "Invalid token","data":str(e)}), 401
            return f(decoded,*args, **kwargs)
        return wrapper
    return decorator