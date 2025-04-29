import sqlite3
import hashlib
import secrets
import re
from datetime import datetime
from app.db import get_db

def validate_name(name):
    """Validate that a name is at least 2 characters."""
    if not name or len(name) < 2:
        return False, "Name must be at least 2 characters long."
    return True, ""

def validate_email(email):
    """Validate email format."""
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format."
    return True, ""

def validate_password(password):
    """
    Validate password complexity.
    Must be at least 8 characters, include one lowercase,
    one uppercase, one symbol, and one number.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    if not re.search(r'[a-z]', password):
        return False, "Password must include at least one lowercase letter."
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must include at least one uppercase letter."
    
    if not re.search(r'[0-9]', password):
        return False, "Password must include at least one number."
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must include at least one symbol."
    
    return True, ""

def validate_date_of_birth(date_str):
    """Validate date format (dd/mm/yyyy)."""
    try:
        # Check format
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
            return False, "Date must be in format dd/mm/yyyy."
        
        # Parse date
        day, month, year = map(int, date_str.split('/'))
        
        # Create date object to validate
        datetime(year, month, day)
        
        return True, ""
    except ValueError:
        return False, "Invalid date. Please use a valid date in format dd/mm/yyyy."

def hash_password(password, salt=None):
    """Hash a password for storing."""
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Create a hash with salt
    pwdhash = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()
    
    return f"{salt}${pwdhash}"

def verify_password(stored_password, provided_password):
    """Verify a stored password against a provided password."""
    salt, stored_hash = stored_password.split('$')
    return stored_password == hash_password(provided_password, salt)

def register_user(first_name, last_name, email, password, date_of_birth):
    """Register a new user with validation."""
    # Validate inputs
    validations = [
        validate_name(first_name),
        validate_name(last_name),
        validate_email(email),
        validate_password(password),
        validate_date_of_birth(date_of_birth)
    ]
    
    # Check for validation errors
    for is_valid, message in validations:
        if not is_valid:
            return {'success': False, 'message': message}
    
    db = get_db()
    try:
        # Check if user already exists
        user = db.execute(
            'SELECT id FROM users WHERE email = ?', (email,)
        ).fetchone()
        
        if user is not None:
            return {'success': False, 'message': 'User already exists'}
        
        # Store the user
        hashed_password = hash_password(password)
        db.execute(
            'INSERT INTO users (first_name, last_name, email, password, date_of_birth) '
            'VALUES (?, ?, ?, ?, ?)',
            (first_name, last_name, email, hashed_password, date_of_birth)
        )
        db.commit()
        return {'success': True, 'message': 'User registered successfully'}
    except sqlite3.Error as e:
        return {'success': False, 'message': f"Database error: {e}"}

def authenticate_user(email, password):
    """Authenticate a user."""
    db = get_db()
    error = None
    
    user = db.execute(
        'SELECT * FROM users WHERE email = ?', (email,)
    ).fetchone()
    
    if user is None:
        error = 'Incorrect email'
    elif not verify_password(user['password'], password):
        error = 'Incorrect password'
    
    if error is None:
        return {'success': True, 'user': dict(user)}
    
    return {'success': False, 'message': error}

def get_user_by_id(user_id):
    """Get a user by ID."""
    db = get_db()
    user = db.execute(
        'SELECT id, first_name, last_name, email, date_of_birth, created_at '
        'FROM users WHERE id = ?', 
        (user_id,)
    ).fetchone()
    
    if user is None:
        return None
    
    return dict(user)
