"""
Authentication utilities for Student Performance Analyzer
"""
import bcrypt
import re

def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password strength:
    - Minimum 6 characters
    - First character must be a capital letter
    - Only alphabets and numbers are allowed
    """
    pattern = r'^[A-Z][a-zA-Z0-9]{5,}$'
    return re.match(pattern, password) is not None

def validate_registration(full_name, email, password, confirm_password):
    """Validate registration data"""
    errors = []
    
    if not full_name or len(full_name.strip()) < 2:
        errors.append("Full name must be at least 2 characters")
    
    if not validate_email(email):
        errors.append("Invalid email format")
    
    if not validate_password(password):
        errors.append("Password must be at least 6 characters, start with a capital letter, and contain only letters and numbers (no special characters)")
    
    if password != confirm_password:
        errors.append("Passwords do not match")
    
    return errors
