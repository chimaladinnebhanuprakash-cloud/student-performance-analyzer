"""
Database connection and query functions for Student Performance Analyzer
"""
import sqlite3
import json
from config import Config

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_database():
    """Initialize the database with schema"""
    conn = get_db_connection()
    with open('../database/schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# User operations
def create_user(full_name, email, password_hash):
    """Create a new user"""
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            'INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)',
            (full_name, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    """Get user by email"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None

# Profile operations
def get_profile(user_id):
    """Get user profile"""
    conn = get_db_connection()
    profile = conn.execute('SELECT * FROM profiles WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return dict(profile) if profile else None

def create_or_update_profile(user_id, age, gender, course, semester, college):
    """Create or update user profile"""
    conn = get_db_connection()
    existing = conn.execute('SELECT id FROM profiles WHERE user_id = ?', (user_id,)).fetchone()
    
    if existing:
        conn.execute(
            '''UPDATE profiles SET age = ?, gender = ?, course = ?, semester = ?, college = ?
               WHERE user_id = ?''',
            (age, gender, course, semester, college, user_id)
        )
    else:
        conn.execute(
            '''INSERT INTO profiles (user_id, age, gender, course, semester, college)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (user_id, age, gender, course, semester, college)
        )
    
    conn.commit()
    conn.close()
    return True

# Performance operations
def save_performance_record(user_id, subject_marks, attendance, study_hours, backlogs):
    """Save a performance record"""
    conn = get_db_connection()
    cursor = conn.execute(
        '''INSERT INTO performance_records (user_id, subject_marks, attendance, study_hours, backlogs)
           VALUES (?, ?, ?, ?, ?)''',
        (user_id, json.dumps(subject_marks), attendance, study_hours, backlogs)
    )
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_performance_history(user_id, limit=10):
    """Get performance history for a user"""
    conn = get_db_connection()
    records = conn.execute(
        '''SELECT * FROM performance_records WHERE user_id = ?
           ORDER BY created_at DESC LIMIT ?''',
        (user_id, limit)
    ).fetchall()
    conn.close()
    
    result = []
    for record in records:
        r = dict(record)
        r['subject_marks'] = json.loads(r['subject_marks'])
        result.append(r)
    return result

def get_latest_performance(user_id):
    """Get the latest performance record"""
    conn = get_db_connection()
    record = conn.execute(
        '''SELECT * FROM performance_records WHERE user_id = ?
           ORDER BY created_at DESC LIMIT 1''',
        (user_id,)
    ).fetchone()
    conn.close()
    
    if record:
        r = dict(record)
        r['subject_marks'] = json.loads(r['subject_marks'])
        return r
    return None

# Analysis operations
def save_analysis(user_id, performance_score, category, explanation, suggestions):
    """Save analysis results"""
    conn = get_db_connection()
    cursor = conn.execute(
        '''INSERT INTO analysis_history (user_id, performance_score, category, explanation, suggestions)
           VALUES (?, ?, ?, ?, ?)''',
        (user_id, performance_score, category, explanation, json.dumps(suggestions))
    )
    conn.commit()
    analysis_id = cursor.lastrowid
    conn.close()
    return analysis_id

def get_analysis_history(user_id, limit=10):
    """Get analysis history for a user"""
    conn = get_db_connection()
    analyses = conn.execute(
        '''SELECT * FROM analysis_history WHERE user_id = ?
           ORDER BY created_at DESC LIMIT ?''',
        (user_id, limit)
    ).fetchall()
    conn.close()
    
    result = []
    for analysis in analyses:
        a = dict(analysis)
        a['suggestions'] = json.loads(a['suggestions'])
        result.append(a)
    return result

def get_latest_analysis(user_id):
    """Get the latest analysis"""
    conn = get_db_connection()
    analysis = conn.execute(
        '''SELECT * FROM analysis_history WHERE user_id = ?
           ORDER BY created_at DESC LIMIT 1''',
        (user_id,)
    ).fetchone()
    conn.close()
    
    if analysis:
        a = dict(analysis)
        a['suggestions'] = json.loads(a['suggestions'])
        return a
    return None
