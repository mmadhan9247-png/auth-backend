from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': f'Welcome to your dashboard, {user.username}!',
            'user': user.to_dict(),
            'data': {
                'total_users': User.query.count(),
                'active_users': User.query.filter_by(is_active=True).count()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to load dashboard', 'details': str(e)}), 500

@protected_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'profile': user.to_dict(),
            'stats': {
                'account_age_days': (user.created_at.utcnow() - user.created_at).days,
                'is_active': user.is_active
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to load profile', 'details': str(e)}), 500

@protected_bp.route('/admin', methods=['GET'])
@jwt_required()
def admin_only():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.username != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        all_users = User.query.all()
        return jsonify({
            'message': 'Admin panel access granted',
            'users': [user.to_dict() for user in all_users],
            'total_users': len(all_users)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Admin panel error', 'details': str(e)}), 500