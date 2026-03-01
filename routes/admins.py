from config.db import db
from flask import Blueprint, request, jsonify
from middleware.requires_auth import requires_auth
from middleware.reqirued_role import require_role
from models import Admin
from werkzeug.security import generate_password_hash
from sqlalchemy import func

admins = Blueprint("admins",__name__)

@admins.route("/admins", methods=["GET"])
@requires_auth()
def get_admins(user):
    try:
        page= request.args.get("page",1,type=int)
        per_page=3
        
        query = Admin.query
        
        total=query.count()
        admins = (
            query
            .limit(per_page)
            .offset((page-1)*per_page)
            .all()
        )
        if not admins:
            return jsonify({"message":"No admins found","data":[]}),404
        return jsonify({"data":[a.to_dict() for a in admins]}), 200
    except Exception as e:
        return jsonify({"error":str(e)}),500

@admins.route("/admins", methods=["POST"])
@requires_auth()
@require_role("Super Admin")
def create_admins(user):
    try:
        data = request.get_json(silent=True) or {}
        if not data:
             return jsonify({"error":"DATA IS REQUIREDDD !"}),400
        email = data.get("email")
        is_admin_exists = Admin.query.filter_by(email=email).first()
        if is_admin_exists :
            return jsonify({"error":"Admin already exist with this email !"}),400
        admin = Admin(
            civility=data.get("civility"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            role=data.get("role"),
            status=data.get("status"),
            password=generate_password_hash(data.get("password")),
        )
        db.session.add(admin)
        db.session.commit()
        return jsonify({"message":"Admin Created"}),201
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@admins.route("/admins/available", methods=["GET"])
@requires_auth()
def get_available_admins(user):
    try:
        admins = (
        Admin.query
        .filter(Admin.complex_id.is_(None))
        .filter(Admin.building_id.is_(None))
        .filter(func.lower(Admin.status) == "active")
        .all()
        )

        data = [
        {
            "id": a.id,
            "first_name": a.first_name,
            "last_name": a.last_name,
            "email": a.email,
        }
        for a in admins
        ]
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error":str(e)}),500
    