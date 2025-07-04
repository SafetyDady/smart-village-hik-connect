"""
Gate Service - MVP Version
Handle gate control operations
"""

import requests
from datetime import datetime
from app import db
from app.models.gate import Gate
from app.models.access_log import AccessLog

class GateService:
    def __init__(self):
        self.default_timeout = 10
    
    def open_gate(self, gate_id, operator_name=None, reason=None):
        """Open gate manually"""
        try:
            gate = Gate.query.get(gate_id)
            if not gate:
                return {'success': False, 'error': 'Gate not found'}
            
            # Get control URL
            control_url = gate.get_control_url('open')
            
            if not control_url:
                # Simulate gate opening for MVP (no actual hardware)
                gate.status = 'open'
                gate.last_heartbeat = datetime.utcnow()
                db.session.commit()
                
                # Log manual override
                self._log_manual_access(gate_id, 'manual_open', operator_name, reason)
                
                return {
                    'success': True,
                    'message': 'Gate opened successfully (simulated)',
                    'gate_status': 'open'
                }
            
            # Send HTTP command to gate controller
            try:
                response = requests.get(control_url, timeout=self.default_timeout)
                
                if response.status_code == 200:
                    gate.status = 'open'
                    gate.is_online = True
                    gate.last_heartbeat = datetime.utcnow()
                    db.session.commit()
                    
                    # Log manual override
                    self._log_manual_access(gate_id, 'manual_open', operator_name, reason)
                    
                    return {
                        'success': True,
                        'message': 'Gate opened successfully',
                        'gate_status': 'open'
                    }
                else:
                    return {
                        'success': False,
                        'error': f'Gate controller error: HTTP {response.status_code}'
                    }
                    
            except requests.exceptions.RequestException as e:
                gate.is_online = False
                db.session.commit()
                return {
                    'success': False,
                    'error': f'Gate controller connection failed: {str(e)}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Gate service error: {str(e)}'
            }
    
    def close_gate(self, gate_id, operator_name=None):
        """Close gate manually"""
        try:
            gate = Gate.query.get(gate_id)
            if not gate:
                return {'success': False, 'error': 'Gate not found'}
            
            # Get control URL
            control_url = gate.get_control_url('close')
            
            if not control_url:
                # Simulate gate closing for MVP (no actual hardware)
                gate.status = 'closed'
                gate.last_heartbeat = datetime.utcnow()
                db.session.commit()
                
                return {
                    'success': True,
                    'message': 'Gate closed successfully (simulated)',
                    'gate_status': 'closed'
                }
            
            # Send HTTP command to gate controller
            try:
                response = requests.get(control_url, timeout=self.default_timeout)
                
                if response.status_code == 200:
                    gate.status = 'closed'
                    gate.is_online = True
                    gate.last_heartbeat = datetime.utcnow()
                    db.session.commit()
                    
                    return {
                        'success': True,
                        'message': 'Gate closed successfully',
                        'gate_status': 'closed'
                    }
                else:
                    return {
                        'success': False,
                        'error': f'Gate controller error: HTTP {response.status_code}'
                    }
                    
            except requests.exceptions.RequestException as e:
                gate.is_online = False
                db.session.commit()
                return {
                    'success': False,
                    'error': f'Gate controller connection failed: {str(e)}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Gate service error: {str(e)}'
            }
    
    def get_gate_status(self, gate_id):
        """Get current gate status"""
        try:
            gate = Gate.query.get(gate_id)
            if not gate:
                return {'success': False, 'error': 'Gate not found'}
            
            return {
                'success': True,
                'gate': gate.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Status check error: {str(e)}'
            }
    
    def get_all_gates_status(self):
        """Get status of all gates"""
        try:
            gates = Gate.query.all()
            gates_status = []
            
            for gate in gates:
                gates_status.append(gate.to_dict())
            
            return {
                'success': True,
                'gates': gates_status,
                'total': len(gates_status)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Status check error: {str(e)}'
            }
    
    def _log_manual_access(self, gate_id, event_type, operator_name, reason):
        """Log manual gate operation"""
        try:
            access_log = AccessLog(
                gate_id=gate_id,
                license_plate='MANUAL',
                event_type=event_type,
                access_method='manual',
                manual_reason=reason or 'Manual override',
                operator_name=operator_name or 'Unknown',
                timestamp=datetime.utcnow()
            )
            
            db.session.add(access_log)
            db.session.commit()
            
        except Exception as e:
            print(f"Failed to log manual access: {e}")

# Global gate service instance
gate_service = GateService()

