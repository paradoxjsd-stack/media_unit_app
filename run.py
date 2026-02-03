"""
Run the Flask application
"""
import os
from app import create_app

# Get environment
env = os.environ.get('FLASK_ENV', 'development')

# Create Flask app
app = create_app(env)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
