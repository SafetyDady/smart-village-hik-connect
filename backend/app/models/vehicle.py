"""
Vehicle Model - MVP Version
Basic vehicle registration for testing
"""

from app import db
from datetime import datetime

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    vehicle_type = db.Column(db.String(50), default='car')  # car, motorcycle, truck
    color = db.Column(db.String(30))
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')  # active, inactive, pending
    is_permanent = db.Column(db.Boolean, default=True)  # True for permanent, False for temporary
    expires_at = db.Column(db.DateTime)  # For temporary vehicles
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    access_logs = db.relationship('AccessLog', backref='vehicle', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'license_plate': self.license_plate,
            'owner_name': self.owner_name,
            'vehicle_type': self.vehicle_type,
            'color': self.color,
            'brand': self.brand,
            'model': self.model,
            'status': self.status,
            'is_permanent': self.is_permanent,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Vehicle {self.license_plate}>'

