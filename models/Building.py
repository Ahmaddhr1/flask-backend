from config.db import db

class Building(db.Model):
    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    complex_id = db.Column(db.Integer, db.ForeignKey("complex.id"), nullable=False)
    complex = db.relationship("Complex", back_populates="buildings")
    admins = db.relationship("Admin", back_populates="building", lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "complex_id": self.complex_id,
            "complex_name": self.complex.name if self.complex else None,
            "admins":
                [admin.to_dict() for admin in self.admins] if self.admins else [],
        }