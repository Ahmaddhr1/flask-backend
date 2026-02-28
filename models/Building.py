from config.db import db

class Building(db.Model):
    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    complex_id = db.Column(db.Integer, db.ForeignKey("complex.id"), nullable=False)
    
    complex = db.relationship("Complex", back_populates="buildings")
    admin = db.relationship("Admin", back_populates="building", lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "complex_id": self.complex_id,
            "complex": self.complex.to_dict() if self.complex else None,
            "admin":self.admin.to_dict() if self.admin else None,
        }