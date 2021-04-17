import json
import vcf
from src import __VCF_FILE__
from src.app.libs import retrieve_json, json_toXML, retrieve_user_data
from flask import Flask, Response, request, jsonify, url_for
from flask_cors import CORS
import xml.etree.cElementTree as e

app = Flask(__name__)

@app.errorhandler(406)
def not_accept(error=None):
    message = {
            'status': 406,
            'message': 'Not Acceptable' 
    }
    resp = jsonify(message)
    resp.status_code = 406

    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found' 
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/retrieve_data/')
def get_all_data():

    accept = request.headers.get('Accept', '*/*')

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
        res= not_found()
    return  res
    

@app.route('/<id>/')
def get_user_data(id):
    
    data = retrieve_user_data(id)
    res = Response(response=json.dumps(data), status=200, mimetype="application/json") if len(data)>0 else not_found()
    return res



@app.route('/insert', methods=['POST'])
def insert_data():
    body = json.dumps(request.json)
    return body



def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()