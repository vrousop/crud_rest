import json
import vcf
import requests
from src import __VCF_FILE__, __SCHEMA__
from src.app.libs import retrieve_json, json_toXML, retrieve_user_data
import src.app.error_handlers as error_handlers
from src.app.middleware import authorization, accepterror, acceptjson, acceptxml, validate_json, validate_schema
from flask import Flask, Response, request, g, jsonify
from flask_cors import CORS
import xml.etree.cElementTree as e


app = Flask(__name__)
app.register_blueprint(error_handlers.blueprint)

app.config['SECRET_KEY']='Th1s1ss3cr3t'
with open(__SCHEMA__, 'r') as fp:
    app.config['INPUT_SCHEMA'] = json.load(fp)


@app.route('/retrieve_data/')
@accepterror
@acceptjson
@acceptxml
def get_data():
    return 

@app.route('/retrieve_data/<id>/')
def get_user_data(id):
    
    data = retrieve_user_data(id)
    res = Response(response=json.dumps(data), status=200, mimetype="application/json") if len(data)>0 else error_handlers.not_found()
    return res



@app.route('/insert', methods=['POST'])
@authorization(app.config['SECRET_KEY'])
@validate_json
@validate_schema(app.config['INPUT_SCHEMA'])
def insert_data():
    # append new data
    message = {
           
            'message': 'Created' 
    }

    return jsonify(message), 201


@app.route('/update', methods=['PUT'])
@authorization(app.config['SECRET_KEY'])
@validate_json
@validate_schema(app.config['INPUT_SCHEMA'])
def update_data():
    # modify data
    userid= request.args.get('id')
    
    message = {
            'status': 200,
            'message': 'OK' 
    }

    return Response(response=json.dumps(message), status=200, mimetype="application/json")

@app.route('/delete', methods=['DELETE'])
@authorization(app.config['SECRET_KEY'])
def delete_data():
    # modify data
    userid= request.args.get('id')
    
    message = {
            'status': 204,
            'message': 'No Content' 
    }

    return Response(response=json.dumps(message), status=202, mimetype="application/json")
    


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)
  
if __name__ == '__main__':
    main()


"""
@app.route('/retrieve_data/')
def get_all_data():
    print(request.accept_mimetypes)
    accept = request.headers.get('Accept', '*/*')
    # print("accept -> ", accept)
    payload_json = retrieve_json(
                    request.base_url, 
                    int(request.args.get('page', 1)), 
                    int(request.args.get('limit', 20))
                    )
    
    if accept in ['*/*', 'application/json']:
        res = Response(response=json.dumps(payload_json), status=200, mimetype="application/json")
    elif accept == 'application/xml':
        res = Response(response=json_toXML(payload_json), status=200, mimetype="application/xml")
    else:
        res= error_handlers.not_accept()
    return  res
"""