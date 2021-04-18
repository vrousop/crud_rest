import flask
from flask import jsonify

blueprint = flask.Blueprint('error_handlers', __name__)

@blueprint.app_errorhandler(406)
def not_accept(error=None):
    message = {
            'status': 406,
            'message': 'Not Acceptable' 
    }
    resp = jsonify(message)
    resp.status_code = 406

    return resp

@blueprint.app_errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found' 
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@blueprint.app_errorhandler(403)
def not_permission(error=None):
    message = {
            'status': 403,
            'message': 'Permission Denied' 
    }
    resp = jsonify(message)
    resp.status_code = 403

    return resp


@blueprint.app_errorhandler(400)
def bad_request(error=None):
    message = {
            'status': 400,
            'message': 'Invalid JSON' 
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp