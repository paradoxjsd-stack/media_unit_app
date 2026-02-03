"""
Flask application factory - WSGI entrypoint for Vercel deployment
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app

# Get environment
env = os.environ.get('FLASK_ENV', 'production')

# Create Flask app
app = create_app(env)

# WSGI application object for Vercel
if __name__ == '__main__':
    # Development
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Production (Vercel)
    pass
