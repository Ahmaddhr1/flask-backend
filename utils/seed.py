from app import app
from models import Admin
from config.db import db
from werkzeug.security import generate_password_hash

with app.app_context():
    admin_exists = Admin.query.filter_by(email="super@admin.com").first()
    if not admin_exists:
        super_admin = Admin(
            civility="Mr",
            first_name="Ahmad",
            last_name="Admin",
            email="ahmad@admin.com",
            phone="000000",
            role="Super Admin",
            status="active",
            password=generate_password_hash("123456")
        )
        db.session.add(super_admin)
        db.session.commit()
        print("Super Admin Created !")
    else :
        print("Error while creating Super Admin !")