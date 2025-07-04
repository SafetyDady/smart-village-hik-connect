"""
Gate API Routes - MVP Version
Handle gate control API endpoints
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models.gate import Gate
from app.services.gate_service import gate_service

gate_bp = Blueprint('gate', __name__)

@gate_bp.route('/list', methods=['GET'])
def get_gates():
    """Get list of all gates"""
    try:
        gates = Gate.query.all()
        return jsonify({
            'success': True,
            'gates': [gate.to_dict() for gate in gates],
            'total': len(gates)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gate_bp.route('/add', methods=['POST'])
def add_gate():
    """Add new gate"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create new gate
        gate = Gate(
            name=data['name'],
            location=data['location'],
            gate_type=data.get('gate_type', 'barrier'),
            controller_ip=data.get('controller_ip'),
            controller_port=data.get('controller_port', 80),
            control_method=data.get('control_method', 'http'),
            open_command=data.get('open_command'),
            close_command=data.get('close_command'),
            camera_id=data.get('camera_id')
        )
        
        db.session.add(gate)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Gate added successfully',
            'gate': gate.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gate_bp.route('/<int:gate_id>', methods=['GET'])
def get_gate(gate_id):
    """Get gate details"""
    try:
        gate = Gate.query.get(gate_id)
        if not gate:
            return jsonify({
                'success': False,
                'error': 'Gate not found'
            }), 404
        
        return jsonify({
            'success': True,
            'gate': gate.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gate_bp.route('/<int:gate_id>/open', methods=['POST'])
def open_gate(gate_id):
    """Open gate manually"""
    try:
        data = request.get_json() or {}
        operator_name = data.get('operator_name', 'Unknown')
        reason = data.get('reason', 'Manual override')
        
        result = gate_service.open_gate(gate_id, operator_name, reason)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gate_bp.route('/<int:gate_id>/close', methods=['POST'])
def close_gate(gate_id):
    """Close gate manually"""
    try:
        data = request.get_json() or {}
        operator_name = data.get('operator_name', 'Unknown')
        
        result = gate_service.close_gate(gate_id, operator_name)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gate_bp.route('/<int:gate_id>/status', methods=['GET'])
def get_gate_status(gate_id):
    """Get gate status"""
    try:
        result = gate_service.get_gate_status(gate_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gate_bp.route('/status', methods=['GET'])
def get_all_gates_status():
    """Get status of all gates"""
    try:
        result = gate_service.get_all_gates_status()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gate_bp.route('/<int:gate_id>/update', methods=['PUT'])
def update_gate(gate_id):
    """Update gate settings"""
    try:
        gate = Gate.query.get(gate_id)
        if not gate:
            return jsonify({
                'success': False,
                'error': 'Gate not found'
            }), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            gate.name = data['name']
        if 'location' in data:
            gate.location = data['location']
        if 'gate_type' in data:
            gate.gate_type = data['gate_type']
        if 'controller_ip' in data:
            gate.controller_ip = data['controller_ip']
        if 'controller_port' in data:
            gate.controller_port = data['controller_port']
        if 'control_method' in data:
            gate.control_method = data['control_method']
        if 'open_command' in data:
            gate.open_command = data['open_command']
        if 'close_command' in data:
            gate.close_command = data['close_command']
        if 'camera_id' in data:
            gate.camera_id = data['camera_id']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Gate updated successfully',
            'gate': gate.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

