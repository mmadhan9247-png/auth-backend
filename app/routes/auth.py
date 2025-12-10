from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies,
)
from ..models import User
from ..extensions import db
import os
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful! Please login with your credentials.',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user:
            return jsonify({'error': 'Login first - Please register your account'}), 401
        
        if not user.check_password(data['password']):
            return jsonify({'error': 'Invalid password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        access_token = create_access_token(identity=str(user.id))

        response = jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
        })
        set_access_cookies(response, access_token)
        return response, 200
        
    except Exception as e:
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500

@auth_bp.route('/google', methods=['POST'])
def google_login():
    try:
        data = request.get_json()
        credential = data.get('credential') if data else None

        if not credential:
            return jsonify({'error': 'Missing Google ID token'}), 400

        client_id = os.getenv("GOOGLE_CLIENT_ID") or "680905646956-5i53ab61lg54mdlt2mcvn3q81vcqojmg.apps.googleusercontent.com"

        idinfo = id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            client_id,
        )

        if idinfo.get('iss') not in ['accounts.google.com', 'https://accounts.google.com']:
            return jsonify({'error': 'Invalid token issuer'}), 400

        email = idinfo.get('email')
        if not email:
            return jsonify({'error': 'Email not available from Google account'}), 400

        username = idinfo.get('name') or email.split('@')[0]

        user = User.query.filter_by(email=email).first()

        if not user:
            user = User(
                username=username,
                email=email,
            )
            user.set_password(os.urandom(16).hex())
            db.session.add(user)
            db.session.commit()
        elif not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401

        access_token = create_access_token(identity=str(user.id))

        response = jsonify({
            'message': 'Google login successful',
            'user': user.to_dict(),
            'access_token': access_token,
        })
        set_access_cookies(response, access_token)
        return response, 200

    except ValueError as e:
        return jsonify({'error': 'Invalid Google token', 'details': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Google login failed', 'details': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user info', 'details': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        response = jsonify({'message': 'Logout successful'})
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify({'error': 'Logout failed', 'details': str(e)}), 500