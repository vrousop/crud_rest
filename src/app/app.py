import json
import requests
from src import __VCF_FILE__, __SCHEMA__
from src.app.libs import retrieve_json, json_toXML, retrieve_user_data, write_new_record, update_record, remove_record, check_if_record
import src.app.error_handlers as error_handlers
from src.app.middleware import authorization, accepterror, acceptjson, acceptxml, validate_json, validate_schema
from src.app.VcfParser import VcfParser
from flask import Flask, Response, request, g, jsonify
from flask_cors import CORS
import xml.etree.cElementTree as e

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('src.config.DevConfig')
app.register_blueprint(error_handlers.blueprint)

vcf = VcfParser(__VCF_FILE__)

with open(__SCHEMA__) as f:
    schema = json.load(f)


@app.route('/retrieve_data/')
@accepterror
@acceptjson(vcf)
@acceptxml
def get_data():
    return 


@app.route('/retrieve_data/<record_id>/')
def get_user_data(record_id):
  
    if check_if_record(record_id, vcf):

        data = retrieve_user_data(record_id, vcf)

        return Response(response=json.dumps(data), status=200, mimetype="application/json") 

    return error_handlers.not_found()


@app.route('/insert', methods=['POST'])
@authorization(app.config['SECRET_KEY'])
@validate_json
@validate_schema(schema)
def insert_data():
    # append new data
    payload = json.loads(request.data)
    write_new_record(payload, vcf)  # TODO: write to original file
   
    message = {
           
            'message': 'Created' , 
            'status': 201,
    }

    return Response(response=json.dumps(message), status=201, mimetype="application/json")


@app.route('/update/<record_id>', methods=['PUT'])
@authorization(app.config['SECRET_KEY'])
@validate_json
@validate_schema(schema)
def update_data(record_id):
    # check if record exists
    if check_if_record(record_id, vcf):
        # modify data
        payload = json.loads(request.data)
        update_record(record_id, payload, vcf)  # TODO: write to original file

        message = {
                'status': 200,
                'message': 'OK' 
        }

        return Response(response=json.dumps(message), status=200, mimetype="application/json")
    return error_handlers.not_found()


@app.route('/delete/<record_id>', methods=['DELETE'])
@authorization(app.config['SECRET_KEY'])
def delete_data(record_id):
    # check if record exists
    if check_if_record(record_id, vcf):
        # delete data
        remove_record(record_id, vcf)
        message = {
                'status': 204,
                'message': 'No Content' 
        }

        return Response(response=json.dumps(message), status=202, mimetype="application/json")
    return error_handlers.not_found()


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)
  
if __name__ == '__main__':
    main()

