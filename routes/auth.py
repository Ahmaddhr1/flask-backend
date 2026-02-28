from models import Admin
from werkzeug.security import check_password_hash
import jwt
import os
from flask import Blueprint, request, jsonify

auth = Blueprint("auth", __name__)

@auth.route('/login',methods=["POST"])
def login():
    try:
        data = request.get_json(silent=True) or {}
       # print("Data::::::",data)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error":"All Credentials are required !"}),400
        
        admin = Admin.query.filter_by(email=email).first()
        if not admin:
            return jsonify({"error":"Admin not found"}),404
       #print("Admin-password::::::",admin.password)    
        
        if admin.status and admin.status.lower() != "active":
            return jsonify({"error": "You can't login with an inactive account!"}), 403

        if not check_password_hash(admin.password , password):
            return jsonify({"error": "Invalid Credentials"}), 401
        
        token = jwt.encode(
            {
                "id":admin.id,
                "role":admin.role
            },
            os.getenv("JWT_SECRET"),
        )

    
        return jsonify({
            "token": token,
            "admin": admin.to_dict()
        }), 200

    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"error": e,  }), 500
    