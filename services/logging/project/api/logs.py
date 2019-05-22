from flask import Blueprint, jsonify, request
from project.api.models import Log
from project import db
from sqlalchemy import exc
from datetime import datetime

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
    visitor_ip = post_data.get('visitor_ip')
    visit_time = post_data.get('visit_time')

    if type(visit_time) != int:
        response_object['message'] = 'sanity check. time should be in milis'
        return jsonify(response_object), 400

    try:
        db.session.add(Log(
            service=service, 
            endpoint=endpoint,
            visit_time=datetime.fromtimestamp(visit_time // 1000),
            visitor_ip=visitor_ip
        ))
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

@logs_blueprint.route('/logs/<log_id>', methods=['GET'])
def get_log_by_id(log_id):
    response_object = {
        'status': 'fail',
        'message': 'Log does not exist.'
    }

    try:
        log = Log.query.filter_by(id=int(log_id)).first()
        if not log:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': log.id,
                    'service': log.service,
                    'endpoint': log.endpoint,
                    'visit_time': log.visit_time,
                    'visitor_ip': log.visitor_ip
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
