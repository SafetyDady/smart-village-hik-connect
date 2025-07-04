"""
Camera Service - MVP Version
Handle camera connections and streaming
"""

import cv2
import requests
import base64
from datetime import datetime
from app import db
from app.models.camera import Camera
import threading
import time

class CameraService:
    def __init__(self):
        self.active_streams = {}
        self.stream_threads = {}
    
    def test_camera_connection(self, camera_id):
        """Test camera connection and update status"""
        try:
            camera = Camera.query.get(camera_id)
            if not camera:
                return {'success': False, 'error': 'Camera not found'}
            
            # Test HTTP snapshot first
            snapshot_url = camera.get_snapshot_url()
            
            try:
                # Add authentication if available
                auth = None
                if camera.username and camera.password:
                    auth = (camera.username, camera.password)
                
                response = requests.get(snapshot_url, auth=auth, timeout=10)
                
                if response.status_code == 200:
                    # Update camera status
                    camera.status = 'online'
                    camera.last_heartbeat = datetime.utcnow()
                    db.session.commit()
                    
                    return {
                        'success': True,
                        'status': 'online',
                        'message': 'Camera connection successful',
                        'snapshot_size': len(response.content)
                    }
                else:
                    camera.status = 'error'
                    db.session.commit()
                    return {
                        'success': False,
                        'error': f'HTTP {response.status_code}: {response.reason}'
                    }
                    
            except requests.exceptions.RequestException as e:
                camera.status = 'offline'
                db.session.commit()
                return {
                    'success': False,
                    'error': f'Connection failed: {str(e)}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Service error: {str(e)}'
            }
    
    def get_camera_snapshot(self, camera_id):
        """Get a single snapshot from camera"""
        try:
            camera = Camera.query.get(camera_id)
            if not camera:
                return {'success': False, 'error': 'Camera not found'}
            
            snapshot_url = camera.get_snapshot_url()
            
            # Add authentication if available
            auth = None
            if camera.username and camera.password:
                auth = (camera.username, camera.password)
            
            response = requests.get(snapshot_url, auth=auth, timeout=10)
            
            if response.status_code == 200:
                # Convert image to base64 for web display
                image_base64 = base64.b64encode(response.content).decode('utf-8')
                
                return {
                    'success': True,
                    'image': f"data:image/jpeg;base64,{image_base64}",
                    'timestamp': datetime.utcnow().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to get snapshot: HTTP {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Snapshot error: {str(e)}'
            }
    
    def start_rtsp_stream(self, camera_id):
        """Start RTSP stream for camera (for future use)"""
        try:
            camera = Camera.query.get(camera_id)
            if not camera:
                return {'success': False, 'error': 'Camera not found'}
            
            rtsp_url = camera.get_rtsp_url()
            
            # Test RTSP connection
            cap = cv2.VideoCapture(rtsp_url)
            
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                
                if ret:
                    camera.status = 'online'
                    camera.last_heartbeat = datetime.utcnow()
                    db.session.commit()
                    
                    return {
                        'success': True,
                        'message': 'RTSP stream accessible',
                        'rtsp_url': rtsp_url
                    }
                else:
                    return {
                        'success': False,
                        'error': 'RTSP stream not readable'
                    }
            else:
                return {
                    'success': False,
                    'error': 'Cannot open RTSP stream'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'RTSP error: {str(e)}'
            }
    
    def get_all_cameras_status(self):
        """Get status of all cameras"""
        try:
            cameras = Camera.query.all()
            camera_status = []
            
            for camera in cameras:
                status = {
                    'id': camera.id,
                    'name': camera.name,
                    'ip_address': camera.ip_address,
                    'status': camera.status,
                    'last_heartbeat': camera.last_heartbeat.isoformat() if camera.last_heartbeat else None,
                    'location': camera.location
                }
                camera_status.append(status)
            
            return {
                'success': True,
                'cameras': camera_status,
                'total': len(camera_status)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Status check error: {str(e)}'
            }

# Global camera service instance
camera_service = CameraService()

