import json
from src import __VCF_FILE__, __SCHEMA__
from src.app.libs import retrieve_record_data, write_new_record, update_record, remove_record, \
    check_if_record
import src.app.error_handlers as error_handlers
from src.app.middleware import authorization, accepterror, acceptjson, acceptxml, validate_json, validate_schema
from src.app.VcfParser import VcfParser
from flask import Flask, Response, request

# Initialize app
app = Flask(__name__, instance_relative_config=False)
app.config.from_object('src.config.DevConfig')
app.register_blueprint(error_handlers.blueprint)

# Initialize VCF object
vcf = VcfParser(__VCF_FILE__)

# Load json schema for validation
with open(__SCHEMA__) as f:
    schema = json.load(f)


@app.route('/retrieve_data/')
@accepterror
@acceptjson(vcf)
@acceptxml
def get_data():
    """
    GET request which returns a paginated response of the variants represented in the VCF.
    example url: /retrieve_data/?page=1&limit=10
    :return: JSON/XML Data or Status 406 Not Acceptable
    """
    return


@app.route('/retrieve_data/<record_id>/')
def get_user_data(record_id):
    """
    GET request which returns the data corresponding to a specific record id of VCF file.
    example url: /retrieve_data/rs123
    :param record_id: id from URL
    :return: JSON data - record with the specific id
    """
    if check_if_record(record_id, vcf):
        data = retrieve_record_data(record_id, vcf)

        return Response(response=json.dumps(data), status=200, mimetype="application/json")

    return error_handlers.not_found()


@app.route('/insert', methods=['POST'])
@authorization(app.config['SECRET_KEY'])
@validate_json
@validate_schema(schema)
def insert_data():
    """
    POST method that will accept json data as input e.g {"CHROM": "chr1", "POS": 1000, "ALT": "A", "REF": "G",
    "ID": "rs123"} and append a new line to the VCF file with the provided data
    example url: /insert
    :return: Status 201 created or 403 Permission denied
    """
    # append new data
    payload = json.loads(request.data)
    write_new_record(payload, vcf)  # TODO: write to original file

    message = {

        'message': 'Created',
        'status': 201,
    }

    return Response(response=json.dumps(message), status=201, mimetype="application/json")


@app.route('/update/<record_id>', methods=['PUT'])
@authorization(app.config['SECRET_KEY'])
@validate_json
@validate_schema(schema)
def update_data(record_id):
    """
    PUT method that will accept json data as input e.g {"CHROM": "chr1", "POS": 1000, "ALT": "A", "REF": "G",
    "ID": "rs123"} and modify an existing line to the VCF file with the provided data request.
    :param record_id: id from URL
    :return: Status 200 ok or 404 not found or 403 Permission denied
    """
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
    """
    DELETE request which deletes the VCF data of the given id
    :param record_id: id from URL
    :return: Status 204 No content or 404 not found or 403 Permission denied
    """
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
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=True)


if __name__ == '__main__':
    main()
