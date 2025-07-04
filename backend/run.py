#!/usr/bin/env python3
"""
Smart Village HIK Connect - Backend Server
Main application entry point
"""

from app import create_app
import os

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Development server configuration
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('PORT', os.getenv('FLASK_PORT', 5000)))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    
    print(f"🚀 Starting Smart Village HIK Connect Backend Server")
    print(f"📡 Server: http://{host}:{port}")
    print(f"🔧 Debug Mode: {debug_mode}")
    print(f"📋 Environment: {'Development' if debug_mode else 'Production'}")
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode,
        threaded=True
    )

