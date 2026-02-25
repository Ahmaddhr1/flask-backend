from config.db import db

class Complex(db.Model):
    __tablename__="complex"
    id=db.Column(db.Integer , primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(20),nullable=False)
    campaign_info=db.Column(db.String(200),nullable=False)
    
    admins=db.relationship("Admin", back_populates="complex")
    buildings=db.relationship("Building", back_populates="complex")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address":self.address,
            "campaign_info":self.campaign_info,
            "admins":
                [admin.to_dict() for admin in self.admins] if self.admins else [],
            "buildings":
                [building.to_dict() for building in self.buildings] if self.buildings else [],
        }