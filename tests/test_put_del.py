import json
from tests.base import BaseCase
from src.config import Config


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
        response = self.app.put('http://localhost:5000/update/testid',
                                headers={'Content-Type': 'application/json', 'x-api-key': Config.SECRET_KEY},
                                data=json.dumps(body))
        expected = {
            "status": 404,
            "message": "Not Found"
        }

        self.assertEqual(expected, response.json)
        self.assertEqual(404, response.status_code)

    def test_del_data_error(self):
        self.maxDiff = None

        response = self.app.delete('http://localhost:5000/delete/rs123/',
                                   headers={'x-api-key': Config.SECRET_KEY})
        expected = {
            "status": 404,
            "message": "Not Found"
        }
        self.assertEqual(expected, response.json)
        self.assertEqual(404, response.status_code)
