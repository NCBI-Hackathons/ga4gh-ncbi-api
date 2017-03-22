from flask import Flask
from flask_testing import TestCase

from ga4gh.schemas import protocol

import ncbi
from app import app

class MyTest(TestCase):

    def create_app(self):
        return app.get_app()

    def test_search_readgroups(self):
        response = self.client.post('/readgroups', data='{}')
        response_proto = protocol.fromJson(
            response.get_data(), protocol.SearchReadgroupsResponse)
        self.assertIsNotNone(response_proto, "Something should be returned")
        self.assertEqual(response.status_code, 200, "A known good endpoint "
                                                    "should return success")
        self.assertGreater(
            len(response_proto.readgroups), 0,
            "Some readgroups should be returned.")

        response = self.client.post('/readgroups', data='{"dataset_id": 356464}')
        response_proto = protocol.fromJson(
            response.get_data(), protocol.SearchReadgroupsResponse)
        self.assertEqual(len(response_proto.readgroups), 356464)

    def test_search_datasets(self):
        response = self.client.post('/datasets/search', data='{}')
        response_proto = protocol.fromJson(
            response.get_data(), protocol.SearchDatasetsResponse)
        self.assertIsNotNone(response_proto, "Something should be returned")
        self.assertEqual(response.status_code, 200, "A known good endpoint "
                                                    "should return success")
        self.assertGreater(
            len(response_proto.datasets), 0,
            "Some datasets should be returned.")

        response = self.client.post('/datasets/search', data='{"pageSize": 2}')
        response_proto = protocol.fromJson(
            response.get_data(), protocol.SearchDatasetsResponse)
        self.assertEqual(len(response_proto.datasets), 2)

    def test_search_read_group_sets(self):
        response = self.client.post('/readgroupsets/search', data='{}')
        response_proto = protocol.fromJson(
            response.get_data(), protocol.SearchReadGroupSetsResponse)
        self.assertIsNotNone(response_proto, "Something should be returned")
        self.assertEqual(response.status_code, 200, "A known good endpoint "
                                                    "should return success")
        self.assertGreater(
            len(response_proto.read_group_sets), 0,
            "Some read group sets should be returned.")

    def test_search_reads(self):
        run_accession = 'SRR2856889'  # paired
        # acc = 'SRR1482462' # unpaired
        reference_name = 'chr1'
        start = 9000000
        end = 9100000
        request = protocol.SearchReadsRequest()
        request.read_group_ids.extend([run_accession])
        request.reference_id = reference_name
        request.start = start
        request.end = end
        reads_list = ncbi.search_reads(request)
        response = self.client.post(
            '/reads/search', data=protocol.toJson(request))
        response_proto = protocol.fromJson(
            response.get_data(), protocol.SearchReadsResponse)
        self.assertIsNotNone(response_proto, "Something should be returned")
        self.assertEqual(response.status_code, 200, "A known good endpoint "
                                                    "should return success")
        i = 0
        for ga_alignment in response_proto.alignments:
            self.assertEqual(reads_list[i], ga_alignment)
            i += 1
        self.assertGreater(
            len(response_proto.alignments), 0,
            "Some alignments should be returned.")

    def test_search_reads_controller(self):
        run_accession = 'SRR2856889'  # paired
        # acc = 'SRR1482462' # unpaired
        reference_name = 'chr1'
        start = 9000000
        end = 9100000
        request = protocol.SearchReadsRequest()
        request.read_group_ids.extend([run_accession])
        request.reference_id = reference_name
        request.start = start
        request.end = end
        reads_list = ncbi.search_reads(request)
        self.assertIsNotNone(reads_list, "The function should return"
                                         "something")
        self.assertGreater(len(reads_list), 0, "The function should return"
                                               "some alignments.")

    def test_schemas_deserialization(self):
        # Mock search datasets request
        request = '{"pageSize": 3, "pageToken": "text"}'
        # We pass the class, not an instance of the class to `fromJson`
        request_schema = protocol.SearchDatasetsRequest
        deserialized_request = protocol.fromJson(request, request_schema)
        self.assertEqual(
            3, deserialized_request.page_size,
            "The deserialized version should also have 3 for page_size.")

    def test_schemas_serialization(self):
        #dataset =
        # Make an empty request protocol buffer
        response = protocol.SearchDatasetsResponse()
