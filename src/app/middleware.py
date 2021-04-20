import json
from functools import wraps
from jsonschema import validate
from flask import Response, request, g
from src.app.error_handlers import not_permission, not_accept, bad_request, not_found
from src.app.libs import retrieve_json, json_toXML


def authorization(secret):
    """
    Authorization check
    """

    def inner_function(func):
        @wraps(func)
        def check_authorization(*args, **kwargs):
            if request.headers.get('x-api-key') == secret:
                return func(*args, **kwargs)

            return not_permission()

        return check_authorization

    return inner_function


def accepterror(func):
    """
    Check if Accept Header of a request does not match any acceptable types
    """

    @wraps(func)
    def return_error(*args, **kwargs):
        if request.headers.get("Accept", '*/*') not in ['*/*', 'application/json', 'application/xml']:
            return not_accept()

        return func()

    return return_error


def acceptxml(func):
    """
    Check if Accept Header of a request is application/XML in order to return response in XML format
    """

    @wraps(func)
    def return_xml(*args, **kwargs):
        if request.headers.get('Accept', '*/*') == 'application/xml':
            return json_toXML(g.payload_json)

    return return_xml


def acceptjson(vcf_object):
    """
    Check if Accept Header of a request is application/json in order to return response in JSON format
    """

    def in_acceptjson(func):
        @wraps(func)
        def return_json(*args, **kwargs):
            g.payload_json = retrieve_json(
                request.base_url,
                int(request.args.get('page', 1)),
                int(request.args.get('limit', 20)),
                vcf_object
            )

            if request.headers.get('Accept', '*/*') in ['*/*', 'application/json']:
                return Response(response=json.dumps(g.payload_json), status=200, mimetype="application/json")

            return func()

        return return_json

    return in_acceptjson


def validate_json(func):
    """
    Validates if an input of request is in Json format
    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            request.json
        except:
            return bad_request()

        return func(*args, **kwargs)

    return wrapper


def validate_schema(schema):
    """
    Validates json input of request
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                validate(request.json, schema)
            except:
                return bad_request()

            return func(*args, **kwargs)

        return wrapper

    return decorator
