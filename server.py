from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
from db_helper import insert_signup, search_login_credentials
from main import proctoringAlgo, main_app
import os
import sys
import logging
from typing import Dict, Any, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variable for camera control
running = True

# Database configuration from environment variables
DB_CONFIG = {
    "host": os.getenv('MYSQL_HOST', 'localhost'),
    "user": os.getenv('MYSQL_USER', 'root'),
    "password": os.getenv('MYSQL_PASSWORD', 'root'),
    "database": os.getenv('MYSQL_DATABASE', 'quizo'),
    "pool_name": "quizo_pool",
    "pool_size": 5
}

"""
Code for the database backend server. 
"""
@app.route('/signup_data', methods=['POST'])
def signup_data() -> Tuple[Dict[str, Any], int]:
    """Handle user signup"""
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['signupEmail', 'username', 'signupPassword']):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400

        status, message = insert_signup(
            data['signupEmail'],
            data['username'],
            data['signupPassword']
        )

        if status == 1:
            return jsonify({
                'success': True,
                'message': message
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400

    except Exception as e:
        logger.error(f"Error in signup_data: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/login_data', methods=['POST'])
def login_data() -> Tuple[Dict[str, Any], int]:
    """Handle user login"""
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['email', 'password']):
            return jsonify({
                'success': False,
                'message': 'Missing email or password'
            }), 400

        success, response = search_login_credentials(data['email'], data['password'])
        return jsonify(response), 200 if success else 401

    except Exception as e:
        logger.error(f"Error in login_data: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/')
def index_page():
    """Render the index page"""
    try:
        return render_template('AiFrontlook.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {str(e)}")
        return "Error loading page", 500

@app.route('/quiz_html')
def quiz_page():
    """Render the quiz page"""
    try:
        return render_template('quiz.html')
    except Exception as e:
        logger.error(f"Error rendering quiz page: {str(e)}")
        return "Error loading quiz page", 500

@app.route('/video_feed')
def video_feed():
    """Stream video frames for proctoring"""
    try:
        return Response(
            proctoringAlgo(),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    except Exception as e:
        logger.error(f"Error in video feed: {str(e)}")
        return "Error accessing camera", 500

@app.route('/stop_camera')
def stop_camera():
    """Stop the camera and server"""
    try:
        global running
        running = False
        main_app()
        logger.info('Camera and Server stopping.....')
        os._exit(0)
    except Exception as e:
        logger.error(f"Error stopping camera: {str(e)}")
        return "Error stopping camera", 500

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'message': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

if __name__ == "__main__":
    try:
        port = int(os.getenv('PORT', 5000))
        logger.info(f"Starting the Python Flask Server on port {port}.....")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        sys.exit(1)