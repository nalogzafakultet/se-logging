from flask import Blueprint, jsonify, request
from project.api.models import Log
from project import db
from sqlalchemy import exc

logs_blueprint = Blueprint('logs', __name__)

@logs_blueprint.route('/logs/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@logs_blueprint.route('/logs', methods=['POST'])
def add_log():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    service = post_data.get('service')
    endpoint = post_data.get('endpoint')
    try:
        db.session.add(Log(service, endpoint))
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Log added!'
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400

@logs_blueprint.route('/logs', methods=['GET'])
def all_logs():
    response_object = {
        'status': 'success',
        'data': {
            'logs': [log.to_json() for log in Log.query.all()]
        }
    }
    return jsonify(response_object), 200
