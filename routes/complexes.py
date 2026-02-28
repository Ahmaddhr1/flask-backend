from config.db import db
from flask import Blueprint, request, jsonify
from middleware.requires_auth import requires_auth
from models import Complex , Admin

complexes = Blueprint("complexes",__name__)

@complexes.route("/complexes", methods=["POST"])
@requires_auth()
def create_complex(user):
    try:
        data= request.get_json(silent=True) or {}
        name=data.get("name")
        address=data.get("address")
        campaign_info=data.get("campaign_info")
        admin_id = data.get("admin_id")
        
        if not name or not address or not campaign_info:
            return jsonify({"error":"Name , address, campaign info are required !"})
        
        complex = Complex(
            name=name,
            address=address,
            campaign_info=campaign_info
        )
        
        db.session.add(complex)
        db.session.flush()
        
        if admin_id:
            admin = Admin.query.get(admin_id)
            
            if not admin:
                db.session.rollback()
                return jsonify({"error": "Admin not found"}), 404

            if admin.complex_id:
                db.session.rollback()
                return jsonify({"error": "Admin already assigned to a complex"}), 400

            admin.complex_id = complex.id

        db.session.commit()

        return jsonify({
            "message": "Complex created !",
            "complex": {
                "id": complex.id,
                "name": complex.name,
                "address": complex.address,
                "campaign_info": complex.campaign_info,
                "admin_id":complex.admin_id
            }
        }), 201  
    except Exception as e:
        return jsonify({"error":"Error creating complex","details":str(e)}),500


    