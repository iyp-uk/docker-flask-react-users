from flask import Blueprint, request, jsonify
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound

from app.api.models import User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    try:
        user = User(**request.get_json())
        user.save()
        response_object = {
            'status': 'success',
            'data': user.get_data(),
            'token': user.encode_auth_token(user.id).decode()
        }
        return jsonify(response_object), 201
    except exc.IntegrityError:
        response_object = {
            'status': 'error',
            'message': 'User already exists.'
        }
        return jsonify(response_object), 409
    except (TypeError, ValueError) as e:
        response_object = {
                'status': 'error',
                'message': 'Invalid payload.'
            }
        return jsonify(response_object), 400


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    try:
        user = User.login(**request.get_json())
        response_object = {
            'status': 'success',
            'message': 'Successfully logged in.',
            'token': user.encode_auth_token(user.id).decode()
        }
        return jsonify(response_object), 200
    except NoResultFound:
        response_object = {
            'status': 'error',
            'message': 'Invalid username or password.'
        }
        return jsonify(response_object), 404
    except (TypeError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@auth_blueprint.route('/auth/logout', methods=['GET'])
def logout_user():
    headers_token = User.get_token_from_authorization_header(request.headers.get('Authorization'))
    response = User.decode_auth_token(headers_token)
    if isinstance(response, str):
        response_object = {
            'status': 'error',
            'message': response
        }
        return jsonify(response_object), 401
    else:
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return jsonify(response_object), 200
