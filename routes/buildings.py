from config.db import db
from flask import Blueprint, request, jsonify
from middleware.requires_auth import requires_auth
from models import Complex , Admin ,Building


buildings = Blueprint("buildings",__name__)

@buildings.route('/buildings',methods=['POST'])
@requires_auth()
def create_building(user):
    try:
        data = request.get_json(silent=True) or {}
        name = data.get("name")
        complex_id = data.get("complex_id")
        admin_id = data.get("admin_id")

        if not name or not complex_id:
            return jsonify({"error": "Name and complex_id are required"}), 400

        complex = Complex.query.get(complex_id)
        if not complex:
            return jsonify({"error": "Complex not found"}), 404

        building = Building(
            name=name,
            complex_id=complex_id
        )

        db.session.add(building)
        db.session.flush()
        
        if admin_id:
            admin = Admin.query.get(admin_id)
            
            if not admin:
                db.session.rollback()
                return jsonify({"error": "Admin not found"}), 404

            if admin.building_id:
                db.session.rollback()
                return jsonify({"error": "Admin already assigned to a building"}), 400
            
            if admin.complex_id:
                db.session.rollback()
                return jsonify({"error": "Admin already assigned to a Complex"}), 400

            admin.building_id = building.id

        db.session.commit()
        
        return jsonify({"message": "Building created!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating building","details": str(e)}), 500
    
@buildings.route("/buildings", methods=["GET"])
@requires_auth()
def get_buildings(user):
    try:
        buildings_list = Building.query.all()
        return jsonify({"data": [b.to_dict() for b in buildings_list]}), 200
    except Exception as e:
        return jsonify({"error": "Error fetching buildings","details": str(e)}), 500
    
@buildings.route("/buildings/<int:building_id>", methods=["DELETE"])
@requires_auth()
def delete_building(user, building_id):
    try:
        building = Building.query.get(building_id)
        
        if not building:
            return jsonify({"error": "Building not found"}), 404
        
        if building.admin:
            building.admin.building_id = None

        db.session.delete(building)
        db.session.commit()

        return jsonify({"message": "Building deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error deleting building","details": str(e)}), 500