import os
import json
from jsonschema import validate as validate_json
from xmlschema import validate as validate_xml
from tests.base import BaseCase
from . import __PACKAGE_DIR__

class TestGetData(BaseCase):
 
    def test_retrieve_data(self):
 
        response = self.app.get('http://localhost:5000/retrieve_data/?page=2&limit=1', headers={"Accept": "application/json"})
        self.assertEqual(200, response.status_code)


    def test_retrieve_data_validate(self):
 
        response = self.app.get('http://localhost:5000/retrieve_data/?page=2&limit=1', headers={"Accept": "application/json"})
        path = os.path.join(__PACKAGE_DIR__, 'test_schema.json')

        with open(path) as f:
            schema = json.load(f)
        validate_json(response.json, schema)
        self.assertEqual(200, response.status_code)


    def test_retrieve_data_xml(self):

        response = self.app.get('http://localhost:5000/retrieve_data/?page=18&limit=1', headers={"Accept": "application/xml"})
        self.assertEqual(200, response.status_code)


    def test_retrieve_data_xml_validate(self):

        response = self.app.get('http://localhost:5000/retrieve_data/?page=28&limit=2', headers={"Accept": "application/xml"})
        path = os.path.join(__PACKAGE_DIR__, 'test_schema.xml')

        with open(path) as f:
            schema = f.read()
        validate_xml(response.data, schema)
        self.assertEqual(200, response.status_code)


    def test_retrieve_data_error(self):

        response = self.app.get('http://localhost:5000/retrieve_data/?page=18&limit=1', headers={"Accept": "application/javascript"})
        expected = {
            "message":"Not Acceptable",
            "status":406
            }
        self.assertEqual(expected, response.json)
        self.assertEqual(406, response.status_code)



    def test_retrieve_record_error(self):

        response = self.app.get('http://localhost:5000/retrieve_data/testid/')
        expected = {
            "message": "Not Found",
            "status": 404
        }
        self.assertEqual(expected, response.json)
        self.assertEqual(404, response.status_code)