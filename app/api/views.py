from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from app import db
from app.api.models import User

users_blueprint = Blueprint('users', __name__,  template_folder='./templates')


def client_prefers_html():
    """Checks if client accepts JSON as a response format"""
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    # if application/json is ranked higher, then return true
    return best == 'text/html' and request.accept_mimetypes[best] > request.accept_mimetypes['application/json']


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    """Add a user to the database."""
    if 'application/json' not in request.content_type:
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()
        users = User.query.order_by(User.created_at.desc()).all()
        return render_template('users.html', users=users)

    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That email already exists.'
            }
            return jsonify(response_object), 409
    except exc.IntegrityError:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@users_blueprint.route('/users/<uid>', methods=['GET'])
def get_user(uid):
    """Get a single user"""
    try:
        user = User.query.filter_by(id=uid).first()
        if not user:
            response_object = {
                'status': 'fail',
                'message': 'User not found.'
            }
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                  'username': user.username,
                  'email': user.email,
                  'created_at': user.created_at
                }
            }
            return jsonify(response_object), 200
    except exc.DataError:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid request, User id must be integer.'
        }
        return jsonify(response_object), 400


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    users = User.query.all()
    users_list = []
    for user in users:
        user_object = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
        users_list.append(user_object)
    response_object = {
        'status': 'success',
        'data': {
          'users': users_list
        }
    }
    if client_prefers_html():
        return render_template('users.html', users=users)
    return jsonify(response_object), 200
