"""
Vehicle API Routes - MVP Version
Handle vehicle registration API endpoints
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app import db
from app.models.vehicle import Vehicle

vehicle_bp = Blueprint('vehicle', __name__)

@vehicle_bp.route('/list', methods=['GET'])
def get_vehicles():
    """Get list of all vehicles"""
    try:
        vehicles = Vehicle.query.all()
        return jsonify({
            'success': True,
            'vehicles': [vehicle.to_dict() for vehicle in vehicles],
            'total': len(vehicles)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@vehicle_bp.route('/add', methods=['POST'])
def add_vehicle():
    """Add new vehicle"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['license_plate', 'owner_name']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Check if vehicle with same license plate already exists
        existing_vehicle = Vehicle.query.filter_by(license_plate=data['license_plate']).first()
        if existing_vehicle:
            return jsonify({
                'success': False,
                'error': 'Vehicle with this license plate already exists'
            }), 400
        
        # Handle temporary vehicle expiration
        expires_at = None
        is_permanent = data.get('is_permanent', True)
        
        if not is_permanent:
            # For temporary vehicles, set expiration to 24 hours from now
            expires_at = datetime.utcnow() + timedelta(hours=24)
        
        # Create new vehicle
        vehicle = Vehicle(
            license_plate=data['license_plate'].upper(),
            owner_name=data['owner_name'],
            vehicle_type=data.get('vehicle_type', 'car'),
            color=data.get('color'),
            brand=data.get('brand'),
            model=data.get('model'),
            is_permanent=is_permanent,
            expires_at=expires_at,
            status='active'
        )
        
        db.session.add(vehicle)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Vehicle added successfully',
            'vehicle': vehicle.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@vehicle_bp.route('/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    """Get vehicle details"""
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({
                'success': False,
                'error': 'Vehicle not found'
            }), 404
        
        return jsonify({
            'success': True,
            'vehicle': vehicle.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@vehicle_bp.route('/search', methods=['GET'])
def search_vehicle():
    """Search vehicle by license plate"""
    try:
        license_plate = request.args.get('license_plate')
        if not license_plate:
            return jsonify({
                'success': False,
                'error': 'License plate parameter required'
            }), 400
        
        vehicle = Vehicle.query.filter_by(license_plate=license_plate.upper()).first()
        
        if vehicle:
            # Check if temporary vehicle has expired
            if not vehicle.is_permanent and vehicle.expires_at:
                if datetime.utcnow() > vehicle.expires_at:
                    vehicle.status = 'expired'
                    db.session.commit()
            
            return jsonify({
                'success': True,
                'vehicle': vehicle.to_dict(),
                'access_allowed': vehicle.status == 'active' and (
                    vehicle.is_permanent or 
                    (vehicle.expires_at and datetime.utcnow() <= vehicle.expires_at)
                )
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Vehicle not found',
                'access_allowed': False
            }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@vehicle_bp.route('/<int:vehicle_id>/update', methods=['PUT'])
def update_vehicle(vehicle_id):
    """Update vehicle information"""
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({
                'success': False,
                'error': 'Vehicle not found'
            }), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'owner_name' in data:
            vehicle.owner_name = data['owner_name']
        if 'vehicle_type' in data:
            vehicle.vehicle_type = data['vehicle_type']
        if 'color' in data:
            vehicle.color = data['color']
        if 'brand' in data:
            vehicle.brand = data['brand']
        if 'model' in data:
            vehicle.model = data['model']
        if 'status' in data:
            vehicle.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Vehicle updated successfully',
            'vehicle': vehicle.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@vehicle_bp.route('/<int:vehicle_id>/delete', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    """Delete vehicle"""
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({
                'success': False,
                'error': 'Vehicle not found'
            }), 404
        
        db.session.delete(vehicle)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Vehicle deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@vehicle_bp.route('/temporary', methods=['GET'])
def get_temporary_vehicles():
    """Get list of temporary vehicles"""
    try:
        temp_vehicles = Vehicle.query.filter_by(is_permanent=False).all()
        
        # Update expired vehicles
        current_time = datetime.utcnow()
        for vehicle in temp_vehicles:
            if vehicle.expires_at and current_time > vehicle.expires_at:
                vehicle.status = 'expired'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'vehicles': [vehicle.to_dict() for vehicle in temp_vehicles],
            'total': len(temp_vehicles)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@vehicle_bp.route('/permanent', methods=['GET'])
def get_permanent_vehicles():
    """Get list of permanent vehicles"""
    try:
        perm_vehicles = Vehicle.query.filter_by(is_permanent=True).all()
        
        return jsonify({
            'success': True,
            'vehicles': [vehicle.to_dict() for vehicle in perm_vehicles],
            'total': len(perm_vehicles)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

