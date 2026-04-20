"""
Student Performance Analyzer - Main Flask Application
"""
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os
import sys

# Add backend directory to path
sys.path.append(os.path.dirname(__file__))

from config import Config
import database as db
import auth
import analyzer
import chatbot

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)
CORS(app, supports_credentials=True)

# Initialize database on first run
def init_db():
    """Initialize database if it doesn't exist"""
    if not os.path.exists(Config.DATABASE_PATH):
        conn = db.get_db_connection()
        with open(os.path.join(os.path.dirname(__file__), '../database/schema.sql'), 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database initialized successfully!")

# Initialize database
init_db()

# Serve frontend files
@app.route('/')
def serve_index():
    """Serve login page"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory(app.static_folder, path)

# Authentication routes
@app.route('/api/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validate input
        errors = auth.validate_registration(full_name, email, password, confirm_password)
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
        
        # Check if user already exists
        existing_user = db.get_user_by_email(email)
        if existing_user:
            return jsonify({'success': False, 'errors': ['Email already registered']}), 400
        
        # Hash password and create user
        password_hash = auth.hash_password(password)
        user_id = db.create_user(full_name, email, password_hash)
        
        if user_id:
            return jsonify({'success': True, 'message': 'Registration successful!'}), 201
        else:
            return jsonify({'success': False, 'errors': ['Registration failed']}), 500
            
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'success': False, 'errors': ['Server error occurred']}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
        
        # Get user
        user = db.get_user_by_email(email)
        if not user:
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not auth.verify_password(password, user['password_hash']):
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        
        # Create session
        session['user_id'] = user['id']
        session['user_name'] = user['full_name']
        session['user_email'] = user['email']
        session.permanent = True
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'full_name': user['full_name'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'error': 'Server error occurred'}), 500

@app.route('/api/logout', methods=['GET', 'POST'])
def logout():
    """User logout endpoint"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@app.route('/api/check-session', methods=['GET'])
def check_session():
    """Check if user is logged in"""
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user': {
                'id': session['user_id'],
                'full_name': session['user_name'],
                'email': session['user_email']
            }
        }), 200
    else:
        return jsonify({'logged_in': False}), 200

# Profile routes
@app.route('/api/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        user_id = session['user_id']
        user = db.get_user_by_id(user_id)
        profile = db.get_profile(user_id)
        
        return jsonify({
            'success': True,
            'user': {
                'full_name': user['full_name'],
                'email': user['email']
            },
            'profile': profile
        }), 200
        
    except Exception as e:
        print(f"Get profile error: {e}")
        return jsonify({'success': False, 'error': 'Server error occurred'}), 500

@app.route('/api/profile', methods=['POST'])
def update_profile():
    """Update user profile"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        user_id = session['user_id']
        data = request.get_json()
        
        age = data.get('age')
        gender = data.get('gender', '').strip()
        course = data.get('course', '').strip()
        semester = data.get('semester', '').strip()
        college = data.get('college', '').strip()
        
        # Update profile
        db.create_or_update_profile(user_id, age, gender, course, semester, college)
        
        return jsonify({'success': True, 'message': 'Profile updated successfully'}), 200
        
    except Exception as e:
        print(f"Update profile error: {e}")
        return jsonify({'success': False, 'error': 'Server error occurred'}), 500

# Performance analysis routes
@app.route('/api/analyze', methods=['POST'])
def analyze_performance():
    """Analyze student performance"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        user_id = session['user_id']
        data = request.get_json()
        
        subject_marks = data.get('subject_marks', {})
        attendance = float(data.get('attendance', 0))
        study_hours = float(data.get('study_hours', 0))
        backlogs = int(data.get('backlogs', 0))
        
        # Validate input
        if not subject_marks:
            return jsonify({'success': False, 'error': 'Subject marks required'}), 400
        
        # Save performance record
        db.save_performance_record(user_id, subject_marks, attendance, study_hours, backlogs)
        
        # Analyze performance
        analysis = analyzer.analyze_performance(subject_marks, attendance, study_hours, backlogs)
        
        # Save analysis
        db.save_analysis(
            user_id,
            analysis['score'],
            analysis['category'],
            analysis['explanation'],
            analysis['suggestions']
        )
        
        return jsonify({
            'success': True,
            'analysis': analysis
        }), 200
        
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({'success': False, 'error': 'Server error occurred'}), 500

@app.route('/api/performance-history', methods=['GET'])
def get_performance_history():
    """Get performance history"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        user_id = session['user_id']
        history = db.get_performance_history(user_id, limit=10)
        
        return jsonify({
            'success': True,
            'history': history
        }), 200
        
    except Exception as e:
        print(f"Performance history error: {e}")
        return jsonify({'success': False, 'error': 'Server error occurred'}), 500

@app.route('/api/analysis-history', methods=['GET'])
def get_analysis_history():
    """Get analysis history"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        user_id = session['user_id']
        history = db.get_analysis_history(user_id, limit=10)
        
        return jsonify({
            'success': True,
            'history': history
        }), 200
        
    except Exception as e:
        print(f"Analysis history error: {e}")
        return jsonify({'success': False, 'error': 'Server error occurred'}), 500

# AI Assistant routes
@app.route('/api/chat', methods=['POST'])
def chat():
    """AI Assistant chatbot endpoint"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        user_id = session['user_id']
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'error': 'Message required'}), 400
        
        # Get user profile and latest analysis
        user = db.get_user_by_id(user_id)
        profile = db.get_profile(user_id)
        latest_analysis = db.get_latest_analysis(user_id)
        
        # Combine user and profile data
        user_profile = {
            'full_name': user['full_name'],
            'email': user['email']
        }
        if profile:
            user_profile.update(profile)
        
        # Generate response
        response = chatbot.get_chatbot_response(message, user_profile, latest_analysis)
        
        return jsonify({
            'success': True,
            'response': response
        }), 200
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'success': False, 'error': 'Server error occurred'}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Student Performance Analyzer")
    print("=" * 50)
    print("Server starting on http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
