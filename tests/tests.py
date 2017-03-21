from flask import Flask
from flask_testing import TestCase

from ga4gh.schemas import protocol

class MyTest(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_search_datasets(self):
        response = self.client.post('/datasets/search', {})
        self.assertIsNotNone(response, "Something should be returned")
        self.assertEqual(response.status_code, 200, "A known good endpoint "
                                                    "should return success")


    def test_schemas_deserialization(self):
        # Mock search datasets request
        request = '{"pageSize": 3, "pageToken": "text"}'
        # We pass the class, not an instance of the class to `fromJson`
        request_schema = protocol.SearchDatasetsRequest
        deserialized_request = protocol.fromJson(request, request_schema)
        self.assertEqual(3, deserialized_request.page_size, "The deserialized "
                                                            "version should also have 3 for page_size")

    def test_schemas_serialization(self):
        #dataset =
        # Make an empty request protocol buffer
        response = protocol.SearchDatasetsResponse()
