from flask import request

def get_token():
    auth= request.headers.get("Authorization", "")
    print("AUTH HEADER RAW:", repr(auth))
    if auth.startswith("Bearer "):
        return auth.split(" ",1)[1]
    return None