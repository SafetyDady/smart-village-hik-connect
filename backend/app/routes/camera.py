"""
Camera API Routes - MVP Version
Handle camera-related API endpoints
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models.camera import Camera
from app.services.camera_service import camera_service

camera_bp = Blueprint('camera', __name__)

@camera_bp.route('/list', methods=['GET'])
def get_cameras():
    """Get list of all cameras"""
    try:
        cameras = Camera.query.all()
        return jsonify({
            'success': True,
            'cameras': [camera.to_dict() for camera in cameras],
            'total': len(cameras)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@camera_bp.route('/add', methods=['POST'])
def add_camera():
    """Add new camera"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'ip_address']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Check if camera with same IP already exists
        existing_camera = Camera.query.filter_by(ip_address=data['ip_address']).first()
        if existing_camera:
            return jsonify({
                'success': False,
                'error': 'Camera with this IP address already exists'
            }), 400
        
        # Create new camera
        camera = Camera(
            name=data['name'],
            ip_address=data['ip_address'],
            port=data.get('port', 80),
            username=data.get('username'),
            password=data.get('password'),
            location=data.get('location', ''),
            anpr_enabled=data.get('anpr_enabled', True),
            confidence_threshold=data.get('confidence_threshold', 0.8)
        )
        
        # Generate URLs
        if data.get('rtsp_url'):
            camera.rtsp_url = data['rtsp_url']
        if data.get('http_url'):
            camera.http_url = data['http_url']
        
        db.session.add(camera)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Camera added successfully',
            'camera': camera.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@camera_bp.route('/<int:camera_id>', methods=['GET'])
def get_camera(camera_id):
    """Get camera details"""
    try:
        camera = Camera.query.get(camera_id)
        if not camera:
            return jsonify({
                'success': False,
                'error': 'Camera not found'
            }), 404
        
        return jsonify({
            'success': True,
            'camera': camera.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@camera_bp.route('/<int:camera_id>/test', methods=['POST'])
def test_camera(camera_id):
    """Test camera connection"""
    try:
        result = camera_service.test_camera_connection(camera_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@camera_bp.route('/<int:camera_id>/snapshot', methods=['GET'])
def get_snapshot(camera_id):
    """Get camera snapshot"""
    try:
        result = camera_service.get_camera_snapshot(camera_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@camera_bp.route('/<int:camera_id>/stream', methods=['GET'])
def get_stream_info(camera_id):
    """Get camera stream information"""
    try:
        camera = Camera.query.get(camera_id)
        if not camera:
            return jsonify({
                'success': False,
                'error': 'Camera not found'
            }), 404
        
        return jsonify({
            'success': True,
            'stream_info': {
                'rtsp_url': camera.get_rtsp_url(),
                'snapshot_url': camera.get_snapshot_url(),
                'status': camera.status,
                'anpr_enabled': camera.anpr_enabled
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@camera_bp.route('/status', methods=['GET'])
def get_all_status():
    """Get status of all cameras"""
    try:
        result = camera_service.get_all_cameras_status()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@camera_bp.route('/<int:camera_id>/update', methods=['PUT'])
def update_camera(camera_id):
    """Update camera settings"""
    try:
        camera = Camera.query.get(camera_id)
        if not camera:
            return jsonify({
                'success': False,
                'error': 'Camera not found'
            }), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            camera.name = data['name']
        if 'location' in data:
            camera.location = data['location']
        if 'username' in data:
            camera.username = data['username']
        if 'password' in data:
            camera.password = data['password']
        if 'anpr_enabled' in data:
            camera.anpr_enabled = data['anpr_enabled']
        if 'confidence_threshold' in data:
            camera.confidence_threshold = data['confidence_threshold']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Camera updated successfully',
            'camera': camera.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

