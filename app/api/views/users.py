from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from app import db
from app.api.models import User

users_blueprint = Blueprint('users', __name__,  template_folder='../templates')


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
        User(
            username=request.form['username'],
            email=request.form['email'],
            password=request.form['password'],
        ).save()
        return render_template('users.html', users=User.get_all_users())

    try:
        user = User(**request.get_json())
        user.save()
        response_object = {
            'status': 'success',
            'data': user.get_data()
        }
        return jsonify(response_object), 201
    except exc.IntegrityError:
        response_object = {
            'status': 'fail',
            'message': 'User already exists.'
        }
        return jsonify(response_object), 409
    except (ValueError, TypeError) as e:
        response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
        return jsonify(response_object), 400


@users_blueprint.route('/users/<uid>', methods=['GET'])
def get_user(uid):
    """Get a single user"""
    user = User.get_by_id(user_id=uid)
    if not user:
        response_object = {
            'status': 'fail',
            'message': 'User not found.'
        }
        return jsonify(response_object), 404
    else:
        response_object = {
            'status': 'success',
            'data': user
        }
        return jsonify(response_object), 200


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    users = User.get_all_users()
    response_object = {
        'status': 'success',
        'data': {
          'users': users
        }
    }
    if client_prefers_html():
        return render_template('users.html', users=users)
    return jsonify(response_object), 200
