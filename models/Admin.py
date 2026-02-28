from config.db import db

class Admin(db.Model):
    __tablename__ = "admins"
    id=db.Column(db.Integer , primary_key=True)
    first_name =db.Column(db.String(20),nullable=False)
    last_name =db.Column(db.String(20),nullable=False)
    email =db.Column(db.String(20),unique=True ,nullable=False)
    phone =db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    civility =db.Column(db.String(20),nullable=False)
    role=db.Column(db.String(20),nullable=False)
    status=db.Column(db.String(20),nullable=False)
    complex_id = db.Column(db.Integer, db.ForeignKey("complex.id"))
    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"))

    complex = db.relationship("Complex", back_populates="admin")
    building = db.relationship("Building", back_populates="admin")
    
    def to_dict(self):
        return {
           "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "civility": self.civility,
            "role": self.role,
            "status": self.status,
            "complex_id": self.complex_id,
            "building_id": self.building_id,
            "complex":self.complex.to_dict if self.complex else None,
            "building":self.building.to_dict if self.building else None
        }
    
