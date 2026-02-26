from flask import request

def get_token():
    auth= request.headers.get("Authorization", "")
    if auth.startsWith("Bearer "):
        return auth.split(" ",1)[1]
    return None