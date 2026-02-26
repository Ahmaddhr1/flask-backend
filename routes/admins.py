from flask import Blueprint, request, jsonify
from middleware.requires_auth import requires_auth
from models import Admin

admins = Blueprint("admins",__name__)

@admins.route("/admins", methods=["GET"])
@requires_auth()
def get_admins(user):
    try:
        admins = Admin.query.all()
        if not admins:
            return jsonify({"message":"No admins found","data":[]}),404
        return jsonify({"data":[a.to_dict() for a in admins]}), 200
    except Exception as e:
        return jsonify({"error":str(e)}),500
