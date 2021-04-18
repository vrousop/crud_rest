import json
from tests.base import BaseCase


class TestPutDelData(BaseCase):

    def test_put_data(self):
        
        
        self.maxDiff = None
        body = {
            "CHROM": "chr1",
            "POS": 1000,
            "ALT": "A",
            "REF": "G",
            "ID": "rs123"
        }
        response = self.app.put('http://localhost:5000//update?id=rs123', 
                                headers={'Content-Type': 'application/json', 'x-api-key':'Th1s1ss3cr3t'}, 
                                data=json.dumps(body))
        expected ={
            "status": 200,
            "message": "OK"
        }

        self.assertEqual(expected, response.json)
        self.assertEqual(200, response.status_code)

    def test_del_data_error(self):
        
        self.maxDiff = None
  
        response = self.app.delete('http://localhost:5000/delete?id=rs123/', 
                            headers={'x-api-key':'Th1s1ss3cr3t'})
        expected ={
            "status": 204,
            "message": "No Content"
        }
        self.assertEqual(expected, response.json)
        # self.assertEqual(204, response.status_code)

    