import json
from tests.base import BaseCase


class TestPostData(BaseCase):

    def test_post_data(self):
        
        
        self.maxDiff = None
        body = {
            "CHROM": "chr1",
            "POS": 1000,
            "ALT": "A",
            "REF": "G",
            "ID": "rs123"
        }
        response = self.app.post('http://localhost:5000/insert', 
                                headers={'Content-Type': 'application/json', 'x-api-key':'Th1s1ss3cr3t'}, 
                                data=json.dumps(body))
        expected ={ 
            'message':'Created'
        }

        self.assertEqual(expected, response.json)
        self.assertEqual(201, response.status_code)

    def test_post_data_error(self):
        
        self.maxDiff = None
        body = {
            "CHROM": "chr1",
            "POS": 1000,
            "ALT": "A",
            "REF": "G",
            "ID": "rs123"
        }
        response = self.app.post('http://localhost:5000/insert', 
                            headers={'Content-Type':'application/json', 'x-api-key':'lksjdla'}, 
                            data=json.dumps(body))
        expected ={
                "message": "Permission Denied",
                "status": 403
            }

        self.assertEqual(expected, response.json)
        self.assertEqual(403, response.status_code)

    def test_post_data_validate(self):
        
        self.maxDiff = None
        body = {
            "CHROM": "chr1",
            "POS": "1000",
            "ALT": "A",
            "REF": "G",
            "ID": "rs123"
        }
        response = self.app.post('http://localhost:5000/insert', 
                            headers={'Content-Type':'application/json', 'x-api-key':'Th1s1ss3cr3t'}, 
                            data=json.dumps(body))
        expected = {
                "message": "Invalid JSON",
                "status": 400
            }

        self.assertEqual(expected, response.json)
        self.assertEqual(400, response.status_code)
