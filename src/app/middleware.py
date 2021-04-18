import json 
from functools import wraps
from jsonschema import validate
from flask import Response, request, g
from src.app.error_handlers import not_permission, not_accept, bad_request
from src.app.libs import retrieve_json, json_toXML

def authorization(secret):
    def inner_function(func):
        @wraps(func)
        def check_authorization(*args, **kwargs):

            if request.headers.get('x-api-key') == secret:
                
                return func(*args, **kwargs)

            return not_permission()

        return check_authorization
    return inner_function


def accepterror(func):
    @wraps(func)
    def return_error(*args, **kwargs):
        
        if request.headers.get("Accept", '*/*') not in ['*/*', 'application/json', 'application/xml']:
            # g.output = not_accept()
            return not_accept()
        return func()

    return return_error

def acceptxml(func):
    @wraps(func)
    def return_xml(*args, **kwargs):  

        if request.headers.get('Accept', '*/*') == 'application/xml':    
            # g.output = json_toXML(g.payload_json)
            return json_toXML(g.payload_json)
    return return_xml

def acceptjson(func):
    @wraps(func)
    def return_json(*args, **kwargs):

        g.payload_json = retrieve_json(
                request.base_url, 
                int(request.args.get('page', 1)), 
                int(request.args.get('limit', 20))
                )    

        if request.headers.get("Accept", '*/*') in ['*/*', 'application/json']:
            # g.output = Response(response=json.dumps(g.payload_json), status=200, mimetype="application/json")
            return Response(response=json.dumps(g.payload_json), status=200, mimetype="application/json")
        return func()
    
    return return_json

def validate_json(func):
    @wraps(func)
    def wrapper(*args, **kw):
        try:
            request.json
        except:
            return bad_request()  
        return func(*args, **kw)
    return wrapper


def validate_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            try:
                validate(request.json, schema)
            except:
                return bad_request()         
            return func(*args, **kw)
        return wrapper
    return decorator