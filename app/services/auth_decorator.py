from functools import wraps
from flask import request, jsonify, g, redirect, url_for, session
from app.services.token_service import decode_token
from app.services.user_service import get_user_by_id

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in via session
        if session.get('user_id'):
            user_id = session.get('user_id')
            user = get_user_by_id(user_id)
            
            if not user:
                # User ID in session is invalid
                session.clear()
                return redirect(url_for('auth.login'))
            
            g.user = user
            return f(*args, **kwargs)
        
        # If API request with token in header
        if request.headers.get('Authorization'):
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else auth_header
            
            result = decode_token(token)
            
            if not result['success']:
                # For API requests, return JSON error
                return jsonify({'message': result['message']}), 401
            
            # Get the user and attach to flask.g for the view
            user = get_user_by_id(result['user_id'])
            
            if not user:
                return jsonify({'message': 'User not found'}), 401
            
            g.user = user
            return f(*args, **kwargs)
        
        # No session or token, redirect to login
        if request.headers.get('Accept') == 'application/json':
            # For API requests, return JSON error
            return jsonify({'message': 'Authentication required'}), 401
        else:
            # For browser requests, redirect to login
            return redirect(url_for('auth.login'))
    
    return decorated_function
