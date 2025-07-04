"""
Access Log Model - MVP Version
Track vehicle access events
"""

from app import db
from datetime import datetime

class AccessLog(db.Model):
    __tablename__ = 'access_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('cameras.id'), nullable=True)
    gate_id = db.Column(db.Integer, db.ForeignKey('gates.id'), nullable=True)
    
    # Event details
    license_plate = db.Column(db.String(20), nullable=False)
    event_type = db.Column(db.String(20), nullable=False)  # entry, exit, denied
    access_method = db.Column(db.String(20), default='anpr')  # anpr, manual, emergency
    
    # ANPR details
    confidence_score = db.Column(db.Float)
    image_path = db.Column(db.String(255))
    
    # Manual override details
    manual_reason = db.Column(db.String(255))
    operator_name = db.Column(db.String(100))
    
    # Timestamps
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'camera_id': self.camera_id,
            'gate_id': self.gate_id,
            'license_plate': self.license_plate,
            'event_type': self.event_type,
            'access_method': self.access_method,
            'confidence_score': self.confidence_score,
            'image_path': self.image_path,
            'manual_reason': self.manual_reason,
            'operator_name': self.operator_name,
            'timestamp': self.timestamp.isoformat(),
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<AccessLog {self.license_plate} - {self.event_type}>'

