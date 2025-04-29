from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from app.services.user_service import (
    register_user, authenticate_user, validate_name, validate_email, 
    validate_password, validate_date_of_birth
)
from app.services.token_service import generate_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        date_of_birth = request.form.get('date_of_birth')
        
        # Validate input
        error = None
        
        # Check if all required fields are provided
        if not first_name or not last_name or not email or not password or not confirm_password or not date_of_birth:
            error = 'All fields are required.'
        
        # If all fields are provided, validate each field
        if error is None:
            # Validate first name
            valid_first_name, message = validate_name(first_name)
            if not valid_first_name:
                error = message
            
            # Validate last name
            if error is None:
                valid_last_name, message = validate_name(last_name)
                if not valid_last_name:
                    error = message
            
            # Validate email
            if error is None:
                valid_email, message = validate_email(email)
                if not valid_email:
                    error = message
            
            # Validate password
            if error is None:
                valid_password, message = validate_password(password)
                if not valid_password:
                    error = message
            
            # Check if passwords match
            if error is None and password != confirm_password:
                error = 'Passwords do not match.'
            
            # Validate date of birth
            if error is None:
                valid_date, message = validate_date_of_birth(date_of_birth)
                if not valid_date:
                    error = message
        
        # If all validations pass, try to register the user
        if error is None:
            result = register_user(first_name, last_name, email, password, date_of_birth)
            
            if result['success']:
                flash('Registration successful. Please log in.')
                return redirect(url_for('auth.login'))
            
            error = result['message']
        
        flash(error)
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if session.get('user_id'):
        return redirect(url_for('main.home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate input
        error = None
        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            result = authenticate_user(email, password)
            
            if result['success']:
                # Generate JWT token
                token = generate_token(result['user']['id'])
                
                # Store in session for browser clients
                session.clear()
                session['user_id'] = result['user']['id']
                session['token'] = token
                
                # Return token for API clients
                if request.headers.get('Accept') == 'application/json':
                    return jsonify({
                        'token': token,
                        'user': {
                            'id': result['user']['id'],
                            'email': result['user']['email'],
                            'first_name': result['user']['first_name'],
                            'last_name': result['user']['last_name']
                        }
                    })
                
                return redirect(url_for('main.home'))
            
            error = result['message']
        
        flash(error)
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

# API route for token-based authentication
@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    if not email:
        return jsonify({"message": "Missing email parameter"}), 400
    if not password:
        return jsonify({"message": "Missing password parameter"}), 400
    
    result = authenticate_user(email, password)
    
    if result['success']:
        token = generate_token(result['user']['id'])
        
        return jsonify({
            'token': token,
            'user': {
                'id': result['user']['id'],
                'email': result['user']['email'],
                'first_name': result['user']['first_name'],
                'last_name': result['user']['last_name']
            }
        })
    
    return jsonify({"message": result['message']}), 401
