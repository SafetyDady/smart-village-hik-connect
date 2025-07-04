"""
Camera Model - MVP Version
Basic camera configuration and monitoring
"""

from app import db
from datetime import datetime

class Camera(db.Model):
    __tablename__ = 'cameras'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)  # IPv4 or IPv6
    port = db.Column(db.Integer, default=80)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    rtsp_url = db.Column(db.String(255))
    http_url = db.Column(db.String(255))
    location = db.Column(db.String(100))  # Gate entrance, exit, etc.
    status = db.Column(db.String(20), default='offline')  # online, offline, error
    last_heartbeat = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Camera settings
    anpr_enabled = db.Column(db.Boolean, default=True)
    confidence_threshold = db.Column(db.Float, default=0.8)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ip_address': self.ip_address,
            'port': self.port,
            'username': self.username,
            'rtsp_url': self.rtsp_url,
            'http_url': self.http_url,
            'location': self.location,
            'status': self.status,
            'last_heartbeat': self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            'anpr_enabled': self.anpr_enabled,
            'confidence_threshold': self.confidence_threshold,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_rtsp_url(self):
        """Generate RTSP URL for camera stream"""
        if self.rtsp_url:
            return self.rtsp_url
        
        # Default Hikvision RTSP URL format
        auth = f"{self.username}:{self.password}@" if self.username and self.password else ""
        return f"rtsp://{auth}{self.ip_address}:554/Streaming/Channels/101"
    
    def get_snapshot_url(self):
        """Generate HTTP URL for camera snapshot"""
        if self.http_url:
            return self.http_url
        
        # Default Hikvision snapshot URL format
        return f"http://{self.ip_address}/ISAPI/Streaming/channels/1/picture"
    
    def __repr__(self):
        return f'<Camera {self.name} ({self.ip_address})>'

