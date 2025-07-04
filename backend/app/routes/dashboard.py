"""
Dashboard API Routes - MVP Version
Handle dashboard and monitoring API endpoints
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from app.models.vehicle import Vehicle
from app.models.camera import Camera
from app.models.gate import Gate
from app.models.access_log import AccessLog

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/overview', methods=['GET'])
def get_overview():
    """Get dashboard overview statistics"""
    try:
        # Vehicle statistics
        total_vehicles = Vehicle.query.count()
        permanent_vehicles = Vehicle.query.filter_by(is_permanent=True).count()
        temporary_vehicles = Vehicle.query.filter_by(is_permanent=False).count()
        active_vehicles = Vehicle.query.filter_by(status='active').count()
        
        # Camera statistics
        total_cameras = Camera.query.count()
        online_cameras = Camera.query.filter_by(status='online').count()
        offline_cameras = Camera.query.filter_by(status='offline').count()
        
        # Gate statistics
        total_gates = Gate.query.count()
        online_gates = Gate.query.filter_by(is_online=True).count()
        open_gates = Gate.query.filter_by(status='open').count()
        
        # Access log statistics (last 24 hours)
        yesterday = datetime.utcnow() - timedelta(hours=24)
        recent_entries = AccessLog.query.filter(
            AccessLog.timestamp >= yesterday,
            AccessLog.event_type == 'entry'
        ).count()
        
        recent_exits = AccessLog.query.filter(
            AccessLog.timestamp >= yesterday,
            AccessLog.event_type == 'exit'
        ).count()
        
        manual_overrides = AccessLog.query.filter(
            AccessLog.timestamp >= yesterday,
            AccessLog.access_method == 'manual'
        ).count()
        
        return jsonify({
            'success': True,
            'overview': {
                'vehicles': {
                    'total': total_vehicles,
                    'permanent': permanent_vehicles,
                    'temporary': temporary_vehicles,
                    'active': active_vehicles
                },
                'cameras': {
                    'total': total_cameras,
                    'online': online_cameras,
                    'offline': offline_cameras
                },
                'gates': {
                    'total': total_gates,
                    'online': online_gates,
                    'open': open_gates
                },
                'access_logs_24h': {
                    'entries': recent_entries,
                    'exits': recent_exits,
                    'manual_overrides': manual_overrides
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/recent-activity', methods=['GET'])
def get_recent_activity():
    """Get recent access activity"""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        recent_logs = AccessLog.query.order_by(
            AccessLog.timestamp.desc()
        ).limit(limit).all()
        
        return jsonify({
            'success': True,
            'recent_activity': [log.to_dict() for log in recent_logs],
            'total': len(recent_logs)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/system-status', methods=['GET'])
def get_system_status():
    """Get overall system health status"""
    try:
        # Check camera status
        cameras = Camera.query.all()
        camera_health = {
            'total': len(cameras),
            'online': sum(1 for c in cameras if c.status == 'online'),
            'offline': sum(1 for c in cameras if c.status == 'offline'),
            'error': sum(1 for c in cameras if c.status == 'error')
        }
        
        # Check gate status
        gates = Gate.query.all()
        gate_health = {
            'total': len(gates),
            'online': sum(1 for g in gates if g.is_online),
            'offline': sum(1 for g in gates if not g.is_online)
        }
        
        # Determine overall system health
        camera_health_percentage = (camera_health['online'] / camera_health['total'] * 100) if camera_health['total'] > 0 else 100
        gate_health_percentage = (gate_health['online'] / gate_health['total'] * 100) if gate_health['total'] > 0 else 100
        
        overall_health = (camera_health_percentage + gate_health_percentage) / 2
        
        if overall_health >= 90:
            system_status = 'healthy'
        elif overall_health >= 70:
            system_status = 'warning'
        else:
            system_status = 'critical'
        
        return jsonify({
            'success': True,
            'system_status': {
                'overall': system_status,
                'health_percentage': round(overall_health, 1),
                'cameras': camera_health,
                'gates': gate_health,
                'last_updated': datetime.utcnow().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/access-stats', methods=['GET'])
def get_access_stats():
    """Get access statistics for charts"""
    try:
        days = request.args.get('days', 7, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Daily access counts
        daily_stats = db.session.query(
            func.date(AccessLog.timestamp).label('date'),
            func.count(AccessLog.id).label('count'),
            AccessLog.event_type
        ).filter(
            AccessLog.timestamp >= start_date
        ).group_by(
            func.date(AccessLog.timestamp),
            AccessLog.event_type
        ).all()
        
        # Process data for chart
        chart_data = {}
        for stat in daily_stats:
            date_str = stat.date.strftime('%Y-%m-%d')
            if date_str not in chart_data:
                chart_data[date_str] = {'entries': 0, 'exits': 0}
            
            if stat.event_type == 'entry':
                chart_data[date_str]['entries'] = stat.count
            elif stat.event_type == 'exit':
                chart_data[date_str]['exits'] = stat.count
        
        # Convert to list format for frontend
        chart_list = []
        for date_str, counts in sorted(chart_data.items()):
            chart_list.append({
                'date': date_str,
                'entries': counts['entries'],
                'exits': counts['exits']
            })
        
        return jsonify({
            'success': True,
            'access_stats': chart_list,
            'period_days': days
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """Get system alerts and warnings"""
    try:
        alerts = []
        
        # Check for offline cameras
        offline_cameras = Camera.query.filter_by(status='offline').all()
        for camera in offline_cameras:
            alerts.append({
                'type': 'warning',
                'category': 'camera',
                'message': f'Camera "{camera.name}" is offline',
                'timestamp': camera.last_heartbeat.isoformat() if camera.last_heartbeat else None
            })
        
        # Check for offline gates
        offline_gates = Gate.query.filter_by(is_online=False).all()
        for gate in offline_gates:
            alerts.append({
                'type': 'warning',
                'category': 'gate',
                'message': f'Gate "{gate.name}" is offline',
                'timestamp': gate.last_heartbeat.isoformat() if gate.last_heartbeat else None
            })
        
        # Check for expired temporary vehicles
        expired_vehicles = Vehicle.query.filter(
            Vehicle.is_permanent == False,
            Vehicle.expires_at < datetime.utcnow(),
            Vehicle.status == 'active'
        ).all()
        
        for vehicle in expired_vehicles:
            alerts.append({
                'type': 'info',
                'category': 'vehicle',
                'message': f'Temporary vehicle "{vehicle.license_plate}" has expired',
                'timestamp': vehicle.expires_at.isoformat()
            })
        
        # Check for excessive manual overrides (last hour)
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        manual_count = AccessLog.query.filter(
            AccessLog.timestamp >= one_hour_ago,
            AccessLog.access_method == 'manual'
        ).count()
        
        if manual_count > 10:
            alerts.append({
                'type': 'warning',
                'category': 'security',
                'message': f'High number of manual overrides in last hour: {manual_count}',
                'timestamp': datetime.utcnow().isoformat()
            })
        
        return jsonify({
            'success': True,
            'alerts': alerts,
            'total': len(alerts)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

