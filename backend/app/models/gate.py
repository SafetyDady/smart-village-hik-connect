"""
Gate Model - MVP Version
Basic gate control and monitoring
"""

from app import db
from datetime import datetime

class Gate(db.Model):
    __tablename__ = 'gates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    gate_type = db.Column(db.String(20), default='barrier')  # barrier, sliding, swing
    
    # Control settings
    controller_ip = db.Column(db.String(45))
    controller_port = db.Column(db.Integer, default=80)
    control_method = db.Column(db.String(20), default='http')  # http, tcp, relay
    open_command = db.Column(db.String(255))
    close_command = db.Column(db.String(255))
    
    # Status
    status = db.Column(db.String(20), default='closed')  # open, closed, error, maintenance
    is_online = db.Column(db.Boolean, default=False)
    last_heartbeat = db.Column(db.DateTime)
    
    # Associated camera
    camera_id = db.Column(db.Integer, db.ForeignKey('cameras.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    access_logs = db.relationship('AccessLog', backref='gate', lazy=True)
    camera = db.relationship('Camera', backref='gates', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'gate_type': self.gate_type,
            'controller_ip': self.controller_ip,
            'controller_port': self.controller_port,
            'control_method': self.control_method,
            'status': self.status,
            'is_online': self.is_online,
            'last_heartbeat': self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            'camera_id': self.camera_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_control_url(self, action='open'):
        """Generate control URL for gate operation"""
        if not self.controller_ip:
            return None
        
        if action == 'open' and self.open_command:
            return f"http://{self.controller_ip}:{self.controller_port}/{self.open_command}"
        elif action == 'close' and self.close_command:
            return f"http://{self.controller_ip}:{self.controller_port}/{self.close_command}"
        
        # Default commands for common gate controllers
        commands = {
            'open': 'relay/open',
            'close': 'relay/close'
        }
        
        return f"http://{self.controller_ip}:{self.controller_port}/{commands.get(action, 'status')}"
    
    def __repr__(self):
        return f'<Gate {self.name} ({self.location})>'

