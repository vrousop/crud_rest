import json
from tests.base import BaseCase

class TestGetData(BaseCase):
    
 
    def test_retrieve_data(self):
        
        self.maxDiff = None
        response = self.app.get('http://localhost:5000/retrieve_data/?page=2&limit=1', headers={"Accept": "application/json"})
        expected ={
            "previous_url": "http://localhost:5000/retrieve_data/?page=1&limit=1",
            "next_url": "http://localhost:5000/retrieve_data/?page=3&limit=1",
            "data": [
                {
                    "CHROM": "chr1",
                    "POS": 13116,
                    "ID": "rs62635286",
                    "REF": "T",
                    "ALT_1": "G",
                    "ALT_2": None, 
                    "ALT_3": None,
                    "QUAL": 736.7700195312,
                    "FILTER_PASS": True
                }
            ]
        }

        self.assertEqual(expected, response.json)
        self.assertEqual(200, response.status_code)

    def test_retrieve_data_xml(self):

        self.maxDiff = None

        response = self.app.get('http://localhost:5000/retrieve_data/?page=18&limit=1', headers={"Accept": "application/xml"})

        expected = b'<payload><previous_url>http://localhost:5000/retrieve_data/?page=17&amp;limit=1</previous_url><next_url>http://localhost:5000/retrieve_data/?page=19&amp;limit=1</next_url><data><ALT_1>T</ALT_1><ALT_2 /><ALT_3 /><CHROM>chr1</CHROM><FILTER_PASS>False</FILTER_PASS><ID>rs4951864</ID><POS>798026</POS><QUAL>21.7700004578</QUAL><REF>C</REF></data></payload>'
        
        self.assertEqual(expected, response.data)
        self.assertEqual(200, response.status_code)

    def test_retrieve_data_error(self):

        self.maxDiff = None

        response = self.app.get('http://localhost:5000/retrieve_data/?page=18&limit=1', headers={"Accept": "application/javascript"})
        
        expected = {
            "message":"Not Acceptable",
            "status":406
            }
        
        self.assertEqual(expected, response.json)
        self.assertEqual(406, response.status_code)

    def test_retrieve_data_user(self):

        self.maxDiff = None
        response = self.app.get('http://localhost:5000/retrieve_data/rs10910098/', headers={"Content-Type": "application/javascript"})
        expected = [{"CHROM": "chr1", 
                "POS": 2533250, 
                "ID": "rs10910098", 
                "REF": "C", 
                "ALT_1": "A", 
                "ALT_2": None, 
                "ALT_3": None, 
                "QUAL": 36.7400016785, 
                "FILTER_PASS": False}] 
        self.assertEqual(expected, response.json)
        self.assertEqual(200, response.status_code)